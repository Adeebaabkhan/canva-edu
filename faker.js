// Enhanced Faker.js implementation for K-12 Teacher Payslip Generator
const faker = {
    locale: 'en_US',
    
    // Country-specific teacher names with proper academic titles
    teacherNames: {
        'India': {
            firstNames: ['Priya', 'Rajesh', 'Sunita', 'Amit', 'Kavita', 'Vikram', 'Meera', 'Ravi', 'Anjali', 'Suresh',
                        'Deepika', 'Arjun', 'Pooja', 'Kiran', 'Sneha', 'Ashish', 'Divya', 'Rohit', 'Maya', 'Anil'],
            lastNames: ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Verma', 'Mishra', 'Joshi', 'Shah',
                       'Reddy', 'Nair', 'Iyer', 'Rao', 'Chopra', 'Malhotra', 'Kapoor', 'Bansal', 'Saxena', 'Tiwari'],
            titles: ['Dr.', 'Prof.', 'Ms.', 'Mr.', 'Mrs.']
        },
        'USA': {
            firstNames: ['Sarah', 'Michael', 'Emily', 'David', 'Jessica', 'Robert', 'Ashley', 'Christopher', 'Amanda', 'Matthew',
                        'Jennifer', 'Joshua', 'Elizabeth', 'Andrew', 'Heather', 'Daniel', 'Michelle', 'Ryan', 'Melissa', 'James'],
            lastNames: ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez',
                       'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White'],
            titles: ['Ms.', 'Mr.', 'Mrs.', 'Dr.', 'Prof.']
        },
        'UK': {
            firstNames: ['Emma', 'Oliver', 'Amelia', 'George', 'Ava', 'Harry', 'Isla', 'Jack', 'Mia', 'Charlie',
                        'Sophie', 'Jacob', 'Grace', 'Thomas', 'Lily', 'Oscar', 'Freya', 'William', 'Poppy', 'James'],
            lastNames: ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'Davies', 'Evans', 'Wilson', 'Thomas', 'Roberts',
                       'Johnson', 'Lewis', 'Walker', 'Robinson', 'Wood', 'Thompson', 'White', 'Watson', 'Jackson', 'Wright'],
            titles: ['Ms.', 'Mr.', 'Mrs.', 'Dr.', 'Prof.']
        },
        'Australia': {
            firstNames: ['Charlotte', 'Oliver', 'Amelia', 'William', 'Ava', 'Jack', 'Isla', 'Noah', 'Mia', 'Thomas',
                        'Grace', 'James', 'Zoe', 'Lucas', 'Lily', 'Henry', 'Sophie', 'Alexander', 'Chloe', 'Mason'],
            lastNames: ['Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White', 'Martin', 'Anderson',
                       'Thompson', 'Nguyen', 'Thomas', 'Walker', 'Harris', 'Lee', 'Ryan', 'Robinson', 'Kelly', 'King'],
            titles: ['Ms.', 'Mr.', 'Mrs.', 'Dr.', 'Prof.']
        }
    },

    // K-12 specific job titles and departments
    education: {
        jobTitles: [
            'Mathematics Teacher - Grade 10', 'English Teacher - Grade 8', 'Science Teacher - Grade 9',
            'Primary School Teacher - Grade 2', 'Primary School Teacher - Grade 4', 'History Teacher - Grade 11',
            'Physical Education Teacher', 'Art Teacher - Middle School', 'Music Teacher',
            'Chemistry Teacher - High School', 'Physics Teacher - Grade 12', 'Biology Teacher - Grade 10',
            'Computer Science Teacher', 'French Teacher - High School', 'Spanish Teacher - Middle School',
            'Mathematics Department Head', 'Science Department Head', 'English Department Head',
            'Elementary School Coordinator', 'Middle School Vice Principal', 'High School Counselor',
            'Special Education Teacher', 'Library Media Specialist', 'Drama Teacher',
            'Kindergarten Teacher', 'Grade 1 Teacher', 'Grade 3 Teacher', 'Grade 5 Teacher'
        ],
        departments: [
            'Elementary Education (K-5)', 'Middle School (6-8)', 'High School (9-12)',
            'Mathematics Department', 'Science Department', 'English Department',
            'Social Studies Department', 'Arts Department', 'Physical Education',
            'Special Education', 'Administration', 'Student Services'
        ],
        subjects: [
            'Mathematics', 'English Language Arts', 'Science', 'Biology', 'Chemistry', 'Physics',
            'Social Studies', 'History', 'Geography', 'Art', 'Music', 'Physical Education', 
            'Computer Science', 'Foreign Languages', 'Spanish', 'French', 'Drama/Theater',
            'Special Education', 'ESL/ELL'
        ],
        gradeLevels: [
            'Elementary (K-5)', 'Kindergarten', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5',
            'Middle School (6-8)', 'Grade 6', 'Grade 7', 'Grade 8',
            'High School (9-12)', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12', 'Multi-Grade'
        ],
        positionTypes: [
            'Full-time', 'Part-time', 'Substitute', 'Special Education', 'ESL/ELL',
            'Department Head', 'Lead Teacher', 'Assistant Teacher'
        ],
        experienceLevels: ['entry', 'mid', 'senior', 'master'],
        benefits: {
            health: ['Health Insurance', 'Dental Insurance', 'Vision Insurance', 'Mental Health Coverage'],
            retirement: ['403(b) Plan', 'Pension Plan', 'Teacher Retirement System', 'Social Security'],
            professional: ['Professional Development Fund', 'Conference Attendance', 'Graduate Course Reimbursement'],
            classroom: ['Classroom Supply Stipend', 'Technology Allowance', 'Book Allowance'],
            leave: ['Sick Leave', 'Personal Leave', 'Bereavement Leave', 'Maternity/Paternity Leave']
        },
        payStructures: {
            'monthly': '12-month pay',
            'academic': '10-month academic year',
            'biweekly': 'Bi-weekly payments',
            'summer': 'Summer session payments'
        }
    },

    // Academic qualifications for teachers
    qualifications: [
        'B.Ed (Bachelor of Education)', 'M.Ed (Master of Education)', 'Ph.D in Education',
        'B.A. in Teaching', 'M.A. in Subject Area', 'Teaching Certificate',
        'Special Education Certification', 'ESL Certification'
    ],

    name: {
        firstName: function() {
            const names = [
                'James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda',
                'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
                'Thomas', 'Sarah', 'Christopher', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa',
                'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
                'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle'
            ];
            return names[Math.floor(Math.random() * names.length)];
        },
        
        lastName: function() {
            const surnames = [
                'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
                'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
                'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
                'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores'
            ];
            return surnames[Math.floor(Math.random() * surnames.length)];
        },

        // Generate country-specific teacher name with title
        teacherName: function(country) {
            const countryData = faker.teacherNames[country] || faker.teacherNames['USA'];
            const title = faker.random.arrayElement(countryData.titles);
            const firstName = faker.random.arrayElement(countryData.firstNames);
            const lastName = faker.random.arrayElement(countryData.lastNames);
            return `${title} ${firstName} ${lastName}`;
        }
    },
    
    datatype: {
        number: function(options = {}) {
            const min = options.min || 0;
            const max = options.max || 100;
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }
    },
    
    random: {
        arrayElement: function(array) {
            return array[Math.floor(Math.random() * array.length)];
        }
    },

    // Generate education-specific employee ID
    generateTeacherID: function(country) {
        const year = new Date().getFullYear();
        const countryPrefix = {
            'India': 'EDU-IN',
            'USA': 'TEACH-US',
            'UK': 'EDU-UK',
            'Australia': 'EDU-AU',
            'Canada': 'EDU-CA',
            'Singapore': 'EDU-SG',
            'Philippines': 'EDU-PH'
        };
        const prefix = countryPrefix[country] || 'EDU-US';
        const id = faker.datatype.number({min: 1000, max: 9999});
        return `${prefix}-${year}-${id}`;
    },

    // Generate realistic teacher salary based on country and experience
    generateTeacherSalary: function(country, experienceLevel = 'mid') {
        const salaryRanges = {
            'India': {
                'entry': {min: 25000, max: 40000},      // ₹25,000 - ₹40,000 per month
                'mid': {min: 40000, max: 70000},        // ₹40,000 - ₹70,000 per month
                'senior': {min: 70000, max: 120000},    // ₹70,000 - ₹1,20,000 per month
                'master': {min: 120000, max: 180000}    // ₹1,20,000 - ₹1,80,000 per month
            },
            'USA': {
                'entry': {min: 3500, max: 4500},        // $3,500 - $4,500 per month
                'mid': {min: 4500, max: 6500},          // $4,500 - $6,500 per month
                'senior': {min: 6500, max: 9000},       // $6,500 - $9,000 per month
                'master': {min: 9000, max: 12000}       // $9,000 - $12,000 per month
            },
            'UK': {
                'entry': {min: 2200, max: 3000},        // £2,200 - £3,000 per month
                'mid': {min: 3000, max: 4200},          // £3,000 - £4,200 per month
                'senior': {min: 4200, max: 6000},       // £4,200 - £6,000 per month
                'master': {min: 6000, max: 8500}        // £6,000 - £8,500 per month
            },
            'Australia': {
                'entry': {min: 4500, max: 6000},        // AUD 4,500 - 6,000 per month
                'mid': {min: 6000, max: 8500},          // AUD 6,000 - 8,500 per month
                'senior': {min: 8500, max: 12000},      // AUD 8,500 - 12,000 per month
                'master': {min: 12000, max: 16000}      // AUD 12,000 - 16,000 per month
            },
            'Canada': {
                'entry': {min: 3800, max: 5000},        // CAD 3,800 - 5,000 per month
                'mid': {min: 5000, max: 7000},          // CAD 5,000 - 7,000 per month
                'senior': {min: 7000, max: 9500},       // CAD 7,000 - 9,500 per month
                'master': {min: 9500, max: 12500}       // CAD 9,500 - 12,500 per month
            },
            'Singapore': {
                'entry': {min: 3000, max: 4200},        // SGD 3,000 - 4,200 per month
                'mid': {min: 4200, max: 6000},          // SGD 4,200 - 6,000 per month
                'senior': {min: 6000, max: 8500},       // SGD 6,000 - 8,500 per month
                'master': {min: 8500, max: 11000}       // SGD 8,500 - 11,000 per month
            },
            'Philippines': {
                'entry': {min: 25000, max: 35000},      // PHP 25,000 - 35,000 per month
                'mid': {min: 35000, max: 55000},        // PHP 35,000 - 55,000 per month
                'senior': {min: 55000, max: 80000},     // PHP 55,000 - 80,000 per month
                'master': {min: 80000, max: 120000}     // PHP 80,000 - 120,000 per month
            }
        };

        const countryRanges = salaryRanges[country] || salaryRanges['USA'];
        const range = countryRanges[experienceLevel] || countryRanges['mid'];
        return faker.datatype.number(range);
    },

    // Generate realistic school district names
    generateSchoolDistrict: function(country, region = null) {
        const districts = {
            'USA': [
                'Metropolitan Public Schools', 'City Unified School District', 'County Educational Services',
                'Regional School District', 'Independent School District', 'Community School Corporation'
            ],
            'UK': [
                'Borough Council Education', 'County Council Schools', 'Academy Trust',
                'Local Education Authority', 'Multi-Academy Trust', 'Foundation Trust'
            ],
            'Canada': [
                'Public School Board', 'Catholic School Board', 'Regional School Division',
                'School District', 'Educational Services', 'Public School Division'
            ],
            'Australia': [
                'Department of Education', 'Catholic Education Office', 'Independent Schools',
                'Education Queensland', 'NSW Department of Education', 'Education Department'
            ]
        };
        
        const countryDistricts = districts[country] || districts['USA'];
        return faker.random.arrayElement(countryDistricts);
    }
};