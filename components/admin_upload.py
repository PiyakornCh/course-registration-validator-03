"""
Upload and processing module for CSV to JSON conversion
"""
import streamlit as st
import pandas as pd
import json
import os
import re
from components.admin_manage import get_existing_curriculums

def csv_to_json(df, year):
    """Convert CSV to JSON format according to the structure"""
    courses = []
    
    for _, row in df.iterrows():
        # Convert Course Code to 8-digit format
        code = str(row['Code']).strip()
        # Remove .0 if present
        if code.endswith('.0'):
            code = code[:-2]
        if len(code) == 7:
            code = '0' + code
        
        # Handle Prerequisites
        prereq_str = str(row['Prerequisites']).strip()
        prerequisites = []
        if prereq_str and prereq_str != 'nan' and prereq_str != '' and prereq_str != '-':
            # Split prerequisites by comma or semicolon
            prereqs = [p.strip() for p in prereq_str.replace(';', ',').split(',')]
            for p in prereqs:
                # Remove .0 if present
                if p.endswith('.0'):
                    p = p[:-2]
                if len(p) == 7:
                    p = '0' + p
                prerequisites.append(p)
        
        # Handle Corequisites
        coreq_str = str(row['Corequisites']).strip()
        corequisites = []
        if coreq_str and coreq_str != 'nan' and coreq_str != '' and coreq_str != '-':
            # Split corequisites by comma or semicolon
            coreqs = [c.strip() for c in coreq_str.replace(';', ',').split(',')]
            for c in coreqs:
                # Remove .0 if present
                if c.endswith('.0'):
                    c = c[:-2]
                if len(c) == 7:
                    c = '0' + c
                corequisites.append(c)
        
        # Create credits format
        credits_value = str(row['Credits']).strip()
        # Remove .0 from credits if present
        if credits_value.endswith('.0'):
            credits_value = credits_value[:-2]
        
        # Check if Technical Elective
        tech_elective = str(row.get('Technical Elective', 'No')).strip().lower() in ['yes', 'true', '1']
        
        course = {
            "code": code,
            "name": str(row['Name']).strip(),
            "credits": credits_value,
            "prerequisites": prerequisites,
            "corequisites": corequisites
        }
        
        # Add technical_electives flag if Yes
        if tech_elective:
            course["technical_electives"] = True
        
        courses.append(course)
    
    return {
        "industrial_engineering_courses": courses
    }

def create_template_json(df, year):
    """Create template.json from CSV data with inline array format"""
    # Group by year and semester
    year_semester_map = {}
    
    # Parse elective requirements from CSV
    elective_requirements = {
        "free_electives": 6,
        "technical_electives": 12,
        "wellness": 6,
        "wellness_PE": 1,
        "entrepreneurship": 3,
        "thai_citizen_global": 3,
        "language_communication_thai": 3,
        "language_communication_foreigner": 9,
        "language_communication_computer": 3,
        "aesthetics": 3
    }
    
    # Check if CSV has Elective Requirements columns
    if 'Elective Requirements' in df.columns and 'TotalCredits' in df.columns:
        # Extract elective requirements from CSV
        for _, row in df.iterrows():
            req_name = str(row['Elective Requirements']).strip()
            req_value = str(row['TotalCredits']).strip()
            
            if req_name and req_name != 'nan' and req_name != '' and req_value and req_value != 'nan' and req_value != '':
                try:
                    elective_requirements[req_name] = int(float(req_value))
                except:
                    pass
    
    for _, row in df.iterrows():
        code = str(row['Code']).strip()
        # Remove .0 if present
        if code.endswith('.0'):
            code = code[:-2]
        if len(code) == 7:
            code = '0' + code
        
        # Handle Year and Semester - skip if empty or NaN
        year_str = str(row['Year']).strip()
        semester_str = str(row['Semester']).strip()
        
        # Skip rows without Year or Semester (elective requirement rows or empty rows)
        if not year_str or year_str == 'nan' or year_str == '' or not semester_str or semester_str == 'nan' or semester_str == '':
            continue
        
        try:
            year_num = int(float(year_str))
            semester = int(float(semester_str))
        except (ValueError, TypeError):
            continue
        
        year_key = f"year_{year_num}"
        semester_key = "first_semester" if semester == 1 else "second_semester"
        
        if year_key not in year_semester_map:
            year_semester_map[year_key] = {}
        if semester_key not in year_semester_map[year_key]:
            year_semester_map[year_key][semester_key] = []
        
        year_semester_map[year_key][semester_key].append(code)
    
    # Sort year_semester_map by year number (year_1, year_2, year_3, year_4)
    sorted_year_semester_map = {}
    for year_key in sorted(year_semester_map.keys(), key=lambda x: int(x.split('_')[1])):
        sorted_year_semester_map[year_key] = year_semester_map[year_key]
    
    template = {
        "curriculum_name": f"B-IE-{year}",
        "core_curriculum": sorted_year_semester_map,
        "elective_requirements": elective_requirements
    }
    
    return template

