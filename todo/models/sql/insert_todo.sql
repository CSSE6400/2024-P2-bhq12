INSERT INTO todos (
	title,
	description,
	completed,
	deadline_at,
	created_at,
	updated_at
)
SELECT
	? AS title,
	? AS description,
	COALESCE(?, False) AS completed,
	? AS deadline_at,
	CURRENT_TIMESTAMP AS created_at,
	CURRENT_TIMESTAMP AS updated_at;
