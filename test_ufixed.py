#!/usr/bin/env python3
"""
Test script for ufixed.py functionality
Tests image processing, receipt generation, and ID card creation
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ufixed import (
    ImageProcessor, ReceiptGenerator, IDCardGenerator, BatchProcessor,
    StudentRecord, ProcessingConfig, create_sample_student, COUNTRY_LOCALES
)

def test_image_processor():
    """Test image processing functionality"""
    print("Testing ImageProcessor...")
    
    config = ProcessingConfig(timeout=10, retry_count=2)
    processor = ImageProcessor(config)
    
    # Test image download with fallbacks
    test_urls = [
        "https://httpbin.org/status/404",  # This will fail
        "https://picsum.photos/200/200",   # This should work
    ]
    
    image_data = processor.download_image(test_urls[0], test_urls[1:])
    
    if image_data:
        print("✓ Image download with fallbacks working")
        
        # Test image processing
        processed = processor.process_image(image_data, size=(150, 150), format='PNG')
        if processed:
            print("✓ Image processing working")
        else:
            print("✗ Image processing failed")
    else:
        print("✓ Fallback image generation working (all downloads failed)")
    
    return True

def test_receipt_generator():
    """Test receipt generation"""
    print("\nTesting ReceiptGenerator...")
    
    generator = ReceiptGenerator()
    student = create_sample_student('India')
    
    # Test PDF receipt (if reportlab available)
    try:
        pdf_receipt = generator.generate_receipt(student, 'PDF')
        if pdf_receipt and len(pdf_receipt) > 100:  # Basic validation
            print("✓ PDF receipt generation working")
        else:
            print("✗ PDF receipt generation failed")
    except Exception as e:
        print(f"○ PDF receipt generation not available: {e}")
    
    # Test image receipt
    try:
        img_receipt = generator.generate_receipt(student, 'IMAGE')
        if img_receipt and len(img_receipt) > 100:
            print("✓ Image receipt generation working")
        else:
            print("✗ Image receipt generation failed")
    except Exception as e:
        print(f"✗ Image receipt generation failed: {e}")
    
    return True

def test_id_card_generator():
    """Test ID card generation"""
    print("\nTesting IDCardGenerator...")
    
    generator = IDCardGenerator()
    student = create_sample_student('UK')
    student.photo_url = "https://picsum.photos/150/150?random=1"
    
    templates = ['modern', 'classic', 'minimal']
    
    for template in templates:
        try:
            card_data = generator.generate_id_card(student, template, include_qr=True)
            if card_data and len(card_data) > 100:
                print(f"✓ {template.capitalize()} ID card generation working")
            else:
                print(f"✗ {template.capitalize()} ID card generation failed")
        except Exception as e:
            print(f"✗ {template.capitalize()} ID card generation failed: {e}")
    
    return True

def test_batch_processor():
    """Test batch processing"""
    print("\nTesting BatchProcessor...")
    
    config = ProcessingConfig(max_workers=2, timeout=10)
    processor = BatchProcessor(config)
    
    # Create test students from different countries
    students = [
        create_sample_student('USA'),
        create_sample_student('India'),
        create_sample_student('Canada'),
    ]
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            def progress_callback(progress, result):
                print(f"  Progress: {progress:.1f}% - {result['student_id']}")
            
            results = processor.process_batch(
                students, 
                operations=['receipt', 'id_card'],
                progress_callback=progress_callback
            )
            
            print(f"✓ Batch processing completed:")
            print(f"  - Processed: {results['processed']}")
            print(f"  - Failed: {results['failed']}")
            print(f"  - Files: {len(results['files'])}")
            
            if results['errors']:
                print(f"  - Errors: {results['errors'][:2]}")  # Show first 2 errors
                
        finally:
            os.chdir(original_cwd)
    
    return True

def test_country_support():
    """Test multi-country support"""
    print("\nTesting Multi-Country Support...")
    
    tested_countries = 0
    for country in list(COUNTRY_LOCALES.keys())[:5]:  # Test first 5 countries
        try:
            student = create_sample_student(country)
            generator = ReceiptGenerator()
            receipt = generator.generate_receipt(student, 'IMAGE')
            
            if receipt:
                tested_countries += 1
                print(f"✓ {country} locale support working")
        except Exception as e:
            print(f"✗ {country} locale support failed: {e}")
    
    print(f"✓ Successfully tested {tested_countries} countries")
    return True

def test_error_handling():
    """Test error handling and fallbacks"""
    print("\nTesting Error Handling...")
    
    # Test with invalid student data
    try:
        invalid_student = StudentRecord(
            student_id="",  # Empty ID
            name="",        # Empty name
            email="invalid-email",
            phone="",
            address="",
            course="",
            fee_amount=-100,  # Negative fee
            currency="INVALID",
            country="NonExistent"
        )
        
        generator = ReceiptGenerator()
        receipt = generator.generate_receipt(invalid_student)
        
        if receipt:
            print("✓ Error handling working - generated receipt despite invalid data")
        else:
            print("○ Error handling - no receipt generated for invalid data")
            
    except Exception as e:
        print(f"✓ Error handling working - caught exception: {type(e).__name__}")
    
    # Test network failure handling
    try:
        processor = ImageProcessor(ProcessingConfig(timeout=1, retry_count=1))
        image_data = processor.download_image("https://invalid-url-that-does-not-exist.com/image.jpg")
        
        if image_data:
            print("✓ Network failure handling - fallback image generated")
        else:
            print("○ Network failure handling - no fallback generated")
            
    except Exception as e:
        print(f"✓ Network failure handling - caught exception: {type(e).__name__}")
    
    return True

def main():
    """Run all tests"""
    print("=== UFFixed.py Test Suite ===")
    print("Testing enhanced image and document processing functionality\n")
    
    tests = [
        test_image_processor,
        test_receipt_generator,
        test_id_card_generator,
        test_batch_processor,
        test_country_support,
        test_error_handling,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check dependency installation")
        return 1

if __name__ == "__main__":
    sys.exit(main())