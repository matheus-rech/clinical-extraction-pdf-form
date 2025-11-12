# Persistent Submission ID - One Row Per Study

## 🎯 New Behavior (Implemented)

**One PDF/Study = One Row in Submissions Sheet**

### How It Works:

1. **First Save:**
   - Generates unique Submission ID: `sub_kim2016_pdf_1731393600000`
   - Stores ID in browser localStorage tied to document name
   - **INSERTS** new row in Submissions sheet
   - Status: ✓ Created new submission!

2. **Subsequent Saves (Same PDF):**
   - Retrieves existing Submission ID from localStorage
   - Searches Submissions sheet for this ID
   - **UPDATES** the existing row with latest data
   - Status: ✓ Updated existing submission (Row 5)!

3. **New PDF:**
   - Different document name = Different Submission ID
   - Creates new row in sheet
   - Each study maintains its own persistent ID

---

## 📊 Data Structure

### Submission ID Format:
```
sub_{sanitized_document_name}_{timestamp}

Examples:
- Kim2016.pdf       → sub_kim2016_pdf_1731393600000
- Study_2024.pdf    → sub_study_2024_pdf_1731393650000
- stroke-data.pdf   → sub_stroke_data_pdf_1731393700000
```

### localStorage Storage:
```javascript
Key: submissionId_kim2016_pdf
Value: sub_kim2016_pdf_1731393600000
```

---

## 🔄 Workflow Example

### Scenario: Working on Kim2016.pdf

```
1. Load Kim2016.pdf
2. Extract Citation field
3. Click "Save to Google Sheets"
   → Creates Row 2: sub_kim2016_pdf_1731393600000 | 2025-11-12... | Kim2016.pdf | ...

4. Continue working, extract DOI field
5. Click "Save to Google Sheets" again
   → Updates Row 2: sub_kim2016_pdf_1731393600000 | 2025-11-12... | Kim2016.pdf | Smith et al | 10.1234/...

6. Close browser, come back tomorrow
7. Load Kim2016.pdf again, add more fields
8. Click "Save to Google Sheets"
   → Still updates Row 2! (Same submission ID retrieved from localStorage)

9. Load different PDF: Study_2024.pdf
10. Click "Save to Google Sheets"
    → Creates Row 3: sub_study_2024_pdf_1731480000000 | ... (New row!)
```

---

## ✅ Benefits

1. **No Duplicates**: One study = One row forever
2. **Incremental Work**: Save as you go, same row gets updated
3. **Session Persistence**: Works across browser sessions via localStorage
4. **Clear Tracking**: Submission ID includes document name for easy identification

---

## 📋 Extractions Tab Behavior

**Still appends** - this is correct!

The Extractions tab maintains a **trace log** of every extraction action:
- Row 2: sub_kim2016_pdf_... | Citation | Smith et al 2024 | Page 1 | text | x,y,w,h
- Row 3: sub_kim2016_pdf_... | DOI | 10.1234/example | Page 1 | text | x,y,w,h
- Row 4: sub_kim2016_pdf_... | PMID | 12345678 | Page 2 | text | x,y,w,h

This gives you a complete audit trail of how you collected the data.

---

## 🔍 Status Messages

**You'll see:**

First save:
```
✓ Created new submission!
Adding 3 extraction trace records...
✓ Successfully saved! (ID: sub_kim2016_pdf_1731393600000)
```

Subsequent saves:
```
Checking for existing submission...
✓ Updated existing submission (Row 2)!
Adding 5 extraction trace records...
✓ Successfully saved! (ID: sub_kim2016_pdf_1731393600000)
```

---

## 🧹 Clearing localStorage (If Needed)

If you want to start fresh for a document:

**Browser Console:**
```javascript
// Clear specific document
localStorage.removeItem('submissionId_kim2016_pdf');

// Clear all submissions
Object.keys(localStorage)
    .filter(key => key.startsWith('submissionId_'))
    .forEach(key => localStorage.removeItem(key));
```

**Result**: Next save will create a NEW submission ID and row.

---

## 🎯 Summary

**Before:**
- Every "Save to Google Sheets" → New row (duplicates!)
- Kim2016.pdf saved 3 times → 3 rows

**After:**
- Every "Save to Google Sheets" → UPDATE if exists, INSERT if new
- Kim2016.pdf saved 3 times → 1 row (updated 3 times)

**Perfect for:**
- Working on studies across multiple sessions
- Incremental data extraction
- Collaborative work (same PDF, same row)
- Data integrity (one study = one row)

---

**Ready to test!** 🚀
