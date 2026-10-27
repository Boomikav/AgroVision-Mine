"""Captures end-to-end browser demonstration screenshots for faculty presentation.

Covers:
1. Apple Healthy specimen analysis (97.6% confident prediction, nearest reference)
2. Potato Late Blight specimen analysis (96.2% confident prediction)
3. Rice Bacterial Leaf Blight scanner specimen (unsupported domain rejection)
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOT_DIR = ROOT_DIR / "data" / "reports" / "browser_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

tests = [
    ("apple_healthy", "data/processed_v2/plantdoc/apple/healthy/proc_AGRO_V2_00037.png", "10_image_analysis_apple_healthy.png"),
    ("potato_late_blight", "data/processed_v2/plantdoc/potato/late_blight/proc_AGRO_V2_00167.png", "11_image_analysis_potato_late_blight.png"),
    ("rice_unsupported_domain", "data/processed_v2/icar_ogd/rice/bacterial_leaf_blight/proc_AGRO_V2_00001.png", "12_image_analysis_rice_unsupported_domain.png")
]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True, args=["--no-sandbox"])

    for name, img_rel, out_name in tests:
        print(f"--- Processing {name} ---", flush=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1080})
        page = context.new_page()

        page.goto("http://127.0.0.1:8000", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Click Image Analysis nav
        nav_btn = page.locator("nav button", has_text="Image Analysis").first
        nav_btn.click()
        page.wait_for_timeout(1000)

        img_path = str(ROOT_DIR / img_rel)
        file_input = page.locator("input[type='file']").first
        file_input.set_input_files(img_path)
        page.wait_for_timeout(800)

        analyze_btn = page.locator("button", has_text="Analyze Specimen").first
        analyze_btn.click()

        # Wait for analysis output
        page.wait_for_selector("text=Validation & Preprocessing Integrity", timeout=30000)
        # Wait for supervised prediction section
        page.wait_for_selector("text=Supervised Crop-Disease Classification", timeout=30000)
        page.wait_for_timeout(2000)

        out_path = SCREENSHOT_DIR / out_name
        page.screenshot(path=str(out_path), full_page=True)
        print(f"Captured {out_name}: {os.path.getsize(out_path):,} bytes", flush=True)

        context.close()

    browser.close()

print("All faculty demonstration screenshots successfully captured!", flush=True)
