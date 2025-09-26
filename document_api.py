#!/usr/bin/env python3
"""
Document Generation API Bridge
This script provides a web API interface for the enhanced document generators
"""

import json
import sys
import os
import base64
from datetime import datetime
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_teacher_documents(data_json):
    """Generate teacher documents from JSON input"""
    try:
        # Import the generator (will fail gracefully if dependencies missing)
        try:
            from canva import EnhancedTeacherDocumentGenerator
            generator = EnhancedTeacherDocumentGenerator()
        except ImportError as e:
            return {
                'success': False, 
                'error': f'Missing dependencies: {str(e)}',
                'suggestion': 'Run: pip install -r requirements.txt'
            }
        
        data = json.loads(data_json)
        teacher_data = data.get('teacher_data', {})
        salary_data = data.get('salary_data', {})
        country = data.get('country', 'India')
        
        results = {}
        
        # Generate ID card if requested
        if data.get('generate_id_card', True):
            try:
                id_card_path = generator.generate_teacher_id_card(teacher_data, country)
                results['id_card'] = id_card_path
            except Exception as e:
                results['id_card_error'] = str(e)
        
        # Generate salary slip if requested
        if data.get('generate_salary_slip', True):
            try:
                salary_slip_path = generator.generate_salary_slip(teacher_data, salary_data, country)
                results['salary_slip'] = salary_slip_path
            except Exception as e:
                results['salary_slip_error'] = str(e)
        
        return {'success': True, 'results': results}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def generate_student_documents(data_json):
    """Generate student documents from JSON input"""
    try:
        # Import the generator
        try:
            from u import EnhancedStudentDocumentGenerator
            generator = EnhancedStudentDocumentGenerator()
        except ImportError as e:
            return {
                'success': False, 
                'error': f'Missing dependencies: {str(e)}',
                'suggestion': 'Run: pip install -r requirements.txt'
            }
        
        data = json.loads(data_json)
        student_data = data.get('student_data', {})
        country = data.get('country', 'India')
        
        results = {}
        
        # Generate ID card if requested
        if data.get('generate_id_card', True):
            try:
                id_card_path = generator.generate_student_id_card(student_data, country)
                results['id_card'] = id_card_path
            except Exception as e:
                results['id_card_error'] = str(e)
        
        # Generate transcript if requested
        if data.get('generate_transcript', True):
            try:
                # Generate realistic academic data
                academic_data = generator._generate_realistic_academic_data(
                    student_data.get('program', 'Computer Science'), 
                    int(student_data.get('year', 2))
                )
                transcript_path = generator.generate_transcript(student_data, academic_data, country)
                results['transcript'] = transcript_path
            except Exception as e:
                results['transcript_error'] = str(e)
        
        # Generate enrollment certificate if requested
        if data.get('generate_enrollment_cert', True):
            try:
                enrollment_path = generator.generate_enrollment_certificate(student_data, country)
                results['enrollment_certificate'] = enrollment_path
            except Exception as e:
                results['enrollment_cert_error'] = str(e)
        
        return {'success': True, 'results': results}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_document_preview(file_path):
    """Get base64 encoded preview of generated document"""
    try:
        if not os.path.exists(file_path):
            return {'success': False, 'error': 'File not found'}
        
        # For images, return base64 encoded data
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            with open(file_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
                return {
                    'success': True, 
                    'type': 'image', 
                    'data': encoded,
                    'mime_type': 'image/png'
                }
        
        # For PDFs, return file path for download
        elif file_path.lower().endswith('.pdf'):
            return {
                'success': True,
                'type': 'pdf',
                'path': file_path,
                'mime_type': 'application/pdf'
            }
        
        else:
            return {'success': False, 'error': 'Unsupported file type'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def simulate_document_generation(doc_type, country='India'):
    """Simulate document generation for testing without heavy dependencies"""
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    if doc_type == 'teacher':
        # Simulate teacher document generation
        teacher_data = {
            'employee_id': f'TID-{country[:2].upper()}-2024-{hash(datetime.now().isoformat()) % 10000:04d}',
            'name': 'Dr. Sample Teacher',
            'department': 'Mathematics',
            'position': 'Senior Teacher',
            'validity': '2025-12-31'
        }
        
        salary_data = {
            'basic_salary': 50000,
            'pay_period': datetime.now().strftime('%Y-%m'),
            'pay_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Create mock files
        id_card_path = f"output/teacher_id_{teacher_data['employee_id']}.png"
        salary_slip_path = f"output/salary_slip_{teacher_data['employee_id']}_{salary_data['pay_period']}.pdf"
        
        # Create placeholder files
        with open(id_card_path, 'w') as f:
            f.write("# Mock Teacher ID Card\n")
            f.write(f"ID: {teacher_data['employee_id']}\n")
            f.write(f"Name: {teacher_data['name']}\n")
            f.write(f"Department: {teacher_data['department']}\n")
        
        with open(salary_slip_path, 'w') as f:
            f.write("# Mock Salary Slip\n")
            f.write(f"Employee: {teacher_data['name']}\n")
            f.write(f"Basic Salary: {salary_data['basic_salary']}\n")
            f.write(f"Period: {salary_data['pay_period']}\n")
        
        return {
            'success': True,
            'results': {
                'id_card': id_card_path,
                'salary_slip': salary_slip_path,
                'teacher_data': teacher_data,
                'salary_data': salary_data
            }
        }
    
    elif doc_type == 'student':
        # Simulate student document generation
        student_data = {
            'student_id': f'SID-{country[:2].upper()}-2024-{hash(datetime.now().isoformat()) % 10000:04d}',
            'name': 'Sample Student',
            'program': 'Bachelor of Technology in Computer Science',
            'academic_year': '2023-24',
            'validity': '2025-12-31'
        }
        
        # Create mock files
        id_card_path = f"output/student_id_{student_data['student_id']}.png"
        transcript_path = f"output/transcript_{student_data['student_id']}.pdf"
        enrollment_path = f"output/enrollment_cert_{student_data['student_id']}.pdf"
        
        # Create placeholder files
        for path, content in [
            (id_card_path, f"# Mock Student ID\nID: {student_data['student_id']}\nName: {student_data['name']}\n"),
            (transcript_path, f"# Mock Transcript\nStudent: {student_data['name']}\nProgram: {student_data['program']}\n"),
            (enrollment_path, f"# Mock Enrollment Certificate\nStudent: {student_data['name']}\nStatus: Enrolled\n")
        ]:
            with open(path, 'w') as f:
                f.write(content)
        
        return {
            'success': True,
            'results': {
                'id_card': id_card_path,
                'transcript': transcript_path,
                'enrollment_certificate': enrollment_path,
                'student_data': student_data
            }
        }

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='Enhanced Document Generator API')
    parser.add_argument('--type', choices=['teacher', 'student'], required=True,
                       help='Document type to generate')
    parser.add_argument('--country', default='India',
                       help='Country for document generation')
    parser.add_argument('--data', help='JSON data for document generation')
    parser.add_argument('--simulate', action='store_true',
                       help='Simulate generation without dependencies')
    parser.add_argument('--preview', help='Generate preview for file path')
    
    args = parser.parse_args()
    
    try:
        if args.preview:
            result = get_document_preview(args.preview)
            print(json.dumps(result, indent=2))
            return
        
        if args.simulate:
            result = simulate_document_generation(args.type, args.country)
        else:
            if args.type == 'teacher':
                if not args.data:
                    # Use default data
                    data = {
                        'teacher_data': {
                            'employee_id': 'TID-IN-2024-1001',
                            'name': 'Dr. Sample Teacher',
                            'department': 'Mathematics',
                            'position': 'Senior Teacher',
                            'validity': '2025-12-31'
                        },
                        'salary_data': {
                            'basic_salary': 50000,
                            'pay_period': '2024-03',
                            'pay_date': '2024-03-28'
                        },
                        'country': args.country
                    }
                    args.data = json.dumps(data)
                
                result = generate_teacher_documents(args.data)
            
            elif args.type == 'student':
                if not args.data:
                    # Use default data
                    data = {
                        'student_data': {
                            'student_id': 'SID-IN-2024-2001',
                            'name': 'Sample Student',
                            'program': 'Bachelor of Technology in Computer Science',
                            'academic_year': '2023-24',
                            'validity': '2025-12-31'
                        },
                        'country': args.country
                    }
                    args.data = json.dumps(data)
                
                result = generate_student_documents(args.data)
        
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}, indent=2))

if __name__ == '__main__':
    main()