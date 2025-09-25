# Web Interface Integration Guide for NWN GFF API Service

## Overview

This guide explains how a webpage can interact with the NWN GFF API service to provide file conversion functionality. The included `web_interface.html` demonstrates a complete implementation.

## How the Webpage Interacts with the API Service

### 1. API Endpoints Used

The web interface connects to these API endpoints:

- **Health Check**: `GET /api/v1/health` - Verifies the service is running
- **GFF to JSON**: `POST /api/v1/convert/gff-to-json` - Converts GFF files to JSON
- **JSON to GFF**: `POST /api/v1/convert/json-to-gff` - Converts JSON files to GFF

### 2. JavaScript Integration Pattern

```javascript
// Example: Converting GFF to JSON
async function convertGffToJson() {
    const fileInput = document.getElementById('gffFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showError('Please select a file');
        return;
    }
    
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('http://localhost:8000/api/v1/convert/gff-to-json', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const jsonData = await response.json();
            // Handle the converted JSON data
            downloadJsonFile(jsonData, file.name);
        } else {
            const error = await response.json();
            showError(error.detail || 'Conversion failed');
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    }
}
```

### 3. Button Click Handler Implementation

```html
<!-- HTML Button -->
<button id="convertGffToJson" class="convert-btn" onclick="convertGffToJson()">
    Convert to JSON
</button>

<!-- JavaScript Handler -->
async function convertGffToJson() {
    // Disable button during conversion
    const button = document.getElementById('convertGffToJson');
    button.disabled = true;
    
    try {
        // Conversion logic here
        await performConversion();
        
        // Show success message and download link
        showSuccess('Conversion successful!');
        createDownloadLink(convertedData);
        
    } catch (error) {
        showError(`Conversion failed: ${error.message}`);
    } finally {
        // Re-enable button
        button.disabled = false;
    }
}
```

## File Upload and Download Process

### File Upload (GFF → JSON)
1. **User selects file** via `<input type="file">`
2. **JavaScript validates** file type and size (max 10MB)
3. **FormData object** created with file
4. **POST request** sent to API endpoint
5. **Response handling** - JSON data received
6. **Download link** created for converted file

### File Download (JSON → GFF)
1. **User selects JSON file**
2. **FormData upload** to API endpoint
3. **Binary response** received (application/octet-stream)
4. **Blob object** created from response
5. **Download link** generated with proper filename
6. **User downloads** converted GFF file

## CORS Configuration

The API service already has CORS enabled for all origins:

```python
# From app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This means your web interface can run from:
- `file://` (local HTML file)
- `http://localhost:3000` (local dev server)
- `https://yourdomain.com` (production website)
- Any other origin

## Error Handling and User Feedback

### API Error Responses
```javascript
// Handle different error scenarios
if (response.status === 413) {
    showError('File too large. Maximum size is 10MB.');
} else if (response.status === 400) {
    const error = await response.json();
    showError(`Invalid file: ${error.detail}`);
} else if (response.status === 500) {
    showError('Server error. Please try again later.');
} else {
    showError(`Unexpected error: ${response.statusText}`);
}
```

### Network Error Handling
```javascript
try {
    const response = await fetch(apiUrl, options);
    // Handle response...
} catch (error) {
    if (error.name === 'TypeError' && error.message.includes('fetch')) {
        showError('Cannot connect to API service. Make sure it\'s running on http://localhost:8000');
    } else {
        showError(`Network error: ${error.message}`);
    }
}
```

## User Experience Features

### 1. File Selection Feedback
```javascript
function updateFileInfo(input, infoElementId) {
    const file = input.files[0];
    const infoElement = document.getElementById(infoElementId);
    
    if (file) {
        const fileSize = (file.size / 1024).toFixed(2);
        infoElement.textContent = `Selected: ${file.name} (${fileSize} KB)`;
    } else {
        infoElement.textContent = '';
    }
}
```

### 2. Loading States
```javascript
// Show loading spinner
statusElement.innerHTML = '<div class="loading"></div>Converting file...';

// Hide loading and show result
statusElement.innerHTML = 'Conversion successful!';
```

### 3. Progress Indication
```javascript
button.disabled = true;  // Disable during operation
button.disabled = false; // Re-enable when complete
```

## Complete Workflow Example

### GFF to JSON Conversion Workflow:
1. **User clicks "Convert to JSON" button**
2. **JavaScript validates file selection**
3. **File size check** (must be ≤ 10MB)
4. **FormData creation** with selected file
5. **API request** with proper headers
6. **Response processing** - success or error
7. **Result display** - JSON data or error message
8. **Download link creation** for converted file
9. **Button re-enabling** for next conversion

### JSON to GFF Conversion Workflow:
1. **User selects JSON file**
2. **File validation** (type and size)
3. **Binary API request** with FormData
4. **Binary response handling**
5. **Blob object creation** from response
6. **Download link generation** with proper filename
7. **User downloads** converted GFF file

## Testing the Web Interface

1. **Start the API service**:
   ```bash
   python main.py
   ```

2. **Open the web interface**:
   - Save the `web_interface.html` file
   - Open it in a web browser (works from `file://` due to CORS)

3. **Test the functionality**:
   - Click "Check API Health" to verify connection
   - Select a GFF file and convert to JSON
   - Select a JSON file and convert to GFF
   - Test error conditions (no file, large file, etc.)

## Security Considerations

### Client-Side Validation
- File type validation (accept attribute)
- File size validation (10MB limit)
- Input sanitization (FormData handles this)

### Server-Side Protection
- API validates file types server-side
- File size limits enforced
- No authentication required (for this version)
- CORS properly configured

This web interface provides a complete, user-friendly way to interact with the NWN GFF API service for file format conversions.