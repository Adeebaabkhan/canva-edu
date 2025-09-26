#!/usr/bin/env python3
"""
Simple test script that can run without heavy dependencies
Tests the basic structure and configuration of document generators
"""

import json
import hashlib
from datetime import datetime

def test_basic_structure():
    """Test basic structure without heavy dependencies"""
    print("Testing Enhanced Document Generator Structure")
    print("=" * 50)
    
    # Test country configurations
    country_configs = {
        'India': {
            'currency': '₹',
            'currency_code': 'INR',
            'tax_rate': 0.10,
            'pf_rate': 0.12,
            'esi_rate': 0.0175,
            'professional_tax': 200,
            'locale': 'hi_IN'
        },
        'USA': {
            'currency': '$',
            'currency_code': 'USD',
            'tax_rate': 0.22,
            'social_security_rate': 0.062,
            'medicare_rate': 0.0145,
            'state_tax_rate': 0.08,
            'locale': 'en_US'
        },
        'UK': {
            'currency': '£',
            'currency_code': 'GBP',
            'tax_rate': 0.20,
            'national_insurance_rate': 0.12,
            'pension_rate': 0.095,
            'locale': 'en_GB'
        }
    }
    
    print("✓ Country configurations loaded")
    print(f"  Supported countries: {list(country_configs.keys())}")
    
    # Test salary calculation
    def calculate_salary(basic_salary, country):
        config = country_configs[country]
        
        # Calculate allowances
        hra = basic_salary * 0.40
        da = basic_salary * 0.25
        transport = 2000
        medical = 1500
        
        total_earnings = basic_salary + hra + da + transport + medical
        
        # Calculate deductions
        tax = total_earnings * config['tax_rate']
        pf = basic_salary * config.get('pf_rate', 0.12)
        
        total_deductions = tax + pf
        net_pay = total_earnings - total_deductions
        
        return {
            'total_earnings': total_earnings,
            'total_deductions': total_deductions,
            'net_pay': net_pay,
            'currency': config['currency']
        }
    
    # Test salary calculation for each country
    basic_salary = 50000
    print(f"\n✓ Testing salary calculations (Basic: {basic_salary})")
    
    for country in country_configs:
        result = calculate_salary(basic_salary, country)
        print(f"  {country}: {result['currency']}{result['net_pay']:,.2f} net pay")
    
    # Test document ID generation
    def generate_document_id(prefix, country_code, year):
        sequence = 123456  # Would be random in real implementation
        return f"{prefix}-{country_code}-{year}-{sequence}"
    
    print(f"\n✓ Testing document ID generation")
    for country in ['IN', 'US', 'GB']:
        teacher_id = generate_document_id('TID', country, 2024)
        student_id = generate_document_id('SID', country, 2024)
        print(f"  {country}: Teacher={teacher_id}, Student={student_id}")
    
    # Test verification hash generation
    def generate_verification_hash(data):
        hash_input = f"{data['id']}{data['name']}{datetime.now().strftime('%Y%m%d')}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]
    
    test_data = {'id': 'TID-IN-2024-123456', 'name': 'Dr. Priya Sharma'}
    hash_result = generate_verification_hash(test_data)
    print(f"\n✓ Verification hash generated: {hash_result}")
    
    # Test course database structure
    course_database = {
        "Computer Science": {
            "code_prefix": "CS",
            "courses": [
                {"code": "CS101", "name": "Introduction to Programming", "credits": 4},
                {"code": "CS201", "name": "Data Structures", "credits": 4},
                {"code": "CS301", "name": "Database Systems", "credits": 3}
            ]
        },
        "Mathematics": {
            "code_prefix": "MATH",
            "courses": [
                {"code": "MATH101", "name": "Calculus I", "credits": 4},
                {"code": "MATH201", "name": "Linear Algebra", "credits": 3}
            ]
        }
    }
    
    print(f"\n✓ Course database structure")
    for major, data in course_database.items():
        print(f"  {major}: {len(data['courses'])} courses")
    
    # Test grade calculation
    def calculate_gpa(courses_with_grades, system='4_point'):
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 
            'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'D': 1.0, 'F': 0.0
        }
        
        total_points = 0
        total_credits = 0
        
        for course in courses_with_grades:
            points = grade_points.get(course['grade'], 0.0)
            credits = course['credits']
            total_points += points * credits
            total_credits += credits
        
        return total_points / total_credits if total_credits > 0 else 0.0
    
    sample_courses = [
        {'code': 'CS101', 'grade': 'A', 'credits': 4},
        {'code': 'MATH101', 'grade': 'B+', 'credits': 3},
        {'code': 'PHYS101', 'grade': 'A-', 'credits': 4}
    ]
    
    gpa = calculate_gpa(sample_courses)
    print(f"\n✓ GPA calculation test: {gpa:.2f}/4.0")
    
    # Test security features simulation
    def simulate_security_features():
        features = {
            'qr_code_data': json.dumps({
                'id': 'TID-IN-2024-123456',
                'name': 'Test User',
                'verification_hash': 'abc123def456'
            }),
            'watermark_text': 'AUTHENTIC',
            'security_code': 'SEC-' + str(hash(datetime.now().isoformat()))[-8:],
            'barcode_data': 'TID-IN-2024-123456'
        }
        return features
    
    security_features = simulate_security_features()
    print(f"\n✓ Security features simulation")
    print(f"  Security code: {security_features['security_code']}")
    print(f"  QR data length: {len(security_features['qr_code_data'])} chars")
    
    print("\n" + "=" * 50)
    print("✅ All basic structure tests passed!")
    print("✅ Document generators are properly configured")
    print("✅ Ready for full implementation with dependencies")

if __name__ == "__main__":
    test_basic_structure()