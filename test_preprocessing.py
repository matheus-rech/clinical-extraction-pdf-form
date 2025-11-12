#!/usr/bin/env python3
"""
Test PDF Preprocessing System
"""

from playwright.sync_api import sync_playwright
import time
import json

def test_preprocessing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Capture console messages
        console_logs = []
        def handle_console(msg):
            text = msg.text
            console_logs.append(text)
            if any(keyword in text for keyword in ['Preprocessing', 'Cache', 'sections', 'tables', 'citations', '📊']):
                print(f"[CONSOLE] {text}")

        page.on("console", handle_console)

        print("🌐 Opening application...")
        page.goto('http://localhost:8000/Clinical_Study_Extraction.html')
        page.wait_for_load_state('networkidle')
        time.sleep(2)

        print("📸 Initial state...")
        page.screenshot(path='/tmp/preprocessing_test_1_initial.png')

        # Load Kim2016.pdf (should be in /pdfs/)
        print("📂 Loading Kim2016.pdf...")

        # Try to upload PDF
        try:
            # Set file input
            file_input = page.locator('input[type="file"]').first
            file_input.set_input_files('/Users/matheusrech/clinical_extraction_pdf_form/pdfs/Kim2016.pdf')

            print("⏳ Waiting for PDF to load...")
            time.sleep(3)

            # Wait for preprocessing to start (look for progress bar)
            print("⏳ Waiting for preprocessing...")

            # Wait up to 60 seconds for preprocessing to complete
            max_wait = 60
            start_time = time.time()
            preprocessing_complete = False

            while (time.time() - start_time) < max_wait:
                # Check if preprocessing is complete by looking for the success message in console
                if any('Document analyzed' in log or 'Analysis complete' in log for log in console_logs):
                    preprocessing_complete = True
                    print("✅ Preprocessing complete!")
                    break

                # Check for preprocessing progress bar
                try:
                    progress_bar = page.locator('#preprocessing-progress').first
                    if progress_bar.is_visible():
                        # Get progress text
                        try:
                            stage = page.locator('#preprocessing-stage').first.text_content()
                            detail = page.locator('#preprocessing-detail').first.text_content()
                            print(f"  Progress: {stage} - {detail}")
                        except:
                            pass
                except:
                    pass

                time.sleep(1)

            if preprocessing_complete:
                print("✅ Preprocessing completed successfully!")
            else:
                print("⚠️ Preprocessing timeout or not triggered")

            # Take screenshot after preprocessing
            time.sleep(2)
            print("📸 After preprocessing...")
            page.screenshot(path='/tmp/preprocessing_test_2_complete.png', full_page=True)

            # Try to access preprocessing data from console
            print("\n🔍 Checking preprocessing data in state...")
            try:
                # Execute JavaScript to get preprocessing data
                preprocessing_data = page.evaluate("""
                    () => {
                        const state = AppStateManager.getState();
                        return state.preprocessingData || null;
                    }
                """)

                if preprocessing_data:
                    print("\n✅ Preprocessing data found in state:")
                    print(f"  Filename: {preprocessing_data.get('filename', 'N/A')}")
                    print(f"  Total Pages: {preprocessing_data.get('totalPages', 'N/A')}")

                    metadata = preprocessing_data.get('metadata', {})
                    print(f"  Sections: {metadata.get('sectionCount', 0)}")
                    print(f"  Tables: {metadata.get('tableCount', 0)}")
                    print(f"  Citations: {metadata.get('citationCount', 0)}")
                    print(f"  Total Text Items: {metadata.get('totalTextItems', 0)}")

                    # Save detailed results
                    with open('/tmp/preprocessing_results.json', 'w') as f:
                        json.dump(preprocessing_data, f, indent=2)
                    print("\n💾 Full results saved to /tmp/preprocessing_results.json")

                    # Check sections
                    sections = preprocessing_data.get('sections', [])
                    if sections:
                        print(f"\n📑 Found {len(sections)} sections:")
                        for section in sections[:5]:  # Show first 5
                            print(f"  - {section.get('type', '?')}: '{section.get('title', '?')}' (Page {section.get('page', '?')})")

                    # Check tables
                    tables = preprocessing_data.get('tables', [])
                    if tables:
                        print(f"\n📊 Found {len(tables)} tables:")
                        for table in tables:
                            print(f"  - {table.get('label', '?')} (Page {table.get('page', '?')})")

                    # Check citations
                    citations = preprocessing_data.get('citations', [])
                    if citations:
                        print(f"\n📚 Found {len(citations)} citations:")
                        for citation in citations[:3]:  # Show first 3
                            doi = citation.get('doi', 'N/A')
                            pmid = citation.get('pmid', 'N/A')
                            year = citation.get('year', 'N/A')
                            print(f"  - {year} | DOI: {doi} | PMID: {pmid}")

                else:
                    print("❌ No preprocessing data found in state")

            except Exception as e:
                print(f"❌ Error accessing preprocessing data: {e}")

        except Exception as e:
            print(f"❌ Error loading PDF: {e}")

        print("\n📋 Console summary:")
        preprocessing_logs = [log for log in console_logs if any(kw in log for kw in ['Preprocessing', 'Cache', 'Analysis', 'sections', 'tables', 'citations', '📊'])]
        for log in preprocessing_logs:
            print(f"  {log}")

        print("\n⏸️ Browser will close in 10 seconds...")
        time.sleep(10)

        browser.close()

if __name__ == "__main__":
    test_preprocessing()
