# Shared FFmpeg Slide Extraction Issue

## Issue

The shared slide-extraction code uses FFmpeg's `-vsync` option, but the installed FFmpeg build rejects it (`Unrecognized option 'vsync'`). The failure is recorded in the `db application` course's `lecture3` extraction log.

## Impact

All three courses use the same slide-extraction code, so this issue can prevent video keyframes from being extracted and slide decks from being aligned in any of them. In the observed `lecture3` run, the deck was detected (`lecture3.pdf`, 57 slides), but no frames were extracted. Its zero alignment counts do not mean the deck is empty or that slide matching failed; alignment was not performed.

## Recommended next step

Update the shared extraction command in `engine/vision.py` to use `-fps_mode vfr` instead of `-vsync vfr`. Then rerun affected tasks with `--force` to regenerate keyframes and alignment reports.
