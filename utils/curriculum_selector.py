"""
Utility for automatic curriculum selection based on student ID
"""
from pathlib import Path
import os

def get_curriculum_for_student_id(student_id: str) -> str:
    """
    Auto-select curriculum based on student ID first 2 digits
    Rule:
        - Curriculum changes every 5 years
        - 60–64 -> B-IE-2560
        - 65–69 -> B-IE-2565
        - ...
    """
    # fallback: newest curriculum
    if not student_id or len(student_id) < 2:
        return get_newest_curriculum()

    try:
        student_year = int(student_id[:2])
    except (ValueError, IndexError):
        return get_newest_curriculum()

    curricula = get_available_curricula()
    if not curricula:
        return get_newest_curriculum()

    # Extract curriculum start years (e.g., B-IE-2565 -> 65)
    curriculum_years = []
    for name in curricula:
        try:
            be_year = int(name.split("-")[-1])   # 2565
            start_year = be_year - 2500          # 65
            curriculum_years.append((start_year, name))
        except ValueError:
            continue

    if not curriculum_years:
        return get_newest_curriculum()

    # Match 5-year window
    for start_year, name in sorted(curriculum_years):
        if start_year <= student_year <= start_year + 4:
            return name

    # Older than oldest curriculum
    if student_year < min(y for y, _ in curriculum_years):
        return get_oldest_curriculum()

    # Newer than newest curriculum
    return get_newest_curriculum()


def get_available_curricula() -> list:
    """Get list of available curriculum folders"""
    course_data_dir = Path(__file__).parent.parent / "course_data"
    curricula = []
    
    for item in course_data_dir.iterdir():
        if item.is_dir() and item.name.startswith("B-IE-"):
            curricula.append(item.name)
    
    return sorted(curricula)

def get_newest_curriculum() -> str:
    """Get the newest curriculum (highest version number)"""
    curricula = get_available_curricula()
    return curricula[-1] if curricula else "B-IE-2565"

def get_oldest_curriculum() -> str:
    """Get the oldest curriculum (lowest version number)"""
    curricula = get_available_curricula()
    return curricula[0] if curricula else "B-IE-2560"

def curriculum_exists(curriculum_name: str) -> bool:
    """Check if a curriculum folder exists"""
    course_data_dir = Path(__file__).parent.parent / "course_data"
    curriculum_path = course_data_dir / curriculum_name
    return curriculum_path.exists() and curriculum_path.is_dir()