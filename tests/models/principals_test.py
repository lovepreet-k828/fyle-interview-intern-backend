import pytest
from core.models.principals import Principal


def test_principal_repr():
    # Create a Principal object with a known ID
    principal = Principal(id=123)

    # Call the __repr__ method
    repr_output = repr(principal)

    # Assert that the output matches the expected format
    assert repr_output == "<Principal 123>"
