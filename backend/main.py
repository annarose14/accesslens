from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import base64

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

async def capture_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto(url, timeout=20000, wait_until="networkidle")

        # inject axe-core into the page
        await page.add_script_tag(
            url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js"
        )

        # run axe-core and get violations
        violations = await page.evaluate("axe.run().then(r => r.violations)")

        screenshot = await page.screenshot(full_page=False)
        html = await page.content()
        await browser.close()
        return screenshot, html, violations

@app.post("/scan")
async def scan(req: ScanRequest):
    screenshot, html, violations = await capture_page(req.url)
    img_base64 = base64.b64encode(screenshot).decode("utf-8")

    # simplify violations to only what we need
    simplified = []
    for v in violations:
        simplified.append({
            "id": v["id"],
            "impact": v["impact"],
            "description": v["description"],
            "help": v["help"],
            "helpUrl": v["helpUrl"],
            "nodes_affected": len(v["nodes"])
        })

    return {
        "screenshot": img_base64,
        "url": req.url,
        "violation_count": len(simplified),
        "violations": simplified
    }