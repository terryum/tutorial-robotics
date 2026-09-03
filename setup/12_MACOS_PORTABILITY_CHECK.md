# Optional macOS Portability Check

This is not a curriculum prerequisite. Run it only to confirm that the shared project remains usable while mobile.

Check:

- native arm64 Python and no accidental Rosetta dependency
- MuJoCo viewer/offscreen rendering
- MPS availability and CPU fallback
- small PPO/BC/ACT memory ceiling
- RoboStack ROS 2 basics if installed
- SSH to WS2/WS1 and Isaac WebRTC/browser client
- rerun one completed core tutorial without changing global progress

Write a host-specific verification report and do not replace canonical training results.
