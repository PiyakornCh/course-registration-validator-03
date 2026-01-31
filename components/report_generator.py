import streamlit as st
import json
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from utils.excel_generator import create_smart_registration_excel
from validator import CourseRegistrationValidator


class ReportGenerator:
    """Handles generation and download of various report formats."""
    
    def __init__(self):
        pass
    
    def generate_excel_report(self, student_info: Dict, semesters: List[Dict], 
                             validation_results: List[Dict]) -> tuple[bytes, int]:
        """Generate Excel report with comprehensive analysis."""
        try:
            return create_smart_registration_excel(student_info, semesters, validation_results)
        except Exception as e:
            raise Exception(f"Error creating Excel report: {e}")
    
    def generate_text_report(self, student_info: Dict, semesters: List[Dict], 
                           validation_results: List[Dict], course_data_path: str) -> str:
        """Generate text-based validation report."""
        try:
            validator = CourseRegistrationValidator(course_data_path)
            return validator.generate_summary_report(student_info, semesters, validation_results)
        except Exception as e:
            raise Exception(f"Error creating text report: {e}")
    
    def generate_json_export(self, student_info: Dict, semesters: List[Dict], 
                           validation_results: List[Dict], selected_course_data: Dict, 
                           unidentified_count: int) -> str:
        """Generate JSON export with all data."""
        try:
            export_data = {
                "student_info": student_info,
                "semesters": semesters,
                "validation_results": validation_results,
                "unidentified_count": unidentified_count,
                "metadata": {
                    "course_catalog": selected_course_data.get('filename', ''),
                    "generated_timestamp": str(st.session_state.get('processing_timestamp', 'unknown'))
                }
            }
            
            return json.dumps(export_data, indent=2)
        except Exception as e:
            raise Exception(f"Error creating JSON export: {e}")
    
    def generate_flow_chart_html(self, student_info: Dict, semesters: List[Dict], 
                               validation_results: List[Dict], selected_course_data: Dict) -> tuple[str, int]:
        """Generate HTML flow chart for download."""
        try:
            from components.flow_chart_generator import FlowChartGenerator
            flow_generator = FlowChartGenerator()
            return flow_generator.create_enhanced_template_flow_html(
                student_info, semesters, validation_results, selected_course_data
            )
        except Exception as e:
            raise Exception(f"Error creating HTML flow chart: {e}")
    
    def display_download_section(self, student_info: Dict, semesters: List[Dict], 
                               validation_results: List[Dict], selected_course_data: Dict):
        """Display the download section with all available report formats."""
        st.divider()
        st.header("📥 Download Reports")
        
        col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
        
        # Comprehensive Report
        with col_dl1:
            self._handle_comprehensive_report_download(student_info, semesters, validation_results, selected_course_data)
        
        # HTML Flow Chart
        with col_dl2:
            self._handle_flow_chart_download(student_info, semesters, validation_results, selected_course_data)
        
        # Text Report
        with col_dl3:
            self._handle_text_report_download(student_info, semesters, validation_results, selected_course_data)
        
        # JSON Export
        with col_dl4:
            self._handle_json_export_download(student_info, semesters, validation_results, selected_course_data)
    
    def _handle_comprehensive_report_download(self, student_info: Dict, semesters: List[Dict], 
                                            validation_results: List[Dict], selected_course_data: Dict):
        """Handle comprehensive HTML report download."""
        try:
            with st.spinner("Generating comprehensive academic report..."):
                from components.comprehensive_report_generator import ComprehensiveReportGenerator
                report_generator = ComprehensiveReportGenerator()
                report_html = report_generator.generate_comprehensive_report(
                    student_info, semesters, validation_results, selected_course_data
                )
            
            if report_html and len(report_html.strip()) > 0:
                st.download_button(
                    label="📋 Comprehensive Report",
                    data=report_html.encode('utf-8'),
                    file_name=f"academic_report_{student_info.get('id', 'student')}.html",
                    mime="text/html",
                    help="Detailed academic progress analysis with recommendations and planning",
                    use_container_width=True
                )
                st.success("✅ Report ready for download")
            else:
                st.error("❌ Report generation failed")
                
        except Exception as e:
            st.error(f"❌ Report error: {str(e)[:50]}...")
            with st.expander("Debug"):
                st.code(str(e))
    
    def _handle_flow_chart_download(self, student_info: Dict, semesters: List[Dict], 
                                   validation_results: List[Dict], selected_course_data: Dict):
        """Handle HTML flow chart download."""
        try:
            flow_html, flow_unidentified = self.generate_flow_chart_html(
                student_info, semesters, validation_results, selected_course_data
            )
            
            st.download_button(
                label="🗂️ Flow Chart (HTML)",
                data=flow_html.encode('utf-8'),
                file_name=f"curriculum_flow_{student_info.get('id', 'unknown')}.html",
                mime="text/html",
                help="Interactive semester-based curriculum flow chart with enhanced deviation detection",
                use_container_width=True
            )
            
            if flow_unidentified > 0:
                st.warning(f"⚠️ {flow_unidentified} unidentified")
                
        except Exception as e:
            st.error(f"❌ Flow chart error: {str(e)[:50]}...")
    
    def _handle_text_report_download(self, student_info: Dict, semesters: List[Dict], 
                                    validation_results: List[Dict], selected_course_data: Dict):
        """Handle text report download."""
        try:
            course_data_path = str(Path(__file__).parent.parent / "course_data" / selected_course_data['filename'])
            report_text = self.generate_text_report(
                student_info, semesters, validation_results, course_data_path
            )
            
            st.download_button(
                label="📄 Validation Report",
                data=report_text,
                file_name=f"validation_report_{student_info.get('id', 'unknown')}.txt",
                mime="text/plain",
                help="Detailed prerequisite validation report",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ Report error: {str(e)[:50]}...")
    
    def _handle_json_export_download(self, student_info: Dict, semesters: List[Dict], 
                                    validation_results: List[Dict], selected_course_data: Dict):
        """Handle JSON export download."""
        try:
            unidentified_count = st.session_state.get('unidentified_count', 0)
            json_data = self.generate_json_export(
                student_info, semesters, validation_results, selected_course_data, unidentified_count
            )
            
            st.download_button(
                label="💾 Raw Data (JSON)",
                data=json_data,
                file_name=f"transcript_data_{student_info.get('id', 'unknown')}.json",
                mime="application/json",
                help="Raw extracted and validated data",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"❌ JSON error: {str(e)[:50]}...")
