#!/usr/bin/env python3
"""
Simple test for the fixed citation search
"""

from playwright.sync_api import sync_playwright
import time

def test_citation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Capture console messages
        console_logs = []
        def handle_console(msg):
            console_logs.append(f"[{msg.type}] {msg.text}")
            print(f"[CONSOLE {msg.type}] {msg.text}")

        page.on("console", handle_console)

        print("🌐 Opening app...")
        page.goto('http://localhost:8000/Clinical_Study_Extraction.html')
        page.wait_for_load_state('networkidle')
        time.sleep(3)

        print("📸 Taking screenshot of initial state...")
        page.screenshot(path='/tmp/test_step1.png', full_page=True)

        # Find citation textarea by placeholder
        print("🔍 Looking for citation field...")
        citation_field = page.locator('textarea').filter(has_text="Paste citation")

        if citation_field.count() == 0:
            # Try alternative selector
            citation_field = page.locator('textarea').first

        print("✍️ Filling citation field...")
        test_citation = "Kim J, Lee JH. Suboccipital decompressive craniectomy for cerebellar infarction. Neurosurgery 2016;79(3):423-430"
        citation_field.fill(test_citation)

        print("📸 Taking screenshot after filling citation...")
        page.screenshot(path='/tmp/test_step2.png', full_page=True)
        time.sleep(1)

        # Find and click the sparkle button
        print("✨ Looking for sparkle button...")
        sparkle_btn = page.locator('button').filter(has_text="✨").first

        print("🖱️ Clicking sparkle button...")
        sparkle_btn.click()

        print("⏳ Waiting 30 seconds for API call to complete...")
        time.sleep(30)

        print("📸 Taking final screenshot...")
        page.screenshot(path='/tmp/test_step3.png', full_page=True)

        # Check for success indicators in console
        success_found = False
        failure_found = False

        for log in console_logs:
            if "✅ Success with Gemini" in log:
                success_found = True
                print(f"\n🎉 SUCCESS! {log}")
            elif "❌" in log and "failed" in log.lower():
                failure_found = True
                print(f"\n⚠️ {log}")

        # Try to read populated fields
        print("\n📋 Checking populated fields:")
        try:
            doi = page.locator('input[placeholder*="DOI"]').first.input_value()
            print(f"  DOI: {doi if doi else '(empty)'}")
        except:
            print("  DOI: Could not read")

        try:
            pmid = page.locator('input[placeholder*="PMID"]').first.input_value()
            print(f"  PMID: {pmid if pmid else '(empty)'}")
        except:
            print("  PMID: Could not read")

        try:
            journal = page.locator('input[placeholder*="Journal"]').first.input_value()
            print(f"  Journal: {journal if journal else '(empty)'}")
        except:
            print("  Journal: Could not read")

        try:
            year = page.locator('input[placeholder*="Year"]').first.input_value()
            print(f"  Year: {year if year else '(empty)'}")
        except:
            print("  Year: Could not read")

        # Final verdict
        print("\n" + "="*80)
        if success_found:
            print("✅ TEST PASSED! Citation search completed successfully!")
        elif failure_found:
            print("❌ TEST FAILED! Citation search encountered errors.")
        else:
            print("⚠️ TEST UNCLEAR - Check screenshots and console logs")
        print("="*80)

        print("\n📸 Screenshots saved:")
        print("  - /tmp/test_step1.png (initial state)")
        print("  - /tmp/test_step2.png (after filling citation)")
        print("  - /tmp/test_step3.png (after API call)")

        print("\n⏸️ Browser will stay open for 10 seconds for inspection...")
        time.sleep(10)

        browser.close()

if __name__ == "__main__":
    test_citation()
