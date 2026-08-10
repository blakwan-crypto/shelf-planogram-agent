expected: rejected
reason_contains: too large
note: shelf1.jpg upscaled to 8100px wide (9438px tall) — above the pipeline's
8000px maximum. Stage 2 must reject it. (Stage 2 reads only the header for
this check, so the file is never fully decoded.)
