# Integration Guide - Enhanced Document Generator

## Overview

This guide explains how to integrate and deploy the Enhanced Document Generator system with full Python backend support.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Web Interface  │───▶│   Document API   │───▶│ Python Backend  │
│ (HTML/CSS/JS)   │    │  (document_api.py)│   │ (canva.py/u.py) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
  User Interaction          API Bridge             Document Generation
  - Form Input              - JSON Processing      - PDF/PNG Creation
  - Progress Tracking       - Error Handling       - Security Features
  - Results Display         - File Management      - QR Codes/Watermarks
```

## Installation Steps

### 1. Python Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
# Test basic structure
python simple_test.py

# Test with simulation mode
python document_api.py --type teacher --simulate
python document_api.py --type student --simulate
```

### 3. Full Backend Setup (Production)

For production deployment with actual document generation:

```bash
# Install additional system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev libjpeg-dev libpng-dev libfreetype6-dev

# Or on macOS with Homebrew
brew install python3 jpeg libpng freetype

# Test full functionality
python test_generators.py
```

## Web Interface Integration

### Current Interface (index.html)
- Basic teacher payslip generation
- Client-side JavaScript processing
- Limited to web-based functionality

### Enhanced Interface (enhanced_interface.html)
- Professional UI with document type selection
- Progress tracking and status indicators
- Security feature highlights
- API integration ready

### Integration Options

#### Option 1: Client-Side Only (Current)
```html
<!-- Use existing index.html -->
<script src="faker.js"></script>
<!-- JavaScript-only generation -->
```

#### Option 2: Hybrid Mode (Recommended)
```html
<!-- Use enhanced_interface.html -->
<script>
// Call Python API for generation
async function generateDocuments(data) {
    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return await response.json();
}
</script>
```

#### Option 3: Full Backend Integration
```python
# Flask/FastAPI server integration
from flask import Flask, request, jsonify
from canva import EnhancedTeacherDocumentGenerator
from u import EnhancedStudentDocumentGenerator

app = Flask(__name__)

@app.route('/api/generate/teacher', methods=['POST'])
def generate_teacher():
    data = request.json
    generator = EnhancedTeacherDocumentGenerator()
    # Process and return results
```

## API Endpoints

### Document Generation API

```python
# Command Line Usage
python document_api.py --type teacher --country India --data '{"teacher_data": {...}}'

# Programmatic Usage
from document_api import generate_teacher_documents, generate_student_documents

# Generate teacher documents
result = generate_teacher_documents(json.dumps({
    "teacher_data": {
        "employee_id": "TID-IN-2024-1001",
        "name": "Dr. Priya Sharma",
        "department": "Mathematics",
        "position": "Senior Teacher",
        "validity": "2025-12-31"
    },
    "salary_data": {
        "basic_salary": 75000,
        "pay_period": "2024-03",
        "pay_date": "2024-03-28"
    },
    "country": "India"
}))
```

### Response Format

```json
{
  "success": true,
  "results": {
    "id_card": "output/teacher_id_TID-IN-2024-1001.png",
    "salary_slip": "output/salary_slip_TID-IN-2024-1001_2024-03.pdf",
    "verification_hash": "abc123def456",
    "security_features": {
      "qr_code": true,
      "watermark": true,
      "barcode": true,
      "digital_signature": true
    }
  }
}
```

## Security Features Implementation

### QR Code Generation
```python
# QR codes contain verification data
qr_data = {
    'id': employee_id,
    'name': name,
    'institution': school_code,
    'valid_until': validity_date,
    'verification_hash': hash_value
}
```

### Document Authentication
- **Watermarks**: Layered security patterns
- **Barcodes**: Unique identification codes
- **Digital Signatures**: Hash-based verification
- **Holographic Elements**: Security strips for IDs

### Country-Specific Compliance
- **India**: PF, ESI, Professional Tax calculations
- **USA**: Federal tax, Social Security, Medicare
- **UK**: PAYE, National Insurance, pension contributions

## Deployment Options

### Development Server
```bash
# Simple HTTP server for testing
python -m http.server 8080

# Access at: http://localhost:8080/enhanced_interface.html
```

