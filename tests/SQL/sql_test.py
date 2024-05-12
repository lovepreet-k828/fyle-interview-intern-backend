import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def get_graded_assignments_count_by_teacher(teacher_id: int = 1) -> int:
    """
    Get the count of assignments being gradded by a particular teacher

    Parameters:
    - teacher_id (int): The ID of the teacher by which assignments are being graded

    Returns:
    - int: Count of graded assignments
    """
    return sum(
        1
        for assignment in Assignment.get_assignments_by_teacher(teacher_id)
        if assignment.state == AssignmentStateEnum.GRADED
    )


def create_n_graded_assignments_for_teacher(
    number: int = 0, teacher_id: int = 1
) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id, Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content="test content",
            state=AssignmentStateEnum.GRADED,
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 2 and change its state to 'GRADED'
    student1_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)
    student2_assignments: Assignment = Assignment.filter(Assignment.student_id == 2)

    student1_graded_assignments = 0
    student2_graded_assignments = 0

    # Iterate over each assignment and update its state
    for assignment in student1_assignments:
        if assignment.state == AssignmentStateEnum.GRADED:
            student1_graded_assignments = student1_graded_assignments + 1

    # Iterate over each assignment and update its state
    for assignment in student2_assignments:
        if assignment.state == AssignmentStateEnum.GRADED:
            student2_graded_assignments = student2_graded_assignments + 1

    # Define the expected result
    expected_result = [
        (1, student1_graded_assignments),
        (2, student2_graded_assignments),
    ]

    # Execute the SQL query and compare the result with the expected result
    with open(
        "tests/SQL/number_of_graded_assignments_for_each_student.sql", encoding="utf8"
    ) as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()

    assert expected_result == sql_result


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open(
        "tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql",
        encoding="utf8",
    ) as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    desired_grade_a_count = create_n_graded_assignments_for_teacher(5)
    desired_teacher_id = 1

    # if a different teacher has more assignments
    if get_graded_assignments_count_by_teacher(
        2
    ) > get_graded_assignments_count_by_teacher(1):
        # Just count the number of 'A' graded assignments by a different teacher (teacher_id=2)
        desired_grade_a_count = create_n_graded_assignments_for_teacher(teacher_id=2)
        desired_teacher_id = 2

    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()

    assert desired_grade_a_count == sql_result[0][1]

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    desired_grade_a_count = create_n_graded_assignments_for_teacher(10, 2)
    desired_teacher_id = 2

    # if a default teacher has more assignments
    if get_graded_assignments_count_by_teacher(
        1
    ) >= get_graded_assignments_count_by_teacher(2):
        # Just count the number of 'A' graded assignments by default teacher (teacher_id=1)
        desired_grade_a_count = create_n_graded_assignments_for_teacher()
        desired_teacher_id = 1

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()

    # Define the expected result
    expected_result = [(desired_teacher_id, desired_grade_a_count)]
    assert expected_result == sql_result
