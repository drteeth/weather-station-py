# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A teaching-oriented MicroPython workshop. Learners build a battery-powered weather station on an ESP32-C6 board that reads temperature/humidity/pressure from a BME280 sensor and serves them on a webpage. `slides.md` is the workshop deck — it walks learners through writing `main.py` line-by-line. `doc/done.py` is the finished reference implementation.

`main.py` is intentionally empty in the repo: learners fill it in as they follow the slides. Do not add code to it unless the user explicitly asks — and even then, prefer pointing at `doc/done.py`.

## Audience for docs

User-facing docs (README, slides) target first-time learners — kids and beginners — not software engineers. Use plain English, expand acronyms inline ("WLAN means WiFi"), describe what learners physically see and touch before explaining abstractions, and avoid SE jargon ("REPL", "vendored", "spike"). Lead with what something *does*, not what it's built from.

## Commands beyond the README

The README covers `setup` / `flash-firmware` / `flash` / `connect`. Also useful:

- `script/reset` — hard-reset the board without opening a REPL.
- `script/slides` — live-preview `slides.md` at http://localhost:8080 via marp-cli (requires `npx`).
- `script/render-slides` — render `slides.md` → `slides.html` (one-shot).

All scripts respect `PORT=/dev/ttyXXX` for non-default serial devices. There is no test suite, linter, or build step — the "build" is `script/flash`.

## Layout that isn't obvious from a file listing

- `lib/` — third-party MicroPython libraries downloaded by `script/setup` (`bme280.py` sensor driver, `microdot.py` web framework). Don't hand-edit; setup refetches them.
- `bin/` — MicroPython firmware images, downloaded by setup. `*.bin` is gitignored.
- `slides.html` is generated from `slides.md` — edit the markdown, not the HTML.

## Hardware constraints to remember

- WiFi must be 2.4 GHz; 5 GHz won't work on the ESP32-C6.
- I²C is on `Pin(6)` (SDA) and `Pin(7)` (SCL). BME280 is at address `0x76` (118); the battery fuel gauge is at `0x36`.
- The webpage auto-refreshes every 10 seconds via `<meta http-equiv="refresh">` — no JS, no websockets.
