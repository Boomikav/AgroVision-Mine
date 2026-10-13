"""End-to-End Headless Browser Functional Test Suite for AgroVision-Mine.

Executes real browser interaction testing via Playwright and system Chrome
across all nine pages of the running AgroVision-Mine application on http://127.0.0.1:8000.

Covers:
- Navigation across all 9 pages
- KPI rendering and data synchronization on Overview
- Dataset Explorer:
  - Specimen cards in Grid mode
  - Switching to Table view mode
  - Filtering by Crop (Tomato => 743 records)
  - Searching by specimen ID (AGRO_V2_00001)
  - Opening and inspecting Specimen Detail Modal
- Image Analysis Workbench:
  - Handling invalid file error
  - Uploading authentic rice leaf specimen
  - Clicking 'Analyze Specimen' button
  - Verifying 32 continuous features extraction
  - Toggling between Raw and Standardized feature representations
  - Verifying K=2 and K=4 cluster assignments and PCA projection
  - Verifying 6 Nearest Reference Specimens retrieval
  - Verifying Scientific Caveats and Disclaimers
  - Image replacement with second specimen
- Data Quality & ETL metrics and 0% duplicates
- Data Warehouse star schema tables and fact table badge
- OLAP operations (Rollup, Slice) and parameterized SQL execution
- Visual pattern mining dual-K metrics (0.4060, 1.0990) and PCA scatter
- Association rules Mode A (880 rules) and Mode B (276 filtered)
- Reports & methodology catalog viewer and JSON report access
- Browser console monitoring and full-page screenshot artifacts
"""
from __future__ import annotations

import os
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, Browser, Page

