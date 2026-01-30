# KU IE Course Planner Helper

Comprehensive Streamlit web app for Industrial Engineering students at Kasetsart University to plan, track, and validate their academic progress.

## Features

### 📋 Current Features
- **PDF Transcript Upload** - Extract and analyze existing course data
- **Auto-Curriculum Selection** - Automatically selects curriculum based on student ID
- **Course Validation** - Automatic prerequisite checking
- **Interactive Flow Chart** - Visual curriculum progression
- **Credit Analysis** - Track progress by course categories
- **Smart Excel Reports** - Detailed academic analysis
- **Admin Panel** - Comprehensive curriculum data management system

### 🚀 Planned Features
- **Course Recommendation Engine** - Suggest optimal course sequences
- **Semester Planning** - Interactive course selection for upcoming terms
- **Graduation Timeline** - Project completion dates and requirements
- **GPA Forecasting** - Predict academic outcomes
- **Schedule Optimization** - Avoid time conflicts and balance workload

## Quick Start

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Usage

### For Students
1. Upload PDF transcript in sidebar
2. Curriculum is automatically selected based on your student ID
3. View validation results and progress analysis
4. Download interactive reports and flow charts

### For Administrators
1. Navigate to **Admin Home** from the multipage menu
2. Login with credentials (default: username `admin`, password `admin`)
3. Use the admin panel to manage curriculum data

## Admin Panel

The admin panel provides a comprehensive curriculum data management system with the following features:

### 🏠 Admin Dashboard
- **Statistics Overview** - Total curriculums, current user status
- **Recent Curriculums** - Quick access to latest curriculum data
- **Quick Navigation** - Direct links to main features

### 📤 Upload Data
**Features:**
- CSV file upload and validation
- Automatic conversion to JSON format
- Data integrity checking
- Curriculum data storage

**Usage:**
1. Download the format template (format.csv)
2. Prepare your data according to the template
3. Upload the CSV file
4. Specify curriculum year (e.g., 2565)
5. Click **"💾 Save Data"**

### 📂 Manage Curriculums
**Features:**
- View all existing curriculums
- Inspect curriculum details and course lists
- View raw JSON files
- Delete unwanted curriculums

**Usage:**
1. Select curriculum to view
2. Expand to see detailed information
3. Use action buttons to view data or delete

### 🔐 Security Features
- **Authentication System** - Secure login required for all admin functions
- **Session Management** - Automatic logout on navigation away from admin pages
- **Password Management** - Change password functionality with strength requirements
- **Secure Storage** - Passwords stored in `.streamlit/secrets.toml` (excluded from version control)

