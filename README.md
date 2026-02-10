# KU IE Course Validator & Academic Planner

A comprehensive web application for Industrial Engineering students at Kasetsart University to validate course prerequisites, track academic progress, and plan their curriculum path to graduation.

## 🎯 Overview

This Streamlit-based application analyzes transcript PDFs, validates course prerequisites, tracks graduation progress, and generates interactive curriculum visualizations to help IE students plan their academic journey.

## ✨ Key Features

### 📄 PDF Transcript Processing
- **Automatic Extraction**: Upload official transcript PDF for instant data extraction
- **Smart Parsing**: Advanced pattern matching handles various transcript formats
- **Student Info Detection**: Automatically extracts student ID, name, and admission details

### 🎓 Curriculum Management
- **Auto-Selection**: Automatically selects correct curriculum based on student ID
  - Student ID 65XXXXXXXX → B-IE-2565 curriculum
  - Student ID 60-64XXXXXXXX → B-IE-2560 curriculum
  - Student ID 59XXXXXXXX or lower → B-IE-2560 curriculum
- **Manual Override**: Option to manually select curriculum
- **Multi-Curriculum Support**: Supports multiple curriculum versions simultaneously

### ✅ Course Validation
- **Prerequisite Checking**: Validates prerequisites were completed before enrollment
- **Corequisite Validation**: Ensures corequisites are taken in same semester
- **Credit Limit Validation**: Checks semester credit loads (22 credits regular, 9 summer)
- **Propagation Analysis**: Identifies cascading effects of invalid registrations

### 📊 Progress Tracking
- **Category Analysis**: Tracks credits by course category
  - IE Core courses
  - Technical Electives
  - General Education (Wellness, Language, Entrepreneurship, etc.)
  - Free Electives
- **Completion Metrics**: Visual progress bars showing completion percentage
- **GPA Calculation**: Automatic GPA calculation from completed courses
- **Deviation Detection**: Identifies courses taken outside standard timeline

### 🗺️ Interactive Flow Chart
- **Visual Curriculum Map**: Interactive HTML flow chart by year and semester
- **Prerequisite Lines**: Visual connections showing course dependencies
- **Hover Details**: Detailed course information on hover
- **Downloadable**: Export as standalone HTML file

### 📋 Comprehensive Reports
- **Academic Progress Report**: Detailed HTML report with
  - Executive summary with key metrics
  - Progress timeline by semester
  - Course completion analysis by category
  - Validation issues and recommendations
  - Graduation requirements status
  - Next semester planning suggestions
- **Validation Report**: Text-based prerequisite validation details
- **Raw Data Export**: JSON export of all extracted and validated data


## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run Home.py
```

### Requirements
- Python 3.8+
- Streamlit >= 1.28.0
- PyPDF2 >= 3.0.0
- openpyxl >= 3.1.0
- pandas >= 2.0.0

## 📖 Usage Guide

### For Students

1. **Upload Transcript**
   - Click "Browse files" in sidebar
   - Select official transcript PDF
   - Wait for automatic processing

2. **Review Results**
   - Check validation results for prerequisite violations
   - Review credit progress by category
   - Examine interactive flow chart

3. **Download Reports**
   - 📋 Comprehensive Report: Detailed academic analysis
   - 🗂️ Flow Chart (HTML): Interactive curriculum visualization
   - 📄 Validation Report: Text-based prerequisite validation
   - 💾 Raw Data (JSON): Complete extracted data

### For Administrators

1. **Access Admin Panel**
   - Navigate to "Admin Home" from sidebar

2. **Upload New Curriculum Data**
   - Download format template (upload_courses_format.csv)
   - Prepare curriculum data
   - Upload CSV file and specify curriculum year
   - System automatically converts to JSON format

3. **Manage Existing Curriculums**
   - View all available curriculums
   - Inspect course lists and requirements
   - View raw JSON data
   - Delete outdated curriculums

## 📁 Project Structure

```
├── Home.py                          # Main application entry point
├── pages/
│   └── Admin_Home.py               # Admin panel interface
├── components/                      # Modular components
│   ├── admin_auth.py               # Authentication system
│   ├── admin_upload.py             # File upload handling
│   ├── admin_manage.py             # Curriculum management
│   ├── admin_panel.py              # Admin panel UI
│   ├── course_analyzer.py          # Course classification & analysis
│   ├── flow_chart_generator.py     # Flow chart generation
│   ├── flow_chart_data_analyzer.py # Flow chart data processing
│   ├── flow_chart_html_generator.py # Flow chart HTML rendering
│   ├── report_generator.py         # Report generation
│   ├── comprehensive_report_generator.py # Detailed academic reports
│   ├── session_manager.py          # Session state management
│   └── ui_components.py            # Reusable UI components
├── utils/                          # Utility modules
│   ├── pdf_processor.py            # PDF text extraction
│   ├── pdf_extractor.py            # Transcript data parsing
│   ├── course_data_loader.py       # Course data loading
│   ├── curriculum_selector.py      # Auto curriculum selection
│   └── excel_generator.py          # Excel report generation
├── course_data/                    # Course catalogs
│   ├── B-IE-2560/                  # 2560 curriculum
│   │   ├── courses.json            # Course definitions
│   │   └── template.json           # Curriculum structure
│   ├── B-IE-2565/                  # 2565 curriculum
│   │   ├── courses.json
│   │   └── template.json
│   ├── gen_ed_courses.json         # General education courses
│   ├── technical_elective_config.json # Technical elective configuration
│   └── [Removed - moved to example_files/]
├── example_files/                  # Example and template files
│   └── upload_courses_format.csv   # CSV upload template
├── validator.py                    # Core validation logic
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🎨 Features in Detail

### Course Classification System

Priority-based classification:

1. **General Education** (Highest Priority)
   - Wellness & PE
   - Entrepreneurship
   - Thai Language & Communication
   - English Language & Communication
   - Thai Citizen & Global Awareness
   - Aesthetics

2. **Technical Electives**
   - Courses marked as technical electives in database
   - Courses with configurable prefixes (default: 01206)

3. **IE Core**
   - Required Industrial Engineering courses
   - Related courses from other departments

4. **Free Electives** (Lowest Priority)
   - Any course not classified above

### Validation Logic

The validator checks:
- **Prerequisites**: All required courses completed before enrollment
- **Corequisites**: Required courses taken in same semester
- **Credit Limits**: 
  - Regular semester: 22 credits maximum
  - Summer session: 9 credits maximum
- **Grade Requirements**: Minimum passing grades for prerequisites
- **Propagation**: Cascading effects of invalid registrations

**Note**: This application is designed specifically for Kasetsart University Industrial Engineering students. Curriculum data and validation rules are based on official university requirements but should be verified with academic advisors for official guidance.
