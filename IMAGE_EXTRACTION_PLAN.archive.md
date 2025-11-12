# Image Extraction Feature - Implementation Plan

## 🎯 Overview
Add ability to capture visual regions from PDF as images (PNG/JPEG) for extracting figures, graphs, tables, and diagrams.

## ✨ Features to Implement

### 1. Image Capture Mode Toggle
- **Button:** "📷 Image" in PDF toolbar
- **Behavior:** Similar to Region mode, but captures visual content instead of text
- **Visual:** Orange button when active, crosshair cursor
- **Status Message:** "📷 Image mode: Draw a box to capture an image"

### 2. Selection & Capture
- **Draw Box:** User draws rectangle around desired area
- **Preview:** Show dashed box during selection (blue border)
- **Capture:** On mouse up, capture canvas region to image
- **Minimum Size:** 50x50px (prevent accidental clicks)

### 3. Image Processing
- **Canvas Export:** Use `canvas.toDataURL()` for high-quality capture
- **Formats:** PNG (lossless) and JPEG (compressed)
- **Quality Options:** 
  - Low: 0.5 quality, ~50KB
  - Medium: 0.8 quality, ~150KB
  - High: 1.0 quality, ~500KB
- **Resolution:** Respect `devicePixelRatio` for high-DPI displays

### 4. Image Storage & Linking
- **Storage:** Base64 data URL or Blob
- **Link to Field:** Associate image with active form field
- **Metadata:** Page number, coordinates, timestamp, field name
- **Extraction Record:** Store in ExtractionTracker with method: 'image'

### 5. Thumbnail Display
- **Location:** Trace log panel
- **Size:** 80x80px thumbnail
- **Click:** Open full-size image in new tab
- **Hover:** Show image preview tooltip
- **Icon:** 🖼️ prefix for image entries

### 6. Export Options
- **Download Individual:** Click thumbnail to download
- **Batch Export:** Export all images as ZIP
- **Include in Audit:** Embed images in audit report
- **Clipboard Copy:** Copy image to clipboard (Ctrl+C)

## 🔧 Technical Implementation

### HTML Changes
```html
<!-- Add to toolbar -->
<button id="image-mode-btn" class="selection-mode-toggle" onclick="toggleImageMode()" 
        title="Toggle Image Capture Mode">📷 Image</button>

<!-- Add quality selector modal -->
<div id="image-quality-modal" class="settings-modal">
    <div class="settings-content" style="max-width: 400px;">
        <h2>📷 Export Image</h2>
        <label>Format:</label>
        <select id="image-format">
            <option value="png">PNG (Lossless)</option>
            <option value="jpeg">JPEG (Compressed)</option>
        </select>
        <label>Quality:</label>
        <select id="image-quality">
            <option value="0.5">Low (~50KB)</option>
            <option value="0.8" selected>Medium (~150KB)</option>
            <option value="1.0">High (~500KB)</option>
        </select>
        <div class="settings-actions">
            <button onclick="cancelImageExport()">Cancel</button>
            <button onclick="confirmImageExport()">Download</button>
        </div>
    </div>
</div>
```

### CSS Changes
```css
/* Image capture mode */
.image-selection-box {
    position: absolute;
    border: 2px dashed #2196F3;
    background: rgba(33, 150, 243, 0.1);
    pointer-events: none;
    z-index: 1000;
}

/* Image thumbnails in trace log */
.trace-entry .image-thumbnail {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 8px;
    border: 2px solid #2196F3;
}

.trace-entry .image-thumbnail:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
```

