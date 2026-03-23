# AccessLens 🔍

> AI-powered web accessibility auditor — paste any URL and get a prioritised report of WCAG violations with AI-generated fix suggestions.

**Status: 🚧 In progress — actively building**

![AccessLens demo](https://raw.githubusercontent.com/annarose14/accesslens/main/demo.png)

---

## What it does

Most websites unintentionally block users with disabilities. AccessLens scans any public URL, detects accessibility violations (missing alt text, low contrast, keyboard traps, unlabelled forms, and 40+ more), and uses AI to explain each issue in plain English and suggest the exact code fix.

**Who it helps:** blind users relying on screen readers, users with low vision, motor-impaired users who navigate by keyboard only.

---

## Features (building in public)

- [x] Page capture — screenshot + DOM extraction via Playwright
- [x] Accessibility rule engine — axe-core WCAG 2.1 checker
- [x] React dashboard — screenshot display + colour-coded violations
- [ ] AI fix suggestions — Claude API generates plain-English explanations + code diffs
- [ ] Visual heatmap — severity overlay on the page screenshot
- [ ] Score dashboard — WCAG A / AA / AAA compliance score

---

## Built with

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Playwright |
| Accessibility engine | axe-core (Deque) |
| AI layer | Claude API (Anthropic) |
| Frontend | React, TypeScript, Tailwind CSS |
| Deployment | Docker, Railway, Vercel |

---

## Getting started
```bash
# Clone the repo
git clone https://github.com/annarose14/accesslens.git
cd accesslens

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
uvicorn main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm start
```

---

## Why I built this

Over 96% of the world's top websites fail basic accessibility standards.
Existing tools like Lighthouse only catch ~30% of issues and give no
actionable fix suggestions.

In the first week of building AccessLens, I scanned 5 major Australian
websites and found 16 real WCAG violations including:
- ABC News: 13 duplicate ARIA IDs affecting screen readers (critical)
- University of Sydney: colour contrast failures affecting low vision users
- Canva: landmark violations affecting keyboard navigation

AccessLens combines automated rule-checking with AI to make accessibility
auditing fast, specific, and actionable.

---

*Built by Anna Rose | MIT student at UNSW Sydney | Portfolio project*