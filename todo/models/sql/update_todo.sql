UPDATE todos
SET
	title = coalesce(?, title),
	description = coalesce(?, description),
	completed = coalesce(?, completed),
	deadline_at = coalesce(?, deadline_at),
	updated_at = current_timestamp
WHERE id = ?;
