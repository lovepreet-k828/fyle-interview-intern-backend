from flask.testing import FlaskClient
from core.models.assignments import Assignment, AssignmentStateEnum
from core import db


def test_get_assignments_student_1(client: FlaskClient, h_student_1: dict[str, str]):
    response = client.get("/student/assignments", headers=h_student_1)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["student_id"] == 1


def test_get_assignments_student_2(client: FlaskClient, h_student_2: dict[str, str]):
    response = client.get("/student/assignments", headers=h_student_2)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["student_id"] == 2


def test_post_assignment_null_content(client: FlaskClient, h_student_1: dict[str, str]):
    """
    failure case: content cannot be null
    """

    response = client.post(
        "/student/assignments", headers=h_student_1, json={"content": None}
    )

    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "content cannot be null"


def test_post_assignment_student_1(client: FlaskClient, h_student_1: dict[str, str]):
    content = "ABCD TESTPOST"

    response = client.post(
        "/student/assignments", headers=h_student_1, json={"content": content}
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["content"] == content
    assert data["state"] == "DRAFT"
    assert data["teacher_id"] is None


def test_update_assignment_student_1(client: FlaskClient, h_student_1: dict[str, str]):
    draft_assignment = Assignment(student_id=1, content="new content TESTUPDATE")

    # Add the assignment to the database session
    db.session.add(draft_assignment)
    db.session.commit()
    response = client.post(
        "/student/assignments",
        headers=h_student_1,
        json={"content": draft_assignment.content, "id": draft_assignment.id},
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["id"] == draft_assignment.id
    assert data["content"] == draft_assignment.content
    assert data["state"] == "DRAFT"
    assert data["teacher_id"] is None


def test_submit_assignment_student_1(client: FlaskClient, h_student_1: dict[str, str]):
    draft_assignment = Assignment(
        student_id=1,
        content="test content",
    )

    # Add the assignment to the database session
    db.session.add(draft_assignment)
    db.session.commit()

    response = client.post(
        "/student/assignments/submit",
        headers=h_student_1,
        json={"id": draft_assignment.id, "teacher_id": 2},
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["student_id"] == 1
    assert data["state"] == "SUBMITTED"
    assert data["teacher_id"] == 2


def test_assignment_resubmit_error(client: FlaskClient, h_student_1: dict[str, str]):
    submitted_assignment = Assignment(
        teacher_id=2,
        student_id=1,
        content="test content",
        state=AssignmentStateEnum.SUBMITTED,
    )

    # Add the assignment to the database session
    db.session.add(submitted_assignment)
    db.session.commit()

    response = client.post(
        "/student/assignments/submit",
        headers=h_student_1,
        json={"id": submitted_assignment.id, "teacher_id": 2},
    )
    error_response = response.json
    assert response.status_code == 400
    assert error_response["error"] == "FyleError"
    assert error_response["message"] == "only a draft assignment can be submitted"