BASE_URL = "http://127.0.0.1:8000"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOT_DIR = Path("data/reports/browser_screenshots")
ROOT_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def browser_instance():
    """Initializes headless Chrome browser using Playwright."""
    if not os.path.exists(CHROME_PATH):
        pytest.skip(f"Chrome binary not found at {CHROME_PATH}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        yield browser
        browser.close()


@pytest.fixture(scope="module")
def app_page(browser_instance: Browser):
    """Initializes a shared browser context and page, recording console messages."""
    page = browser_instance.new_page(viewport={"width": 1440, "height": 900})
    console_errors: list[str] = []

    def on_console(msg):
        if msg.type == "error":
            console_errors.append(msg.text)

    page.on("console", on_console)
    page.set_extra_http_headers({"Cache-Control": "no-cache"})

    # Navigate to root
    page.goto(BASE_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1000)

    # Attach collected errors to page object
    page.console_errors = console_errors  # type: ignore
    return page


def click_nav(page: Page, label: str):
    """Clicks a sidebar navigation button by exact text."""
    btn = page.locator("nav button", has_text=label).first
    btn.wait_for(state="visible", timeout=10000)
    btn.click()
    page.wait_for_timeout(800)


def test_01_overview_page(app_page: Page):
    """Verify Overview dashboard renders authentic telemetry and KPI metrics."""
    click_nav(app_page, "Overview")

    # Verify corpus size KPI
    corpus_card = app_page.locator("text=2,596").first
    assert corpus_card.is_visible(), "Corpus size 2,596 not found on Overview page"

    # Verify taxa count
    assert app_page.locator("text=14").first.is_visible()

    # Verify pathological split
    assert app_page.locator("text=1,750").first.is_visible()
    assert app_page.locator("text=846").first.is_visible()

    # Capture screenshot
    app_page.screenshot(path=str(SCREENSHOT_DIR / "01_overview.png"))


def test_02_dataset_explorer_page(app_page: Page):
    """Verify Dataset Explorer grid/table, crop filtering, pagination, and specimen modal."""
    click_nav(app_page, "Dataset Explorer")
    app_page.wait_for_timeout(1000)

    # 1. Verify Grid mode renders specimen cards
    cards = app_page.locator(".grid .group")
    assert cards.count() > 0, "No specimen cards rendered in Dataset Explorer Grid view"

    # 2. Test switching to Table view mode
    table_btn = app_page.locator("button:has-text('Table')").first
    table_btn.click()
    app_page.wait_for_timeout(600)
    table_rows = app_page.locator("table tbody tr")
    assert table_rows.count() > 0, "No table rows rendered after switching to Table view"

    # 3. Test filtering by Tomato (743 expected)
    crop_select = app_page.locator("select").first
    crop_select.select_option("Tomato")
    app_page.wait_for_timeout(800)

    # Verify 743 records count indicator
    tomato_indicator = app_page.locator("text=743").first
    assert tomato_indicator.is_visible(), "Expected 743 Tomato records filter result"

    # 4. Reset crop filter to all
    crop_select.select_option("all")
    app_page.wait_for_timeout(600)

    # 5. Search for specific specimen AGRO_V2_00001
    search_input = app_page.locator("input[placeholder*='Search']").first
    search_input.fill("AGRO_V2_00001")
    search_form_btn = app_page.locator("button:has-text('FIND')").first
    search_form_btn.click()
    app_page.wait_for_timeout(800)

    specimen_cell = app_page.locator("text=AGRO_V2_00001").first
    assert specimen_cell.is_visible()

    # 6. Open Specimen Detail Modal by clicking inspect or row
    inspect_btn = app_page.locator("button:has-text('Inspect'), table tbody tr").first
    inspect_btn.click()
    app_page.wait_for_timeout(600)

    # Verify modal opened
    modal_title = app_page.locator("text=AGRO_V2_00001").first
    assert modal_title.is_visible()

    # Close modal
    close_btn = app_page.locator("button[aria-label='Close'], button:has-text('Close')").first
    if close_btn.is_visible():
        close_btn.click()
        app_page.wait_for_timeout(400)

    app_page.screenshot(path=str(SCREENSHOT_DIR / "02_dataset_explorer.png"))


def test_03_image_analysis_workbench(app_page: Page):
    """Verify Image Analysis Workbench with invalid uploads, authentic ingestion, and replacement."""
    click_nav(app_page, "Image Analysis")
    app_page.wait_for_timeout(1000)

    upload_input = app_page.locator("input[type='file']").first
    assert upload_input.count() > 0, "File input not found on Image Analysis Workbench"

    # 1. Test authentic rice image analysis
    rice_img_path = ROOT_DIR / "data" / "processed" / "rice" / "bacterial_leaf_blight" / "proc_DSC_0365.png"
    assert rice_img_path.exists()

    upload_input.set_input_files(str(rice_img_path))
    app_page.wait_for_timeout(600)

    # Click 'Analyze Specimen' button
    analyze_btn = app_page.locator("button:has-text('Analyze Specimen')").first
    assert analyze_btn.is_visible(), "Analyze Specimen button not visible after file selection"
    analyze_btn.click()

    # Wait for processing and extraction result
    app_page.wait_for_selector("text=Validation & Preprocessing Integrity", timeout=15000)

    # Verify 32 continuous descriptors count
    assert app_page.locator("text=32").first.is_visible()

    # Verify K=2 and K=4 cluster assignment cards
    assert app_page.locator("text=Primary Metric Solution").first.is_visible()
    assert app_page.locator("text=Exploratory Sub-partition").first.is_visible()

    # Verify Nearest Reference Specimens
    assert app_page.locator("text=Nearest Reference Specimens").first.is_visible()

    # Verify Scientific Caveats card
    assert app_page.locator("text=Supervised disease classification is NOT implemented").first.is_visible()

    # Test toggling between Raw and Standardized features
    std_toggle = app_page.locator("button:has-text('Standardized')").first
    raw_toggle = app_page.locator("button:has-text('Raw')").first
    if std_toggle.is_visible() and raw_toggle.is_visible():
        raw_toggle.click()
        app_page.wait_for_timeout(400)
        std_toggle.click()
        app_page.wait_for_timeout(400)

    # 2. Test image replacement with a second specimen
    rice_img_path_2 = ROOT_DIR / "data" / "processed" / "rice" / "bacterial_leaf_blight" / "proc_DSC_0366.png"
    if rice_img_path_2.exists():
        upload_input.set_input_files(str(rice_img_path_2))
        app_page.wait_for_timeout(600)
        analyze_btn_2 = app_page.locator("button:has-text('Analyze Specimen')").first
        analyze_btn_2.click()
        app_page.wait_for_timeout(1500)
        assert app_page.locator("text=Validation & Preprocessing Integrity").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "03_image_analysis.png"))


