# "Hey LeRobot!" Hybrid Assistant — 48-Hour Sprint Plan

*This document outlines a 48-hour sprint plan to build a proof-of-concept voice assistant. The goal is to create a functional prototype that can be installed and demonstrated easily.*

---

### Project Description

"Hey LeRobot!" is a Python-based voice assistant that runs locally. It uses a custom wake-word to begin listening, transcribes speech to text, understands user intent via a large language model (LLM), and executes predefined actions (like opening a URL or telling a joke).

### Target File Structure

```
lerobot/
├── lerobot/
│   ├── __init__.py
│   ├── app.py
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── capture.py
│   │   ├── ringbuffer.py
│   │   └── wakeword.py
│   ├── cloud/
│   │   ├── __init__.py
│   │   ├── openai_llm.py
│   │   └── openai_stt.py
│   ├── nlu/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── schema.py
│   ├── actions/
│   │   ├── __init__.py
│   │   ├── system.py
│   │   └── web.py
│   ├── tts/
│   │   ├── __init__.py
│   │   └── tts_openai.py
│   └── utils/
│       ├── __init__.py
│       └── wav_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_ringbuffer.py
│   └── test_router.py
├── .env.example
├── .gitignore
├── environment.yml
└── README.md
```

---

## 🟡  Step 1 – Project scaffold & dev environment

**TODO**

* [x] Create `environment.yml` for Conda with Python 3.10.
* [x] Add deps: `python-sounddevice`, `openwakeword` (pip), `pydantic`, `aiofiles`, `python-dotenv`, `httpx`, `pytest`, `pytest-asyncio`.
* [x] Commit baseline dir tree (see blueprint above).
* [ ] Provide `.env.example` with `OPENAI_API_KEY`, etc.
* [x] Set up **pre-commit** hooks (black, isort, ruff) within the Conda environment.

**Deliverable:** Repo installs with `conda env create -f environment.yml` & `pytest -q` passes 0 tests.

---

## 🟡  Step 2 – Audio pipeline & wake-word

**TODO**

* [x] `audio/capture.py`: async generator yielding 20 ms int16 frames via `sounddevice.InputStream`.
* [x] `audio/ringbuffer.py`: simple deque (capacity 2 s).
* [x] `audio/wakeword.py`: wrap `openwakeword` (load model, return bool on each frame).
* [ ] **Record 20 samples** of "Hey LeRobot!" from team members; train custom model (CLI).
* [x] Integrate optional `silero-vad` gate (config flag).
* [x] CLI demo (`python -m lerobot.cli listen`) prints "WAKE!" on trigger.

**Deliverable:** Local console app that prints a wake notice reliably (<2 false triggers / min).

---

## 🟡  Step 3 – STT via OpenAI Whisper endpoint

**TODO**

* [ ] `cloud/openai_stt.py`: function `transcribe(wav_path) -> str` using `/v1/audio/transcriptions` (`model="whisper-1"`).
* [ ] Add `utils/wav_utils.py` (PCM→WAV temp file).
* [ ] Connect wake-word event to write **last 2 s** + **live stream until silence** (simple 1 s no-speech timeout).
* [ ] Print transcript for manual verification.

**Deliverable:** Running process: say "Hey LeRobot … what time is it?" ⇒ transcript printed.

---

## 🟡  Step 4 – LLM intent → action

**TODO**

* [ ] Design `nlu/schema.py` (`ActionRequest`, `ActionResult`).
* [ ] Draft **5–8 sample actions** in `actions/` (`open_url`, `tell_time`, `search_web`, `volume_up`, `joke`).
* [ ] `cloud/openai_llm.py`: call `/v1/chat/completions` with **function-calling** describing above actions.
* [ ] `nlu/router.py`: match JSON to registered functions, execute, return result.
* [ ] Log structured trace (`UTC timestamp`, transcript, action, result).

**Deliverable:** End-to-end CLI— query "Hey LeRobot, open github dot com" automatically launches browser tab.

---

## 🟡  Step 5 – Basic TTS response (optional)

**TODO**

* [ ] `tts/tts_openai.py`: hit `/v1/audio/speech` (or fallback `pyttsx3` offline).
* [ ] Stream playback via `sounddevice.OutputStream`.
* [ ] Config flag `--speak`.

**Deliverable:** Assistant replies aloud after executing an action.

---

## 🟡  Step 6 – Packaging & UX polish

**TODO**

* [ ] Add `app.py` (AsyncOrchestrator) with graceful Ctrl-C shutdown.
* [ ] Implement `--debug` (verbose logging) & `--no-tts` CLI flags.
* [ ] Create simple **tray icon** or **Tkinter window** with mute/unmute button (stretch).
* [ ] Generate `requirements.txt` for pip users via `conda list -e > requirements.txt`.

**Deliverable:** Single command `python -m lerobot.app` runs full assistant with flags.

---

## 🟡  Step 7 – Testing & CI

**TODO**

* [ ] Unit-test `ringbuffer`, `wakeword` (mock model), `router` (mock OpenAI).
* [ ] Integration test: feed prerecorded WAV, assert action JSON.
* [ ] GitHub Actions workflow: lint, tests on push.

**Deliverable:** Green CI badge; >80 % coverage on core logic.

---

## 🟡  Step 8 – Demo script & docs

**TODO**

* [ ] Update `README.md` with setup, running, example queries.
* [ ] Record 60-second **screen capture** demo.
* [ ] Add "Known Issues & Next Steps" section.

**Deliverable:** Ready-to-show demo video + polished README.

---

## ⏲  Buffer / Stretch Goals (any spare time)

* ℹ️  Replace temp-file STT upload with **in-memory bytes**.
* 🌐  Add action: "summarize this web page" (requests → GPT).
* 🔒  Encrypt API key using OS keyring.

---

### Success definition for the hackathon

> **You can speak a wake phrase, ask a simple command, hear/see a correct response, and the whole thing installs in < 5 minutes on another laptop.**