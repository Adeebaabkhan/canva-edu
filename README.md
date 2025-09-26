# Enhanced Realistic Document Generator

A comprehensive document generation system that creates authentic-looking educational documents with advanced security features and verification systems.

## Features

### 🎓 Teacher Document Generation (`canva.py`)
- **Realistic Salary Slips**: Country-specific tax calculations, authentic formatting
- **Teacher ID Cards**: Professional design with security features
- **Multi-Country Support**: India, USA, UK with localized compliance
- **Security Features**: QR codes, barcodes, watermarks, verification hashes
- **Authentic Details**: Real government codes, banking formats, institutional branding

### 📚 Student Document Generation (`u.py`)
- **Student ID Cards**: University-branded with security strips
- **Academic Transcripts**: Realistic grade systems, course codes, GPA calculations
- **Enrollment Certificates**: Official verification documents
- **Multi-University Support**: Comprehensive database of real institutions
- **Academic Authenticity**: Proper semester systems, credit calculations, grading scales

## Key Enhancements

### 🔒 Security & Verification
- **QR Code Verification**: Embedded verification data with hash validation
- **Security Watermarks**: Multi-layer authentication patterns
- **Document Hashing**: Unique verification codes for each document
- **Holographic Elements**: Security strips and patterns
- **Digital Signatures**: Authentic signature sections

### 🌍 Country-Specific Compliance
- **Tax Calculations**: Accurate tax rates and deductions per country
- **Government Codes**: Real registration numbers and institutional codes
- **Banking Details**: Authentic account and routing number formats
- **Regulatory Compliance**: Country-specific educational standards

### 🎨 Professional Design
- **Institutional Branding**: Realistic logos and letterheads
- **Typography**: Professional fonts and layouts
- **Color Schemes**: University/school-specific color themes
- **Layout Standards**: Industry-compliant document formats

## Installation

1. **Install Python Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Required Dependencies**:
- PIL/Pillow (Image processing)
- ReportLab (PDF generation)
- QRCode (QR code generation)
- Faker (Realistic data generation)
- NumPy (Mathematical operations)
- OpenCV (Image processing)
- Matplotlib (Graphics)

## Usage

### Teacher Documents

```python
from canva import EnhancedTeacherDocumentGenerator

generator = EnhancedTeacherDocumentGenerator()

# Teacher data
teacher_data = {
    'employee_id': 'TID-IN-2024-1001',
    'name': 'Dr. Priya Sharma',
    'department': 'Mathematics',
    'position': 'Senior Mathematics Teacher',
    'validity': '2025-03-31'
}

# Salary data
salary_data = {
    'basic_salary': 75000,
    'pay_period': '2024-03',
    'pay_date': '2024-03-28'
}

# Generate documents
id_card = generator.generate_teacher_id_card(teacher_data, 'India')
salary_slip = generator.generate_salary_slip(teacher_data, salary_data, 'India')
```

### Student Documents

```python
from u import EnhancedStudentDocumentGenerator

generator = EnhancedStudentDocumentGenerator()

# Student data
student_data = {
    'student_id': 'SID-IN-2024-2001',
    'name': 'Arjun Patel',
    'program': 'Bachelor of Technology in Computer Science',
    'academic_year': '2023-24',
    'validity': '2025-12-31'
}

# Generate documents
id_card = generator.generate_student_id_card(student_data, 'India')
transcript = generator.generate_transcript(student_data, academic_data, 'India')
enrollment_cert = generator.generate_enrollment_certificate(student_data, 'India')
```

### Testing

Run the test script to generate sample documents:

```bash
python test_generators.py
```

## Document Types

### Teacher Documents
1. **Salary Slips** (PDF)
   - Complete earnings breakdown
   - Tax calculations
   - Deductions (PF, ESI, Professional Tax)
   - Net pay calculations
   - Digital verification

2. **Teacher ID Cards** (PNG)
   - Professional photo area
   - School branding
   - Security features
   - QR code verification
   - Barcode identification

### Student Documents
1. **Student ID Cards** (PNG)
   - University branding
   - Student photo area
   - Academic information
   - Security strips
   - QR code verification

2. **Academic Transcripts** (PDF)
   - Complete course history
   - Grade calculations
   - GPA/CGPA computation
   - Grading scale reference
   - Official verification

3. **Enrollment Certificates** (PDF)
   - Official letterhead
   - Enrollment verification
   - Academic status
   - Registrar signatures
   - Verification codes

## Security Features

### 🔐 Multi-Layer Authentication
- **QR Codes**: Embedded verification data with hash validation
- **Barcodes**: Unique identification numbers
- **Watermarks**: Security patterns and institutional marks
- **Digital Hashes**: Document integrity verification
- **Security Strips**: Holographic-style authentication elements

### 📋 Compliance Standards
- **Government Regulations**: Adheres to educational authority standards
- **Institutional Formats**: Matches real document templates
- **Verification Systems**: Compatible with standard verification processes
- **Quality Standards**: High-resolution output for professional use

## Output Directory Structure

```
output/
├── teacher_id_TID-IN-2024-1001.png
├── salary_slip_TID-IN-2024-1001_2024-03.pdf
├── student_id_SID-IN-2024-2001.png
├── transcript_SID-IN-2024-2001.pdf
└── enrollment_cert_SID-IN-2024-2001.pdf
```

## Supported Countries

- **India**: Complete tax structure, PF/ESI, government codes
- **USA**: Federal/state taxes, Social Security, realistic formats
- **UK**: PAYE tax system, National Insurance, proper compliance

## Configuration

Each country has specific configurations for:
- Tax rates and calculation methods
- Government registration formats
- Banking system standards
- Educational authority requirements
- Document layout standards

## Legal Notice

This software is designed for educational and testing purposes. Users are responsible for ensuring compliance with local laws and regulations. The generated documents are for simulation and verification testing only.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add enhancements or new country support
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, feature requests, or questions:
- Create an issue in the repository
- Check the documentation
- Review the test examples

---

**Note**: This system generates realistic-looking documents for testing and educational purposes. Ensure compliance with local laws and institutional policies when using this software.