"""
Clean, modular flow chart generator.
Uses JavaScript-based interactive flowchart with SVG prerequisite lines.
"""

import streamlit as st
from typing import Dict, List
import streamlit.components.v1 as components
from components.flow_chart_data_analyzer import FlowChartDataAnalyzer
from components.flow_chart_html_generator import FlowChartHTMLGenerator


class FlowChartGenerator:
    """Main flow chart generator class - clean and modular."""
    
    def __init__(self):
        self.data_analyzer = FlowChartDataAnalyzer()
        self.html_generator = FlowChartHTMLGenerator()
    
    def load_course_categories_for_flow(self):
        """Load course categories for the flow generator."""
        return self.data_analyzer.load_course_categories()
    
    def load_curriculum_template_for_flow(self, catalog_name: str):
        """Load curriculum template."""
        return self.data_analyzer.load_curriculum_template(catalog_name)
    
    def classify_course_for_flow(self, course_code: str, course_name: str = "", course_categories=None):
        """Classify course for flow chart."""
        return self.data_analyzer.classify_course(course_code, course_name)
    
    def _sort_courses_by_prerequisites(self, course_codes: List[str], course_categories: Dict) -> List[str]:
        """Sort courses in a semester so prerequisites and corequisites come before dependent courses."""
        if not course_codes:
            return []
        
        # Build dependency graph
        dependencies = {}  # course -> list of prerequisites in same semester
        corequisite_deps = {}  # course -> list of corequisites in same semester
        
        for code in course_codes:
            dependencies[code] = []
            corequisite_deps[code] = []
            
            if code in course_categories.get("all_courses", {}):
                course_info = course_categories["all_courses"][code]
                
                # Add prerequisites
                prereqs = list(course_info.get("prerequisites", []))
                dependencies[code] = [p for p in prereqs if p in course_codes]
                
                # Add corequisites - courses with corequisites should come AFTER their corequisites
                coreqs = list(course_info.get("corequisites", []))
                corequisite_deps[code] = [c for c in coreqs if c in course_codes]
        
        # Topological sort with corequisite ordering
        sorted_courses = []
        visited = set()
        temp_mark = set()
        
        def visit(course):
            if course in temp_mark:
                # Circular dependency - just add it
                return
            if course in visited:
                return
            
            temp_mark.add(course)
            
            # Visit prerequisites first
            for prereq in dependencies.get(course, []):
                visit(prereq)
            
            # Visit corequisites first (so they appear above this course)
            for coreq in corequisite_deps.get(course, []):
                visit(coreq)
            
            temp_mark.remove(course)
            visited.add(course)
            sorted_courses.append(course)
        
        for course in course_codes:
            if course not in visited:
                visit(course)
        
        return sorted_courses
    
    def analyze_student_progress_enhanced(self, semesters: List[Dict], template: Dict, course_categories: Dict):
        """Analyze student progress."""
        return self.data_analyzer.analyze_student_progress(semesters, template)

    def create_enhanced_template_flow_html(self, student_info: Dict, semesters: List[Dict], 
                                         validation_results: List[Dict], selected_course_data=None) -> tuple:
        """Create template-based HTML flow chart with JavaScript interactivity."""
        
        # Load data
        course_categories = self.load_course_categories_for_flow()
        curriculum_name = selected_course_data.get('curriculum_folder', 'B-IE-2565') if selected_course_data else 'B-IE-2565'
        template = self.load_curriculum_template_for_flow(curriculum_name)
        
        if not template:
            return "Error: Could not load curriculum template", 1
        
        # Analyze progress
        analysis = self.data_analyzer.analyze_student_progress(semesters, template)
        
        # Generate curriculum grid HTML
        curriculum_grid_html = ""
        
        for year_num in range(1, 5):
            year_key = f"year_{year_num}"
            year_data = template.get('core_curriculum', {}).get(year_key, {})
            
            first_semester_html = ""
            second_semester_html = ""
            
            # First semester - sort by prerequisites
            first_semester_courses = year_data.get('first_semester', [])
            sorted_first_semester = self._sort_courses_by_prerequisites(first_semester_courses, course_categories)
            for course_code in sorted_first_semester:
                course_html = self._generate_course_box_html(
                    course_code, course_categories, analysis, year_num, 1
                )
                first_semester_html += course_html
            
            # Second semester - sort by prerequisites
            second_semester_courses = year_data.get('second_semester', [])
            sorted_second_semester = self._sort_courses_by_prerequisites(second_semester_courses, course_categories)
            for course_code in sorted_second_semester:
                course_html = self._generate_course_box_html(
                    course_code, course_categories, analysis, year_num, 2
                )
                second_semester_html += course_html
            
            curriculum_grid_html += self.html_generator.generate_year_section(
                year_num, first_semester_html, second_semester_html
            )
        
        # Generate electives section
        electives_html = self.html_generator.generate_electives_section(template, analysis)
        
        # Generate complete HTML
        complete_html = self.html_generator.generate_complete_html(
            student_info, template, curriculum_grid_html, electives_html
        )
        
        return complete_html, 0
    
    def _generate_course_box_html(self, course_code: str, course_categories: Dict, 
                                  analysis: Dict, year: int, term: int) -> str:
        """Generate HTML for a single course box."""
        # Get course details
        course_name = "Unknown Course"
        credits = 0
        prerequisites = []
        corequisites = []
        
        if course_code in course_categories["all_courses"]:
            course_info = course_categories["all_courses"][course_code]
            course_name = course_info.get("name", "Unknown Course")
            prerequisites = list(course_info.get("prerequisites", []))
            corequisites = list(course_info.get("corequisites", []))
            
            # Remove duplicates
            prerequisites = list(set(prerequisites))
            corequisites = list(set(corequisites))
            
            credits_str = course_info.get("credits", "0")
            if isinstance(credits_str, str) and "(" in credits_str:
                credits = int(credits_str.split("(")[0])
            else:
                credits = int(credits_str) if str(credits_str).isdigit() else 0
        
        # Determine status
        status_class = "not-enrolled"
        grade = "Not Enrolled"
        actual_semester = ""  # เทอมที่เรียนผ่านจริง
        
        if course_code in analysis['completed_courses']:
            status_class = "passed"
            grade = analysis['completed_courses'][course_code]['grade']
            actual_semester = analysis['completed_courses'][course_code].get('semester', '')
        elif course_code in analysis['failed_courses']:
            status_class = "grade-f"
            grade = "F"
        elif course_code in analysis['withdrawn_courses']:
            status_class = "grade-w"
            grade = "W"
        elif course_code in analysis['current_courses']:
            current_grade = analysis['current_courses'][course_code]['grade']
            if current_grade == "N":
                status_class = "grade-n"
                grade = "N"
            elif current_grade == "I":
                status_class = "grade-i"
                grade = "I"
            else:
                status_class = "grade-n"
                grade = current_grade if current_grade else "In Progress"
        
        # Format prerequisites and corequisites
        prereq_str = " ".join(prerequisites) if prerequisites else ""
        coreq_str = " ".join(corequisites) if corequisites else ""
        
        return self.html_generator.generate_course_box(
            course_code, course_name, credits, status_class, grade, year, term, prereq_str, actual_semester, coreq_str
        )

    def generate_and_display_flow_chart(self, student_info: Dict, semesters: List[Dict], 
                                       validation_results: List[Dict], selected_course_data: Dict):
        """Generate and display the flow chart in Streamlit."""
        st.divider()
        st.header("Visualizations & Downloads")
        
        try:
            with st.spinner("Generating curriculum flow chart..."):
                flow_html, flow_unidentified = self.create_enhanced_template_flow_html(
                    student_info, semesters, validation_results, selected_course_data
                )
            
            st.subheader("Curriculum Flow Chart")
            st.markdown("Interactive curriculum template with progress tracking and prerequisite visualization")
            
            if flow_html and len(flow_html.strip()) > 0:
                # Auto popup - opens immediately when page loads
                auto_popup_js = f"""
                <script>
                setTimeout(function() {{
                    const flowWindow = window.open('', 'flowchart', 'width=1400,height=900,scrollbars=yes,resizable=yes');
                    if (flowWindow) {{
                        flowWindow.document.write(`{flow_html.replace('`', '\\`')}`);
                        flowWindow.document.close();
                        flowWindow.focus();
                    }}
                }}, 500);
                </script>
                """
                components.html(auto_popup_js, height=0)
                
                st.success("Flow chart opened in new window")
                if flow_unidentified > 0:
                    st.info(f"Note: {flow_unidentified} courses require classification")
                
                # Backup button in case popup was blocked
                st.download_button(
                    label="Re-open Flow Chart (if popup blocked)",
                    data=flow_html.encode('utf-8'),
                    file_name=f"curriculum_flow_{student_info.get('id', 'student')}.html",
                    mime="text/html",
                    help="Backup option if popup was blocked by browser"
                )
                
            else:
                st.error("Unable to generate flow chart")
                
        except Exception as e:
            st.error(f"Error generating flow chart: {e}")
            with st.expander("Debug Information"):
                st.code(str(e))
