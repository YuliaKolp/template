import json
from contextlib import contextmanager
from typing import Generator


import httpx

success_codes = {
    httpx.codes.OK: "200 - OK",
    httpx.codes.CREATED: "201 - Created",
    httpx.codes.ACCEPTED: "202 - Accepted",
    httpx.codes.NO_CONTENT: "204 - No Content",
    httpx.codes.RESET_CONTENT: "205 - Reset Content",
    httpx.codes.PARTIAL_CONTENT: "206 - Partial Content"
}


@contextmanager  # type: ignore[arg-type]
def check_status_code_http(
        exception: type[Exception],
        expected_status_code: httpx.codes = httpx.codes.OK,
        expected_message: str = "",
        ) -> Generator:
    try:
        yield
        if expected_status_code not in success_codes:
            raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Должно быть получено сообщение '{expected_message}', но запрос прошел успешно")
    except exception as e:
        if hasattr(e, 'status'):
            assert e.status == expected_status_code
        else:
            raise AssertionError(f"Исключение {type(e)} не имеет атрибута 'status'")
        if hasattr(e, 'body'):
            if expected_message:
                actual_title = json.loads(e.body)['title']
                assert actual_title == expected_message, f"Должно быть получено сообщение {expected_message}', но получено '{actual_title}'"
        else:
            raise AssertionError(f"Исключение {type(e)} не имеет атрибута 'body'")
