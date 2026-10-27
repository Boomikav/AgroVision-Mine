import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOT_DIR = ROOT_DIR / "data" / "reports" / "browser_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

log_file = open(ROOT_DIR / "server_temp.log", "w", encoding="utf-8")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "src.api.app:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=str(ROOT_DIR),
    stdout=log_file,
    stderr=log_file
)

try:
    print("Waiting for server startup...", flush=True)
    ready = False
    for i in range(25):
        time.sleep(1)
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/api/overview", timeout=2) as r:
                if r.status == 200:
                    ready = True
                    print(f"Server ready after {i+1}s!", flush=True)
                    break
        except Exception:
            pass

    if not ready:
        raise RuntimeError("FastAPI server failed to start within 25 seconds.")

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport={"width": 1440, "height": 1080})
        page = context.new_page()

        print("Navigating to http://127.0.0.1:8000...", flush=True)
        page.goto("http://127.0.0.1:8000", wait_until="networkidle")
        page.wait_for_timeout(1000)

        nav_btn = page.locator("nav button", has_text="Image Analysis").first
        nav_btn.click()
        page.wait_for_timeout(1000)

        img_path = str(ROOT_DIR / "data/processed_v2/icar_ogd/rice/bacterial_leaf_blight/proc_AGRO_V2_00001.png")
        print(f"Setting input file to {img_path}...", flush=True)
        page.locator("input[type='file']").first.set_input_files(img_path)
        page.wait_for_timeout(800)

        print("Clicking Analyze Specimen...", flush=True)
        page.locator("button", has_text="Analyze Specimen").first.click()

        print("Waiting for analysis results...", flush=True)
        page.wait_for_selector("text=Supervised Crop-Disease Classification", timeout=35000)
        page.wait_for_timeout(2500)

        out_path = SCREENSHOT_DIR / "12_image_analysis_rice_unsupported_domain.png"
        page.screenshot(path=str(out_path), full_page=True)
        print(f"Captured 12_image_analysis_rice_unsupported_domain.png: {os.path.getsize(out_path):,} bytes", flush=True)
        browser.close()
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
    log_file.close()
