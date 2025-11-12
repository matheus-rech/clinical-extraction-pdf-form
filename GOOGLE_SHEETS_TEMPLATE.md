# Google Sheets Template

## 📋 Quick Copy Template

Use this to quickly create your Google Sheet with the correct structure.

---

## Tab 1: Submissions

**Complete Column Headers (48 columns organized by form steps):**

### Copy-Paste Ready (Tab-separated):
```
Submission ID	Timestamp	Document	Citation	DOI	PMID	Journal	Year	Country	Centers	Funding	Conflicts	Registration	Population	Intervention	Comparator	Outcomes	Timing	Study Type	Inclusion Met	Total N	Surgical N	Control N	Age Mean	Age SD	Age Median	Age IQR Lower	Age IQR Upper	Male N	Female N	Pre-stroke mRS	NIHSS Mean	GCS Mean	Vascular Territory	Infarct Volume	Stroke Volume Cerebellum	Edema Dynamics	Peak Swelling Window	Brainstem Involvement	Supratentorial Involvement	Non-Cerebellar Stroke	Indications (JSON)	Interventions (JSON)	Study Arms (JSON)	Mortality Data (JSON)	mRS Data (JSON)	Complications (JSON)	Predictors (JSON)	Predictors Summary
```

### Organized by Form Steps:

**Metadata (3 columns):**
- Submission ID, Timestamp, Document

**Step 1: Study ID (10 columns):**
- Citation, DOI, PMID, Journal, Year, Country, Centers, Funding, Conflicts, Registration

**Step 2: PICO-T (7 columns):**
- Population, Intervention, Comparator, Outcomes, Timing, Study Type, Inclusion Met

**Step 3: Baseline (13 columns):**
- Total N, Surgical N, Control N
- Age Mean, Age SD, Age Median, Age IQR Lower, Age IQR Upper
- Male N, Female N
- Pre-stroke mRS, NIHSS Mean, GCS Mean

**Step 4: Imaging (8 columns):**
- Vascular Territory, Infarct Volume, Stroke Volume Cerebellum
- Edema Dynamics, Peak Swelling Window
- Brainstem Involvement, Supratentorial Involvement, Non-Cerebellar Stroke

**Steps 5-8: Dynamic Fields (7 columns, stored as JSON arrays):**
- Indications (JSON), Interventions (JSON), Study Arms (JSON)
- Mortality Data (JSON), mRS Data (JSON)
- Complications (JSON), Predictors (JSON), Predictors Summary

**Example Data Row:**
```
sub_1705483200000 | 2025-01-17T10:30:00.000Z | study_2024.pdf | Smith et al. 2024 | 10.1234/example | 12345678 | Stroke | 2024 | USA | Multi | NIH Grant | None | NCT12345678 | Cerebellar stroke patients | Suboccipital decompressive craniectomy | Medical management | Mortality, mRS at 90 days | 90 days | RCT | true | 150 | 75 | 75 | 65.5 | 12.3 | 64 | 58 | 72 | 90 | 60 | 0 | 14.2 | 8.5 | PICA | 45.2 | 38.5 mL | Progressive | 24-48 hours | true | false | false | [{"field":"indication_sign_1","value":"Hydrocephalus"}] | [{"field":"intervention_type_1","value":"SDC_EVD"}] | [{"field":"arm_n_1","value":"75"}] | [{"field":"mortality_deaths_1","value":"15"}] | [{"field":"mrs_0_1","value":"10"}] | [{"field":"comp_desc_1","value":"Infection"}] | [{"field":"pred_var_1","value":"Age"}] | Age and infarct volume independently predict poor outcome
```

**Google Sheets Formula (Row 2 onwards):**

| Column | Formula | Purpose |
|--------|---------|---------|
| A (Submission ID) | `=TEXT(NOW(),"sub_"&B2*86400)` | Auto-generate unique ID |
| B (Timestamp) | (auto-filled by app) | ISO timestamp |
| C-G | (auto-filled by app) | Study data |

