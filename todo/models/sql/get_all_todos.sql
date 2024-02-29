SELECT
	*
FROM todos
WHERE (completed = ?1 OR ?1 IS NULL)
AND (deadline_at BETWEEN CURRENT_DATE AND DATE(CURRENT_DATE, '+' || $2 || ' days') OR ?2 IS NULL)
