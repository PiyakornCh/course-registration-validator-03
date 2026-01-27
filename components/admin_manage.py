"""
Management module for viewing and deleting curriculums
"""
import streamlit as st
import pandas as pd
import json
import os
import shutil

def get_existing_curriculums():
    """Get list of existing curriculums"""
    course_data_path = "course_data"
    if not os.path.exists(course_data_path):
        return []
    
    curriculums = []
    for item in os.listdir(course_data_path):
        item_path = os.path.join(course_data_path, item)
        if os.path.isdir(item_path) and item.startswith("B-IE-"):
            curriculums.append(item)
    
    return sorted(curriculums)

def delete_curriculum(curriculum_name):
    """Delete curriculum"""
    folder_path = os.path.join("course_data", curriculum_name)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        return True
    return False

def render_manage_page():
    """Render the manage curriculums page"""
    st.header("📂 Manage Curriculums")
    st.markdown("View, inspect, and delete existing curriculums")
    
    curriculums = get_existing_curriculums()
    
    if not curriculums:
        st.info("ℹ️ No curriculums found in the system")
    else:
        st.subheader(f"Available Curriculums ({len(curriculums)})")
        
        # Display curriculum list
        for curriculum in curriculums:
            with st.expander(f"📚 {curriculum}", expanded=False):
                folder_path = os.path.join("course_data", curriculum)
                
                # Read courses.json
                courses_file = os.path.join(folder_path, "courses.json")
                template_file = os.path.join(folder_path, "template.json")
                
                if os.path.exists(courses_file):
                    with open(courses_file, 'r', encoding='utf-8') as f:
                        courses_data = json.load(f)
                    
                    # Read template.json for elective requirements and core curriculum
                    elective_reqs = {}
                    core_course_codes = set()
                    
                    if os.path.exists(template_file):
                        with open(template_file, 'r', encoding='utf-8') as f:
                            template_data = json.load(f)
                            elective_reqs = template_data.get('elective_requirements', {})
                            
                            # Extract all course codes from core_curriculum
                            core_curriculum = template_data.get('core_curriculum', {})
                            for year_key, year_data in core_curriculum.items():
                                for semester_key, course_list in year_data.items():
                                    core_course_codes.update(course_list)
                    
                    # Display total courses (all courses in courses.json)
                    total_courses = len(courses_data.get('industrial_engineering_courses', []))
                    st.metric("Total Courses", total_courses)
                    
                    # Display elective requirements
                    if elective_reqs:
                        st.markdown("**Elective Requirements:**")
                        elective_cols = st.columns(5)
                        idx = 0
                        for req_name, req_value in elective_reqs.items():
                            with elective_cols[idx % 5]:
                                # Format name for display
                                display_name = req_name.replace('_', ' ').title()
                                st.metric(display_name, req_value)
                            idx += 1
                        st.markdown("---")
                    
                    # Display courses in table (all courses in order from courses.json)
                    st.markdown("**Course List:**")
                    courses_list = []
                    
                    # Show all courses in the same order as courses.json (no sorting)
                    for course in courses_data['industrial_engineering_courses']:
                        tech_elec = "Yes" if course.get('technical_electives', False) else "No"
                        courses_list.append({
                            "Code": course['code'],
                            "Course Name": course['name'],
                            "Credits": course['credits'],
                            "Technical Elective": tech_elec,
                            "Prerequisites": ", ".join(course['prerequisites']) if course['prerequisites'] else "-",
                            "Corequisites": ", ".join(course['corequisites']) if course['corequisites'] else "-"
                        })
                    
                    df_courses = pd.DataFrame(courses_list)
                    st.dataframe(df_courses, use_container_width=True, height=300)
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📄 View courses.json", key=f"view_courses_{curriculum}"):
                            st.json(courses_data)
                    
                    with col2:
                        if os.path.exists(template_file):
                            if st.button(f"📄 View template.json", key=f"view_template_{curriculum}"):
                                with open(template_file, 'r', encoding='utf-8') as f:
                                    template_data = json.load(f)
                                st.json(template_data)
                    
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_{curriculum}", type="secondary"):
                            if st.session_state.get(f"confirm_delete_{curriculum}", False):
                                if delete_curriculum(curriculum):
                                    st.success(f"✅ Deleted {curriculum} successfully")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to delete curriculum")
                            else:
                                st.session_state[f"confirm_delete_{curriculum}"] = True
                                st.warning("⚠️ Click again to confirm deletion")
                else:
                    st.error("❌ courses.json not found")