def save_course_data(courses_json, template_json, year):
    """Save data to course_data folder"""
    folder_name = f"B-IE-{year}"
    folder_path = os.path.join("course_data", folder_name)
    
    # Create folder if not exists
    os.makedirs(folder_path, exist_ok=True)
    
    # Save courses.json
    with open(os.path.join(folder_path, "courses.json"), 'w', encoding='utf-8') as f:
        json.dump(courses_json, f, ensure_ascii=False, indent=2)
    
    # Save template.json with custom formatting (inline arrays)
    template_str = json.dumps(template_json, ensure_ascii=False, indent=2)
    # Keep arrays on single line for course codes
    # Find arrays of course codes and put them on one line
    def format_array(match):
        array_content = match.group(1)
        # Remove newlines and extra spaces within the array
        formatted = re.sub(r'\s+', ' ', array_content).strip()
        # Remove trailing comma and space before closing bracket
        formatted = re.sub(r',\s*$', '', formatted)
        return f'[{formatted}]'
    
    # Match arrays that contain course codes (strings starting with digits)
    template_str = re.sub(r'\[\s*((?:"[^"]*",?\s*)+)\s*\]', format_array, template_str)
    
    with open(os.path.join(folder_path, "template.json"), 'w', encoding='utf-8') as f:
        f.write(template_str)
    
    return folder_path

