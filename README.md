# AccessLens 🔍

> AI-powered web accessibility auditor — paste any URL and get a prioritised report of WCAG violations with AI-generated fix suggestions.

**Status: ✅ Live and working**

🌐 **Live demo:** [accesslens.vercel.app](https://accesslens-326ymdmm2-accesslens.vercel.app/)
📁 **GitHub:** [github.com/annarose14/accesslens](https://github.com/annarose14/accesslens)

---

![AccessLens demo](https://raw.githubusercontent.com/annarose14/accesslens/main/demo.png)

---

## What it does

Over 96% of the world's top websites fail basic accessibility standards. AccessLens scans any public URL, detects WCAG 2.1 violations, and uses AI to explain each issue in plain English and suggest the exact code fix.

**In the first two weeks of building AccessLens, scanning 5 major Australian websites found:**
- ABC News — 13 duplicate ARIA IDs affecting screen readers (critical)
- University of Sydney — colour contrast failures affecting low vision users
- Canva — landmark navigation issues affecting keyboard users
- health.gov.au — 4 links with no discernible text for screen readers
- Sydney University — tabindex violations blocking keyboard navigation

**Who it helps:** blind users relying on screen readers, users with low vision, motor-impaired users who navigate by keyboard only.

---

## Features

- ✅ Paste any URL → get a full accessibility report in seconds
- ✅ Screenshot of the scanned page
- ✅ Colour-coded violation cards (critical / serious / moderate / minor)
- ✅ AI-generated plain English explanation for every violation
- ✅ AI-generated before/after code fix for every violation
- ✅ Direct links to WCAG 2.1 documentation
- ✅ Checks 40+ WCAG rules including contrast, alt text, landmarks, keyboard access

---

## Built with

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Playwright |
| Accessibility engine | axe-core 4.7 (Deque) |
| AI fix suggestions | Groq API (Llama 3.3 70B) |
| Frontend | React, TypeScript, Tailwind CSS |
| Deployment | Railway (backend), Vercel (frontend) |

---

## Getting started locally

```bash
# Clone the repo
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

Create a `.env` file in the `backend` folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

```bash
uvicorn main:app --reload
```

**Frontend (separate terminal):**
```bash
cd frontend
npm install
npm start
```

Open [localhost:3000](http://localhost:3000)

---

## How it works

```
URL input
    ↓
Playwright visits the page (headless Chrome)
    ↓
axe-core injected → runs 40+ WCAG rule checks
    ↓
Violations sent to Groq LLM
    ↓
AI generates: explanation + before code + after code
    ↓
React dashboard shows results
```

---

## Project structure

```
accesslens/
├── backend/
│   ├── main.py           # FastAPI app, scan endpoint, AI fix logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── src/
│       └── App.tsx       # React dashboard
├── demo.png
└── README.md
```

---

## Why I built this

Existing tools like Lighthouse catch only ~30% of accessibility issues and give no fix suggestions. AccessLens combines automated rule-checking with AI to make accessibility auditing fast, specific, and actionable for any developer or designer — completely free and open source.

---

## Roadmap

- [ ] Visual heatmap — severity overlay on the page screenshot
- [ ] WCAG score dashboard — A / AA / AAA compliance score
- [ ] Bulk URL scanning — scan entire websites at once
- [ ] Export report as PDF

---

*Built by Anna Rose | MIT student, UNSW Sydney*
*Targeting roles in AI/ML engineering and UX at Google, Canva, Atlassian, Microsoft*