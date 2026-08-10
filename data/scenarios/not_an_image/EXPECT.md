expected: rejected
reason_contains: corrupt or unreadable
note: notes.jpg is really a text file wearing a .jpg name — Stage 2 must
reject it. notes.txt (a real .txt) never reaches the pipeline at all: the
orchestrator only iterates files whose extension is a known image type, so
the .txt is ignored by design, not by accident.
