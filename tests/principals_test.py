from flask.testing import FlaskClient
from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client: FlaskClient, h_principal: dict[str, str]):
    response = client.get("/principal/assignments", headers=h_principal)

    assert response.status_code == 200

    data = response.json["data"]
    for assignment in data:
        assert assignment["state"] in [
            AssignmentStateEnum.SUBMITTED,
            AssignmentStateEnum.GRADED,
        ]


def test_grade_assignment_draft_assignment(
    client: FlaskClient, h_principal: dict[str, str]
):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 5, "grade": GradeEnum.A.value},
        headers=h_principal,
    )

    assert response.status_code == 400


def test_grade_assignment(client: FlaskClient, h_principal: dict[str, str]):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": GradeEnum.C.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.C


def test_regrade_assignment(client: FlaskClient, h_principal: dict[str, str]):
    response = client.post(
        "/principal/assignments/grade",
        json={"id": 4, "grade": GradeEnum.B.value},
        headers=h_principal,
    )

    assert response.status_code == 200

    assert response.json["data"]["state"] == AssignmentStateEnum.GRADED.value
    assert response.json["data"]["grade"] == GradeEnum.B


def test_get_teachers(client: FlaskClient, h_principal: dict[str, str]):
    response = client.get("/principal/teachers", headers=h_principal)

    assert response.status_code == 200
