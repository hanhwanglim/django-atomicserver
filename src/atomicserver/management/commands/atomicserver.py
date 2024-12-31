from typing import TypedDict

from django.core.servers.basehttp import (
    WSGIRequestHandler,
    get_internal_wsgi_application,
)
from django.core.servers.basehttp import WSGIServer
from django.core.management import CommandError, CommandParser  # type: ignore[attr-defined]

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.core.signals import request_started, request_finished
from django.db import close_old_connections
from django.test import override_settings
from django.utils.module_loading import import_string
from typing_extensions import Unpack

from atomicserver.atomic import AtomicSession


class OptionsDict(TypedDict):
    addrport: str
    collectstatic: bool
    use_ipv6: bool


class Command(BaseCommand):
    help = "Runs an atomic server"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "args",
            metavar="functions",
            nargs="*",
            help="Functions to call before running the server.",
        )
        parser.add_argument(
            "--addrport",
            default="127.0.0.1:8000",
            help="Port number or ipaddr:port to run the server on.",
        )
        parser.add_argument(
            "--collectstatic",
            action="store_true",
            help="Collects static files from static folder.",
        )
        parser.add_argument(
            "--ipv6",
            "-6",
            action="store_true",
            dest="use_ipv6",
            help="Start server on IPv6 address.",
        )

    def handle(self, *args: str, **options: Unpack[OptionsDict]) -> None:
        if options["collectstatic"]:
            call_command("collectstatic", interactive=False)

        try:
            addr, port = options["addrport"].split(":")
        except ValueError:
            raise CommandError("Not a valid address:port")

        for func in args:
            import_string(func)()

        database_settings = settings.DATABASES
        for db_settings in database_settings.values():
            db_settings["AUTO_COMMIT"] = False  # disabling autocommit allows rollback
        override_settings(DATABASES=database_settings)

        httpd = WSGIServer(
            (addr, int(port)), WSGIRequestHandler, ipv6=options.get("use_ipv6", False)
        )
        httpd.set_app(get_internal_wsgi_application())
        self.stdout.write(f"Starting atomic server on {options['addrport']}.")

        AtomicSession.enter_atomics()

        # connection signals closes the connections to the database. if it's
        # disconnected, we cant rollback as it will throw connection has been closed
        request_started.disconnect(close_old_connections)
        request_finished.disconnect(close_old_connections)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            self.stdout.write("\nShutting down E2E server.")
        finally:
            AtomicSession.rollback_atomics()
            AtomicSession.close_all()
