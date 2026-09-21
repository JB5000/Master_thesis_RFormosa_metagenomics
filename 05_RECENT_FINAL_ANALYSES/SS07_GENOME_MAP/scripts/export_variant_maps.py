#!/usr/bin/env python3
"""Export reproducible PNG/SVG files for the two SS-07 Proksee/CGView variants."""

from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "proksee_output"
REPORT_JS = REPORT_DIR / "data/genome_maps/genome_1.js"
VARIANTS = ROOT / "proksee_variants"
EXPORTS = ROOT / "exports"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> None:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    variants = {
        "SS-07_Bakta_general": VARIANTS / "SS-07_Bakta_general.cgview.json",
        "SS-07_MIMAG_RNA": VARIANTS / "SS-07_MIMAG_RNA.cgview.json",
        "SS-07_MIMAG_RNA_coverage": VARIANTS / "SS-07_MIMAG_RNA_coverage.cgview.json",
    }
    original_js = REPORT_JS.read_bytes()
    handler = functools.partial(QuietHandler, directory=str(REPORT_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1200")
    options.add_experimental_option("prefs", {
        "download.default_directory": str(EXPORTS),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    })

    try:
        for stem, source in variants.items():
            data = json.loads(source.read_text(encoding="utf-8"))
            REPORT_JS.write_text("json = " + json.dumps(data, separators=(",", ":")) + ";\n", encoding="utf-8")
            png = EXPORTS / f"{stem}.png"
            svg = EXPORTS / f"{stem}.svg"
            png.unlink(missing_ok=True)
            svg.unlink(missing_ok=True)

            driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
            try:
                driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": str(EXPORTS)})
                driver.get(f"http://127.0.0.1:{server.server_port}/report.html?variant={stem}")
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".genome-item"))).click()
                WebDriverWait(driver, 60).until(lambda browser: browser.execute_script(
                    "return document.querySelector('#my-viewer').dataset.key === 'genome_1' && window.cgv && cgv.features().length > 50"
                ))
                driver.execute_script(f"cgv.io.downloadImage(2600,2600,'{stem}.png');")
                WebDriverWait(driver, 60).until(lambda browser: png.exists() and png.stat().st_size > 1000)
                driver.execute_script(
                    "var script=document.createElement('script');script.src='assets/scripts/svgcanvas.iife.js';document.head.appendChild(script);"
                )
                WebDriverWait(driver, 30).until(lambda browser: driver.execute_script("return typeof svgcanvas !== 'undefined'"))
                svg_text = driver.execute_script("cgv.externals.SVGContext=svgcanvas.Context; return cgv.io.getSVG();")
                if not svg_text or "<svg" not in svg_text[:500]:
                    raise RuntimeError(f"CGView did not return SVG for {stem}")
                svg.write_text(svg_text, encoding="utf-8")
            finally:
                driver.quit()
            print(f"{stem}: PNG={png.stat().st_size}; SVG={svg.stat().st_size}")
    finally:
        REPORT_JS.write_bytes(original_js)
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
