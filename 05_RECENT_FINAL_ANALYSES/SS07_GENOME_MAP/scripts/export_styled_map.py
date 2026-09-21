#!/usr/bin/env python3
"""Export the styled SS-07 CGView map from the local Proksee Batch report."""

from __future__ import annotations

import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "proksee_output"
EXPORT_DIR = ROOT / "exports"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    targets = {
        "png": EXPORT_DIR / "SS-07_Proksee_pilot.png",
        "svg": EXPORT_DIR / "SS-07_Proksee_pilot.svg",
        "json": EXPORT_DIR / "SS-07_Proksee_pilot.json",
        "report": EXPORT_DIR / "SS-07_Proksee_batch_report.png",
    }
    for target in targets.values():
        target.unlink(missing_ok=True)

    handler = functools.partial(QuietHandler, directory=str(REPORT_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1200")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(EXPORT_DIR),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )

    driver = webdriver.Chrome(options=options)
    try:
        driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": str(EXPORT_DIR)},
        )
        driver.get(f"http://127.0.0.1:{server.server_port}/report.html")
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".genome-item"))
        ).click()
        WebDriverWait(driver, 60).until(
            lambda browser: browser.execute_script(
                "return document.querySelector('#my-viewer').dataset.key === 'genome_1' "
                "&& window.cgv && cgv.features().length > 5000"
            )
        )

        driver.execute_script(
            "cgv.io.downloadImage(2400,2400,'SS-07_Proksee_pilot.png');"
        )
        WebDriverWait(driver, 60).until(
            lambda browser: targets["png"].exists() and targets["png"].stat().st_size > 1000
        )
        driver.execute_script("cgv.io.downloadJSON('SS-07_Proksee_pilot.json');")
        WebDriverWait(driver, 60).until(
            lambda browser: targets["json"].exists() and targets["json"].stat().st_size > 1000
        )

        driver.execute_script(
            "var script=document.createElement('script');"
            "script.src='assets/scripts/svgcanvas.iife.js';"
            "document.head.appendChild(script);"
        )
        WebDriverWait(driver, 30).until(
            lambda browser: browser.execute_script("return typeof svgcanvas !== 'undefined'")
        )
        svg = driver.execute_script(
            "cgv.externals.SVGContext=svgcanvas.Context; return cgv.io.getSVG();"
        )
        if not svg or "<svg" not in svg[:500]:
            raise RuntimeError("CGView did not return SVG content")
        targets["svg"].write_text(svg, encoding="utf-8")
        driver.save_screenshot(str(targets["report"]))
    finally:
        driver.quit()
        server.shutdown()
        server.server_close()

    for name, target in targets.items():
        print(f"{name}\t{target}\t{target.stat().st_size}")


if __name__ == "__main__":
    main()
