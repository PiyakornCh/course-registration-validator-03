import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from components.session_manager import SessionManager
from components.ui_components import UIComponents
import re

class CourseAnalyzer:
    """Handles course analysis and classification."""
    
    def __init__(self):
        self.course_categories = None
    
    def load_course_categories(self) -> Dict:
        """FUTURE-PROOF VERSION: Load course categories from separate JSON files."""
        course_data_dir = Path(__file__).parent.parent / "course_data"
        
        categories = {
            "ie_core": {},
            "technical_electives": {},
            "gen_ed": {
                "wellness": {},
                "wellness_PE": {},
                "entrepreneurship": {},
                "language_communication_thai": {},
                "language_communication_foreigner": {},
                "language_communication_computer": {},
                "thai_citizen_global": {},
                "aesthetics": {}
            },
            "all_courses": {}
        }
        
        # FUTURE-PROOF: Find all B-IE files dynamically
        ie_files = []
        if course_data_dir.exists():
            for json_file in course_data_dir.glob("**/courses.json"):
                # Extract year from parent directory name (e.g., B-IE-2560)
                parent_dir = json_file.parent.name
                year_match = re.search(r'B-IE-(\d{4})', parent_dir)
                if year_match:
                    year = int(year_match.group(1))
                    ie_files.append((year, json_file))
        
        # Sort by year (newest first) and process
        ie_files.sort(key=lambda x: x[0], reverse=True)
        
        # Load IE Core courses from available B-IE files
        for year, ie_file in ie_files:
            try:
                with open(ie_file, 'r', encoding='utf-8') as f:
                    ie_data = json.load(f)
                    
                    # Process industrial_engineering_courses
                    for course in ie_data.get("industrial_engineering_courses", []):
                        if course["code"] not in categories["all_courses"]:
                            if course.get("technical_electives", False):
                                categories["technical_electives"][course["code"]] = course
                            else:
                                categories["ie_core"][course["code"]] = course
                            categories["all_courses"][course["code"]] = course
                    
                    # Process other_related_courses
                    for course in ie_data.get("other_related_courses", []):
                        if course["code"] not in categories["all_courses"]:
                            categories["ie_core"][course["code"]] = course  
                            categories["all_courses"][course["code"]] = course
                            
            except Exception as e:
                print(f"Error loading {ie_file}: {e}")
                continue
        
        # Load Gen-Ed courses (unchanged)
        gen_ed_file = course_data_dir / "gen_ed_courses.json"
        if gen_ed_file.exists():
            try:
                with open(gen_ed_file, 'r', encoding='utf-8') as f:
                    gen_ed_data = json.load(f)
                    gen_ed_courses = gen_ed_data.get("gen_ed_courses", {})
                    # Handle all gen_ed subcategories dynamically
                    for subcategory, courses_list in gen_ed_courses.items():
                        if subcategory in categories["gen_ed"]:
                            for course in courses_list:
                                categories["gen_ed"][subcategory][course["code"]] = course
                                categories["all_courses"][course["code"]] = course
            except Exception as e:
                print(f"Error loading gen_ed_courses.json: {e}")
        
        self.course_categories = categories
        return categories
    
    def classify_course(self, course_code: str, course_name: str = "", 
                       course_categories: Optional[Dict] = None) -> Tuple[str, str, bool]:
        """
        Classify course into appropriate category.
        PRIORITY ORDER: Gen-Ed → Technical Electives → IE Core → Free Electives
        
        ENHANCED: Now supports configurable technical elective prefixes
        """
        if course_categories is None:
            if self.course_categories is None:
                self.course_categories = self.load_course_categories()
            course_categories = self.course_categories
        
        code = course_code.upper()
        
        # PRIORITY 1: Check Gen-Ed courses FIRST (highest priority)
        for subcategory, courses in course_categories["gen_ed"].items():
            if code in courses:
                return ("gen_ed", subcategory, True)
        
        # PRIORITY 2: Check Technical Electives (from database)
        if code in course_categories["technical_electives"]:
            return ("technical_electives", "technical", True)
        
        # PRIORITY 3: Check IE Core courses
        if code in course_categories["ie_core"]:
            return ("ie_core", "core", True)
        
        # PRIORITY 4: Check Technical Electives by prefix (configurable)
        technical_elective_prefixes = self._get_technical_elective_prefixes()
        
        for prefix in technical_elective_prefixes:
            if code.startswith(prefix):
                return ("technical_electives", "technical", False)  # False = not in database but classified by prefix
        
        # PRIORITY 5: Everything else is free elective (not in our database)
        return ("free_electives", "free", False)  # False = not identified in database
    
    def analyze_unidentified_courses(self, semesters: List[Dict], template=None) -> List[Dict]:
        """
        Analyze transcript for truly unidentified courses.
        
        UPDATED LOGIC:
        - Courses in template = mandatory courses (not unidentified)
        - Courses with "01206" prefix not in template = technical electives (not unidentified)  
        - Only other courses are truly unidentified
        """
        if self.course_categories is None:
            self.course_categories = self.load_course_categories()
        
        # Get all courses from template if provided
        template_courses = set()
        if template:
            for year_data in template.get('core_curriculum', {}).values():
                for course_codes in year_data.values():
                    template_courses.update(course_codes)
        
        # Get technical elective prefixes
        technical_prefixes = self._get_technical_elective_prefixes()
        
        unidentified_courses = []
        
        try:
            for semester in semesters:
                for course in semester.get("courses", []):
                    course_code = course.get("code", "")
                    course_name = course.get("name", "")
                    
                    if course_code:
                        # Check if course is in template (mandatory course)
                        if course_code in template_courses:
                            continue  # Not unidentified - it's a mandatory course
                        
                        # Check if course has technical elective prefix
                        is_technical_by_prefix = any(course_code.upper().startswith(prefix) 
                                                   for prefix in technical_prefixes)
                        if is_technical_by_prefix:
                            continue  # Not unidentified - it's a technical elective by prefix
                        
                        # Check if course is in our database
                        category, subcategory, is_identified = self.classify_course(
                            course_code, course_name, self.course_categories
                        )
                        
                        # Only count as unidentified if not in database AND not covered by above rules
                        if not is_identified:
                            unidentified_courses.append({
                                "code": course_code,
                                "name": course_name,
                                "semester": semester.get("semester", ""),
                                "credits": course.get("credits", 0),
                                "grade": course.get("grade", "")
                            })
        except Exception as e:
            st.error(f"Error analyzing courses: {e}")
        
        return unidentified_courses
    
    def calculate_credit_summary(self, semesters: List[Dict]) -> Dict:
        """
        Calculate credit summary by category.
        FIXED: Now properly handles technical electives from B-IE files.
        """
        if self.course_categories is None:
            self.course_categories = self.load_course_categories()
        
        try:
            summary = {
                "ie_core": 0,
                "wellness": 0,
                "wellness_PE": 0,
                "entrepreneurship": 0,
                "language_communication_thai": 0,
                "language_communication_foreigner": 0,
                "language_communication_computer": 0,
                "thai_citizen_global": 0,
                "aesthetics": 0,
                "technical_electives": 0,
                "free_electives": 0,
                "unidentified": 0
            }
            
            for semester in semesters:
                for course in semester.get("courses", []):
                    course_code = course.get("code", "")
                    course_name = course.get("name", "")
                    grade = course.get("grade", "")
                    credits = course.get("credits", 0)
                    
                    # Only count completed courses
                    if grade in ["A", "B+", "B", "C+", "C", "D+", "D"]:
                        category, subcategory, is_identified = self.classify_course(
                            course_code, course_name, self.course_categories
                        )
                        
                        if category == "ie_core":
                            summary["ie_core"] += credits
                        elif category == "gen_ed":
                            # Handle gen-ed subcategories safely
                            if subcategory in summary:
                                summary[subcategory] += credits
                            else:
                                # Fallback for unknown gen-ed subcategories
                                summary["free_electives"] += credits
                        elif category == "technical_electives":
                            summary["technical_electives"] += credits
                        elif category == "unidentified":
                            summary["unidentified"] += credits
                        else:
                            summary["free_electives"] += credits
            
            return summary
        except Exception as e:
            st.error(f"Error calculating credit summary: {e}")
            return {}
    
    def analyze_and_display_courses(self, semesters: List[Dict], template=None):
        """Analyze courses and display results."""
        session_manager = SessionManager()
        
        # Load course categories if not already loaded
        if self.course_categories is None:
            self.course_categories = self.load_course_categories()
            session_manager.set_course_categories(self.course_categories)
        
        # Analyze unidentified courses with template context
        unidentified_courses = self.analyze_unidentified_courses(semesters, template)
        session_manager.set_unidentified_count(len(unidentified_courses))
        
        # Calculate and display credit summary
        credit_summary = self.calculate_credit_summary(semesters)
        UIComponents.display_credit_summary(credit_summary)
    
    def _get_technical_elective_prefixes(self):
        """
        Get configurable technical elective prefixes.
        Loads from configuration file with fallback to defaults.
        """
        try:
            config_file = Path(__file__).parent.parent / "course_data" / "technical_elective_config.json"
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get("technical_elective_prefixes", ["01206"])
        except Exception as e:
            print(f"Warning: Could not load technical elective config: {e}")
        
        # Fallback to default prefixes
        return ["01206"]
