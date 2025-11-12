# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-file web application for extracting structured data from clinical research PDFs with AI-powered assistance, interactive PDF viewer, and comprehensive audit trail capabilities. Built with pure HTML/CSS/JavaScript (no framework dependencies).

## Quick Start

### Running the Application
```bash
# Start local development server
python3 -m http.server 8000

# Access application
# http://localhost:8000/Clinical_Study_Extraction.html
```

### Testing
No automated test suite. Manual testing workflow:
1. Load application in Chrome/Firefox/Edge
2. Load `Kim2016.pdf` (test PDF)
3. Test extraction methods: text selection, region mode, image capture, search
4. Verify exports: JSON, CSV, Audit Report, Annotated PDF
5. Check trace log for extraction records

## Architecture

### Single-File Application Structure
The entire application is contained in `Clinical_Study_Extraction.html` with embedded JavaScript organized into manager objects:

**Core Managers:**
- `AppStateManager` - Central state management (PDF document, scale, page number)
- `StatusManager` - User notifications and status messages
- `MemoryManager` - Text layer rendering and extraction coordination
- `FormManager` - 8-step form navigation and validation
- `ExtractionTracker` - Audit trail of all extractions with coordinates

**Extraction Managers:**
- `RegionSelectionManager` - Box-based text extraction from PDF regions
- `ImageExtractionManager` - Visual capture of PDF regions as PNG images
- `PDFAnnotationManager` - Import existing PDF highlights/annotations

**AI & Export:**
- `AIProviders` - Multi-provider AI integration (Gemini, Claude, GPT-4)
- `ExportManager` - JSON, CSV, Audit Report, Annotated PDF exports

### Key Dependencies (CDN)
- **PDF.js 3.11.174** - PDF rendering and text layer
- **pdf-lib 1.17.1** - PDF annotation generation
- **Google API client** - Google Sheets integration (optional)

### Data Flow
```
PDF Load → PDF.js Rendering → Text Layer → User Selection →
ExtractionTracker → FormManager → Export/GoogleSheets
```

### State Management Pattern
All managers access global state via `AppStateManager.getState()`:
```javascript
const state = AppStateManager.getState();
// Returns: { pdfDoc, currentPage, scale, documentName, ... }
```

## 8-Step Extraction Form

The application guides users through structured data collection:
1. **Study ID & Metadata** - Citation, DOI, PMID, journal
2. **PICO-T Framework** - Population, Intervention, Comparator, Outcomes, Timing
3. **Baseline Demographics** - Sample size, age, gender, comorbidities
4. **Imaging Data** - Volume measurements, swelling indices
5. **Interventions** - Surgical procedures, medical management
6. **Study Arms** - Control vs treatment groups
7. **Outcomes** - Mortality, mRS (modified Rankin Scale) distributions
8. **Complications & Predictors** - Adverse events, prognostic factors

Dynamic fields support multiple entries (e.g., multiple study arms, mortality timepoints).

## AI Integration

### Supported Providers
- **Gemini** (Recommended) - Google Search grounding for metadata extraction
- **Claude** - Anthropic Sonnet 3.5 for text generation
- **GPT-4** - OpenAI for text generation

### AI Features
- **PICO-T Generation** - Auto-extract study framework from full PDF text
- **Metadata Search** - Find DOI, PMID, journal, year using web search (Gemini only)
- **Summary Generation** - Generate key findings from predictors section
- **Field Validation** - Verify extracted text against PDF content

### Adding New AI Providers
1. Add provider to `AIProviders` object with:
   - `name`, `endpoint`
   - `formatRequest(systemPrompt, userPrompt, schema)` - Format API request
   - `parseResponse(result)` - Extract text from API response
2. Add to Settings UI dropdown
3. Update `updateProviderFields()` for API key help text

## Extraction Methods

### 1. Manual Text Selection (Native)
- Click form field → Highlight text in PDF
- Uses browser Selection API for precise multi-line selection
- Records coordinates: `{x, y, width, height, page}`

### 2. Region Box Selection
- Click 🔲 Region button → Draw box around text area
- Extracts text from specific PDF region (tables, columns)
- Smart text ordering: top-to-bottom, left-to-right

### 3. Image Capture
- Click 📷 Image button → Draw box around figure/graph
- Captures high-DPI PNG image (respects `devicePixelRatio`)
- Auto-downloads image, displays thumbnail in trace log
- Naming: `figure_p{page}_{timestamp}.png`

### 4. PDF Annotation Import
- Click 📝 Annotations button
- Imports existing PDF highlights/comments
- Auto-suggests appropriate form fields based on content
- Supports: Highlight, Text, FreeText, Underline

### 5. Full-Text Search
- Search text across all PDF pages
- Visual highlighting with orange markers and pulsing animation
- Coordinate-based precise positioning

## Trace Log & Audit Trail

Every extraction is recorded with:
- Field name
- Extracted text/image
- Page number
- Coordinates `{x, y, width, height}`
- Method (`manual`, `ai`, `region`, `image`, `annotation`)
- Timestamp
- Document name

Visual indicators:
- 🟢 Green markers → Manual extractions
- 🟣 Purple markers → AI extractions
- 🔵 Blue boxes → Image captures
- 📷 Image icon + thumbnail → Image extraction records

## Export Formats

### JSON Export
```javascript
{
  document: "documentName.pdf",
  exportDate: "2025-11-12T...",
  formData: { /* all form fields */ },
  extractions: [ /* trace log with coordinates */ ]
}
```

