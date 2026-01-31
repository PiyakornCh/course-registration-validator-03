import json
from pathlib import Path
from .curriculum_selector import get_curriculum_for_student_id, get_available_curricula

def load_comprehensive_course_data():
    """
    Load all course data from new folder structure.
    """
    course_data_dir = Path(__file__).parent.parent / "course_data"
    available_files = {}
    
    if course_data_dir.exists():
        # Get available curricula from folder structure (newest first for UI)
        curricula = get_available_curricula()
        curricula.sort(reverse=True)  # Sort newest first for UI display
        
        # Process each curriculum folder
        for curriculum in curricula:
            curriculum_dir = course_data_dir / curriculum
            courses_file = curriculum_dir / "courses.json"
            
            if courses_file.exists():
                try:
                    with open(courses_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Validate that the file contains course data
                    has_courses = (
                        'industrial_engineering_courses' in data or
                        'gen_ed_courses' in data or
                        'other_related_courses' in data
                    )
                    
                    if has_courses:
                        available_files[curriculum] = {
                            'data': data,
                            'filename': f"{curriculum}/courses.json",
                            'path': str(courses_file),
                            'curriculum_folder': curriculum
                        }
                except Exception as e:
                    print(f"Error loading {courses_file}: {e}")
                    continue
    
    return available_files

def load_curriculum_data(curriculum_name: str = None, student_id: str = None):
    """
    Load curriculum data with auto-selection based on student ID.
    
    Args:
        curriculum_name: Specific curriculum to load (e.g., "B-IE-2565")
        student_id: Student ID for auto-selection (e.g., "6512345678")
    
    Returns:
        Dictionary with curriculum data and template
    """
    course_data_dir = Path(__file__).parent.parent / "course_data"
    
    # Determine which curriculum to use
    if curriculum_name:
        selected_curriculum = curriculum_name
    elif student_id:
        selected_curriculum = get_curriculum_for_student_id(student_id)
    else:
        selected_curriculum = get_curriculum_for_student_id("")  # Gets newest
    
    curriculum_dir = course_data_dir / selected_curriculum
    courses_file = curriculum_dir / "courses.json"
    template_file = curriculum_dir / "template.json"
    
    result = {
        'curriculum_name': selected_curriculum,
        'courses': None,
        'template': None,
        'error': None
    }
    
    # Load courses
    if courses_file.exists():
        try:
            with open(courses_file, 'r', encoding='utf-8') as f:
                result['courses'] = json.load(f)
        except Exception as e:
            result['error'] = f"Error loading courses: {e}"
    else:
        result['error'] = f"Courses file not found: {courses_file}"
    
    # Load template
    if template_file.exists():
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                result['template'] = json.load(f)
        except Exception as e:
            result['error'] = f"Error loading template: {e}"
    else:
        result['error'] = f"Template file not found: {template_file}"
    
    return result
