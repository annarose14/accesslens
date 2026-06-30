# AccessLens 🔍

> AI-powered web accessibility auditor — paste any URL and get a prioritised report of WCAG 2.1 violations with AI-generated plain-English explanations and exact code fixes.

**Status: ✅ Live and fully working**

🌐 **Live demo:** [accesslens-gules.vercel.app](https://accesslens-gules.vercel.app)
📁 **Source code:** [github.com/annarose14/accesslens](https://github.com/annarose14/accesslens)

---

![AccessLens demo](https://raw.githubusercontent.com/annarose14/accesslens/main/demo.png)

---

## What it does

Over 96% of the world's top websites fail basic accessibility standards. Existing free tools like Google Lighthouse catch roughly 30% of issues and stop there — they tell you something is wrong but not what to change or why it matters.

AccessLens closes that gap. It visits any URL with a real headless browser, scans the fully rendered page against 40+ WCAG 2.1 success criteria, and uses an LLM to generate a plain-English explanation of the human impact alongside an exact before/after code fix — for every single violation found.

---

## Real results from live testing

AccessLens has been tested against major Australian websites, with results pulled directly from the deployed production app:

| Website | Violations | Highest severity | Notable finding |
|---|---|---|---|
| ABC News | 4 | 🔴 Critical | 8 elements with duplicate ARIA/label IDs — screen readers cannot distinguish between them |
| University of Sydney | 6 | 🟠 Serious | Colour contrast failure, link with no discernible text, invalid tabindex ordering |
| Canva | 2 | 🟡 Moderate | Landmark structure issues only — no critical or serious violations found |

**Why this matters:** ABC News is Australia's national public broadcaster. The duplicate ARIA ID issue means a blind user navigating ABC's coverage with a screen reader encounters genuine ambiguity about which content belongs to which element — a real, fixable barrier on a platform serving millions of Australians daily.

---

## Features

- ✅ Paste any URL → full accessibility report in 10–15 seconds
- ✅ Headless browser capture — tests the page exactly as a real visitor experiences it, including JavaScript-rendered content
- ✅ 40+ WCAG 2.1 success criteria checked via axe-core (industry standard, maintained by Deque)
- ✅ AI-generated plain-English explanation of who each violation affects and why
- ✅ AI-generated before/after code fix for every violation
- ✅ Colour-coded severity (critical / serious / moderate / minor)
- ✅ Direct links to official WCAG documentation for every rule
- ✅ Fully deployed and publicly accessible — no signup required

---

## Built with

| Layer | Technology |
|---|---|
| Backend | Python 3.10, FastAPI |
| Browser automation | Playwright (headless Chromium) |
| Accessibility engine | axe-core 4.7 (Deque) |
| AI fix generation | Groq API — Llama 3.3 70B |
| Frontend | React, TypeScript, Tailwind CSS |
| Backend hosting | Railway (Docker, official Playwright image) |
| Frontend hosting | Vercel |

---

## How it works

```
URL submitted
    ↓
Playwright launches headless Chromium, navigates to the page,
waits for full JavaScript render
    ↓
axe-core injected into the live DOM → runs full WCAG 2.1 ruleset
    ↓
Each violation sent to Groq (Llama 3.3 70B) with a structured prompt
    ↓
LLM returns: plain-English explanation + before code + after code
    ↓
Full report (screenshot + violations + AI fixes) returned to React UI
```

---

## Getting started locally

```bash
git clone https://github.com/annarose14/accesslens.git
cd accesslens
```

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

Create `backend/.env`:
```
GROQ_API_KEY=your_free_groq_api_key
```

Get a free key at [console.groq.com](https://console.groq.com) — no credit card required.

```bash
uvicorn main:app --reload
```

**Frontend** (separate terminal):
```bash
cd frontend
npm install
npm start
```

Visit [localhost:3000](http://localhost:3000)

---

## Deployment notes

The backend runs on Railway using the official `mcr.microsoft.com/playwright/python` Docker image, which ships with Chromium and all required system dependencies pre-installed — critical for running headless browser automation reliably in a containerised environment. Chromium is launched with `--disable-dev-shm-usage --no-sandbox --single-process` flags to operate within Railway's memory constraints.

A known limitation: some government and enterprise domains (e.g. Atlassian, some `.gov.au` sites) employ bot detection that blocks headless browser navigation as a security measure. This is expected and not a defect in the scanning logic.

---

## Project structure

```
accesslens/
├── backend/
│   ├── main.py          # FastAPI app, Playwright capture, axe-core injection, Groq AI integration
│   ├── requirements.txt
│   └── Dockerfile        # Official Playwright base image for Railway
├── frontend/
│   └── src/
│       └── App.tsx       # React dashboard — scan input, screenshot, violation cards, expandable fixes
├── demo.png
└── README.md
```

---

## Roadmap

- [ ] Visual heatmap overlaying violation locations directly on the page screenshot
- [ ] WCAG conformance score (A / AA / AAA) per scan
- [ ] Bulk scanning across multiple pages of a single site
- [ ] PDF export for compliance reporting
- [ ] Adjusted browser fingerprinting to handle bot-protected domains

---

## Why this project exists

I previously built a Malayalam Sign Language recognition system from scratch — collecting data, training models, building the interface — because existing tools were built for English and excluded the deaf community I grew up around. That experience shaped how I think about accessibility: not as a compliance checkbox, but as a measure of who technology is actually built for.

AccessLens applies that same conviction to the web. It is free, open source, and built to make the gap between "accessibility matters" and "I know exactly what to fix" as small as possible.

---

*Anna Rose | MIT student, UNSW Sydney, specialising in AI*