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
            'Mathematics', 'English Language Arts', 'Science', 'Social Studies', 'Art',
            'Music', 'Physical Education', 'Computer Science', 'Foreign Languages',
            'Chemistry', 'Physics', 'Biology', 'History', 'Geography', 'Drama'
        ]
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
                'entry': {min: 25000, max: 40000},    // ₹25,000 - ₹40,000 per month
                'mid': {min: 40000, max: 70000},      // ₹40,000 - ₹70,000 per month
                'senior': {min: 70000, max: 120000}   // ₹70,000 - ₹1,20,000 per month
            },
            'USA': {
                'entry': {min: 3500, max: 4500},      // $3,500 - $4,500 per month
                'mid': {min: 4500, max: 6500},        // $4,500 - $6,500 per month
                'senior': {min: 6500, max: 9000}      // $6,500 - $9,000 per month
            },
            'UK': {
                'entry': {min: 2200, max: 3000},      // £2,200 - £3,000 per month
                'mid': {min: 3000, max: 4200},        // £3,000 - £4,200 per month
                'senior': {min: 4200, max: 6000}      // £4,200 - £6,000 per month
            },
            'Australia': {
                'entry': {min: 4500, max: 6000},      // AUD 4,500 - 6,000 per month
                'mid': {min: 6000, max: 8500},        // AUD 6,000 - 8,500 per month
                'senior': {min: 8500, max: 12000}     // AUD 8,500 - 12,000 per month
            }
        };

        const countryRanges = salaryRanges[country] || salaryRanges['USA'];
        const range = countryRanges[experienceLevel] || countryRanges['mid'];
        return faker.datatype.number(range);
    }
};