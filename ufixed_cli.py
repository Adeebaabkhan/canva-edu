#!/usr/bin/env python3
"""
Command Line Interface for UFFixed
Enhanced document processing for educational institutions
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

from ufixed import (
    StudentRecord, ProcessingConfig, BatchProcessor,
    ReceiptGenerator, IDCardGenerator, create_sample_student,
    COUNTRY_LOCALES
)

def load_students_from_json(filepath: str) -> list:
    """Load student records from JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        students = []
        for item in data:
            student = StudentRecord(
                student_id=item.get('student_id', ''),
                name=item.get('name', ''),
                email=item.get('email', ''),
                phone=item.get('phone', ''),
                address=item.get('address', ''),
                course=item.get('course', ''),
                fee_amount=float(item.get('fee_amount', 0)),
                currency=item.get('currency', 'USD'),
                country=item.get('country', 'USA'),
                photo_url=item.get('photo_url'),
                transaction_id=item.get('transaction_id'),
            )
            
            # Parse dates if provided
            if item.get('enrollment_date'):
                student.enrollment_date = datetime.fromisoformat(item['enrollment_date'])
            if item.get('expiry_date'):
                student.expiry_date = datetime.fromisoformat(item['expiry_date'])
            
            students.append(student)
        
        return students
        
    except Exception as e:
        print(f"Error loading students from {filepath}: {e}")
        return []

def create_sample_data(count: int = 10, countries: list = None) -> list:
    """Create sample student data"""
    countries = countries or ['USA', 'India', 'UK', 'Canada', 'Australia']
    students = []
    
    for i in range(count):
        country = countries[i % len(countries)]
        student = create_sample_student(country)
        student.student_id = f"DEMO{i+1:03d}"
        students.append(student)
    
    return students

def main():
    parser = argparse.ArgumentParser(description='UFFixed - Enhanced Educational Document Processor')
    
    # Input options
    parser.add_argument('--input', '-i', help='JSON file with student data')
    parser.add_argument('--sample', '-s', type=int, default=0, 
                       help='Generate N sample students for testing')
    parser.add_argument('--countries', nargs='+', 
                       choices=list(COUNTRY_LOCALES.keys()),
                       default=['USA', 'India', 'UK'],
                       help='Countries to use for sample data')
    
    # Output options
    parser.add_argument('--output', '-o', default='output', 
                       help='Output directory (default: output)')
    parser.add_argument('--operations', nargs='+', 
                       choices=['receipt', 'id_card', 'both'],
                       default=['both'],
                       help='Operations to perform')
    
    # Processing options
    parser.add_argument('--workers', '-w', type=int, default=4,
                       help='Number of worker threads')
    parser.add_argument('--timeout', '-t', type=int, default=30,
                       help='Network timeout in seconds')
    parser.add_argument('--memory-limit', type=int, default=512,
                       help='Memory limit in MB')
    
    # Output format options
    parser.add_argument('--receipt-format', choices=['PDF', 'IMAGE'], 
                       default='PDF', help='Receipt output format')
    parser.add_argument('--id-template', choices=['modern', 'classic', 'minimal'],
                       default='modern', help='ID card template')
    parser.add_argument('--no-qr', action='store_true',
                       help='Disable QR codes on ID cards')
    
    # Utility options
    parser.add_argument('--list-countries', action='store_true',
                       help='List supported countries')
    parser.add_argument('--test', action='store_true',
                       help='Run system tests')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Handle utility commands
    if args.list_countries:
        print("Supported Countries:")
        for country, info in COUNTRY_LOCALES.items():
            print(f"  {country:<15} - {info['currency']:<3} ({info['symbol']})")
        return 0
    
    if args.test:
        print("Running system tests...")
        import subprocess
        result = subprocess.run([sys.executable, 'test_ufixed.py'], cwd=Path.cwd())
        return result.returncode
    
    # Load or create student data
    students = []
    
    if args.input:
        students = load_students_from_json(args.input)
        if not students:
            print(f"No valid students loaded from {args.input}")
            return 1
        print(f"Loaded {len(students)} students from {args.input}")
    
    elif args.sample > 0:
        students = create_sample_data(args.sample, args.countries)
        print(f"Generated {len(students)} sample students")
    
    else:
        print("No input specified. Use --input <file> or --sample <count>")
        print("Use --help for more options")
        return 1
    
    # Configure processing
    config = ProcessingConfig(
        max_workers=args.workers,
        timeout=args.timeout,
        memory_limit_mb=args.memory_limit
    )
    
    # Determine operations
    operations = []
    if 'both' in args.operations:
        operations = ['receipt', 'id_card']
    else:
        operations = args.operations
    
    # Setup output directory
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    # Create processor
    processor = BatchProcessor(config)
    
    # Progress callback
    def progress_callback(progress, result):
        if args.verbose:
            status = "✓" if not result.get('errors') else "✗"
            print(f"  {status} Progress: {progress:5.1f}% - {result['student_id']}")
        else:
            print(f"\rProgress: {progress:5.1f}%", end='', flush=True)
    
    # Process batch
    print(f"\nProcessing {len(students)} students...")
    print(f"Operations: {', '.join(operations)}")
    print(f"Output directory: {output_dir}")
    
    start_time = datetime.now()
    
    # Change to output directory
    original_cwd = Path.cwd()
    try:
        import os
        os.chdir(output_dir)
        
        results = processor.process_batch(
            students,
            operations=operations,
            progress_callback=progress_callback
        )
        
    finally:
        os.chdir(original_cwd)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Print results
    print(f"\n\n{'='*50}")
    print("PROCESSING COMPLETE")
    print(f"{'='*50}")
    print(f"Students processed: {results['processed']}")
    print(f"Students failed:    {results['failed']}")
    print(f"Files generated:    {len(results['files'])}")
    print(f"Processing time:    {duration:.2f} seconds")
    print(f"Output directory:   {output_dir.absolute()}")
    
    if results['errors']:
        print(f"\nErrors ({len(results['errors'])}):")
        for error in results['errors'][:5]:  # Show first 5 errors
            print(f"  - {error}")
        if len(results['errors']) > 5:
            print(f"  ... and {len(results['errors']) - 5} more")
    
    # Show files
    if results['files'] and args.verbose:
        print(f"\nGenerated Files:")
        for file in sorted(results['files']):
            filepath = output_dir / file
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"  {file} ({size:,} bytes)")
    
    print(f"\n✓ Success! Check {output_dir} for generated files.")
    
    return 0 if results['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())