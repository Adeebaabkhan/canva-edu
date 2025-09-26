#!/usr/bin/env python3
"""
Enhanced Realistic Teacher Salary Slip and ID Card Generator
This module generates authentic-looking teacher documents with enhanced security features.
"""

import os
import sys
import random
import json
import qrcode
import logging
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from faker import Faker
import concurrent.futures
import threading
from typing import Dict, List, Optional, Tuple
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedTeacherDocumentGenerator:
    """Enhanced generator for realistic teacher salary slips and ID cards"""
    
    def __init__(self):
        self.fake = Faker()
        self.country_configs = self._load_country_configs()
        self.schools_database = self._load_schools_database()
        self.security_features = SecurityFeatures()
        
    def _load_country_configs(self) -> Dict:
        """Load country-specific configurations for realistic document generation"""
        return {
            'India': {
                'currency': '₹',
                'currency_code': 'INR',
                'tax_rate': 0.10,
                'pf_rate': 0.12,
                'esi_rate': 0.0175,
                'professional_tax': 200,
                'locale': 'hi_IN',
                'govt_codes': {
                    'education_dept': 'ED/GOI/',
                    'school_code_prefix': 'DL',
                    'teacher_id_prefix': 'TID-IN',
                    'payroll_code': 'PR-EDU-IN'
                },
                'compliance': {
                    'epf_number_format': 'DL/12345/0001234/000/0000001',
                    'pan_format': 'ABCDE1234F',
                    'aadhaar_format': '1234 5678 9012',
                    'uan_format': '123456789012'
                },
                'banking': {
                    'ifsc_codes': ['SBIN0000001', 'HDFC0000001', 'ICIC0000001', 'AXIS0000001'],
                    'account_format': '1234567890123456'
                }
            },
            'USA': {
                'currency': '$',
                'currency_code': 'USD',
                'tax_rate': 0.22,
                'social_security_rate': 0.062,
                'medicare_rate': 0.0145,
                'state_tax_rate': 0.08,
                'locale': 'en_US',
                'govt_codes': {
                    'education_dept': 'DOE/US/',
                    'school_code_prefix': 'US',
                    'teacher_id_prefix': 'TID-US',
                    'payroll_code': 'PR-EDU-US'
                },
                'compliance': {
                    'ssn_format': '123-45-6789',
                    'ein_format': '12-3456789',
                    'teaching_license': 'TL-123456789'
                },
                'banking': {
                    'routing_numbers': ['021000021', '026009593', '011401533', '053000196'],
                    'account_format': '1234567890'
                }
            },
            'UK': {
                'currency': '£',
                'currency_code': 'GBP',
                'tax_rate': 0.20,
                'national_insurance_rate': 0.12,
                'pension_rate': 0.095,
                'locale': 'en_GB',
                'govt_codes': {
                    'education_dept': 'DFE/UK/',
                    'school_code_prefix': 'UK',
                    'teacher_id_prefix': 'TID-UK',
                    'payroll_code': 'PR-EDU-UK'
                },
                'compliance': {
                    'ni_number_format': 'AB123456C',
                    'teacher_ref_number': 'TRN1234567',
                    'utr_format': '1234567890'
                },
                'banking': {
                    'sort_codes': ['12-34-56', '65-43-21', '11-22-33', '99-88-77'],
                    'account_format': '12345678'
                }
            }
        }
    
    def _load_schools_database(self) -> Dict:
        """Load comprehensive school database with realistic information"""
        return {
            "India": [
                {
                    "name": "Delhi Public School",
                    "location": "R.K. Puram, New Delhi",
                    "code": "DPS-RKP-001",
                    "principal": "Dr. Vandana Shiva",
                    "phone": "+91-11-26185741",
                    "email": "principal@dpsrkp.net",
                    "address": "Sector 12, R.K. Puram, New Delhi - 110022",
                    "established": "1972",
                    "board": "CBSE",
                    "logo_path": "logos/dps_logo.png"
                },
                {
                    "name": "The Doon School",
                    "location": "Dehradun, Uttarakhand",
                    "code": "TDS-DHN-001",
                    "principal": "Dr. Matthew Raggett",
                    "phone": "+91-135-2526400",
                    "email": "headmaster@doonschool.com",
                    "address": "The Mall, Dehradun - 248001",
                    "established": "1935",
                    "board": "ICSE",
                    "logo_path": "logos/doon_logo.png"
                }
            ],
            "USA": [
                {
                    "name": "Lincoln Elementary School",
                    "location": "New York, NY",
                    "code": "LES-NY-001",
                    "principal": "Dr. Sarah Johnson",
                    "phone": "+1-212-555-0123",
                    "email": "principal@lincolnelem.nyc.gov",
                    "address": "123 Education Ave, New York, NY 10001",
                    "established": "1965",
                    "district": "NYC Department of Education",
                    "logo_path": "logos/lincoln_logo.png"
                }
            ],
            "UK": [
                {
                    "name": "Hillcrest Primary School",
                    "location": "London, England",
                    "code": "HPS-LDN-001",
                    "principal": "Ms. Emma Thompson",
                    "phone": "+44-20-7946-0958",
                    "email": "head@hillcrest.sch.uk",
                    "address": "45 Education Road, London SW1A 1AA",
                    "established": "1892",
                    "local_authority": "Westminster City Council",
                    "logo_path": "logos/hillcrest_logo.png"
                }
            ]
        }
    
    def generate_teacher_id_card(self, teacher_data: Dict, country: str = 'India') -> str:
        """Generate a realistic teacher ID card with security features"""
        try:
            config = self.country_configs[country]
            school = random.choice(self.schools_database[country])
            
            # Create ID card image
            card_width, card_height = 856, 540  # Standard ID card size in pixels
            img = Image.new('RGB', (card_width, card_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Add background gradient
            self._add_gradient_background(img, draw)
            
            # Add school logo area
            logo_area = (50, 30, 200, 100)
            self._add_logo_placeholder(draw, logo_area, school['name'][:3])
            
            # Add school information
            school_info_y = 30
            draw.text((220, school_info_y), school['name'], fill='navy', 
                     font=self._get_font(24, bold=True))
            draw.text((220, school_info_y + 30), f"Est. {school['established']}", 
                     fill='gray', font=self._get_font(12))
            draw.text((220, school_info_y + 45), school['location'], 
                     fill='gray', font=self._get_font(12))
            
            # Add teacher photo placeholder
            photo_area = (50, 130, 200, 280)
            self._add_photo_placeholder(draw, photo_area, teacher_data.get('photo_path'))
            
            # Add teacher information
            info_x, info_y = 220, 130
            draw.text((info_x, info_y), f"ID: {teacher_data['employee_id']}", 
                     fill='black', font=self._get_font(14, bold=True))
            draw.text((info_x, info_y + 25), teacher_data['name'], 
                     fill='black', font=self._get_font(18, bold=True))
            draw.text((info_x, info_y + 50), f"Dept: {teacher_data['department']}", 
                     fill='black', font=self._get_font(12))
            draw.text((info_x, info_y + 70), f"Designation: {teacher_data['position']}", 
                     fill='black', font=self._get_font(12))
            draw.text((info_x, info_y + 90), f"Valid Until: {teacher_data['validity']}", 
                     fill='red', font=self._get_font(12))
            
            # Add security features
            self._add_security_watermark(draw, card_width, card_height)
            
            # Add QR code
            qr_data = {
                'id': teacher_data['employee_id'],
                'name': teacher_data['name'],
                'school': school['code'],
                'valid_until': teacher_data['validity'],
                'verification_hash': self._generate_verification_hash(teacher_data)
            }
            qr_img = self._generate_qr_code(json.dumps(qr_data))
            qr_img = qr_img.resize((120, 120))
            img.paste(qr_img, (700, 380))
            
            # Add barcode
            barcode = self._generate_barcode(teacher_data['employee_id'])
            img.paste(barcode, (50, 450))
            
            # Save ID card
            output_path = f"output/teacher_id_{teacher_data['employee_id']}.png"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, quality=95, dpi=(300, 300))
            
            logger.info(f"Teacher ID card generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating teacher ID card: {str(e)}")
            raise
    
    def generate_salary_slip(self, teacher_data: Dict, salary_data: Dict, 
                           country: str = 'India') -> str:
        """Generate enhanced realistic salary slip with security features"""
        try:
            config = self.country_configs[country]
            school = random.choice(self.schools_database[country])
            
            # Create PDF document
            output_path = f"output/salary_slip_{teacher_data['employee_id']}_{salary_data['pay_period']}.pdf"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Add watermark
            self._add_pdf_watermark(doc)
            
            # Header with school information
            header_style = ParagraphStyle(
                'CustomHeader',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.darkblue,
                alignment=TA_CENTER,
                spaceAfter=12
            )
            
            story.append(Paragraph(school['name'].upper(), header_style))
            story.append(Paragraph(f"Salary Slip - {salary_data['pay_period']}", 
                                 styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Employee information table
            emp_data = [
                ['Employee Name:', teacher_data['name'], 'Employee ID:', teacher_data['employee_id']],
                ['Designation:', teacher_data['position'], 'Department:', teacher_data['department']],
                ['PAN No:', config['compliance'].get('pan_format', 'N/A'), 
                 'Bank A/C:', self._generate_account_number(config)],
                ['Pay Period:', salary_data['pay_period'], 'Pay Date:', salary_data['pay_date']]
            ]
            
            emp_table = Table(emp_data, colWidths=[2*inch, 2*inch, 1.5*inch, 2*inch])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(emp_table)
            story.append(Spacer(1, 20))
            
            # Salary breakdown table
            salary_breakdown = self._calculate_realistic_salary(salary_data, config)
            
            salary_table_data = [['Description', 'Amount (' + config['currency'] + ')']]
            
            # Earnings
            salary_table_data.append(['EARNINGS', ''])
            for item, amount in salary_breakdown['earnings'].items():
                salary_table_data.append([item, f"{config['currency']}{amount:,.2f}"])
            
            salary_table_data.append(['Total Earnings', f"{config['currency']}{salary_breakdown['total_earnings']:,.2f}"])
            salary_table_data.append(['', ''])
            
            # Deductions
            salary_table_data.append(['DEDUCTIONS', ''])
            for item, amount in salary_breakdown['deductions'].items():
                salary_table_data.append([item, f"{config['currency']}{amount:,.2f}"])
            
            salary_table_data.append(['Total Deductions', f"{config['currency']}{salary_breakdown['total_deductions']:,.2f}"])
            salary_table_data.append(['', ''])
            salary_table_data.append(['NET PAY', f"{config['currency']}{salary_breakdown['net_pay']:,.2f}"])
            
            salary_table = Table(salary_table_data, colWidths=[4*inch, 2*inch])
            salary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(salary_table)
            story.append(Spacer(1, 30))
            
            # Add digital signature and verification
            self._add_digital_signature_section(story, styles, school, teacher_data)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Salary slip generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating salary slip: {str(e)}")
            raise
    
    def _calculate_realistic_salary(self, salary_data: Dict, config: Dict) -> Dict:
        """Calculate realistic salary with proper tax calculations"""
        basic_salary = float(salary_data.get('basic_salary', 50000))
        
        # Calculate allowances
        hra = basic_salary * 0.40  # 40% HRA
        da = basic_salary * 0.25   # 25% DA
        transport = 2000           # Fixed transport allowance
        medical = 1500            # Fixed medical allowance
        
        total_earnings = basic_salary + hra + da + transport + medical
        
        # Calculate deductions
        tax = total_earnings * config['tax_rate']
        pf = basic_salary * config.get('pf_rate', 0.12)
        esi = total_earnings * config.get('esi_rate', 0.0175) if total_earnings <= 21000 else 0
        professional_tax = config.get('professional_tax', 200)
        
        total_deductions = tax + pf + esi + professional_tax
        net_pay = total_earnings - total_deductions
        
        return {
            'earnings': {
                'Basic Salary': basic_salary,
                'House Rent Allowance': hra,
                'Dearness Allowance': da,
                'Transport Allowance': transport,
                'Medical Allowance': medical
            },
            'deductions': {
                'Income Tax': tax,
                'Provident Fund': pf,
                'ESI': esi,
                'Professional Tax': professional_tax
            },
            'total_earnings': total_earnings,
            'total_deductions': total_deductions,
            'net_pay': net_pay
        }
    
    def _generate_verification_hash(self, data: Dict) -> str:
        """Generate verification hash for security"""
        hash_input = f"{data['employee_id']}{data['name']}{datetime.now().strftime('%Y%m%d')}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _generate_qr_code(self, data: str) -> Image.Image:
        """Generate QR code for verification"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    def _generate_barcode(self, data: str) -> Image.Image:
        """Generate barcode for the ID"""
        # Simple barcode simulation
        img = Image.new('RGB', (300, 50), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw simple barcode pattern
        x = 10
        for i, char in enumerate(data):
            if i % 2 == 0:
                draw.rectangle([x, 10, x+5, 40], fill='black')
            x += 8
            
        return img
    
    def _get_font(self, size: int, bold: bool = False) -> ImageFont.ImageFont:
        """Get font for text rendering"""
        try:
            if bold:
                return ImageFont.truetype("arial.ttf", size)
            else:
                return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()
    
    def _add_gradient_background(self, img: Image.Image, draw: ImageDraw.Draw):
        """Add subtle gradient background"""
        width, height = img.size
        for y in range(height):
            alpha = int(255 * (1 - y / height * 0.1))
            color = (245, 245, 250, alpha)
            draw.line([(0, y), (width, y)], fill=color[:3])
    
    def _add_logo_placeholder(self, draw: ImageDraw.Draw, area: Tuple, text: str):
        """Add logo placeholder"""
        draw.rectangle(area, outline='navy', width=2)
        # Center text in area
        text_x = area[0] + (area[2] - area[0]) // 2 - 20
        text_y = area[1] + (area[3] - area[1]) // 2 - 10
        draw.text((text_x, text_y), text, fill='navy', 
                 font=self._get_font(16, bold=True))
    
    def _add_photo_placeholder(self, draw: ImageDraw.Draw, area: Tuple, photo_path: Optional[str]):
        """Add photo or placeholder"""
        draw.rectangle(area, outline='gray', width=2)
        if photo_path and os.path.exists(photo_path):
            # Load and resize photo
            try:
                photo = Image.open(photo_path)
                photo = photo.resize((area[2]-area[0], area[3]-area[1]))
                # This would require additional handling to paste onto the main image
            except:
                pass
        
        # Add placeholder text
        text_x = area[0] + 30
        text_y = area[1] + 70
        draw.text((text_x, text_y), "PHOTO", fill='gray', 
                 font=self._get_font(14))
    
    def _add_security_watermark(self, draw: ImageDraw.Draw, width: int, height: int):
        """Add security watermark"""
        watermark_text = "AUTHENTIC"
        for i in range(0, width, 200):
            for j in range(0, height, 100):
                draw.text((i, j), watermark_text, fill=(200, 200, 200, 128), 
                         font=self._get_font(20))
    
    def _add_pdf_watermark(self, doc: SimpleDocTemplate):
        """Add watermark to PDF"""
        # This would be implemented with reportlab's watermark functionality
        pass
    
    def _generate_account_number(self, config: Dict) -> str:
        """Generate realistic account number"""
        if 'banking' in config:
            format_str = config['banking']['account_format']
            return ''.join([str(random.randint(0, 9)) for _ in range(len(format_str))])
        return "1234567890"
    
    def _add_digital_signature_section(self, story: List, styles, school: Dict, teacher_data: Dict):
        """Add digital signature and verification section"""
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("This is a system generated salary slip and does not require physical signature.", 
                             signature_style))
        story.append(Spacer(1, 10))
        
        # Add verification QR code info
        story.append(Paragraph(f"Document ID: {self._generate_verification_hash(teacher_data)}", 
                             signature_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                             signature_style))


class SecurityFeatures:
    """Handle security features for documents"""
    
    def __init__(self):
        self.watermark_patterns = [
            "CONFIDENTIAL", "AUTHENTIC", "VERIFIED", "ORIGINAL"
        ]
    
    def generate_security_code(self, length: int = 12) -> str:
        """Generate security code"""
        import string
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=length))
    
    def create_hologram_pattern(self, size: Tuple[int, int]) -> Image.Image:
        """Create hologram-like pattern"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create rainbow pattern
        colors_list = [(255, 0, 0, 50), (0, 255, 0, 50), (0, 0, 255, 50),
                      (255, 255, 0, 50), (255, 0, 255, 50), (0, 255, 255, 50)]
        
        for i in range(0, size[0], 20):
            color = colors_list[i // 20 % len(colors_list)]
            draw.line([(i, 0), (i, size[1])], fill=color, width=2)
        
        return img


def main():
    """Main function for command-line usage"""
    generator = EnhancedTeacherDocumentGenerator()
    
    # Example teacher data
    teacher_data = {
        'employee_id': 'TID-IN-2024-1001',
        'name': 'Dr. Priya Sharma',
        'department': 'Mathematics',
        'position': 'Senior Mathematics Teacher',
        'validity': '2025-03-31',
        'photo_path': None
    }
    
    # Example salary data
    salary_data = {
        'basic_salary': 75000,
        'pay_period': '2024-03',
        'pay_date': '2024-03-28'
    }
    
    try:
        # Generate ID card
        id_card_path = generator.generate_teacher_id_card(teacher_data, 'India')
        print(f"Teacher ID card generated: {id_card_path}")
        
        # Generate salary slip
        salary_slip_path = generator.generate_salary_slip(teacher_data, salary_data, 'India')
        print(f"Salary slip generated: {salary_slip_path}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()