import pytest
from unittest.mock import patch, MagicMock
from core.models.teachers import Teacher


def test_get_all_teachers_details():
    # Create a MagicMock to represent the return value of query.all()
    mock_teacher_1 = MagicMock(id=1)
    mock_teacher_2 = MagicMock(id=2)
    mock_return_value = [mock_teacher_1, mock_teacher_2]

    # Mock the query.all() method of Teacher
    with patch.object(Teacher, "query") as mock_query:
        # Set up the return value of query.all()
        mock_query.all.return_value = mock_return_value

        # Call the class method under test
        teachers = Teacher.get_all_teachers_details()

        # Assert that the query.all() method was called
        mock_query.all.assert_called_once()

        # Assert that the return value matches the mocked return value
        assert teachers == mock_return_value


def test_teacher_repr():
    # Create a Teacher object with a known ID
    teacher = Teacher(id=123)

    # Call the __repr__ method
    repr_output = repr(teacher)

    # Assert that the output matches the expected format
    assert repr_output == "<Teacher 123>"
