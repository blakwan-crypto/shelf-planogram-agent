expected: rejected
reason_contains: corrupt or unreadable
note: shelf3.jpg cut to its first 800 bytes — the JPEG header is intact but
the scan data ends mid-way. Stage 2 must reject it with a clear reason.
(Also in this folder: truncated_2000bytes.bin — at 2000 bytes PIL's
verify() is too lenient, the file slips past Stage 2 into the detector and
crashes it. That is a known pipeline gap this suite documents; see
SCENARIO_REPORT.md "Known robustness gaps".
