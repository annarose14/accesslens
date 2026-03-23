
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import base64

app = FastAPI()

# This allows your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health():
    return {"status": "ok", "project": "AccessLens"}

# Request model
class ScanRequest(BaseModel):
    url: str

# Page capture function
async def capture_page(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto(url, timeout=20000, wait_until="networkidle")
        screenshot = await page.screenshot(full_page=False)
        html = await page.content()
        await browser.close()
        return screenshot, html

# Scan endpoint
@app.post("/scan")
async def scan(req: ScanRequest):
    screenshot, html = await capture_page(req.url)
    img_base64 = base64.b64encode(screenshot).decode("utf-8")
    return {
        "screenshot": img_base64,
        "html_length": len(html),
        "url": req.url
    }