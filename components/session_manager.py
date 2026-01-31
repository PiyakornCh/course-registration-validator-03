import streamlit as st
from typing import Dict, List, Optional


class SessionManager:
    """Centralized manager for Streamlit session state."""

    @staticmethod
    def initialize_session_state():
        """Initialize all required session state variables."""
        st.session_state.setdefault("student_info", {})
        st.session_state.setdefault("semesters", [])
        st.session_state.setdefault("validation_results", [])
        st.session_state.setdefault("selected_course_data", None)
        st.session_state.setdefault("processing_complete", False)
        st.session_state.setdefault("unidentified_count", 0)
        st.session_state.setdefault("course_categories", None)
        st.session_state.setdefault("last_pdf_name", None)
        st.session_state.setdefault("admin_logged_in", False)
        st.session_state.setdefault("admin_mode", False)
        st.session_state.setdefault("admin_nav", "Manage Curriculums")
        st.session_state.setdefault("came_from_admin", False)


    @staticmethod
    def is_processing_complete() -> bool:
        return st.session_state.processing_complete

    @staticmethod
    def get_student_info() -> Dict:
        return st.session_state.student_info

    @staticmethod
    def get_semesters() -> List[Dict]:
        return st.session_state.semesters

    @staticmethod
    def get_validation_results() -> List[Dict]:
        return st.session_state.validation_results

    @staticmethod
    def get_unidentified_count() -> int:
        return st.session_state.unidentified_count

    @staticmethod
    def get_course_categories() -> Optional[Dict]:
        return st.session_state.course_categories

    @staticmethod
    def set_unidentified_count(count: int):
        st.session_state.unidentified_count = count

    @staticmethod
    def set_course_categories(categories: Dict):
        st.session_state.course_categories = categories

    @staticmethod
    def store_processing_results(
        student_info: Dict,
        semesters: List[Dict],
        validation_results: List[Dict],
        pdf_name: str,
    ):
        st.session_state.student_info = student_info
        st.session_state.semesters = semesters
        st.session_state.validation_results = validation_results
        st.session_state.processing_complete = True
        st.session_state.last_pdf_name = pdf_name

    @staticmethod
    def should_reset_for_new_file(pdf_name: str) -> bool:
        return st.session_state.last_pdf_name != pdf_name

    @staticmethod
    def reset_processing_state():
        """Reset only PDF / validation related state."""
        st.session_state.processing_complete = False
        st.session_state.student_info = {}
        st.session_state.semesters = []
        st.session_state.validation_results = []
        st.session_state.unidentified_count = 0
        st.session_state.last_pdf_name = None

        if "last_validation_curriculum" in st.session_state:
            del st.session_state.last_validation_curriculum

    @staticmethod
    def logout_admin():
        """Clean logout for admin."""
        st.session_state.admin_logged_in = False
        st.session_state.admin_nav = "Manage Curriculums"
        st.session_state.came_from_admin = True

    @staticmethod
    def reset_all():
        """Reset EVERYTHING (use carefully)."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
