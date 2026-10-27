"""
Render Mermaid architecture diagram to SVG and high-resolution PNG using Playwright.
"""
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

async def render():
    base_dir = Path(__file__).resolve().parent.parent
    mmd_path = base_dir / "research_paper" / "figures" / "fig1_system_architecture.mmd"
    svg_out = base_dir / "research_paper" / "figures" / "fig1_system_architecture.svg"
    png_out = base_dir / "research_paper" / "figures" / "fig1_system_architecture.png"
    mermaid_js_path = base_dir / "scripts" / "mermaid.min.js"

    mmd_content = mmd_path.read_text(encoding="utf-8")
    js_content = mermaid_js_path.read_text(encoding="utf-8")

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 20px;
    background-color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  #container {{
    display: inline-block;
  }}
</style>
<script>
{js_content}
</script>
</head>
<body>
<div id="container">
  <pre class="mermaid">
{mmd_content}
  </pre>
</div>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'default',
    flowchart: {{
      useMaxWidth: false,
      htmlLabels: true,
      curve: 'basis'
    }}
  }});
</script>
</body>
</html>
"""

    temp_html = base_dir / "scripts" / "temp_render.html"
    temp_html.write_text(html_content, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True,
            args=["--no-sandbox", "--disable-gpu"]
        )
        # device_scale_factor=3 gives ~300 DPI resolution
        context = await browser.new_context(device_scale_factor=3)
        page = await context.new_page()
        await page.goto(f"file:///{temp_html.as_posix()}")
        
        # Wait for SVG element inside container
        svg_element = await page.wait_for_selector("#container svg", timeout=15000)
        svg_xml = await page.evaluate("() => document.querySelector('#container svg').outerHTML")
        svg_out.write_text(svg_xml, encoding="utf-8")
        print(f"Saved SVG to: {svg_out} ({len(svg_xml)} bytes)")

        # Screenshot container to PNG
        await svg_element.screenshot(path=str(png_out))
        print(f"Saved 300-DPI PNG to: {png_out}")

        await browser.close()

    try:
        if temp_html.exists():
            temp_html.unlink()
    except Exception:
        pass

if __name__ == "__main__":
    asyncio.run(render())