### JavaScript Implementation
```javascript
const ImageExtractionManager = {
    mode: false,
    startPoint: null,
    currentBox: null,
    capturedRegion: null,
    
    enable() {
        this.mode = true;
        const btn = document.getElementById('image-mode-btn');
        btn?.classList.add('active');
        // ... setup event listeners (similar to RegionSelectionManager)
        StatusManager.show('📷 Image mode: Draw a box to capture an image', 'info', 5000);
    },
    
    disable() {
        this.mode = false;
        // ... cleanup
    },
    
    async captureRegion(region, pageNum) {
        const state = AppStateManager.getState();
        const page = await state.pdfDoc.getPage(pageNum);
        const viewport = page.getViewport({ scale: state.scale });
        
        // Create temporary canvas for capture
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size to match region
        const dpr = window.devicePixelRatio || 1;
        canvas.width = region.width * dpr;
        canvas.height = region.height * dpr;
        canvas.style.width = region.width + 'px';
        canvas.style.height = region.height + 'px';
        
        // Render full page to temp canvas
        const tempCanvas = document.createElement('canvas');
        const tempCtx = tempCanvas.getContext('2d');
        tempCanvas.width = viewport.width * dpr;
        tempCanvas.height = viewport.height * dpr;
        
        await page.render({
            canvasContext: tempCtx,
            viewport: viewport,
            transform: [dpr, 0, 0, dpr, 0, 0]
        }).promise;
        
        // Crop to selected region
        ctx.drawImage(
            tempCanvas,
            region.x * dpr, region.y * dpr, region.width * dpr, region.height * dpr,
            0, 0, region.width * dpr, region.height * dpr
        );
        
        return canvas;
    },
    
    async exportImage(canvas, format, quality) {
        const mimeType = format === 'png' ? 'image/png' : 'image/jpeg';
        const dataUrl = canvas.toDataURL(mimeType, quality);
        
        // Download
        const a = document.createElement('a');
        a.href = dataUrl;
        a.download = `extracted_image_${Date.now()}.${format}`;
        a.click();
        
        return dataUrl; // Return for storage
    },
    
    createImageRecord(fieldName, dataUrl, pageNum, coords) {
        const extraction = ExtractionTracker.addExtraction({
            fieldName: fieldName,
            text: '[Image]',
            page: pageNum,
            coordinates: coords,
            method: 'image',
            imageData: dataUrl.substring(0, 100) + '...', // Store truncated for size
            imageUrl: dataUrl, // Store full for display
            documentName: AppStateManager.getState().documentName
        });
        
        return extraction;
    }
};
```

## 🎨 User Workflow

1. Click **📷 Image** button in toolbar
2. Button turns orange, cursor becomes crosshair
3. Click and drag to select image region
4. Blue dashed box shows selection
5. On mouse release:
   - Quality modal appears
   - Select format (PNG/JPEG) and quality
   - Click "Download"
6. Image downloads to computer
7. Thumbnail appears in trace log
8. Click thumbnail to view full-size

## 📊 Use Cases

### Medical Research Papers:
- **Figures:** Extract survival curves, forest plots
- **Tables:** Capture complex tables as images
- **Diagrams:** Save anatomical illustrations
- **Scans:** Extract CT/MRI images from papers
- **Graphs:** Capture bar charts, scatter plots

### Benefits:
- No need to manually screenshot
- Maintains quality with high-DPI support
- Linked to extraction workflow
- Full traceability (page, coords, timestamp)

## 🚀 Implementation Time
**Estimated:** 30-45 minutes  
**Complexity:** Medium  
**Lines of Code:** ~200 lines  

## ❓ Open Questions

1. **Storage:** Store images as Base64 in extraction records? (May increase file size)
2. **Export:** Include images in PDF export? JSON export?
3. **Thumbnail Size:** 80x80px or larger (100x100px)?
4. **Quality Default:** Medium (0.8) or High (1.0)?
5. **Clipboard:** Also copy to clipboard automatically?

## 📝 Decision Needed

**Should I implement this feature now?**
- [ ] Yes, implement full image extraction
- [ ] Yes, but simplified version (PNG only, no quality options)
- [ ] No, not needed right now
- [ ] Let me test current features first

---

**Status:** 📋 Plan Ready - Awaiting User Decision  
**Estimated Time:** 30-45 minutes for full implementation  
**Alternative:** Can implement simplified version in 15 minutes
