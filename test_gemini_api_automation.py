#!/usr/bin/env python3
"""
Automated testing for Gemini API to identify which models and strategies work.
"""

from playwright.sync_api import sync_playwright
import time
import json

def test_gemini_api():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Visible for debugging
        page = browser.new_page()

        # Capture console logs
        console_messages = []
        page.on("console", lambda msg: console_messages.append({
            "type": msg.type,
            "text": msg.text
        }))

        # Navigate to test page
        print("🌐 Opening test page...")
        page.goto('http://localhost:8000/test_gemini_api.html')
        page.wait_for_load_state('networkidle')

        # Take initial screenshot
        page.screenshot(path='/tmp/gemini_test_initial.png', full_page=True)
        print("📸 Initial screenshot saved to /tmp/gemini_test_initial.png")

        # Wait for API key to load
        time.sleep(1)

        # First, list available models
        print("\n🔍 Step 1: Checking available models...")
        page.goto('http://localhost:8000/list_available_models.html')
        page.wait_for_load_state('networkidle')
        time.sleep(1)

        # Click list models button
        page.click('button:has-text("List All Models")')
        time.sleep(5)

        # Take screenshot of available models
        page.screenshot(path='/tmp/gemini_available_models.png', full_page=True)
        print("📸 Available models screenshot saved to /tmp/gemini_available_models.png")

        # Go back to test page
        print("\n🧪 Step 2: Running API tests...")
        page.goto('http://localhost:8000/test_gemini_api.html')
        page.wait_for_load_state('networkidle')
        time.sleep(1)

        # Run Test 5 (Run All Tests)
        page.click('button:has-text("Run All Tests")')

        # Wait for tests to complete (generous timeout for API calls)
        print("⏳ Waiting for tests to complete (60 seconds)...")
        time.sleep(60)

        # Take final screenshot
        page.screenshot(path='/tmp/gemini_test_results.png', full_page=True)
        print("📸 Results screenshot saved to /tmp/gemini_test_results.png")

        # Extract results from the page
        test_results = []
        result_divs = page.locator('.result').all()

        for i, div in enumerate(result_divs, 1):
            result_text = div.inner_text()
            test_results.append({
                "test": f"Test {i}",
                "result": result_text
            })

        # Save console logs
        print("\n📋 Console Logs:")
        print("=" * 80)
        for msg in console_messages:
            print(f"[{msg['type'].upper()}] {msg['text']}")
        print("=" * 80)

        # Save results to file
        results_summary = {
            "test_results": test_results,
            "console_logs": console_messages
        }

        with open('/tmp/gemini_test_results.json', 'w') as f:
            json.dump(results_summary, f, indent=2)

        print("\n✅ Results saved to /tmp/gemini_test_results.json")

        # Analyze results
        print("\n🔍 Analysis:")
        for result in test_results:
            print(f"\n{result['test']}:")
            if "✅" in result['result']:
                print("  ✅ PASSED")
            elif "❌" in result['result']:
                print("  ❌ FAILED")
            print(f"  {result['result'][:200]}")

        # Keep browser open for manual inspection
        print("\n⏸️  Browser will close in 10 seconds...")
        time.sleep(10)

        browser.close()

if __name__ == "__main__":
    test_gemini_api()
