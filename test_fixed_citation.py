#!/usr/bin/env python3
"""
Test the FIXED citation search functionality
"""

from playwright.sync_api import sync_playwright
import time
import json

def test_fixed_citation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Capture console logs
        console_messages = []
        page.on("console", lambda msg: console_messages.append({
            "type": msg.type,
            "text": msg.text
        }))

        print("🌐 Opening Clinical Study Extraction app...")
        page.goto('http://localhost:8000/Clinical_Study_Extraction.html')
        page.wait_for_load_state('networkidle')
        time.sleep(2)

        print("📸 Taking initial screenshot...")
        page.screenshot(path='/tmp/app_initial.png', full_page=True)

        # Wait for Kim2016.pdf to auto-load
        print("⏳ Waiting for PDF to load...")
        time.sleep(5)

        # Find citation field and paste test citation
        print("📝 Entering test citation...")
        citation_input = page.locator('input[id*="citation"], input[placeholder*="Citation"]').first
        citation_input.fill("Kim J et al. Suboccipital decompressive craniectomy for cerebellar infarction. Neurosurgery 2016;79(3):423-430")

        # Take screenshot before clicking
        page.screenshot(path='/tmp/before_citation_search.png', full_page=True)
        print("📸 Screenshot before search saved")

        # Find and click the ✨ button
        print("🔍 Clicking citation search button (✨)...")
        try:
            # Try different selectors
            search_button = page.locator('button:has-text("✨")').first
            search_button.click()
        except Exception as e:
            print(f"⚠️ Could not find ✨ button, trying alternative selector: {e}")
            # Try by nearby text or icon
            search_button = page.locator('button').filter(has_text="✨").first
            search_button.click()

        # Wait for API call to complete
        print("⏳ Waiting for citation search to complete (30 seconds)...")
        time.sleep(30)

        # Take screenshot after search
        page.screenshot(path='/tmp/after_citation_search.png', full_page=True)
        print("📸 Screenshot after search saved")

        # Check console logs
        print("\n📋 Console Logs:")
        print("=" * 80)
        for msg in console_messages[-20:]:  # Last 20 messages
            print(f"[{msg['type'].upper()}] {msg['text']}")
        print("=" * 80)

        # Check if fields were populated
        print("\n🔍 Checking populated fields...")

        # Try to read DOI field
        try:
            doi_input = page.locator('input[id*="doi"], input[placeholder*="DOI"]').first
            doi_value = doi_input.input_value()
            print(f"  DOI: {doi_value if doi_value else '(empty)'}")
        except:
            print("  DOI: Could not find field")

        # Try to read PMID field
        try:
            pmid_input = page.locator('input[id*="pmid"], input[placeholder*="PMID"]').first
            pmid_value = pmid_input.input_value()
            print(f"  PMID: {pmid_value if pmid_value else '(empty)'}")
        except:
            print("  PMID: Could not find field")

        # Try to read Journal field
        try:
            journal_input = page.locator('input[id*="journal"], input[placeholder*="Journal"]').first
            journal_value = journal_input.input_value()
            print(f"  Journal: {journal_value if journal_value else '(empty)'}")
        except:
            print("  Journal: Could not find field")

        # Try to read Year field
        try:
            year_input = page.locator('input[id*="year"], input[placeholder*="Year"]').first
            year_value = year_input.input_value()
            print(f"  Year: {year_value if year_value else '(empty)'}")
        except:
            print("  Year: Could not find field")

        # Analyze console logs for success indicators
        print("\n🎯 Analysis:")
        success_indicators = [
            "✅ Success with Gemini 2.5 Flash + google_search",
            "✅ Success with Gemini 2.0 Flash + google_search",
            "✅ Success with Gemini 2.5 Flash (no search)",
            "Metadata auto-populated"
        ]

        failure_indicators = [
            "❌ All strategies failed",
            "404:",
            "models/gemini-1.5-flash"
        ]

        has_success = any(indicator in msg['text'] for msg in console_messages for indicator in success_indicators)
        has_failure = any(indicator in msg['text'] for msg in console_messages for indicator in failure_indicators)

        if has_success:
            print("✅ SUCCESS! Citation search completed successfully!")
        elif has_failure:
            print("❌ FAILED! Citation search encountered errors")
        else:
            print("⚠️ UNKNOWN - Check console logs and screenshots")

        # Keep browser open for inspection
        print("\n⏸️  Browser will close in 15 seconds (inspect results)...")
        time.sleep(15)

        browser.close()

        # Save summary
        summary = {
            "test": "Fixed Citation Search",
            "success": has_success,
            "failure": has_failure,
            "console_logs": console_messages[-20:]
        }

        with open('/tmp/citation_test_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)

        print("\n✅ Summary saved to /tmp/citation_test_summary.json")

if __name__ == "__main__":
    test_fixed_citation()