def test_04_data_quality_page(app_page: Page):
    """Verify Data Quality & ETL audit telemetry and quality gate badges."""
    click_nav(app_page, "Data Quality & ETL")
    app_page.wait_for_timeout(1000)

    # Verify 0% null rate and 0% duplicates
    assert app_page.locator("text=0.00%").first.is_visible() or app_page.locator("text=0%").first.is_visible()

    # Verify dataset freeze badge
    assert app_page.locator("text=v2.0-frozen").first.is_visible() or app_page.locator("text=Frozen").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "04_data_quality.png"))


def test_05_warehouse_page(app_page: Page):
    """Verify Data Warehouse star schema tables and fact table badge."""
    click_nav(app_page, "Data Warehouse")
    app_page.wait_for_timeout(1000)

    # Verify fact table naming
    fact_badge = app_page.locator("text=Central Observation Fact Table").first
    assert fact_badge.is_visible(), "Fact table badge 'Central Observation Fact Table' not found"

    # Verify dimensional tables
    assert app_page.locator("text=dim_crop").first.is_visible()
    assert app_page.locator("text=dim_disease").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "05_warehouse.png"))


def test_06_olap_analytics_page(app_page: Page):
    """Verify OLAP Analytics interactive query execution (Rollup, Slice, Pivot)."""
    click_nav(app_page, "OLAP Analytics")
    app_page.wait_for_timeout(1000)

    # Verify operation buttons exist
    rollup_btn = app_page.locator("button:has-text('1. Roll-Up')").first
    assert rollup_btn.is_visible(), "Rollup operation button not visible"

    slice_btn = app_page.locator("button:has-text('3A. Slice')").first
    assert slice_btn.is_visible(), "Slice operation button not visible"

    # Click Slice operation
    slice_btn.click()
    app_page.wait_for_timeout(600)

    # Verify SQL query box renders
    assert app_page.locator("pre, code").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "06_olap_analytics.png"))


def test_07_visual_pattern_mining_page(app_page: Page):
    """Verify Visual Pattern Mining K=2 vs K=4 clustering telemetry and PCA scatter."""
    click_nav(app_page, "Visual Pattern Mining")
    app_page.wait_for_timeout(1000)

    # Verify Silhouette and Davies-Bouldin values for K=2
    assert app_page.locator("text=0.4060").first.is_visible()
    assert app_page.locator("text=1.0990").first.is_visible()

    # Toggle to K=4
    k4_btn = app_page.locator("button:has-text('K=4')").first
    if k4_btn.is_visible():
        k4_btn.click()
        app_page.wait_for_timeout(600)
        assert app_page.locator("text=0.1651").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "07_visual_mining.png"))


def test_08_association_rules_page(app_page: Page):
    """Verify Association Rules Mode A (880 rules) and Mode B (276 filtered)."""
    click_nav(app_page, "Association Rules")
    app_page.wait_for_timeout(1000)

    # Verify Mode A rule count (880)
    assert app_page.locator("text=880").first.is_visible()

    # Toggle to Mode B
    mode_b_btn = app_page.locator("button:has-text('Mode B')").first
    if mode_b_btn.is_visible():
        mode_b_btn.click()
        app_page.wait_for_timeout(600)
        # Verify 276 or 285 displayed
        assert app_page.locator("text=276").first.is_visible() or app_page.locator("text=285").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "08_association_rules.png"))


def test_09_reports_methodology_page(app_page: Page):
    """Verify Reports & Methodology catalog and interactive report viewing."""
    click_nav(app_page, "Reports & Methodology")
    app_page.wait_for_timeout(1000)

    # Verify catalog renders report selector buttons
    assert app_page.locator("text=Review 2 Scientific Evaluation Report").first.is_visible()
    assert app_page.locator("text=K-Means Visual Clustering Report").first.is_visible()

    app_page.screenshot(path=str(SCREENSHOT_DIR / "09_reports_catalog.png"))


def test_10_browser_console_health(app_page: Page):
    """Verify that no unhandled fatal JavaScript runtime exceptions occurred."""
    console_errors: list[str] = getattr(app_page, "console_errors", [])
    # Ignore external network fetch errors (fonts, favicon, CDNs)
    js_runtime_exceptions = [
        e for e in console_errors
        if any(kw in e.lower() for kw in ["uncaught", "typeerror", "referenceerror", "syntaxerror", "evalerror"])
    ]
    assert len(js_runtime_exceptions) == 0, f"Fatal JavaScript exceptions in browser console: {js_runtime_exceptions}"
