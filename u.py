#!/usr/bin/env python3
"""
Enhanced Realistic Student Document Generator
This module generates authentic-looking student documents including ID cards, transcripts, and enrollment certificates.
"""

import os
import sys
import random
import json
import qrcode
import logging
from datetime import datetime, timedelta, date
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
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedStudentDocumentGenerator:
    """Enhanced generator for realistic student documents"""
    
    def __init__(self):
        self.fake = Faker()
        self.university_configs = self._load_university_configs()
        self.universities_database = self._load_universities_database()
        self.course_database = self._load_course_database()
        self.grade_systems = self._load_grade_systems()
        
    def _load_university_configs(self) -> Dict:
        """Load university-specific configurations"""
        return {
            'India': {
                'academic_year_format': '2023-24',
                'semester_system': True,
                'grade_system': '10_point',
                'registration_format': 'IN{year}{code}{number}',
                'transcript_validity': 365,
                'locale': 'hi_IN',
                'regulatory_body': 'University Grants Commission (UGC)',
                'verification_codes': {
                    'transcript_code': 'TRC-IND',
                    'enrollment_code': 'ENR-IND',
                    'id_code': 'SID-IND'
                }
            },
            'USA': {
                'academic_year_format': '2023-2024',
                'semester_system': True,
                'grade_system': '4_point',
                'registration_format': 'US{year}{code}{number}',
                'transcript_validity': 1095,  # 3 years
                'locale': 'en_US',
                'regulatory_body': 'Department of Education',
                'verification_codes': {
                    'transcript_code': 'TRC-USA',
                    'enrollment_code': 'ENR-USA',
                    'id_code': 'SID-USA'
                }
            },
            'UK': {
                'academic_year_format': '2023/24',
                'semester_system': False,  # Term system
                'grade_system': 'uk_honours',
                'registration_format': 'UK{year}{code}{number}',
                'transcript_validity': 1825,  # 5 years
                'locale': 'en_GB',
                'regulatory_body': 'Office for Students (OfS)',
                'verification_codes': {
                    'transcript_code': 'TRC-GBR',
                    'enrollment_code': 'ENR-GBR',
                    'id_code': 'SID-GBR'
                }
            }
        }
    
    def _load_universities_database(self) -> Dict:
        """Load comprehensive universities database"""
        return {
            "India": [
                {
                    "name": "University of Delhi",
                    "short_name": "DU",
                    "location": "New Delhi",
                    "code": "UOD",
                    "vice_chancellor": "Prof. Yogesh Singh",
                    "registrar": "Dr. Vikas Gupta",
                    "phone": "+91-11-27666666",
                    "email": "info@du.ac.in",
                    "website": "www.du.ac.in",
                    "address": "Vice-Chancellor's Office, University of Delhi, Delhi - 110007",
                    "established": "1922",
                    "type": "Central University",
                    "accreditation": "NAAC A++",
                    "logo_path": "logos/du_logo.png"
                },
                {
                    "name": "Indian Institute of Technology Delhi",
                    "short_name": "IIT Delhi",
                    "location": "New Delhi",
                    "code": "IITD",
                    "director": "Prof. Rangan Banerjee",
                    "registrar": "Dr. Bhaskar Ramamurthi",
                    "phone": "+91-11-26591785",
                    "email": "director@iitd.ac.in",
                    "website": "www.iitd.ac.in",
                    "address": "Hauz Khas, New Delhi - 110016",
                    "established": "1961",
                    "type": "Institute of National Importance",
                    "accreditation": "NAAC A++",
                    "logo_path": "logos/iitd_logo.png"
                }
            ],
            "USA": [
                {
                    "name": "Harvard University",
                    "short_name": "Harvard",
                    "location": "Cambridge, MA",
                    "code": "HARV",
                    "president": "Dr. Alan M. Garber",
                    "registrar": "Dr. Michael Burke",
                    "phone": "+1-617-495-1000",
                    "email": "info@harvard.edu",
                    "website": "www.harvard.edu",
                    "address": "Massachusetts Hall, Cambridge, MA 02138",
                    "established": "1636",
                    "type": "Private Research University",
                    "accreditation": "NECHE",
                    "logo_path": "logos/harvard_logo.png"
                }
            ],
            "UK": [
                {
                    "name": "University of Oxford",
                    "short_name": "Oxford",
                    "location": "Oxford, England",
                    "code": "OXON",
                    "vice_chancellor": "Prof. Irene Tracey",
                    "registrar": "Dr. Ewan McKendrick",
                    "phone": "+44-1865-270000",
                    "email": "information.office@admin.ox.ac.uk",
                    "website": "www.ox.ac.uk",
                    "address": "University Offices, Wellington Square, Oxford OX1 2JD",
                    "established": "1096",
                    "type": "Collegiate Research University",
                    "accreditation": "QAA",
                    "logo_path": "logos/oxford_logo.png"
                }
            ]
        }
    
    def _load_course_database(self) -> Dict:
        """Load comprehensive course database with realistic codes"""
        return {
            "Computer Science": {
                "code_prefix": "CS",
                "courses": [
                    {"code": "CS101", "name": "Introduction to Programming", "credits": 4, "level": "undergraduate"},
                    {"code": "CS201", "name": "Data Structures and Algorithms", "credits": 4, "level": "undergraduate"},
                    {"code": "CS301", "name": "Database Management Systems", "credits": 3, "level": "undergraduate"},
                    {"code": "CS401", "name": "Machine Learning", "credits": 4, "level": "undergraduate"},
                    {"code": "CS501", "name": "Advanced Algorithms", "credits": 3, "level": "graduate"},
                    {"code": "CS601", "name": "Artificial Intelligence", "credits": 4, "level": "graduate"}
                ]
            },
            "Mathematics": {
                "code_prefix": "MATH",
                "courses": [
                    {"code": "MATH101", "name": "Calculus I", "credits": 4, "level": "undergraduate"},
                    {"code": "MATH201", "name": "Linear Algebra", "credits": 3, "level": "undergraduate"},
                    {"code": "MATH301", "name": "Real Analysis", "credits": 4, "level": "undergraduate"},
                    {"code": "MATH401", "name": "Abstract Algebra", "credits": 3, "level": "undergraduate"},
                    {"code": "MATH501", "name": "Topology", "credits": 3, "level": "graduate"}
                ]
            },
            "Physics": {
                "code_prefix": "PHYS",
                "courses": [
                    {"code": "PHYS101", "name": "General Physics I", "credits": 4, "level": "undergraduate"},
                    {"code": "PHYS201", "name": "Classical Mechanics", "credits": 4, "level": "undergraduate"},
                    {"code": "PHYS301", "name": "Quantum Mechanics", "credits": 4, "level": "undergraduate"},
                    {"code": "PHYS401", "name": "Statistical Mechanics", "credits": 3, "level": "undergraduate"}
                ]
            }
        }
    
    def _load_grade_systems(self) -> Dict:
        """Load different grading systems"""
        return {
            '10_point': {
                'scale': 10.0,
                'grades': ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'F'],
                'points': [10, 9, 8, 7, 6, 5, 4, 0],
                'passing_grade': 5.0
            },
            '4_point': {
                'scale': 4.0,
                'grades': ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'],
                'points': [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.0, 0.0],
                'passing_grade': 2.0
            },
            'uk_honours': {
                'scale': 100,
                'grades': ['First Class', 'Upper Second', 'Lower Second', 'Third Class', 'Pass', 'Fail'],
                'ranges': [(70, 100), (60, 69), (50, 59), (40, 49), (35, 39), (0, 34)],
                'passing_grade': 40
            }
        }
    
    def generate_student_id_card(self, student_data: Dict, country: str = 'India') -> str:
        """Generate realistic student ID card"""
        try:
            config = self.university_configs[country]
            university = random.choice(self.universities_database[country])
            
            # Create ID card image
            card_width, card_height = 856, 540
            img = Image.new('RGB', (card_width, card_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Add university colors background
            self._add_university_background(img, draw, university)
            
            # Add university logo area
            logo_area = (50, 30, 200, 120)
            self._add_logo_placeholder(draw, logo_area, university['short_name'])
            
            # Add university information
            uni_info_y = 30
            draw.text((220, uni_info_y), university['name'], fill='navy', 
                     font=self._get_font(20, bold=True))
            draw.text((220, uni_info_y + 25), f"Est. {university['established']}", 
                     fill='gray', font=self._get_font(10))
            draw.text((220, uni_info_y + 40), university['location'], 
                     fill='gray', font=self._get_font(10))
            draw.text((220, uni_info_y + 55), f"Accredited by {university['accreditation']}", 
                     fill='green', font=self._get_font(9))
            
            # Add student photo placeholder
            photo_area = (50, 150, 200, 300)
            self._add_photo_placeholder(draw, photo_area, student_data.get('photo_path'))
            
            # Add student information
            info_x, info_y = 220, 150
            draw.text((info_x, info_y), f"ID: {student_data['student_id']}", 
                     fill='black', font=self._get_font(14, bold=True))
            draw.text((info_x, info_y + 25), student_data['name'], 
                     fill='black', font=self._get_font(18, bold=True))
            draw.text((info_x, info_y + 50), f"Program: {student_data['program']}", 
                     fill='black', font=self._get_font(12))
            draw.text((info_x, info_y + 70), f"Year: {student_data['academic_year']}", 
                     fill='black', font=self._get_font(12))
            draw.text((info_x, info_y + 90), f"Valid Until: {student_data['validity']}", 
                     fill='red', font=self._get_font(12))
            
            # Add academic status
            draw.text((info_x, info_y + 110), f"Status: {student_data.get('status', 'Active')}", 
                     fill='green', font=self._get_font(12, bold=True))
            
            # Add security features
            self._add_security_watermark(draw, card_width, card_height)
            
            # Add QR code with student verification data
            qr_data = {
                'student_id': student_data['student_id'],
                'name': student_data['name'],
                'university': university['code'],
                'program': student_data['program'],
                'year': student_data['academic_year'],
                'valid_until': student_data['validity'],
                'verification_hash': self._generate_verification_hash(student_data)
            }
            qr_img = self._generate_qr_code(json.dumps(qr_data))
            qr_img = qr_img.resize((120, 120))
            img.paste(qr_img, (700, 350))
            
            # Add barcode
            barcode = self._generate_barcode(student_data['student_id'])
            img.paste(barcode, (50, 470))
            
            # Add holographic security strip
            security_strip = self._create_security_strip((card_width, 30))
            img.paste(security_strip, (0, 320), security_strip)
            
            # Save ID card
            output_path = f"output/student_id_{student_data['student_id']}.png"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, quality=95, dpi=(300, 300))
            
            logger.info(f"Student ID card generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating student ID card: {str(e)}")
            raise
    
    def generate_transcript(self, student_data: Dict, academic_data: Dict, 
                          country: str = 'India') -> str:
        """Generate official academic transcript"""
        try:
            config = self.university_configs[country]
            university = random.choice(self.universities_database[country])
            grade_system = self.grade_systems[config['grade_system']]
            
            # Create PDF document
            output_path = f"output/transcript_{student_data['student_id']}.pdf"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(output_path, pagesize=A4,
                                  topMargin=1*inch, bottomMargin=1*inch)
            styles = getSampleStyleSheet()
            story = []
            
            # Add watermark
            self._add_pdf_watermark(doc, "OFFICIAL TRANSCRIPT")
            
            # Header with university seal
            header_style = ParagraphStyle(
                'UniversityHeader',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.darkblue,
                alignment=TA_CENTER,
                spaceAfter=6
            )
            
            story.append(Paragraph(university['name'].upper(), header_style))
            story.append(Paragraph(f"OFFICIAL ACADEMIC TRANSCRIPT", styles['Heading2']))
            story.append(Paragraph(f"Transcript ID: {self._generate_transcript_id(config)}", 
                                 styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Student information
            student_info_data = [
                ['Student Name:', student_data['name'], 'Student ID:', student_data['student_id']],
                ['Date of Birth:', student_data.get('dob', 'N/A'), 'Program:', student_data['program']],
                ['Admission Date:', academic_data['admission_date'], 'Graduation Date:', 
                 academic_data.get('graduation_date', 'In Progress')],
                ['Academic Year:', student_data['academic_year'], 'Degree Status:', 
                 academic_data.get('degree_status', 'In Progress')]
            ]
            
            student_table = Table(student_info_data, colWidths=[2*inch, 2*inch, 1.5*inch, 2*inch])
            student_table.setStyle(self._get_table_style())
            
            story.append(student_table)
            story.append(Spacer(1, 20))
            
            # Academic records
            story.append(Paragraph("ACADEMIC RECORD", styles['Heading3']))
            story.append(Spacer(1, 10))
            
            # Course-wise grades
            courses_data = [['Course Code', 'Course Title', 'Credits', 'Grade', 'Points']]
            
            total_credits = 0
            total_points = 0
            
            for semester in academic_data['semesters']:
                courses_data.append([f"Semester {semester['number']}", '', '', '', ''])
                
                for course in semester['courses']:
                    grade_info = self._get_grade_info(course['grade'], grade_system)
                    credit_points = course['credits'] * grade_info['points']
                    
                    courses_data.append([
                        course['code'],
                        course['name'],
                        str(course['credits']),
                        course['grade'],
                        f"{grade_info['points']:.2f}"
                    ])
                    
                    total_credits += course['credits']
                    total_points += credit_points
                
                courses_data.append(['', '', '', '', ''])  # Spacer
            
            # Calculate GPA
            gpa = total_points / total_credits if total_credits > 0 else 0
            
            courses_data.append(['', 'TOTAL CREDITS', str(total_credits), 
                               f'GPA: {gpa:.2f}/{grade_system["scale"]}', ''])
            
            courses_table = Table(courses_data, colWidths=[1.2*inch, 3*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            courses_table.setStyle(self._get_transcript_table_style())
            
            story.append(courses_table)
            story.append(Spacer(1, 30))
            
            # Add grading scale
            self._add_grading_scale(story, styles, grade_system)
            
            # Add verification and signatures
            self._add_transcript_verification(story, styles, university, student_data)
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Academic transcript generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating transcript: {str(e)}")
            raise
    
    def generate_enrollment_certificate(self, student_data: Dict, country: str = 'India') -> str:
        """Generate enrollment verification certificate"""
        try:
            config = self.university_configs[country]
            university = random.choice(self.universities_database[country])
            
            # Create PDF document
            output_path = f"output/enrollment_cert_{student_data['student_id']}.pdf"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Add university letterhead
            header_style = ParagraphStyle(
                'Letterhead',
                parent=styles['Heading1'],
                fontSize=20,
                textColor=colors.darkblue,
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            story.append(Paragraph(university['name'].upper(), header_style))
            story.append(Paragraph(f"Office of the Registrar", styles['Heading3']))
            story.append(Paragraph(university['address'], styles['Normal']))
            story.append(Spacer(1, 30))
            
            # Certificate title
            cert_title_style = ParagraphStyle(
                'CertTitle',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.darkred,
                alignment=TA_CENTER,
                spaceAfter=20
            )
            
            story.append(Paragraph("ENROLLMENT VERIFICATION CERTIFICATE", cert_title_style))
            story.append(Spacer(1, 20))
            
            # Certificate content
            cert_date = datetime.now().strftime("%B %d, %Y")
            cert_id = f"ENV-{random.randint(100000, 999999)}"
            
            content_style = ParagraphStyle(
                'CertContent',
                parent=styles['Normal'],
                fontSize=12,
                alignment=TA_LEFT,
                spaceAfter=12
            )
            
            story.append(Paragraph(f"Certificate ID: {cert_id}", content_style))
            story.append(Paragraph(f"Date of Issue: {cert_date}", content_style))
            story.append(Spacer(1, 20))
            
            # Main certificate text
            cert_text = f"""
            This is to certify that <b>{student_data['name']}</b> (Student ID: {student_data['student_id']}) 
            is currently enrolled as a <b>{student_data.get('enrollment_status', 'Full-time')}</b> student 
            in the <b>{student_data['program']}</b> program at {university['name']}.
            <br/><br/>
            The student was admitted to the university on <b>{student_data.get('admission_date', 'N/A')}</b> 
            and is in good academic standing. This certificate is valid for official purposes and 
            verification of enrollment status.
            <br/><br/>
            Academic Year: <b>{student_data['academic_year']}</b><br/>
            Expected Graduation: <b>{student_data.get('expected_graduation', 'N/A')}</b>
            """
            
            story.append(Paragraph(cert_text, content_style))
            story.append(Spacer(1, 40))
            
            # Signatures
            signature_data = [
                ['', '', ''],
                ['_____________________', '', '_____________________'],
                [university['registrar'], '', 'Date: ' + cert_date],
                ['Registrar', '', '']
            ]
            
            signature_table = Table(signature_data, colWidths=[2.5*inch, 1*inch, 2.5*inch])
            signature_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 2), (0, 3), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, 1), 20),
            ]))
            
            story.append(signature_table)
            story.append(Spacer(1, 30))
            
            # Add verification footer
            footer_text = f"""
            This certificate is digitally generated and verified. 
            For verification, please contact {university['email']} or call {university['phone']}.
            Certificate Hash: {self._generate_verification_hash(student_data)}
            """
            
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            
            story.append(Paragraph(footer_text, footer_style))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"Enrollment certificate generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating enrollment certificate: {str(e)}")
            raise
    
    def _generate_realistic_academic_data(self, program: str, year: int) -> Dict:
        """Generate realistic academic data with grades"""
        semesters = []
        courses_db = list(self.course_database.keys())
        
        for sem_num in range(1, (year * 2) + 1):
            semester = {
                'number': sem_num,
                'courses': []
            }
            
            # Select relevant courses for the semester
            selected_major = program.split()[0] if ' ' in program else program
            if selected_major in self.course_database:
                available_courses = self.course_database[selected_major]['courses']
            else:
                available_courses = self.course_database['Computer Science']['courses']
            
            # Add 4-6 courses per semester
            num_courses = random.randint(4, 6)
            selected_courses = random.sample(available_courses, 
                                           min(num_courses, len(available_courses)))
            
            for course in selected_courses:
                grade = self._generate_realistic_grade()
                semester['courses'].append({
                    'code': course['code'],
                    'name': course['name'],
                    'credits': course['credits'],
                    'grade': grade
                })
            
            semesters.append(semester)
        
        return {
            'admission_date': f"2023-08-01",
            'expected_graduation': f"2027-05-31",
            'semesters': semesters
        }
    
    def _generate_realistic_grade(self) -> str:
        """Generate realistic grade based on normal distribution"""
        # Simulate realistic grade distribution
        grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        weights = [0.05, 0.15, 0.20, 0.25, 0.20, 0.10, 0.04, 0.01]
        return random.choices(grades, weights=weights)[0]
    
    def _get_grade_info(self, grade: str, grade_system: Dict) -> Dict:
        """Get grade information including points"""
        if grade_system['scale'] == 4.0:  # US system
            grade_points = {
                'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 
                'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0
            }
        elif grade_system['scale'] == 10.0:  # Indian system
            grade_points = {
                'A+': 10, 'A': 9, 'B+': 8, 'B': 7, 'C+': 6, 'C': 5, 'D': 4, 'F': 0
            }
        else:
            grade_points = {'A+': 4.0, 'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        
        return {
            'grade': grade,
            'points': grade_points.get(grade, 0.0)
        }
    
    def _generate_transcript_id(self, config: Dict) -> str:
        """Generate unique transcript ID"""
        prefix = config['verification_codes']['transcript_code']
        year = datetime.now().year
        sequence = random.randint(100000, 999999)
        return f"{prefix}-{year}-{sequence}"
    
    def _add_grading_scale(self, story: List, styles, grade_system: Dict):
        """Add grading scale to transcript"""
        story.append(Paragraph("GRADING SCALE", styles['Heading4']))
        
        if grade_system['scale'] == 4.0:
            scale_data = [
                ['Grade', 'Points', 'Grade', 'Points'],
                ['A', '4.0', 'C+', '2.3'],
                ['A-', '3.7', 'C', '2.0'],
                ['B+', '3.3', 'C-', '1.7'],
                ['B', '3.0', 'D', '1.0'],
                ['B-', '2.7', 'F', '0.0']
            ]
        else:  # 10 point system
            scale_data = [
                ['Grade', 'Points', 'Grade', 'Points'],
                ['A+', '10', 'C+', '6'],
                ['A', '9', 'C', '5'],
                ['B+', '8', 'D', '4'],
                ['B', '7', 'F', '0']
            ]
        
        scale_table = Table(scale_data, colWidths=[0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        scale_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(scale_table)
        story.append(Spacer(1, 20))
    
    def _add_transcript_verification(self, story: List, styles, university: Dict, student_data: Dict):
        """Add verification section to transcript"""
        verification_style = ParagraphStyle(
            'Verification',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=TA_LEFT
        )
        
        story.append(Spacer(1, 30))
        story.append(Paragraph("VERIFICATION", styles['Heading4']))
        
        verification_text = f"""
        This transcript is issued by {university['name']} and contains the complete 
        academic record of the above-named student. This document is valid only when 
        bearing the official seal and signature of the Registrar.
        <br/><br/>
        For verification of this transcript, please contact:<br/>
        Email: {university['email']}<br/>
        Phone: {university['phone']}<br/>
        Website: {university['website']}
        <br/><br/>
        Document Hash: {self._generate_verification_hash(student_data)}<br/>
        Issue Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        story.append(Paragraph(verification_text, verification_style))
    
    # Utility methods (similar to canva.py)
    def _generate_verification_hash(self, data: Dict) -> str:
        """Generate verification hash for security"""
        hash_input = f"{data.get('student_id', '')}{data.get('name', '')}{datetime.now().strftime('%Y%m%d')}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    def _generate_qr_code(self, data: str) -> Image.Image:
        """Generate QR code for verification"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    def _generate_barcode(self, data: str) -> Image.Image:
        """Generate barcode for the ID"""
        img = Image.new('RGB', (300, 50), color='white')
        draw = ImageDraw.Draw(img)
        
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
    
    def _add_university_background(self, img: Image.Image, draw: ImageDraw.Draw, university: Dict):
        """Add university-themed background"""
        width, height = img.size
        # Add subtle institutional colors
        for y in range(height):
            alpha = int(255 * (1 - y / height * 0.05))
            color = (240, 248, 255, alpha)  # Alice blue
            draw.line([(0, y), (width, y)], fill=color[:3])
    
    def _add_logo_placeholder(self, draw: ImageDraw.Draw, area: Tuple, text: str):
        """Add logo placeholder"""
        draw.rectangle(area, outline='navy', width=2)
        text_x = area[0] + (area[2] - area[0]) // 2 - len(text) * 5
        text_y = area[1] + (area[3] - area[1]) // 2 - 10
        draw.text((text_x, text_y), text, fill='navy', 
                 font=self._get_font(16, bold=True))
    
    def _add_photo_placeholder(self, draw: ImageDraw.Draw, area: Tuple, photo_path: Optional[str]):
        """Add photo or placeholder"""
        draw.rectangle(area, outline='gray', width=2)
        text_x = area[0] + 30
        text_y = area[1] + 70
        draw.text((text_x, text_y), "STUDENT\nPHOTO", fill='gray', 
                 font=self._get_font(12))
    
    def _add_security_watermark(self, draw: ImageDraw.Draw, width: int, height: int):
        """Add security watermark"""
        watermark_text = "STUDENT ID"
        for i in range(0, width, 150):
            for j in range(0, height, 80):
                draw.text((i, j), watermark_text, fill=(220, 220, 220, 100), 
                         font=self._get_font(16))
    
    def _create_security_strip(self, size: Tuple[int, int]) -> Image.Image:
        """Create holographic security strip"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Create rainbow pattern
        colors_list = [(255, 0, 0, 80), (0, 255, 0, 80), (0, 0, 255, 80),
                      (255, 255, 0, 80), (255, 0, 255, 80), (0, 255, 255, 80)]
        
        for i in range(0, size[0], 20):
            color = colors_list[i // 20 % len(colors_list)]
            draw.line([(i, 0), (i, size[1])], fill=color, width=3)
        
        return img
    
    def _add_pdf_watermark(self, doc: SimpleDocTemplate, text: str = "CONFIDENTIAL"):
        """Add watermark to PDF"""
        # This would be implemented with reportlab's watermark functionality
        pass
    
    def _get_table_style(self) -> TableStyle:
        """Get standard table style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
    
    def _get_transcript_table_style(self) -> TableStyle:
        """Get transcript-specific table style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (4, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgreen),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
        ])


def main():
    """Main function for command-line usage"""
    generator = EnhancedStudentDocumentGenerator()
    
    # Example student data
    student_data = {
        'student_id': 'SID-IN-2024-2001',
        'name': 'Arjun Patel',
        'program': 'Bachelor of Technology in Computer Science',
        'academic_year': '2023-24',
        'admission_date': '2023-08-01',
        'expected_graduation': '2027-05-31',
        'validity': '2025-12-31',
        'status': 'Active',
        'enrollment_status': 'Full-time',
        'photo_path': None
    }
    
    try:
        # Generate student ID card
        id_card_path = generator.generate_student_id_card(student_data, 'India')
        print(f"Student ID card generated: {id_card_path}")
        
        # Generate academic data
        academic_data = generator._generate_realistic_academic_data('Computer Science', 2)
        
        # Generate transcript
        transcript_path = generator.generate_transcript(student_data, academic_data, 'India')
        print(f"Academic transcript generated: {transcript_path}")
        
        # Generate enrollment certificate
        enrollment_path = generator.generate_enrollment_certificate(student_data, 'India')
        print(f"Enrollment certificate generated: {enrollment_path}")
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()