### CSV Export
Extraction trace log as spreadsheet:
```
Field Name, Text, Page, Method, X, Y, Width, Height, Timestamp
```

### Audit Report (HTML)
Human-readable report with:
- Document metadata
- Extraction summary
- Complete trace log
- Statistics (manual vs AI extractions)

### Annotated PDF
PDF with highlighted extractions overlaid on original document using pdf-lib.

### Google Sheets Integration
Dual-table structure:
- **Submissions tab** - One row per document (summary data)
- **Extractions tab** - One row per extraction (detailed trace)

## Key Technical Details

### High-DPI Rendering
```javascript
const dpr = window.devicePixelRatio || 1;
canvas.width = viewport.width * dpr;
canvas.height = viewport.height * dpr;
// Ensures crisp rendering on Retina/4K displays
```

### Coordinate System
PDF.js coordinates are stored in viewport space. Text selection coordinates are captured relative to the rendered canvas, enabling precise marker positioning and annotation generation.

### Text Layer Implementation
Uses PDF.js official text layer API (`page.getTextContent()`) with 100% opacity overlay on canvas. Text is selectable via browser's native Selection API, not custom mouse tracking.

### Browser localStorage
- API keys stored as Base64-encoded JSON
- Extraction history persisted across sessions
- Settings and preferences cached locally

## Browser Compatibility

- ✅ Chrome/Edge (Recommended)
- ✅ Firefox 90+
- ✅ Safari
- ❌ Internet Explorer (Not supported)

## Development Workflow

### Modifying the Application
All code is in `Clinical_Study_Extraction.html`. Key sections:
- Lines 1-600: CSS styles (`:root` variables for easy theming)
- Lines 600-1400: HTML structure (form steps, PDF viewer, trace panel)
- Lines 1400+: JavaScript (manager objects)

### Adding New Form Fields
1. Add HTML input in appropriate step section
2. Add class `linked-input` for extraction support
3. Field automatically supports manual text extraction
4. Update `FormManager.collectFormData()` if special handling needed

### Customizing Export Format
Edit `ExportManager` methods:
- `exportJSON()` - Modify data structure
- `exportCSV()` - Change columns/format
- `exportAudit()` - Customize HTML template
- `exportAnnotatedPDF()` - Adjust annotation appearance

### Styling Customization
CSS variables in `:root` (lines 14-58):
```css
--primary-blue: #007bff;
--success-green: #4CAF50;
--warning-orange: #FF9800;
/* ...etc */
```

## Common Development Tasks

### Debugging PDF Rendering Issues
1. Open browser console (F12)
2. Check `AppStateManager.getState()` for current PDF state
3. Verify PDF.js loaded: `typeof pdfjsLib !== 'undefined'`
4. Check text layer: Inspect PDF overlay, verify opacity is 1.0

### Testing AI Features
Requires API key configured in Settings (⚙️ button):
1. Select AI provider (Gemini/Claude/GPT-4)
2. Enter API key
3. Save settings (stored in localStorage as Base64)
4. Click ✨ AI buttons to test extraction

### Troubleshooting Google Sheets Export
1. Verify OAuth 2.0 Client ID in Google Cloud Console
2. Check authorized origins: `http://localhost:8000`
3. Ensure Sheet ID is correct (from URL)
4. Verify sheet tabs: "Submissions" and "Extractions"
5. Check browser console for gapi errors

## File Structure

```
clinical_extraction_pdf_form/
├── Clinical_Study_Extraction.html       # Main application (single file)
├── Clinical_Study_Extraction_BACKUP.html # Original backup
├── README.md                             # User-facing documentation
├── FEATURE_SUMMARY.md                    # v2.0 features overview
├── IMPROVEMENTS.md                       # Phase 1-4 technical changelog
├── IMAGE_EXTRACTION_PLAN.md              # Image feature implementation plan
├── TEST_REPORT.md                        # Manual testing checklist (31 tests)
└── Kim2016.pdf                           # Test document (not in repo)
```

## Security Considerations

- **API keys** - Stored as Base64 in localStorage (not encrypted, client-side only)
- **User input sanitization** - All form inputs sanitized before rendering
- **CORS** - Designed for localhost; production requires proper CORS configuration
- **PDF.js worker** - Runs in sandboxed context
- **No server-side processing** - All operations client-side

## Known Limitations

1. **localStorage limit** - 5-10MB quota (may be exceeded with many image captures)
2. **Large PDFs** - Memory-intensive; 50+ page documents may be slow
3. **No OCR** - Scanned PDFs without text layer cannot be extracted
4. **Single session** - No multi-user collaboration features
5. **No undo/redo** - Manual clearing of extractions only

## Version History

- **v1.0** - Initial release with AI provider support
- **v2.0** (Current) - Added 4 extraction methods: text selection, region mode, annotations, image capture

## Performance Notes

- PDF rendering scales with `devicePixelRatio` (2x on Retina, 4x on 5K displays)
- Text layer rendering may be slow on very large pages
- Image captures use canvas cropping (fast for small regions)
- AI calls have network latency (2-10 seconds depending on provider)

## Backup & Recovery

### Restore Original Version
```bash
cp Clinical_Study_Extraction_BACKUP.html Clinical_Study_Extraction.html
```

### Clear All Data
```javascript
// In browser console
localStorage.clear();
location.reload();
```

## Future Enhancement Ideas (Not Implemented)

- Batch PDF processing
- OCR for scanned documents
- Keyboard shortcuts (Ctrl+C to extract)
- R/Python data export scripts
- Team collaboration features
- Custom extraction templates
- Advanced table detection algorithms
