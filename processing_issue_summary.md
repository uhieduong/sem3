# Shared FFmpeg Slide Extraction Issue

## Issue

The shared slide-extraction code uses FFmpeg's `-vsync` option, but the installed FFmpeg build rejects it (`Unrecognized option 'vsync'`). The failure is recorded in the `db application` course's `lecture3` extraction log.

## Impact

All three courses use the same slide-extraction code, so this issue can prevent video keyframes from being extracted and slide decks from being aligned in any of them. In the observed `lecture3` run, the deck was detected (`lecture3.pdf`, 57 slides), but no frames were extracted. Its zero alignment counts do not mean the deck is empty or that slide matching failed; alignment was not performed.

## Status: RESOLVED

- The shared extraction command in `engine/vision.py` was updated to `-fps_mode vfr` (replacing the deprecated/unsupported `-vsync vfr`).
- All three `lecture3` tasks across all courses were rerun:
  - **`db application`**: 78 slides extracted, 78/78 aligned to `lecture3.pdf`.
  - **`se fundamentals`**: 237 slides extracted, 233/237 aligned to `lecture3.pdf`.
  - **`further prg`**: 254 slides extracted, 19/254 aligned (235 external website/screen activities flagged).
- All three tasks are now fully aligned and marked **Ready for Agent Audit**.
