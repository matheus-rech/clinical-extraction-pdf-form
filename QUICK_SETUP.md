# Google Sheets Quick Setup - 5 Minutes

## ✅ Checklist

### ☐ Step 1: Google Cloud Console (5 min)
1. Go to: https://console.cloud.google.com/
2. Create project: `Clinical Extraction App`
3. Enable API: Search "Google Sheets API" → Enable
4. OAuth consent: External → Add your email as test user
5. Create credentials: OAuth Client ID → Web application
6. Add origin: `http://localhost:8000`
7. **Copy Client ID**: `123456789-abc...apps.googleusercontent.com`

### ☐ Step 2: Create Google Sheet (2 min)
1. Go to: https://sheets.google.com/
2. Create blank sheet: `Clinical Study Data`
3. Rename Sheet1 → `Submissions`
4. Add headers:
   ```
   Submission ID | Timestamp | Document | Citation | DOI | PMID | Total N
   ```
5. Create Sheet2 → `Extractions`
6. Add headers:
   ```
   Submission ID | Field Name | Text | Page | Method | X | Y | Width | Height
   ```
7. **Copy Sheet ID** from URL (between `/d/` and `/edit`)

### ☐ Step 3: Configure App (1 min)
1. Open app: http://localhost:8000/Clinical_Study_Extraction.html
2. Click ⚙️ Settings
3. Paste **OAuth Client ID**
4. Paste **Google Sheet ID**
5. Click **Save Settings**
6. See green ✓ checkmarks

### ☐ Step 4: Test (2 min)
1. Load a PDF
2. Extract some data (highlight text)
3. Click **💾 Save to Google Sheets**
4. Authorize (first time only)
5. Check your sheet - data should appear!

---

## 🔑 What You Need to Copy

### 1. OAuth Client ID (from Google Cloud Console)
```
Format: 123456789-abcdefghijklmnop.apps.googleusercontent.com
Length: ~70 characters
Where: Credentials → OAuth 2.0 Client IDs
```

### 2. Google Sheet ID (from Sheet URL)
```
URL: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
                                              ^^^^^^^^^^^^^^
Format: 1BxiMVs0XRA5nFMdKvBQ...
Length: ~44 characters
Where: Browser address bar when sheet is open
```

---

## 🎯 Sheet Column Headers (Must Be Exact)

**Submissions Tab Row 1:**
```
Submission ID	Timestamp	Document	Citation	DOI	PMID	Total N
```

**Extractions Tab Row 1:**
```
Submission ID	Field Name	Text	Page	Method	X	Y	Width	Height
```

**Important:**
- Tab names are case-sensitive: `Submissions` and `Extractions`
- Column order must match exactly
- Headers must be in Row 1

---

## ❌ Common Mistakes

| Error | Cause | Fix |
|-------|-------|-----|
| "OAuth client ID missing" | Didn't save settings | Click Save Settings button |
| "Range 'Submissions!A:A' not found" | Wrong tab name | Rename to exact: `Submissions` |
| "403 Permission denied" | Not added as test user | Add email in OAuth consent screen |
| "redirect_uri_mismatch" | Wrong origin URL | Add `http://localhost:8000` to origins |
| Data not appearing | Wrong Sheet ID | Check ID has no spaces, is correct |

---

## 🚀 One-Line Commands

**Start Server:**
```bash
python3 -m http.server 8000
```

**Open App:**
```
http://localhost:8000/Clinical_Study_Extraction.html
```

**Google Cloud Console:**
```
https://console.cloud.google.com/apis/credentials
```

**Your Sheets:**
```
https://sheets.google.com/
```

---

## 📞 Quick Troubleshooting

**Issue: Authorization popup blocked**
- Allow popups for localhost
- Try Ctrl+Click on "Save to Google Sheets"

**Issue: "API not enabled"**
- Wait 1-2 minutes after enabling
- Refresh the app page

**Issue: Old data still showing**
- Clear browser cache (Ctrl+Shift+R)
- Check you're on correct sheet

**Issue: Multiple authorization prompts**
- First time needs "unsafe app" approval
- Click Advanced → Go to app

---

## 💡 Pro Tips

1. **Bookmark your sheet** for quick access
2. **Share sheet** with team members beforehand
3. **Test with dummy data** first
4. **Add yourself as test user** before creating OAuth client
5. **Use Incognito mode** for clean OAuth test
6. **Wait 5 min** after OAuth changes before testing

---

## 📱 Mobile Setup

Same steps work on mobile browser! Just need:
- Mobile Chrome/Safari
- Active Google account
- Internet connection

OAuth popup may look different but process is identical.

---

## ⏰ Timeline

- Google Cloud setup: **5 minutes**
- Sheet creation: **2 minutes**
- App configuration: **1 minute**
- First authorization: **2 minutes**
- Total: **~10 minutes** (first time)

After initial setup: **Instant** (just click Save to Sheets)

---

## 🎓 Learn More

- Full guide: `GOOGLE_SHEETS_SETUP.md`
- Sheet template: `GOOGLE_SHEETS_TEMPLATE.md`
- Main docs: `DOCUMENTATION.md`

---

**Need help?** Check browser console (F12) for error messages and match them to the troubleshooting section.
