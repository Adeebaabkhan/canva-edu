#!/usr/bin/env python3
"""
Test script for Enhanced Document Generators
This script tests both teacher and student document generation functionality.
"""

import os
import sys
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_teacher_documents():
    """Test teacher document generation"""
    try:
        from canva import EnhancedTeacherDocumentGenerator
        
        logger.info("Testing Teacher Document Generator...")
        generator = EnhancedTeacherDocumentGenerator()
        
        # Test data for teacher
        teacher_data = {
            'employee_id': 'TID-IN-2024-1001',
            'name': 'Dr. Priya Sharma',
            'department': 'Mathematics',
            'position': 'Senior Mathematics Teacher - Grade 10',
            'validity': '2025-03-31',
            'photo_path': None
        }
        
        salary_data = {
            'basic_salary': 75000,
            'pay_period': '2024-03',
            'pay_date': '2024-03-28'
        }
        
        # Test multiple countries
        countries = ['India', 'USA', 'UK']
        
        for country in countries:
            logger.info(f"Generating documents for {country}...")
            
            # Generate ID card
            try:
                id_card_path = generator.generate_teacher_id_card(teacher_data, country)
                logger.info(f"✓ Teacher ID card generated for {country}: {id_card_path}")
            except Exception as e:
                logger.error(f"✗ Failed to generate ID card for {country}: {str(e)}")
            
            # Generate salary slip
            try:
                salary_slip_path = generator.generate_salary_slip(teacher_data, salary_data, country)
                logger.info(f"✓ Salary slip generated for {country}: {salary_slip_path}")
            except Exception as e:
                logger.error(f"✗ Failed to generate salary slip for {country}: {str(e)}")
        
        logger.info("Teacher document generation tests completed.")
        
    except ImportError as e:
        logger.error(f"Failed to import teacher generator: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in teacher document tests: {str(e)}")

def test_student_documents():
    """Test student document generation"""
    try:
        from u import EnhancedStudentDocumentGenerator
        
        logger.info("Testing Student Document Generator...")
        generator = EnhancedStudentDocumentGenerator()
        
        # Test data for student
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
        
        # Test multiple countries
        countries = ['India', 'USA', 'UK']
        
        for country in countries:
            logger.info(f"Generating student documents for {country}...")
            
            # Generate ID card
            try:
                id_card_path = generator.generate_student_id_card(student_data, country)
                logger.info(f"✓ Student ID card generated for {country}: {id_card_path}")
            except Exception as e:
                logger.error(f"✗ Failed to generate student ID card for {country}: {str(e)}")
            
            # Generate academic data and transcript
            try:
                academic_data = generator._generate_realistic_academic_data('Computer Science', 2)
                transcript_path = generator.generate_transcript(student_data, academic_data, country)
                logger.info(f"✓ Academic transcript generated for {country}: {transcript_path}")
            except Exception as e:
                logger.error(f"✗ Failed to generate transcript for {country}: {str(e)}")
            
            # Generate enrollment certificate
            try:
                enrollment_path = generator.generate_enrollment_certificate(student_data, country)
                logger.info(f"✓ Enrollment certificate generated for {country}: {enrollment_path}")
            except Exception as e:
                logger.error(f"✗ Failed to generate enrollment certificate for {country}: {str(e)}")
        
        logger.info("Student document generation tests completed.")
        
    except ImportError as e:
        logger.error(f"Failed to import student generator: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in student document tests: {str(e)}")

def test_security_features():
    """Test security features"""
    logger.info("Testing security features...")
    
    try:
        from canva import SecurityFeatures
        
        security = SecurityFeatures()
        
        # Test security code generation
        sec_code = security.generate_security_code(12)
        logger.info(f"✓ Security code generated: {sec_code}")
        
        # Test hologram pattern creation
        hologram = security.create_hologram_pattern((200, 100))
        logger.info(f"✓ Hologram pattern created: {hologram.size}")
        
    except Exception as e:
        logger.error(f"✗ Security features test failed: {str(e)}")

def create_demo_documents():
    """Create demonstration documents"""
    logger.info("Creating demonstration documents...")
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Test both generators
    test_teacher_documents()
    test_student_documents()
    test_security_features()
    
    # List generated files
    if os.path.exists('output'):
        generated_files = os.listdir('output')
        if generated_files:
            logger.info("Generated files:")
            for file in generated_files:
                logger.info(f"  - {file}")
        else:
            logger.warning("No files were generated in output directory")
    
def check_dependencies():
    """Check if required dependencies are available"""
    logger.info("Checking dependencies...")
    
    required_modules = [
        'PIL', 'reportlab', 'qrcode', 'faker', 'numpy', 'matplotlib'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            logger.info(f"✓ {module} is available")
        except ImportError:
            missing_modules.append(module)
            logger.warning(f"✗ {module} is missing")
    
    if missing_modules:
        logger.error(f"Missing required modules: {', '.join(missing_modules)}")
        logger.info("Install missing modules with: pip install " + ' '.join(missing_modules))
        return False
    
    logger.info("All dependencies are available.")
    return True

def main():
    """Main test function"""
    logger.info("Starting Enhanced Document Generator Tests")
    logger.info("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        logger.error("Cannot proceed without required dependencies")
        return
    
    # Create demonstration documents
    create_demo_documents()
    
    logger.info("=" * 50)
    logger.info("Test completed. Check the 'output' directory for generated documents.")

if __name__ == "__main__":
    main()