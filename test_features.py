#!/usr/bin/env python3
"""
Test navigation and overlay features
"""

from playwright.sync_api import sync_playwright
import time

def test_features():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Capture console messages
        console_logs = []
        errors = []

        def handle_console(msg):
            text = msg.text
            console_logs.append(text)
            print(f"[CONSOLE] {text}")

        def handle_error(err):
            errors.append(str(err))
            print(f"[ERROR] {err}")

        page.on("console", handle_console)
        page.on("pageerror", handle_error)

        print("🌐 Opening application...")
        page.goto('http://localhost:8000/Clinical_Study_Extraction.html')
        page.wait_for_load_state('networkidle')
        time.sleep(3)

        # Check if PDF is already loaded
        pdf_loaded = page.evaluate("() => typeof AppStateManager !== 'undefined' && AppStateManager.getState().pdfDoc !== null")

        if pdf_loaded:
            print("✅ PDF already loaded from cache")
        else:
            print("📂 Loading Kim2016.pdf...")
            try:
                page.set_input_files('input[type="file"]#pdf-file', '/Users/matheusrech/clinical_extraction_pdf_form/pdfs/Kim2016.pdf')
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Could not load PDF: {e}")

        # Wait for preprocessing
        print("⏳ Waiting for preprocessing...")
        time.sleep(5)

        # Check preprocessing data
        print("\n📊 Checking preprocessing data...")
        preprocessing_data = page.evaluate("""
            () => {
                const state = AppStateManager.getState();
                return state.preprocessingData ? {
                    sections: state.preprocessingData.sections.length,
                    tables: state.preprocessingData.tables.length,
                    citations: state.preprocessingData.citations.length
                } : null;
            }
        """)

        if preprocessing_data:
            print(f"  ✅ Preprocessing data exists:")
            print(f"     Sections: {preprocessing_data['sections']}")
            print(f"     Tables: {preprocessing_data['tables']}")
            print(f"     Citations: {preprocessing_data['citations']}")
        else:
            print("  ❌ No preprocessing data found!")

        # Check if sidebar is open
        print("\n📊 Checking sidebar...")
        sidebar_open = page.evaluate("""
            () => {
                const sidebar = document.getElementById('preprocessing-sidebar');
                return sidebar && !sidebar.classList.contains('collapsed');
            }
        """)
        print(f"  Sidebar open: {sidebar_open}")

        # Check if overlays exist
        print("\n🎨 Checking overlays...")
        overlay_info = page.evaluate("""
            () => {
                const pageDiv = document.querySelector('.pdf-page');
                if (!pageDiv) return { pageExists: false };

                const overlay = pageDiv.querySelector('.pdf-overlay');
                return {
                    pageExists: true,
                    pageId: pageDiv.id,
                    overlayExists: overlay !== null,
                    overlayVisible: overlay ? getComputedStyle(overlay).display !== 'none' : false
                };
            }
        """)
        print(f"  PDF page exists: {overlay_info.get('pageExists')}")
        print(f"  PDF page ID: {overlay_info.get('pageId')}")
        print(f"  Overlay exists: {overlay_info.get('overlayExists')}")
        print(f"  Overlay visible: {overlay_info.get('overlayVisible')}")

        # Test navigation from sidebar
        print("\n🧭 Testing sidebar navigation...")
        first_section = page.locator('#sections-list li').first
        if first_section.count() > 0:
            print("  Clicking first section...")
            try:
                first_section.click()
                time.sleep(2)

                current_page = page.evaluate("() => document.getElementById('page-num').value")
                print(f"  ✅ Current page after click: {current_page}")
            except Exception as e:
                print(f"  ❌ Navigation error: {e}")
        else:
            print("  ❌ No sections in list!")

        # Take screenshot
        print("\n📸 Taking screenshot...")
        page.screenshot(path='/tmp/features_test.png', full_page=True)

        # Check for JavaScript errors
        if errors:
            print(f"\n❌ JavaScript errors detected:")
            for err in errors:
                print(f"  - {err}")
        else:
            print("\n✅ No JavaScript errors")

        print("\n⏸️ Browser will close in 30 seconds...")
        time.sleep(30)
        browser.close()

if __name__ == "__main__":
    test_features()
