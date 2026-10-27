import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:8000"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = Path("docs/screenshots/final")
ROOT_DIR = Path(__file__).resolve().parent.parent

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH if os.path.exists(CHROME_PATH) else None,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        # Using 1600x1000 with 1.5x device_scale_factor for crisp presentation slides
        context = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            device_scale_factor=1.5
        )
        page = context.new_page()
        page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1500)
        
        def nav_to(label: str):
            btn = page.locator("nav button", has_text=label).first
            btn.wait_for(state="visible", timeout=10000)
            btn.click()
            page.wait_for_timeout(1200)

        # 1. Overview
        print("Capturing 01_overview.png...")
        nav_to("Overview")
        page.wait_for_selector("text=2,596", timeout=10000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "01_overview.png"))

        # 2. Dataset Explorer
        print("Capturing 02_dataset_explorer.png...")
        nav_to("Dataset Explorer")
        page.wait_for_selector("input[placeholder*='Search']", timeout=10000)
        # Switch to table view or keep grid view with specimens loaded
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUTPUT_DIR / "02_dataset_explorer.png"))

        # 3. Data Quality & ETL
        print("Capturing 03_data_quality_etl.png...")
        nav_to("Data Quality & ETL")
        page.wait_for_selector("text=Scientific Integrity & Dataset Freeze Audit", timeout=10000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "03_data_quality_etl.png"))

        # 4. Data Warehouse
        print("Capturing 04_data_warehouse.png...")
        nav_to("Data Warehouse")
        page.wait_for_selector("text=Central Observation Fact Table", timeout=10000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "04_data_warehouse.png"))

        # 5. OLAP Analytics
        print("Capturing 05_olap_analytics.png...")
        nav_to("OLAP Analytics")
        # Click Slice operation to display active SQL and data slice
        slice_btn = page.locator("button:has-text('3A. Slice')").first
        if slice_btn.is_visible():
            slice_btn.click()
            page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "05_olap_analytics.png"))

        # 6. Visual Pattern Mining
        print("Capturing 06_visual_pattern_mining.png...")
        nav_to("Visual Pattern Mining")
        page.wait_for_selector("text=0.4060", timeout=10000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "06_visual_pattern_mining.png"))

        # 7. Association Rules
        print("Capturing 07_association_rules.png...")
        nav_to("Association Rules")
        page.wait_for_selector("text=880", timeout=10000)
        # Toggle Mode B to show labeled rules with lift >= 1.0
        mode_b_btn = page.locator("button:has-text('Mode B')").first
        if mode_b_btn.is_visible():
            mode_b_btn.click()
            page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "07_association_rules.png"))

        # 8. Image Analysis Workbench
        print("Capturing 08_image_analysis_workbench.png...")
        nav_to("Image Analysis")
        # Upload authentic rice leaf specimen
        upload_input = page.locator("input[type='file']").first
        rice_img_path = ROOT_DIR / "data" / "processed" / "rice" / "bacterial_leaf_blight" / "proc_DSC_0365.png"
        if rice_img_path.exists():
            upload_input.set_input_files(str(rice_img_path))
            page.wait_for_timeout(600)
            analyze_btn = page.locator("button:has-text('Analyze Specimen')").first
            if analyze_btn.is_visible():
                analyze_btn.click()
                page.wait_for_selector("text=Validation & Preprocessing Integrity", timeout=15000)
                page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "08_image_analysis_workbench.png"))

        # 9. Reports & Methodology
        print("Capturing 09_reports_methodology.png...")
        nav_to("Reports & Methodology")
        page.wait_for_selector("text=Review 2 Scientific Evaluation Report", timeout=10000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(OUTPUT_DIR / "09_reports_methodology.png"))

        browser.close()
        print("All screenshots successfully captured!")

if __name__ == "__main__":
    main()