### Production Deployment

#### Option 1: Flask/Gunicorn
```python
# app.py
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('enhanced_interface.html')

@app.route('/api/generate/<doc_type>', methods=['POST'])
def generate_document(doc_type):
    # Implementation here
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

#### Option 2: FastAPI
```python
# main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class DocumentRequest(BaseModel):
    type: str
    data: dict
    country: str = "India"

@app.post("/api/generate")
async def generate_document(request: DocumentRequest):
    # Implementation here
    pass
```

#### Option 3: Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["python", "-m", "http.server", "8080"]
```

## File Management

### Output Directory Structure
```
output/
├── teacher_documents/
│   ├── id_cards/
│   │   └── teacher_id_TID-IN-2024-1001.png
│   └── salary_slips/
│       └── salary_slip_TID-IN-2024-1001_2024-03.pdf
└── student_documents/
    ├── id_cards/
    │   └── student_id_SID-IN-2024-2001.png
    ├── transcripts/
    │   └── transcript_SID-IN-2024-2001.pdf
    └── certificates/
        └── enrollment_cert_SID-IN-2024-2001.pdf
```

### Cleanup and Maintenance
```python
# Automated cleanup script
import os
import time
from datetime import datetime, timedelta

def cleanup_old_files(directory, days_old=7):
    cutoff = time.time() - (days_old * 24 * 60 * 60)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getctime(file_path) < cutoff:
                os.remove(file_path)
```

## Testing and Validation

### Unit Tests
```python
# test_document_generation.py
import unittest
from canva import EnhancedTeacherDocumentGenerator
from u import EnhancedStudentDocumentGenerator

class TestDocumentGeneration(unittest.TestCase):
    def test_teacher_id_generation(self):
        generator = EnhancedTeacherDocumentGenerator()
        # Test implementation
        
    def test_student_transcript_generation(self):
        generator = EnhancedStudentDocumentGenerator()
        # Test implementation
```

### Integration Tests
```bash
# Run comprehensive tests
python test_generators.py

# API tests
python -m pytest tests/ -v
```

## Performance Optimization

### Concurrent Processing
```python
# Batch processing for multiple documents
import concurrent.futures

def generate_batch_documents(document_list):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(generate_document, doc) for doc in document_list]
        results = [future.result() for future in futures]
    return results
```

### Memory Management
```python
# Optimize for large batches
import gc

def generate_large_batch(documents):
    results = []
    for i, doc in enumerate(documents):
        result = generate_document(doc)
        results.append(result)
        
        # Clean up memory every 10 documents
        if i % 10 == 0:
            gc.collect()
    
    return results
```

## Security Considerations

### Input Validation
```python
def validate_input_data(data):
    required_fields = ['name', 'id', 'country']
    for field in required_fields:
        if field not in data or not data[field]:
            raise ValueError(f"Missing required field: {field}")
    
    # Additional validation logic
```

### File Security
```python
# Secure file handling
import os
import tempfile

def secure_file_generation(data):
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate files in temporary directory
        output_path = generate_document(data, output_dir=temp_dir)
        
        # Validate and move to final location
        if validate_document(output_path):
            final_path = move_to_secure_location(output_path)
            return final_path
        else:
            raise SecurityError("Document validation failed")
```

## Support and Maintenance

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('document_generator.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring and Alerts
```python
# Basic monitoring
def monitor_system_health():
    disk_usage = check_disk_usage('output/')
    memory_usage = check_memory_usage()
    
    if disk_usage > 90:
        send_alert("High disk usage detected")
    
    if memory_usage > 80:
        send_alert("High memory usage detected")
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Font Issues**
   ```python
   # Install system fonts
   sudo apt-get install fonts-liberation
   ```

3. **Permission Issues**
   ```bash
   # Fix output directory permissions
   chmod 755 output/
   mkdir -p output/
   ```

4. **Memory Issues**
   ```python
   # Reduce image resolution for large batches
   img.save(path, quality=85, optimize=True)
   ```

This integration guide provides comprehensive instructions for deploying the Enhanced Document Generator in various environments, from development to production.