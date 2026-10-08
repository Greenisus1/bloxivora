# Bloxivora

Offline terminal falling-block line-clear game. Version 1.0.1. Original terminal artwork; no account, desktop or telemetry. No assets or names taken from other games.

## Install and run

    bash app-store.sh install
    bash app-store.sh run

Python3 with curses (normally included on Linux). No downloaded dependencies.

Left/right or A/D move, Up/W rotates, Down/S steps down, Space drops immediately, P pauses, R restarts, Q quits. Seven shapes shuffled in bags, next-piece preview, line clear scores 100/300/500/800 multiplied by level, hard drop adds 2 per square. Gravity speeds up every 10 lines. Simple horizontal wall kicks, no standardized rotation system, hold, ghost, music, saves or online scores. Game ends when a new piece cannot spawn.

Interactive curses terminal at least 82x25. Too-small windows show a resize notice and retain/pause the game. Terminal default, no GUI and no desktop requirement. R with --seed restarts the same seeded sequence, otherwise a fresh random board. For a non-interactive snapshot, use:

    python3 bloxivora.py --seed 42 --demo

For tests:

    python3 -m unittest -v

13 core tests plus actual Linux PTY visual/input smoke. Linux tested; physical Raspberry Pi and non-Linux untested. Without curses the interactive game is unavailable. No paid features. games category marker line3; older stores still list/launch it. MIT license; see LICENSE.txt.

1.0.1: terminal startup failure exits with an error status rather than pretend success. Added gravity-floor, blocked-rotation and double-line compaction regressions. Core play unchanged.