---

## Tab 2: Extractions

**Column Headers (Row 1):**

```
Submission ID | Field Name | Text | Page | Method | X | Y | Width | Height
```

**Example Data (Row 2):**
```
sub_1705483200000 | Population | Patients with acute stroke | 3 | text | 120.5 | 340.2 | 250.0 | 18.5
```

**Column Details:**

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| A | Text | `sub_1705483200000` | Links to Submissions.A |
| B | Text | `Population` | Form field name |
| C | Text | `Patients with...` | Extracted text |
| D | Number | `3` | PDF page number |
| E | Text | `text` | Extraction method (text/region/image/ai-table/annotation) |
| F | Number | `120.5` | X coordinate (pixels) |
| G | Number | `340.2` | Y coordinate (pixels) |
| H | Number | `250.0` | Width (pixels) |
| I | Number | `18.5` | Height (pixels) |

**Note:** The Extractions tab captures the complete trace log of every field extraction with coordinates, allowing you to reproduce and verify the data collection process.

---

## 🎨 Formatting Recommendations

### Submissions Tab
```css
Header Row (Row 1):
- Bold: Yes
- Background: #4A90E2 (blue)
- Text Color: White
- Font Size: 11pt
- Freeze: 1 row

Data Rows (Row 2+):
- Alternating colors: White / #F5F5F5 (light gray)
- Text alignment: Left
- Number format: Automatic
```

### Extractions Tab
```css
Header Row (Row 1):
- Bold: Yes
- Background: #50C878 (green)
- Text Color: White
- Font Size: 11pt
- Freeze: 1 row

Data Rows (Row 2+):
- Alternating colors: White / #E8F5E9 (light green)
- Text alignment: Left
- Coordinate columns (F-I): Number format with 1 decimal
```

---

## 📊 Advanced Features (Optional)

### 1. Data Validation

**Submissions Tab - DOI Column (E):**
```
Custom formula: =REGEXMATCH(E2,"^10\.\d{4,}")
Error message: "Invalid DOI format. Should start with 10."
```

**Extractions Tab - Method Column (E):**
```
List: text, region, image, ai-table, annotation
Error message: "Invalid extraction method"
```

### 2. Conditional Formatting

**Highlight Missing Data:**
```
Apply to: Submissions!D2:G
Format cells if: Is empty
Background: #FFF3CD (yellow)
```

**Highlight AI Extractions:**
```
Apply to: Extractions!E2:E
Format cells if: Text contains "ai-table"
Background: #E1BEE7 (purple)
```

### 3. Pivot Table

**Extractions Summary:**
1. Data → Pivot table
2. Rows: Method
3. Values: COUNTA of Field Name
4. Result: Count extractions per method

### 4. Chart

**Extraction Methods Distribution:**
1. Insert → Chart
2. Type: Pie chart
3. Data range: Pivot table
4. Title: "Extraction Methods Usage"

---

## 🔗 Formulas You Can Add

### Submissions Tab

**Column H: Extract Count**
```excel
=COUNTIF(Extractions!$A:$A,A2)
```
Shows how many extractions this submission has.

**Column I: Completion %**
```excel
=(H2/8)*100
```
Assuming 8-step form, shows completion percentage.

**Column J: Status**
```excel
=IF(I2=100,"✓ Complete",IF(I2>50,"⏳ In Progress","❌ Started"))
```
Visual status indicator.

### Extractions Tab

**Column J: Extraction Size**
```excel
=H2*I2
```
Area in pixels (width × height).

**Column K: Large Extraction**
```excel
=IF(J2>10000,"Yes","No")
```
Flag large extractions (>10,000 px²).

---

## 📱 Mobile-Friendly View

For viewing on mobile devices:

1. **Hide coordinate columns** (F-I):
   - Right-click column header
   - Hide columns

2. **Create filtered view**:
   - Data → Filter views → Create new filter view
   - Name: "Mobile Summary"
   - Show only: A, B, C, D, E columns

