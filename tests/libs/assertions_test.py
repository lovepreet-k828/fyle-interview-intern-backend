import pytest
from core.libs import assertions
from core.libs.exceptions import FyleError


def test_auth_success():
    # Condition is True, so no assertion should be raised
    response = assertions.assert_auth(True)
    assert response is None  # No response should be returned


def test_auth_failure():
    # Condition is False, so the base_assert should be called with 401 and 'UNAUTHORIZED'
    with pytest.raises(FyleError) as exc_info:
        assertions.assert_auth(False)
    assert exc_info.value.message == "UNAUTHORIZED"  # Check the error message
    assert exc_info.value.status_code == 401  # Check the status code


def test_assert_true_success():
    # Condition is True, so no assertion should be raised
    response = assertions.assert_true(True)
    assert response is None  # No response should be returned


def test_assert_true_failure():
    # Condition is False, so the base_assert should be called with 403 and 'FORBIDDEN'
    with pytest.raises(FyleError) as exc_info:
        assertions.assert_true(False)
    assert exc_info.value.message == "FORBIDDEN"  # Check the error message
    assert exc_info.value.status_code == 403  # Check the status code


def test_assert_valid_success():
    # Condition is True, so no assertion should be raised
    response = assertions.assert_valid(True)
    assert response is None  # No response should be returned


def test_assert_valid_failure():
    # Condition is False, so the base_assert should be called with 400 and 'BAD_REQUEST'
    with pytest.raises(FyleError) as exc_info:
        assertions.assert_valid(False)
    assert exc_info.value.message == "BAD_REQUEST"  # Check the error message
    assert exc_info.value.status_code == 400  # Check the status code


def test_assert_found_success():
    # Object is not None, so no assertion should be raised
    assertions.assert_found("some_object")


def test_assert_found_failure():
    # Object is None, so the base_assert should be called with 404 and 'NOT_FOUND'
    with pytest.raises(FyleError) as exc_info:
        assertions.assert_found(None)
    assert exc_info.value.message == "NOT_FOUND"  # Check the error message
    assert exc_info.value.status_code == 404  # Check the status code
