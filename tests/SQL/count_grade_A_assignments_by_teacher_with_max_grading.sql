-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT a.teacher_id,
    COUNT(a.id) AS num_grade_a
FROM assignments a
    JOIN (
        SELECT teacher_id
        FROM assignments
        WHERE assignments.state = "GRADED"
        GROUP BY teacher_id
        ORDER BY COUNT(id) DESC,
            teacher_id ASC
        LIMIT 1
    ) AS max_teacher ON a.teacher_id = max_teacher.teacher_id
    AND a.grade = 'A'
GROUP BY a.teacher_id;