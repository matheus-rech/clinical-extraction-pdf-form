#!/usr/bin/env python3
"""
Test overlay rendering specifically
"""

from playwright.sync_api import sync_playwright
import time

def test_overlays():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({'width': 1920, 'height': 1080})

        # Capture console messages
        console_logs = []
        def handle_console(msg):
            text = msg.text
            console_logs.append(text)
            print(f"[CONSOLE] {text}")

        page.on("console", handle_console)

        print("🌐 Opening application...")
        page.goto('http://localhost:8000/Clinical_Study_Extraction.html')
        page.wait_for_load_state('networkidle')
        time.sleep(3)

        # Wait for preprocessing to complete by watching console
        print("⏳ Waiting for preprocessing...")
        max_wait = 10
        for i in range(max_wait):
            time.sleep(1)
            if any('Preprocessing complete' in log for log in console_logs):
                print("✅ Preprocessing detected!")
                break
        else:
            print("⚠️ Preprocessing timeout - checking anyway")

        time.sleep(2)

        # Check if PDF page exists
        print("\n🔍 Checking PDF page elements...")
        pdf_page_count = page.locator('.pdf-page').count()
        print(f"  PDF pages found: {pdf_page_count}")

        if pdf_page_count > 0:
            # Check for overlay canvas elements
            overlay_count = page.locator('.pdf-overlay').count()
            print(f"  Overlay canvases found: {overlay_count}")

            # Get detailed info about first page
            page_info = page.evaluate("""
                () => {
                    const pageDiv = document.querySelector('.pdf-page');
                    if (!pageDiv) return { exists: false };

                    const overlay = pageDiv.querySelector('.pdf-overlay');
                    return {
                        exists: true,
                        pageId: pageDiv.id,
                        hasOverlay: overlay !== null,
                        overlayClass: overlay ? overlay.className : null,
                        overlayDisplay: overlay ? getComputedStyle(overlay).display : null,
                        overlayWidth: overlay ? overlay.width : null,
                        overlayHeight: overlay ? overlay.height : null
                    };
                }
            """)

            print(f"\n📊 First page details:")
            print(f"  Page exists: {page_info.get('exists')}")
            print(f"  Page ID: {page_info.get('pageId')}")
            print(f"  Has overlay: {page_info.get('hasOverlay')}")
            print(f"  Overlay class: {page_info.get('overlayClass')}")
            print(f"  Overlay display: {page_info.get('overlayDisplay')}")
            print(f"  Overlay size: {page_info.get('overlayWidth')}x{page_info.get('overlayHeight')}")

            # Check if PreprocessingOverlayRenderer exists and has data
            renderer_info = page.evaluate("""
                () => {
                    if (typeof PreprocessingOverlayRenderer === 'undefined') {
                        return { exists: false, error: 'PreprocessingOverlayRenderer not defined' };
                    }
                    return {
                        exists: true,
                        hasData: PreprocessingOverlayRenderer.preprocessingData !== null,
                        sectionCount: PreprocessingOverlayRenderer.preprocessingData?.sections?.length || 0,
                        tableCount: PreprocessingOverlayRenderer.preprocessingData?.tables?.length || 0
                    };
                }
            """)

            print(f"\n🎨 Overlay Renderer status:")
            print(f"  Renderer exists: {renderer_info.get('exists')}")
            print(f"  Has data: {renderer_info.get('hasData')}")
            print(f"  Sections to render: {renderer_info.get('sectionCount')}")
            print(f"  Tables to render: {renderer_info.get('tableCount')}")

        else:
            print("❌ No PDF pages found!")

        # Test navigation
        print("\n🧭 Testing sidebar navigation...")
        section_count = page.locator('#sections-list li').count()
        print(f"  Sections in sidebar: {section_count}")

        if section_count > 0:
            print("  Clicking first section...")
            try:
                page.locator('#sections-list li').first.click()
                time.sleep(2)

                # Check current page number
                current_page = page.evaluate("() => document.getElementById('page-num')?.value || 'unknown'")
                print(f"  ✅ Current page after click: {current_page}")
                print("  ✅ Navigation is working!")
            except Exception as e:
                print(f"  ❌ Navigation error: {e}")
        else:
            print("  ⚠️ No sections found to test navigation")

        # Take screenshot
        print("\n📸 Taking screenshot...")
        page.screenshot(path='/tmp/overlay_test.png', full_page=True)
        print("  Saved to /tmp/overlay_test.png")

        print("\n⏸️ Browser will close in 30 seconds...")
        time.sleep(30)
        browser.close()

if __name__ == "__main__":
    test_overlays()
