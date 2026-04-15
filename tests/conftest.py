import os
from collections.abc import Callable
from typing import cast

import pytest
from hypothesis import HealthCheck, settings

on_ci = bool(os.getenv('CI'))
max_examples = settings().max_examples
settings.register_profile(
    'default',
    deadline=None,
    derandomize=False,
    max_examples=max_examples,
    suppress_health_check=[HealthCheck.too_slow],
)

# FIXME:
#  workaround until https://github.com/pytest-dev/pluggy/issues/191 is fixed
hookimpl = cast(
    Callable[..., Callable[[Callable[..., None]], Callable[..., None]]],
    pytest.hookimpl,
)


@hookimpl(trylast=True)
def pytest_sessionfinish(
    session: pytest.Session, exitstatus: pytest.ExitCode
) -> None:
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        session.exitstatus = pytest.ExitCode.OK
