from typing import Any

from django.db import DEFAULT_DB_ALIAS, connections, transaction
from django.db.transaction import Atomic


class AtomicSession:
    scope: dict[str, Any] | None = None

    @classmethod
    def databases_names(cls, include_mirrors: bool = True) -> list[str]:
        # Only consider allowed database aliases, including mirrors or not.
        return [
            alias
            for alias in connections
            if alias in {DEFAULT_DB_ALIAS}
            and (
                include_mirrors
                or not connections[alias].settings_dict["TEST"]["MIRROR"]
            )
        ]

    @classmethod
    def enter_atomics(cls) -> None:
        """Open atomic blocks for multiple databases."""
        atomics = {}
        for db_name in cls.databases_names():
            atomic: Atomic = transaction.atomic(using=db_name)
            atomic._from_testcase = True  # type: ignore[attr-defined]
            atomic.__enter__()
            atomics[db_name] = atomic
        cls.scope = atomics

    @classmethod
    def rollback_atomics(cls) -> None:
        """Rollback atomic blocks opened by the previous method."""
        if cls.scope is None:
            raise ValueError("Not inside an atomic context")

        for db_name in reversed(cls.databases_names()):
            transaction.set_rollback(True, using=db_name)
            cls.scope[db_name].__exit__(None, None, None)

    @classmethod
    def close_all(cls) -> None:
        connections.close_all()
