import pytest
from core.models.students import Student


def test_student_repr():
    # Create a Student object with a known ID
    student = Student(id=123)

    # Call the __repr__ method
    repr_output = repr(student)

    # Assert that the output matches the expected format
    assert repr_output == "<Student 123>"
