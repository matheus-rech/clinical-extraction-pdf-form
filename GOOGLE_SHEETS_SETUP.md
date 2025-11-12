# Google Sheets API Setup Guide

Complete step-by-step guide to integrate your Clinical Study Extraction app with Google Sheets.

---

## 📋 Overview

The app will export data to a Google Sheet with two tabs:
- **Submissions**: One row per study (metadata)
- **Extractions**: Multiple rows per study (detailed trace log)

---

## ⏱️ Time Required: ~15 minutes

---

## 📝 Part 1: Create Google Cloud Project & Enable APIs

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account

### Step 2: Create a New Project
1. Click the project dropdown at the top (says "Select a project")
2. Click **"NEW PROJECT"** button
3. Enter project name: `Clinical Extraction App`
4. Click **"CREATE"**
5. Wait for project creation (~30 seconds)
6. Switch to the new project from the dropdown

### Step 3: Enable Google Sheets API
1. In the search bar at top, type: **Google Sheets API**
2. Click on "Google Sheets API" result
3. Click the blue **"ENABLE"** button
4. Wait for API to be enabled (~10 seconds)

---

## 🔐 Part 2: Create OAuth 2.0 Credentials

### Step 4: Configure OAuth Consent Screen
1. In left sidebar, click **"OAuth consent screen"**
2. Select **"External"** user type
3. Click **"CREATE"**

**App Information:**
- App name: `Clinical Study Extraction`
- User support email: (your email)
- Developer contact: (your email)

4. Click **"SAVE AND CONTINUE"**

**Scopes:**
5. Click **"ADD OR REMOVE SCOPES"**
6. Search for: `spreadsheets`
7. Check the box: `.../auth/spreadsheets` (See, edit, create, and delete all your Google Sheets)
8. Click **"UPDATE"**
9. Click **"SAVE AND CONTINUE"**

**Test Users:**
10. Click **"ADD USERS"**
11. Enter your email address (and any collaborators)
12. Click **"ADD"**
13. Click **"SAVE AND CONTINUE"**
14. Click **"BACK TO DASHBOARD"**

### Step 5: Create OAuth 2.0 Client ID
1. In left sidebar, click **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at top
3. Select **"OAuth client ID"**

**Configuration:**
- Application type: **Web application**
- Name: `Clinical Extraction Web App`

**Authorized JavaScript origins:**
4. Click **"+ ADD URI"**
5. Add: `http://localhost:8000`
6. Click **"+ ADD URI"** again
7. Add: `http://127.0.0.1:8000`
8. (Optional) If deploying online, add: `https://yourdomain.com`

**Authorized redirect URIs:**
9. Leave empty (not needed for this app)

10. Click **"CREATE"**

### Step 6: Copy Your Client ID
A popup will appear with your credentials.

**IMPORTANT - Copy this:**
```
Client ID: 123456789-abcdefghijk.apps.googleusercontent.com
```

✅ **Save this Client ID** - you'll need it in Step 10

(You can ignore "Client Secret" - not needed for this app)

---

## 📊 Part 3: Create Google Sheet with Proper Structure

### Step 7: Create New Google Sheet
1. Go to: https://sheets.google.com/
2. Click **"+ Blank"** to create new sheet
3. Rename sheet to: `Clinical Study Data`

### Step 8: Create "Submissions" Tab

**Rename Sheet1:**
1. Right-click "Sheet1" tab at bottom
2. Click **"Rename"**
3. Type: `Submissions`
4. Press Enter

**Add Column Headers (Row 1):**
Copy-paste ALL 48 headers (tab-separated) into row 1:

```
Submission ID	Timestamp	Document	Citation	DOI	PMID	Journal	Year	Country	Centers	Funding	Conflicts	Registration	Population	Intervention	Comparator	Outcomes	Timing	Study Type	Inclusion Met	Total N	Surgical N	Control N	Age Mean	Age SD	Age Median	Age IQR Lower	Age IQR Upper	Male N	Female N	Pre-stroke mRS	NIHSS Mean	GCS Mean	Vascular Territory	Infarct Volume	Stroke Volume Cerebellum	Edema Dynamics	Peak Swelling Window	Brainstem Involvement	Supratentorial Involvement	Non-Cerebellar Stroke	Indications (JSON)	Interventions (JSON)	Study Arms (JSON)	Mortality Data (JSON)	mRS Data (JSON)	Complications (JSON)	Predictors (JSON)	Predictors Summary
```