def render_upload_page():
    """Render the upload page"""
    # Header with download button on the same line
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("📤 Upload CSV File")
    with col2:
        try:
            with open("course_data/format.csv", "r", encoding="utf-8") as f:
                format_csv_content = f.read()
            
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing to align with header
            st.download_button(
                label="📥 Download Format",
                data=format_csv_content,
                file_name="format.csv",
                mime="text/csv",
                help="Download the CSV format template",
                type="secondary",
                use_container_width=True
            )
        except FileNotFoundError:
            st.info("💡 format.csv not found in course_data folder")
    
    st.markdown("Upload your course curriculum CSV file to convert it to JSON format")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="File must follow the format specified in format.csv (available for download above)"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV file with specific dtypes to prevent float conversion
            df = pd.read_csv(uploaded_file, dtype={
                'Code': str,
                'Prerequisites': str,
                'Corequisites': str,
                'Credits': str,
                'Technical Elective': str,
                'Year': str,
                'Semester': str,
                'Elective Requirements': str,
                'TotalCredits': str
            })
            
            # Check required columns
            required_columns = ['Code', 'Name', 'Credits', 'Technical Elective', 'Prerequisites', 'Corequisites', 'Year', 'Semester', 'Elective Requirements', 'TotalCredits']
            
            if all(col in df.columns for col in required_columns):
                st.success("✅ File read successfully!")
                
                st.markdown("---")
                # Specify curriculum year
                st.subheader("📅 Specify Curriculum Year")
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    year = st.text_input(
                        "Curriculum Year (e.g., 2560, 2565)",
                        max_chars=4,
                        help="Enter the Buddhist Era year of the curriculum"
                    )
                
                if year and year.isdigit() and len(year) == 4:
                    curriculum_name = f"B-IE-{year}"
                    
                    with col2:
                        st.info(f"📚 Curriculum: **{curriculum_name}**")
                    
                    # Check if curriculum exists
                    existing = get_existing_curriculums()
                    if curriculum_name in existing:
                        st.warning(f"⚠️ Curriculum {curriculum_name} already exists. Saving will overwrite existing data.")
                    
                    # Save button
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("💾 Save Data", type="primary", use_container_width=True):
                            with st.spinner("Processing and saving data..."):
                                # Convert to JSON
                                courses_json = csv_to_json(df, year)
                                template_json = create_template_json(df, year)
                                
                                # Save to folder
                                folder_path = save_course_data(courses_json, template_json, year)
                                
                                st.success(f"✅ Data saved successfully!")
                                st.success(f"📁 Location: {folder_path}")
                                
                                # Show generated JSON
                                with st.expander("📄 View generated courses.json"):
                                    st.json(courses_json)
                                
                                with st.expander("📄 View generated template.json"):
                                    st.json(template_json)
                
                elif year:
                    st.error("❌ Please enter a valid 4-digit year")

                # Preview Data at the bottom
                st.subheader("📋 Preview Data")
                # Show metrics first
                st.metric("Total Courses", len(df))
                # Extract and display Elective Requirements
                elective_reqs = {}
                if 'Elective Requirements' in df.columns and 'TotalCredits' in df.columns:
                    for _, row in df.iterrows():
                        req_name = str(row['Elective Requirements']).strip()
                        req_value = str(row['TotalCredits']).strip()
                        
                        if req_name and req_name != 'nan' and req_name != '' and req_value and req_value != 'nan' and req_value != '':
                            try:
                                # Format name for display
                                display_name = req_name.replace('_', ' ').title()
                                elective_reqs[display_name] = int(float(req_value))
                            except:
                                pass
                
                # Display elective requirements if found
                if elective_reqs:
                    st.markdown("**Elective Requirements:**")
                    elective_cols = st.columns(5)
                    idx = 0
                    for req_name, req_value in elective_reqs.items():
                        with elective_cols[idx % 5]:
                            st.metric(req_name, req_value)
                        idx += 1
                    st.markdown("---")
                
                # Format Code and Prerequisite(s) columns for display
                df_display = df.copy()
                
                # Format Code column - add leading 0 if 7 digits
                df_display['Code'] = df_display['Code'].apply(
                    lambda x: ('0' + str(x).strip()) if len(str(x).strip()) == 7 else str(x).strip()
                )
                
                # Format Prerequisites column - add leading 0 if 7 digits
                def format_prerequisites(prereq_str):
                    prereq_str = str(prereq_str).strip()
                    if prereq_str and prereq_str != 'nan' and prereq_str != '' and prereq_str != 'None':
                        prereqs = [p.strip() for p in prereq_str.replace(';', ',').split(',')]
                        formatted = []
                        for p in prereqs:
                            if len(p) == 7:
                                p = '0' + p
                            formatted.append(p)
                        return ', '.join(formatted)
                    return '-'
                
                df_display['Prerequisites'] = df_display['Prerequisites'].apply(format_prerequisites)
                df_display['Corequisites'] = df_display['Corequisites'].apply(format_prerequisites)
                
                # Reorder columns for display
                display_columns = ['Code', 'Name', 'Credits', 'Technical Elective', 'Prerequisites', 'Corequisites', 'Year', 'Semester']
                df_display = df_display[[col for col in display_columns if col in df_display.columns]]
                
                st.dataframe(df_display, use_container_width=True, height=400)
            
            else:
                st.error("❌ Invalid CSV file. Please check the columns.")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Required columns:**")
                    for col in required_columns:
                        st.write(f"- {col}")
                with col2:
                    st.write("**Found columns:**")
                    for col in df.columns:
                        st.write(f"- {col}")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
