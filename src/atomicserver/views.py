from http import HTTPStatus


from django.http import HttpResponse, HttpRequest

from atomicserver.atomic import AtomicSession


def begin(request: HttpRequest) -> HttpResponse:
    AtomicSession.enter_atomics()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


def rollback(request: HttpRequest) -> HttpResponse:
    AtomicSession.rollback_atomics()
    return HttpResponse(status=HTTPStatus.NO_CONTENT)
