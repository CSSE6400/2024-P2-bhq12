SELECT
	*
FROM todos
WHERE (completed = ?1 OR ?1 IS NULL);