3. **Use QUERY function** for summary:
```excel
=QUERY(Extractions!A2:I,"SELECT A, B, COUNT(C) GROUP BY A, B")
```

---

## 🔄 Import/Export Between Sheets

### Export to CSV
```
File → Download → Comma-separated values (.csv)
```

### Import from CSV
```
File → Import → Upload → Select file → Replace/Append
```

### Apps Script for Auto-Export
```javascript
function autoExportCSV() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Submissions');
  var csv = convertRangeToCsv_(sheet.getDataRange());

  // Save to Google Drive
  var file = DriveApp.createFile('clinical_data_' + new Date().getTime() + '.csv', csv);
  Logger.log('CSV created: ' + file.getUrl());
}

function convertRangeToCsv_(range) {
  var data = range.getValues();
  var csv = '';
  for (var i = 0; i < data.length; i++) {
    csv += data[i].join(',') + '\n';
  }
  return csv;
}
```

---

## 🛡️ Sheet Protection

### Protect Headers
1. Select Row 1 (both tabs)
2. Data → Protect sheets and ranges
3. Set permissions: Only you can edit
4. Description: "Header row protection"

### Protect Formulas
1. Select cells with formulas
2. Data → Protect sheets and ranges
3. Set permissions: Only you can edit

---

## 📈 Performance Tips

1. **Limit to 10,000 rows per tab** (Google Sheets performs best)
2. **Archive old data** to separate sheets yearly
3. **Use FILTER instead of manual filtering** (faster)
4. **Avoid volatile functions** (NOW(), RAND()) in data area
5. **Use ARRAYFORMULA** for column-wide operations

---

## 🎯 Ready-to-Copy Headers

### Submissions (copy this row - 48 columns):
```
Submission ID	Timestamp	Document	Citation	DOI	PMID	Journal	Year	Country	Centers	Funding	Conflicts	Registration	Population	Intervention	Comparator	Outcomes	Timing	Study Type	Inclusion Met	Total N	Surgical N	Control N	Age Mean	Age SD	Age Median	Age IQR Lower	Age IQR Upper	Male N	Female N	Pre-stroke mRS	NIHSS Mean	GCS Mean	Vascular Territory	Infarct Volume	Stroke Volume Cerebellum	Edema Dynamics	Peak Swelling Window	Brainstem Involvement	Supratentorial Involvement	Non-Cerebellar Stroke	Indications (JSON)	Interventions (JSON)	Study Arms (JSON)	Mortality Data (JSON)	mRS Data (JSON)	Complications (JSON)	Predictors (JSON)	Predictors Summary
```

### Extractions (copy this row - 9 columns):
```
Submission ID	Field Name	Text	Page	Method	X	Y	Width	Height
```

**How to use:**
1. Copy the row above (including tabs)
2. Paste into Row 1 of your sheet
3. Format as bold with colored background
4. Freeze the row

---

## 📦 Working with JSON Fields

The last 7 columns of the Submissions sheet contain JSON arrays for dynamic fields (indications, interventions, etc.). Here's how to parse them:

### Google Sheets Formula to Extract JSON Values:

**Extract first indication:**
```excel
=REGEXEXTRACT(AP2, """value"":""([^""]+)""")
```

**Count number of entries:**
```excel
=LEN(AP2)-LEN(SUBSTITUTE(AP2,"field",""))/5
```

### Python/R Parsing:

**Python:**
```python
import json
import pandas as pd

df = pd.read_csv('submissions.csv')
df['indications_parsed'] = df['Indications (JSON)'].apply(json.loads)
```

**R:**
```r
library(jsonlite)
library(tidyverse)

df <- read_csv('submissions.csv')
df$indications_parsed <- map(df$`Indications (JSON)`, fromJSON)
```

---

**Pro Tip:** Save this template as "Clinical Extraction Template" and use File → Make a copy for each new project!