#### Password Requirements
- At least 8 characters
- Contains digits (0-9)
- Contains lowercase letters (a-z)
- Contains uppercase letters (A-Z)
- Contains special characters (!@#$%^&* etc.)

### Admin Panel Access
1. **Start Application**: Run `streamlit run Home.py`
2. **Navigate to Admin**: Click "Admin Home" in the multipage menu
3. **Login**: Use credentials (default: username `admin`, password `admin`)
4. **Navigate**: Use sidebar menu to switch between features

## Course Data Structure

The course data has been redesigned for easier maintenance and automatic curriculum selection based on student IDs.

### Directory Structure
```
course_data/
├── B-IE-2560/
│   ├── courses.json      # Course definitions for 2560 curriculum
│   └── template.json     # Mandatory course structure for 2560
├── B-IE-2565/
│   ├── courses.json      # Course definitions for 2565 curriculum  
│   └── template.json     # Mandatory course structure for 2565
├── gen_ed_courses.json   # Shared general education courses
└── format.csv           # CSV template for data upload
```

### Auto-Selection Logic

The system automatically selects the appropriate curriculum based on student ID:

- **Student ID 65XXXXXXXX or higher** → B-IE-2565 (newest)
- **Student ID 60-64XXXXXXXX** → B-IE-2560  
- **Student ID 59XXXXXXXX or lower** → B-IE-2560 (oldest available)
- **Default (no student ID)** → B-IE-2565 (newest)

### Streamlit Interface Features

#### Auto-Selection
- ✅ **Checkbox**: "Auto-select curriculum based on Student ID" (enabled by default)
- ✅ **Smart Detection**: Automatically selects curriculum after PDF upload
- ✅ **Manual Override**: Can disable auto-selection and choose manually
- ✅ **Visual Feedback**: Shows which curriculum was auto-selected and why

#### User Experience
1. **Before PDF Upload**: Shows newest curriculum (B-IE-2565) by default
2. **After PDF Upload**: Automatically switches to appropriate curriculum based on student ID
3. **Manual Control**: User can uncheck auto-selection to choose manually
4. **Smart Re-validation**: Automatically re-validates courses when curriculum changes
5. **Manual Re-validation**: "🔄 Re-validate with this curriculum" button for manual refresh

## For Developers

### Adding a New Curriculum (e.g., B-IE-2570)

1. Create new folder: `course_data/B-IE-2570/`
2. Add two files:
   - `courses.json` (copy from existing and modify)
   - `template.json` (copy from existing and modify)
3. Update the logic in `utils/curriculum_selector.py` if needed

### Admin Panel Architecture

The admin panel uses Streamlit's multipage architecture with the following structure:

```
pages/
└── Admin_Home.py          # Main admin interface with sidebar navigation
```

**Key Components:**
- **Single Page Design** - All admin functions in one page with sidebar navigation
- **Session Management** - Secure authentication and session handling
- **Component Integration** - Reuses existing `components/admin_*` modules
- **Responsive UI** - Clean interface with gradient styling and intuitive navigation

### Usage Examples

```python
from utils.curriculum_selector import get_curriculum_for_student_id
from utils.course_data_loader import load_curriculum_data

# Auto-select curriculum for a student
curriculum = get_curriculum_for_student_id("6512345678")  # Returns "B-IE-2565"

# Load complete curriculum data
data = load_curriculum_data(student_id="6512345678")
courses = data['courses']
template = data['template']

# Load specific curriculum
data = load_curriculum_data("B-IE-2560")
```

### Benefits of Current Structure

- ✅ **Simple**: Only 2 levels deep, clear naming
- ✅ **Automatic**: Student ID-based curriculum selection
- ✅ **Concurrent**: Multiple curricula can be active simultaneously
- ✅ **Easy Updates**: Just replace files in the relevant folder
- ✅ **No Config**: No configuration files to maintain
- ✅ **Backward Compatible**: Existing functionality preserved
- ✅ **Admin Friendly**: Easy-to-use web interface for data management

## Troubleshooting

### Common Issues

**1. Cannot Login to Admin Panel**
- Check username and password (default: admin/admin)
- Try refreshing the web page
- Check if `.streamlit/secrets.toml` file exists with admin credentials
- If migrating from old version, the system will automatically detect legacy `admin_password.txt`

**2. CSV Upload Fails**
- Verify file format matches format.csv template
- Check file encoding (should be UTF-8)
- Ensure all required columns are present

**3. Curriculums Not Displaying**
- Check `course_data` folder structure
- Verify `courses.json` and `template.json` files exist
- Refresh the web page

**4. Auto-Selection Not Working**
- Ensure PDF contains readable student ID
- Check if student ID follows expected format
- Try manual curriculum selection as fallback

## File Structure

```
├── Home.py                # Main application
├── pages/
│   └── Admin_Home.py     # Admin panel interface
├── validator.py          # Course validation logic
├── components/           # Reusable components
│   ├── admin_auth.py    # Authentication system
│   ├── admin_upload.py  # File upload handling
│   ├── admin_manage.py  # Curriculum management
│   └── ...
├── course_data/         # Course catalogs (JSON)
│   ├── B-IE-2560/      # 2560 curriculum data
│   ├── B-IE-2565/      # 2565 curriculum data
│   └── format.csv      # Upload template
└── utils/              # PDF processing & utilities
    ├── curriculum_selector.py
    └── course_data_loader.py
```

## Requirements

- Python 3.8+
- Streamlit
- PyPDF2
- Pandas
- OpenPyXL

---
*Comprehensive academic planning tool for KU Industrial Engineering students with administrative data management capabilities*