**Structure (48 columns total):**
- **Columns A-C**: Metadata (Submission ID, Timestamp, Document)
- **Columns D-M**: Step 1 - Study ID (10 fields)
- **Columns N-T**: Step 2 - PICO-T (7 fields)
- **Columns U-AG**: Step 3 - Baseline (13 fields)
- **Columns AH-AO**: Step 4 - Imaging (8 fields)
- **Columns AP-AV**: Steps 5-8 - Dynamic fields stored as JSON (7 fields)

**Format Headers:**
- Select row 1
- Click **Bold** (Ctrl/Cmd + B)
- Background color: Light blue
- Freeze row: View → Freeze → 1 row

### Step 9: Create "Extractions" Tab

**Add New Tab:**
1. Click **"+"** button at bottom left
2. Rename to: `Extractions`

**Add Column Headers (Row 1):**
Type these exact headers in row 1:

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Submission ID | Field Name | Text | Page | Method | X | Y | Width | Height |

**Format Headers:**
- Select row 1
- Click **Bold**
- Background color: Light green
- Freeze row: View → Freeze → 1 row

### Step 10: Copy Sheet ID

**Get Sheet ID from URL:**
Your URL looks like:
```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBQ.../edit
                                       ^^^^^^^^^^^^^^^^^^^
                                       This is your SHEET ID
```

✅ **Copy everything between `/d/` and `/edit`**

Example: `1BxiMVs0XRA5nFMdKvBQQQQQQQQQQQQQQQQQQQ`

---

## ⚙️ Part 4: Configure the App

### Step 11: Open Settings in the App

1. Start your local server:
   ```bash
   cd /Users/matheusrech/clinical_extraction_pdf_form
   python3 -m http.server 8000
   ```

2. Open in browser: http://localhost:8000/Clinical_Study_Extraction.html

3. Click the **⚙️ Settings** button (top right of PDF viewer)

### Step 12: Enter Your Credentials

**Google Sheets Integration section:**

1. **OAuth Client ID:** Paste your Client ID from Step 6
   ```
   123456789-abcdefghijk.apps.googleusercontent.com
   ```

2. **Google Sheet ID:** Paste your Sheet ID from Step 10
   ```
   1BxiMVs0XRA5nFMdKvBQQQQQQQQQQQQQQQQQQQ
   ```

3. Click **"Save Settings"**

4. You should see green checkmarks: ✓ Configured

---

## 🧪 Part 5: Test the Integration

### Step 13: Test Export

1. **Load a PDF** in the app
2. **Extract some data**:
   - Click a field (e.g., "Citation")
   - Highlight text in the PDF
   - See it populate the field
3. **Fill a few more fields** to have test data
4. Click **"💾 Save to Google Sheets"** button (bottom of form panel)

### Step 14: First-Time Authorization

You'll see a Google OAuth popup:

1. Select your Google account
2. Click **"Continue"** (you'll see a warning "Google hasn't verified this app")
3. Click **"Advanced"**
4. Click **"Go to Clinical Study Extraction (unsafe)"**
5. Review permissions
6. Click **"Allow"**

### Step 15: Verify Data in Sheets

1. Go back to your Google Sheet
2. Check **"Submissions" tab**:
   - Should have 1 new row with your data
   - Submission ID, timestamp, document name, etc.

3. Check **"Extractions" tab**:
   - Should have multiple rows (one per extraction)
   - Each with field name, text, page, coordinates

✅ **Success!** Your integration is working!

---

## 🔧 Troubleshooting

### ❌ "OAuth client ID is missing"
**Solution:** Make sure you saved settings after entering credentials

### ❌ "Failed to load Google API"
**Solution:** Check your internet connection, refresh the page

### ❌ "Permission denied" or 403 error
**Solution:**
1. Check Sheet ID is correct
2. Make sure you added yourself as Test User (Step 4.10)
3. Verify API is enabled (Step 3)

### ❌ "Range 'Submissions!A:A' not found"
**Solution:**
1. Check tab name is exactly `Submissions` (case-sensitive)
2. Make sure you created both tabs
3. Verify column headers match exactly

### ❌ "redirect_uri_mismatch" error
**Solution:**
1. Go back to Google Cloud Console → Credentials
2. Edit your OAuth Client ID
3. Add `http://localhost:8000` to Authorized JavaScript origins
4. Save and wait 5 minutes for changes to propagate

### ❌ Data not appearing in sheet
**Solution:**
1. Check browser console (F12) for errors
2. Verify Sheet ID is correct (no extra spaces)
3. Make sure columns in Submissions match the code

---

## 📊 Understanding the Data Structure

### Submissions Tab (One row per study, 48 columns)

**Metadata (3 columns):**
```
Submission ID: Unique ID (sub_1234567890)
Timestamp: ISO date (2025-01-17T10:30:00.000Z)
Document: PDF filename
```

**Step 1: Study ID (10 columns):**
```
Citation, DOI, PMID, Journal, Year, Country, Centers, Funding, Conflicts, Registration
```

**Step 2: PICO-T (7 columns):**
```
Population, Intervention, Comparator, Outcomes, Timing, Study Type, Inclusion Met
```

**Step 3: Baseline (13 columns):**
```
Total N, Surgical N, Control N
Age Mean, Age SD, Age Median, Age IQR Lower, Age IQR Upper
Male N, Female N
Pre-stroke mRS, NIHSS Mean, GCS Mean
```

**Step 4: Imaging (8 columns):**
```
Vascular Territory, Infarct Volume, Stroke Volume Cerebellum
Edema Dynamics, Peak Swelling Window
Brainstem Involvement, Supratentorial Involvement, Non-Cerebellar Stroke
```

**Steps 5-8: Dynamic Fields (7 columns, JSON arrays):**
```
Indications (JSON): e.g., [{"field":"indication_sign_1","value":"Hydrocephalus"}]
Interventions (JSON): e.g., [{"field":"intervention_type_1","value":"SDC_EVD"}]
Study Arms (JSON): e.g., [{"field":"arm_n_1","value":"75"}]
Mortality Data (JSON): e.g., [{"field":"mortality_deaths_1","value":"15"}]
mRS Data (JSON): e.g., [{"field":"mrs_0_1","value":"10"}]
Complications (JSON): e.g., [{"field":"comp_desc_1","value":"Infection"}]
Predictors (JSON): e.g., [{"field":"pred_var_1","value":"Age"}]
Predictors Summary: Free-text summary of key predictors
```

**Why JSON for dynamic fields?**
- Handles variable numbers of entries (1 to N indications, interventions, etc.)
- Preserves all data without needing unlimited columns
- Can be parsed later for analysis (e.g., in R/Python/Google Sheets formulas)

### Extractions Tab (Multiple rows per study, 9 columns)
```
Submission ID: Links to Submissions tab
Field Name: Which form field (e.g., "Population")
Text: Extracted text content
Page: PDF page number
Method: text/region/image/ai-table/annotation
X, Y, Width, Height: Coordinates on PDF page
```

This tab provides a detailed trace log of every extraction action with coordinates for reproducibility.

---

## 🔒 Security Best Practices

1. **Never commit credentials** to git
   - Client ID is OK to share (public identifier)
   - Sheet ID is OK to share (if sheet is public anyway)

2. **Control access** via Google Sheet permissions
   - Share sheet only with authorized users
   - Use "Test Users" in OAuth consent screen

3. **Production deployment**:
   - Switch OAuth to "Published" status (after testing)
   - Add production domain to Authorized origins
   - Consider using service account for backend integration

---

## 📈 Next Steps

### Optional Enhancements

1. **Add more columns** to Submissions tab:
   - Edit lines 6344 and 6349-6357 in the HTML file
   - Match your custom fields

2. **Create pivot tables** in Google Sheets:
   - Analyze extraction patterns
   - Track completion rates
   - Monitor data quality

3. **Set up Google Apps Script** triggers:
   - Auto-email notifications on new submissions
   - Data validation rules
   - Automated backups

4. **Deploy online**:
   - Host on GitHub Pages, Netlify, or Vercel
   - Update OAuth origins to include production URL
   - Use HTTPS (required for OAuth)

---

## 💡 Tips

- **Multi-user setup**: Each user needs to be added as Test User
- **Quota limits**: Google Sheets API has limits (300 requests/minute)
- **Offline work**: Save as JSON/CSV first, upload later
- **Backup data**: Export sheet regularly (File → Download → CSV)
- **Version control**: Use sheet's version history (File → Version history)

---

## 📞 Support

If you encounter issues:
1. Check browser console (F12) for error messages
2. Verify all URLs are exact (no typos)
3. Wait 5-10 minutes after changing OAuth settings
4. Try incognito/private browsing mode
5. Clear browser cache and cookies

---

**Last Updated:** January 2025
**Compatible with:** Google Sheets API v4
**Tested on:** Chrome 120+, Firefox 120+, Safari 17+
