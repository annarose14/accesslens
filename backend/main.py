
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
from groq import Groq
from dotenv import load_dotenv
import base64
import os
 
load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
@app.get("/health")
def health():
    return {"status": "ok", "project": "AccessLens"}
 
class ScanRequest(BaseModel):
    url: str
 
async def get_ai_fix(violation_id: str, help_text: str, description: str) -> dict:
    prompt = f"""You are a web accessibility expert.
 
A website has this WCAG accessibility violation:
- Rule: {violation_id}
- Issue: {help_text}
- Description: {description}
 
Respond in exactly this format, nothing else:
EXPLANATION: [2 sentence plain English explanation of why this matters for disabled users]
BEFORE: [one line of broken HTML code example]
AFTER: [one line of fixed HTML code example]"""
 
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3
        )
        text = response.choices[0].message.content
 
        explanation = ""
        before = ""
        after = ""
 
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("EXPLANATION:"):
                explanation = line.replace("EXPLANATION:", "").strip()
            elif line.startswith("BEFORE:"):
                before = line.replace("BEFORE:", "").strip()
            elif line.startswith("AFTER:"):
                after = line.replace("AFTER:", "").strip()
 
        return {
            "explanation": explanation or "See WCAG documentation for details.",
            "before": before or "No example available.",
            "after": after or "No example available."
        }
    except Exception as e:
        return {
            "explanation": "AI fix unavailable.",
            "before": "",
            "after": str(e)
        }
 
async def capture_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        await page.goto(url, timeout=20000, wait_until="networkidle")
        await page.add_script_tag(
            url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js"
        )
        violations = await page.evaluate("axe.run().then(r => r.violations)")
        screenshot = await page.screenshot(full_page=False)
        html = await page.content()
        await browser.close()
        return screenshot, html, violations
 
@app.post("/scan")
async def scan(req: ScanRequest):
    screenshot, html, violations = await capture_page(req.url)
    img_base64 = base64.b64encode(screenshot).decode("utf-8")
 
    simplified = []
    for v in violations:
        ai_fix = await get_ai_fix(v["id"], v["help"], v["description"])
        simplified.append({
            "id": v["id"],
            "impact": v["impact"],
            "description": v["description"],
            "help": v["help"],
            "helpUrl": v["helpUrl"],
            "nodes_affected": len(v["nodes"]),
            "explanation": ai_fix["explanation"],
            "before": ai_fix["before"],
            "after": ai_fix["after"]
        })
 
    return {
        "screenshot": img_base64,
        "url": req.url,
        "violation_count": len(simplified),
        "violations": simplified
    }
 