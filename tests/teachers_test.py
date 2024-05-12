from flask.testing import FlaskClient
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum
from core import db


def test_get_assignments_teacher_1(client: FlaskClient, h_teacher_1: dict[str, str]):
    response = client.get("/teacher/assignments", headers=h_teacher_1)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["teacher_id"] == 1


def test_get_assignments_teacher_2(client: FlaskClient, h_teacher_2: dict[str, str]):
    response = client.get("/teacher/assignments", headers=h_teacher_2)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["teacher_id"] == 2
        assert assignment["state"] in ["SUBMITTED", "GRADED"]


def test_grade_assignment(client: FlaskClient, h_teacher_1: dict[str, str]):
    submitted_assignment = Assignment(
        teacher_id=1,
        student_id=1,
        content="test content",
        state=AssignmentStateEnum.SUBMITTED,
    )

    # Add the assignment to the database session
    db.session.add(submitted_assignment)
    db.session.commit()

    response = client.post(
        "/teacher/assignments/grade",
        headers=h_teacher_1,
        json={"id": submitted_assignment.id, "grade": "A"},
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["student_id"] == 1
    assert data["teacher_id"] == 1
    assert data["state"] == AssignmentStateEnum.GRADED
    assert data["grade"] == GradeEnum.A


def test_grade_assignment_cross(client: FlaskClient, h_teacher_2: dict[str, str]):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        "/teacher/assignments/grade", headers=h_teacher_2, json={"id": 1, "grade": "A"}
    )

    error_response = response.json
    assert response.status_code == 401
    assert error_response["error"] == "FyleError"
    assert (
        error_response["message"]
        == "This assignment is being submitted to some other teacher"
    )


def test_grade_assignment_bad_grade(client: FlaskClient, h_teacher_1: dict[str, str]):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        "/teacher/assignments/grade", headers=h_teacher_1, json={"id": 1, "grade": "AB"}
    )

    assert response.status_code == 400
    data = response.json

    assert data["error"] == "ValidationError"


def test_grade_assignment_bad_assignment(
    client: FlaskClient, h_teacher_1: dict[str, str]
):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        "/teacher/assignments/grade",
        headers=h_teacher_1,
        json={"id": 100000, "grade": "A"},
    )

    error_response = response.json
    assert response.status_code == 404
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "No assignment with this id was found"


def test_grade_assignment_draft_assignment(
    client: FlaskClient, h_teacher_1: dict[str, str]
):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        "/teacher/assignments/grade", headers=h_teacher_1, json={"id": 5, "grade": "A"}
    )

    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "only a submitted assignment can be graded"
