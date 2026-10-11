# MindPulse AI 🧠

> **A privacy-first, one-session wellbeing check-in for students. A short video, a written paragraph, and a few ratings become an evidence-backed summary of what is weighing on you, with honest uncertainty and a clear path to a real person when it matters. Nothing is stored.**

Built for the **AMD Developer Hackathon: ACT III**, **Track 2: Health and Wellbeing**.

MindPulse AI is **not** a diagnostic tool. It never says a person "has" a condition. It is a reflection and navigation aid.

---

## 📌 Table of Contents

- [Problem](#-problem)
- [Solution](#-solution)
- [How It Works](#-how-it-works)
- [System Architecture](#-system-architecture)
- [Analysis Branches](#-analysis-branches)
- [Fusion and the Red Alarm](#-fusion-and-the-red-alarm)
- [Safety and Privacy](#-safety-and-privacy)
- [AI Models](#-ai-models)
- [AMD Component](#-amd-component)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [API Overview](#-api-overview)
- [Evaluation](#-evaluation)
- [Running the Project](#-running-the-project)
- [Limitations](#-limitations)
- [Future Work](#-future-work)
- [Team](#-team)
- [Disclaimer](#-disclaimer)

---

## 🚨 Problem

Students deal with academic pressure, poor sleep, social isolation, money worries, and emotional exhaustion. These pressures build up quietly, and many students cannot name what is actually weighing on them, or whether it is serious enough to ask for help.

Existing wellness apps usually fall into two groups:

- **Questionnaire apps** that reduce a complicated week to one score.
- **Sentiment tools** that label text as positive or negative and say nothing about the cause.

Two further problems:

1. Students do not know **what to bring** to a friend, mentor, or counselor.
2. Students **do not trust apps** with sensitive information. Most wellness tools create accounts and keep history, which is a barrier on its own.

---

## 💡 Solution

MindPulse AI is a **guided, one-session check-in**.

1. The student records short spoken answers (video or voice only) and writes a short paragraph.
2. They answer five quick rating questions.
3. The system analyzes each input **independently**, then merges the results with **fixed, transparent rules**.
4. It shows the **specific stressors**, each with the student's own words as evidence, a confidence level, and what it is unsure about.
5. If it detects a possible crisis, it shows a **red alarm** with verified helplines and nearby help.
6. Otherwise it shows a **dashboard** with a side chat and two downloadable PDFs: a wellbeing summary and a 15-day plan.
7. The session ends and **nothing is stored**.

---

## 🧭 How It Works

```text
Landing notice (English only, not a diagnosis, nothing stored)
   ↓
Consent: video + audio, or voice only
   ↓
Profile: age (18-25), country, city
   ↓
3 spoken questions (each analyzed in the background as soon as it is recorded)
   ↓
Written paragraph
   ↓
5 rating questions (1-5)
   ↓
Fusion (fixed rules)
   ↓
┌────────────────────────────┬─────────────────────────────────────────┐
│ Red alarm                  │ Dashboard                               │
│ Verified helplines first   │ Overall level + confidence              │
│ Nearby help loads after    │ Stressors with the student's own quotes │
│                            │ Side chat                               │
│                            │ PDF 1: wellbeing summary                │
│                            │ PDF 2: 15-day plan                      │
└────────────────────────────┴─────────────────────────────────────────┘
   ↓
End session: all state is cleared
```

---

## 🏗 System Architecture

```text
                       STUDENT (browser, React + TypeScript)
          holds all session data in memory only (no localStorage, no cookies)
                                   │
        consent → profile → 3 spoken answers → paragraph → ratings
                                   │
                                   ▼
                     ┌───────────────────────────┐
                     │   FastAPI (stateless)     │
                     │   no database             │
                     │   no request-body logging │
                     └─────────────┬─────────────┘
                                   │
       ┌──────────────┬────────────┴───────────┬──────────────┐
       ▼              ▼                        ▼              ▼
┌─────────────┐ ┌───────────────┐     ┌────────────────┐ ┌──────────────┐
│ SPOKEN      │ │ VIDEO         │     │ PARAGRAPH      │ │ RATINGS      │
│ audio →     │ │ frames →      │     │ text →         │ │ 5 items →    │
│ transcript  │ │ vision model  │     │ LLM indicators │ │ scoring      │
│ → LLM       │ │ (observable   │     │ + quote check  │ │ + safety item│
│ indicators  │ │ cues only)    │     │                │ │              │
└──────┬──────┘ └───────┬───────┘     └───────┬────────┘ └──────┬───────┘
       │                │                     │                 │
       └────────────────┴──────────┬──────────┴─────────────────┘
                                   ▼
                  ┌──────────────────────────────────┐
                  │ CRISIS RULES (deterministic)     │
                  │ run on every transcript, the     │
                  │ paragraph, ratings, and chat     │
                  └────────────────┬─────────────────┘
                                   ▼
                  ┌──────────────────────────────────┐
                  │ FUSION (fixed weights, config)   │
                  └───────┬──────────────────┬───────┘
                          │                  │
                 red alarm                dashboard
                          │                  │
              Verified helplines      ┌──────┴────────────────┐
              + nearby help           │ Plan │ PDFs │ Chat    │
                                      └───────────────────────┘
```

**The server keeps nothing between requests.** The browser holds every branch result in memory and sends what the next step needs. Closing or refreshing the tab ends the session.

---

## 🔬 Analysis Branches

Each branch is analyzed **independently** and returns the same kind of result: a score, a level, a confidence, evidence, and warnings.

| Branch | Input | What it does | Weight in score |
|---|---|---|---|
| **Spoken** | Audio from the video or voice recording | Speech-to-text, then an LLM extracts stressor indicators with exact supporting quotes | Yes |
| **Paragraph** | Written text | LLM extracts the same indicators with quotes | Yes |
| **Ratings** | Five 1-5 questions | Deterministic scoring, plus a safety item | Yes |
| **Video** | 8 sampled frames | A vision model reports only observable cues (face visible, looking at the camera, yawning, head down, restlessness). It never names emotions or conditions. | **No.** Supporting note only; it can lower confidence and add a "mixed signals" note. |

### Ten fixed indicators

`hopelessness`, `exhaustion`, `overwhelm`, `low_motivation`, `social_withdrawal`, `sleep_disruption`, `concentration`, `academic_pressure`, `financial_stress`, `relationship_stress`

Each indicator gets a level from 0 to 3, a confidence, and **an exact quote from the student's own words**. If the model cannot quote it, the level is 0. Quotes are verified in code, and any indicator whose quote cannot be found in the source is dropped.

The LLM only extracts evidence. **Code computes the score.**

---

## ⚖️ Fusion and the Red Alarm

Fusion is a **pure, deterministic function**. Weights and thresholds are in `backend/app/data/fusion.yaml`. No model is called at this step.

```yaml
branch_weights: { paragraph: 0.35, spoken: 0.30, ratings: 0.35 }   # video weight is 0 by design
levels: { moderate_min: 35, high_min: 65 }
high_signal_min_confidence: 0.5
red_alarm: { crisis_any_source: true, safety_rating_min: 2, high_branches_required: 2 }
```

**The red alarm triggers when:**

- crisis language is detected in any transcript, the paragraph, or a chat message, **or** the safety rating is answered above "never", **or**
- **two independent branches** (spoken, paragraph, ratings) are both high with enough confidence.

The video branch never triggers an alarm and never counts as one of the two.

**Human review is recommended** when overall confidence is low, branches disagree strongly, too few branches succeeded, or the video disagrees with the rest. The dashboard then says so plainly instead of guessing.

---

## 🔐 Safety and Privacy

MindPulse AI is a wellbeing reflection tool. It is not a replacement for psychologists, doctors, or emergency services.

### Safety design

- **No diagnosis.** The product never states or implies a condition. Wording is "high stress and burnout signals".
- **Evidence required.** Every stressor shows the student's own quote, verified in code.
- **Uncertainty is visible.** Every result shows a confidence level, and low confidence shows a "please talk to a person" message.
- **Crisis rules are deterministic.** Self-harm language is matched by rules, not by a learned model. An optional LLM second check can **add** a trigger but can never remove one.
- **Helplines never come from a model.** Emergency numbers and hotlines come from a hand-verified list (with source link and verification date). Local places come from search, and every phone number and address is **copied from the fetched page text by code**, never written by a model. Results carry a "please verify" notice, and the helplines show first and never wait for search.
- **Banned wording check** on all generated text (no diagnosis, no medication or dosage advice).
- **Age and scope:** designed for ages 18-25 (self-declared), English only.

### Privacy design

- **No database, no accounts, no login, no browser storage.**
- Video and audio are processed **in memory**; any unavoidable temp file is deleted in a `finally` block.
- Server logs never contain request bodies, filenames, transcripts, or model outputs.
- PDFs are generated in memory and streamed to the student. They are the only thing that persists, on the student's own device.
- **Content is sent to model providers to produce results.** The consent screen says so honestly. It is "processed and not stored by us", not "never leaves your device".
- The video is optional. Voice-only works fully.
- An automated canary test checks that logs and temp directories contain none of the user's content.

---

## 🤖 AI Models

All model calls go through provider interfaces, so any task can be pointed at a different provider, or at a self-hosted endpoint, by changing an environment variable.

| Task | Approach |
|---|---|
| Speech to text | Hosted Whisper-family or transcription model, English forced |
| Stressor extraction | Open instruction-tuned LLM (via Fireworks) or an OpenAI model, chosen by a bake-off on our labeled set, with JSON-schema output |
| Frame observation | Vision-capable model that sees sampled frames and reports observable cues only |
| Plan and chat | Same LLM family, with strict system prompts and output guards |
| Crisis detection | **Rules only** (optional LLM second check that can only add triggers) |

Every LLM output goes through: schema validation, one retry, deterministic verifiers (quote check, banned phrases, range clamps, 15-day plan checks), and a safe fallback. A failure never produces made-up content.

No model is trained or fine-tuned in this project.

> **Model selection results:** to be filled after the bake-off (see [Evaluation](#-evaluation)).

---

## 🟥 AMD Component

> **Status: to be finalized.**
>
> The hackathon requires a meaningful part of the working product to run on AMD infrastructure. The team will fill in this section with:
>
> - which component runs on AMD (for example speech-to-text, or the main LLM served with vLLM on ROCm),
> - the instance type used,
> - measured latency and throughput.

---

## 🛠️ Technology Stack

**Frontend:** React, TypeScript, Vite, React Router, Zustand (in-memory only), MediaRecorder API

**Backend:** Python 3.11, FastAPI, Pydantic v2, Uvicorn, httpx, ffmpeg, `phonenumbers`, `rapidfuzz`, ReportLab, `sse-starlette`

**AI providers:** Fireworks AI, OpenAI (interchangeable behind provider interfaces)

**Testing and evaluation:** pytest, scikit-learn, a custom `/eval` harness

**Deployment:** Docker, Docker Compose

---

## 📁 Project Structure

```text
mindpulse/
├── frontend/               # Vite + React + TypeScript
│   └── src/
│       ├── api/            # fetch client, generated types
│       ├── store/          # in-memory session store
│       ├── screens/        # Landing, Consent, Profile, SpokenQuestions, Paragraph,
│       │                   # Ratings, Processing, RedAlarm, Dashboard, EndSession
│       ├── components/
│       └── hooks/
├── backend/
│   └── app/
│       ├── main.py  schemas.py  config.py
│       ├── routers/        # analyze, fuse, resources, plan, reports, chat, health
│       ├── services/       # media, asr, crisis, text_analyzer, speech_features,
│       │                   # video_analyzer, ratings, fusion, resources,
│       │                   # plan_generator, pdf_builder, chat_service, providers/
│       ├── data/           # crisis_terms, helplines, indicators, fusion.yaml,
│       │                   # banned_phrases, fallback_plans
│       └── prompts/        # text_analysis, video_observation, plan, chat_system,
│                           # resource_extract
├── eval/                   # datasets, run_all.py, report.md
├── docker-compose.yml
├── .env.example
└── README.md
```

The Pydantic models in `backend/app/schemas.py` are the single source of truth for every JSON shape. The frontend generates its TypeScript types from the backend's OpenAPI file.

---

## 🔌 API Overview

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/config` | Questions, rating items, limits, countries |
| POST | `/api/v1/analyze/spoken` | One spoken answer (video or audio) |
| POST | `/api/v1/analyze/paragraph` | Written paragraph |
| POST | `/api/v1/analyze/ratings` | Five ratings |
| POST | `/api/v1/fuse` | Merge branches and decide the alert |
| POST | `/api/v1/resources/lookup` | Helplines and local places |
| POST | `/api/v1/plan` | 15-day plan |
| POST | `/api/v1/report/summary-pdf` | Wellbeing summary PDF |
| POST | `/api/v1/report/plan-pdf` | 15-day plan PDF |
| POST | `/api/v1/chat` | Side chat (SSE stream) |

The current repository is a starter skeleton: all endpoints return HTTP 501 except
`GET /api/v1/health`, which returns `{"status":"ok","version":"0.1.0"}`.
Interactive documentation is available at `/docs` when the backend is running.

---

## 📊 Evaluation

We evaluate every JSON output the system produces. All evaluation code is in `/eval` and runs with:

```bash
python -m eval.run_all --report eval/report.md
```

**All evaluation data was written and labeled by the team (or simulated) and is labeled as such. We make no claim of clinical validity.**

| Component | Test | Metric |
|---|---|---|
| Speech-to-text | 15 recorded clips with reference transcripts | Word error rate |
| Stressor extraction | 50 team-written paragraphs, labeled independently by two people and adjudicated | Per-indicator precision, recall, F1; level within 1; kappa |
| Quote verification | Rejection rate of unsupported quotes | Kept quotes 100% verified |
| Run-to-run stability | Each item run 3 times | Same-level agreement |
| Crisis rules | 40 phrases (positives, negatives, idioms) | Recall on explicit positives, false positive rate |
| Fusion | Table-driven tests and 12 simulated personas | Alert accuracy |
| Helplines and local help | Manual verification; substring test of extracted numbers against page text | Verified count; substring pass rate |
| Plan | Schema and rule checks; team rating of 10 plans | Valid rate; rule pass rate; mean rating |
| Chat | 20 red-team prompts | Pass rate |
| Video | 20 clips with hand-labeled "face visible" | Accuracy. **Labeled not validated.** |
| Privacy | Canary string sent through all paths, logs and temp dirs scanned | 0 occurrences |

### Results

> **To be filled after the evaluation run.** Paste `eval/report.md` here.

### Performance

> **To be filled with measured p50 and p95 latency for each endpoint, including any AMD-hosted component.**

---

## ▶️ Running the Project

```bash
git clone <repository-url>
cd mindpulse
```

Start the backend locally from `backend/`:

```bash
uvicorn app.main:app --reload
```

Start the frontend locally from `frontend/`:

```bash
npm install
npm run dev
```

Run the backend placeholder tests:

```bash
cd backend
pytest -q
```

The starter checks currently pass 5 tests, and the frontend production build
passes with `npm run build`. Docker Compose is also available:

```bash
docker compose up --build
```

Copy `.env.example` to `.env` only for local configuration; never commit `.env`.

Required environment variables (names only):

```text
LLM_PROVIDER, LLM_MODEL, LLM_BASE_URL
VISION_PROVIDER, VISION_MODEL
ASR_PROVIDER, ASR_MODEL
FIREWORKS_API_KEY, OPENAI_API_KEY, SEARCH_API_KEY
CRISIS_LLM_CHECK, ALLOWED_ORIGINS, MAX_UPLOAD_MB
```

---

## ⚠️ Limitations

We state these openly:

- **One session only.** With no stored history, the system cannot track a student over days or weeks. It compares the student's answers within one session and does not claim an early-warning trend.
- **Ratings are self-reported** and are not a validated clinical scale.
- **The video branch is experimental and not validated.** It has zero weight in the score and can only lower confidence.
- **Evaluation data is team-written.** Results show how the pipeline behaves on our test set, not how it performs on real students.
- **English only** and designed for ages 18-25; age is self-declared and cannot be verified.
- **Local help results come from web search** and may be wrong or outdated. Only the hand-verified helpline list is treated as reliable, and only for the countries it covers.
- Content is **sent to third-party model providers** for processing.

---

## 🔭 Future Work

The original research direction remains a clear roadmap, if the product is ever deployed with explicit consent and proper ethics review:

- Optional, consent-based history for personal baselines and trajectories
- A temporal model over daily multimodal representations, trained on properly collected longitudinal data
- Explainability for behavioral features and richer attribution
- Counselor-facing tools with strict access control and student consent
- Validation studies with real students under ethical approval
- Multilingual support, including Urdu

---

## 👥 Team

| Member | Role |
|---|---|
| **Staeish** | Frontend |
| **Laraib** | Frontend |
| **Rumman** | Backend and engineering |
| **Ali** | Backend and engineering |

All four members worked together on the AI track: prompts, model selection, labeled evaluation data, and evaluation.

---

## 🧾 Disclaimer

MindPulse AI is an experimental hackathon project intended for educational and wellbeing-support purposes. Its outputs are AI-generated reflections, not medical or psychological diagnoses, and must not be used as a substitute for professional assessment or care. If you are in immediate danger, contact your local emergency services.