"""
HTML generation for curriculum flow charts.
Uses JavaScript-based interactive flowchart with SVG prerequisite lines.
"""

import json
from typing import Dict, List


class FlowChartHTMLGenerator:
    """Handles HTML generation for curriculum flow charts with JavaScript interactivity."""
    
    def __init__(self):
        pass
    
    def generate_css_styles(self) -> str:
        """Generate CSS styles for the flow chart."""
        return """
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #D9D9D9;
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                color: #A73239;
                margin-bottom: 20px;
                background: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }

            .header h1 {
                font-size: 1.8em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1em;
                color: #6d2932;
            }
            
            .flowchart-container {
                background: white;
                padding: 30px;
                overflow-x: auto;
                position: relative;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            
            .flowchart-wrapper {
                min-width: 1200px;
                max-width: 100%;
                position: relative;
                overflow: visible;
            }
            
            .flowchart-header {
                text-align: center;
                margin-bottom: 20px;
            }
            
            .flowchart-title {
                font-size: 1.5em;
                color: #A73239;
                margin-bottom: 10px;
            }
            
            .flowchart-legend {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 10px;
                flex-wrap: wrap;
            }
            
            .legend-item {
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 0.85em;
            }
            
            .legend-box {
                width: 25px;
                height: 25px;
                border-radius: 6px;
                border: 2px solid #333;
            }
            
            .legend-box.passed {
                background: white;
                border-color: #28a745;
                border-width: 3px;
            }
            
            .legend-box.grade-f {
                background: white;
                border-color: #dc3545;
                border-width: 3px;
            }
            
            .legend-box.grade-w {
                background: white;
                border-color: #ff8c00;
                border-width: 3px;
            }
            
            .legend-box.grade-n {
                background: white;
                border-color: #6c757d;
                border-width: 3px;
            }
            
            .legend-box.grade-i {
                background: white;
                border-color: #ffc107;
                border-width: 3px;
            }
            
            .legend-box.not-enrolled {
                background: white;
                border-color: #bbb;
                border-width: 3px;
            }

            .flowchart-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 0;
                position: relative;
                margin-top: 15px;
                border: 1px solid #ccc;
            }
            
            .year-group {
                display: flex;
                flex-direction: column;
                border-right: 1px solid #ccc;
            }
            
            .year-group:last-child {
                border-right: none;
            }
            
            .year-header {
                background: #A73239;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: 600;
                font-size: 0.95em;
                border-bottom: 1px solid #ccc;
            }
            
            .semesters-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                flex: 1;
                gap: 0;
            }
            
            .semester-column {
                display: flex;
                flex-direction: column;
                padding: 12px;
                gap: 20px;
            }
            
            .semester-column:first-child {
                border-right: 1px solid #ccc;
            }
            
            .semester-header {
                background: #af4b51;
                color: white;
                padding: 5px;
                text-align: center;
                font-weight: 600;
                font-size: 0.75em;
                border: none;
                border-radius: 4px;
                margin-bottom: 5px;
            }
            
            .course-box {
                background: white;
                border: 3px solid #6c757d;
                border-radius: 20px;
                padding: 6px 12px 6px 8px;
                text-align: left;
                cursor: pointer;
                transition: all 0.3s;
                position: relative;
                min-height: 38px;
                display: flex;
                align-items: center;
                gap: 8px;
                z-index: 2;
            }
            
            .course-box:hover {
                transform: scale(1.05);
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
                z-index: 10;
            }

            /* Highlight colors based on course status */
            .course-box.highlight-passed {
                transform: scale(1.05);
                box-shadow: 0 0 8px rgba(255, 215, 0, 0.9);
                z-index: 9;
            }
            
            .course-box.highlight-failed {
                transform: scale(1.05);
                box-shadow: 0 0 8px rgba(255, 68, 68, 0.9);
                z-index: 9;
            }
            
            .course-box.highlight-withdrawn {
                transform: scale(1.05);
                box-shadow: 0 0 8px rgba(255, 149, 0, 0.9);
                z-index: 9;
            }
            
            .course-box.highlight-grade-n {
                transform: scale(1.05);
                box-shadow: 0 0 8px rgba(158, 158, 158, 0.9);
                z-index: 9;
            }
            
            .course-box.highlight-incomplete {
                transform: scale(1.05);
                box-shadow: 0 0 8px rgba(255, 235, 59, 0.9);
                z-index: 9;
            }
            
            .course-box.highlight-not-enrolled {
                transform: scale(1.05);
                box-shadow: 0 0 8px rgba(208, 208, 208, 0.9);
                z-index: 9;
            }
            
            .course-box.passed {
                border-color: #28a745;
            }
            
            .course-box.grade-f {
                border-color: #dc3545;
            }
            
            .course-box.grade-w {
                border-color: #ff8c00;
            }
            
            .course-box.grade-n {
                border-color: #6c757d;
            }
            
            .course-box.grade-i {
                border-color: #ffc107;
            }
            
            .course-box.not-enrolled {
                border-color: #bbb;
            }
            
            .course-box-indicator {
                width: 24px;
                height: 24px;
                border-radius: 50%;
                background: #e3f2fd;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.7em;
                font-weight: 600;
                color: #1976d2;
                flex-shrink: 0;
            }
            
            .course-box.passed .course-box-indicator {
                background: #d4edda;
                color: #28a745;
            }
            
            .course-box.grade-f .course-box-indicator {
                background: #f8d7da;
                color: #dc3545;
            }
            
            .course-box.grade-w .course-box-indicator {
                background: #ffe5cc;
                color: #cc6f00;
            }
            
            .course-box.grade-n .course-box-indicator {
                background: #e9ecef;
                color: #495057;
            }
            
            .course-box.grade-i .course-box-indicator {
                background: #fff3cd;
                color: #856404;
            }
            
            .course-box-info {
                flex: 1;
                display: flex;
                flex-direction: column;
                gap: 2px;
            }
            
            .course-box-code {
                font-weight: 600;
                font-size: 0.75em;
                color: #333;
            }

            /* Tooltip */
            .course-tooltip {
                position: absolute;
                background: rgba(0, 0, 0, 0.75);
                color: white;
                padding: 12px 16px;
                border-radius: 8px;
                font-size: 0.9em;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                max-width: 350px;
                white-space: normal;
                backdrop-filter: blur(4px);
            }
            
            .tooltip-code {
                font-weight: 600;
                color: #ffc107;
                margin-bottom: 4px;
            }
            
            .tooltip-name {
                margin-bottom: 4px;
            }
            
            .tooltip-grade {
                color: #28a745;
                font-weight: 600;
            }
            
            .tooltip-grade.failed {
                color: #dc3545;
            }
            
            .tooltip-grade.not-enrolled {
                color: #6c757d;
            }
            
            .tooltip-semester {
                color: #17a2b8;
                font-size: 0.85em;
                margin-top: 4px;
                border-top: 1px solid rgba(255,255,255,0.2);
                padding-top: 4px;
            }
            
            .tooltip-prereq {
                color: #ffc107;
                font-size: 0.85em;
                margin-top: 4px;
            }
            
            .tooltip-coreq {
                color: #ff6b6b;
                font-size: 0.85em;
                margin-top: 2px;
            }
            
            /* SVG Canvas for Lines */
            .flowchart-svg {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 0;
            }
            
            .prerequisite-line {
                stroke: #dc3545;
                stroke-width: 1;
                fill: none;
                opacity: 1;
                transition: all 0.3s;
            }
            
            .corequisite-line {
                stroke: #dc3545;
                stroke-width: 1;
                fill: none;
                opacity: 1;
                transition: all 0.3s;
            }
            
            .prerequisite-line.highlight-passed,
            .corequisite-line.highlight-passed {
                stroke: #ffd700;
                stroke-width: 3;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 215, 0, 0.6));
            }
            
            .prerequisite-line.highlight-failed,
            .corequisite-line.highlight-failed {
                stroke: #ff4444;
                stroke-width: 3;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 68, 68, 0.6));
            }
            
            .prerequisite-line.highlight-withdrawn,
            .corequisite-line.highlight-withdrawn {
                stroke: #ff9500;
                stroke-width: 3;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 149, 0, 0.6));
            }
            
            .prerequisite-line.highlight-grade-n,
            .corequisite-line.highlight-grade-n {
                stroke: #9e9e9e;
                stroke-width: 3;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(158, 158, 158, 0.6));
            }
            
            .prerequisite-line.highlight-incomplete,
            .corequisite-line.highlight-incomplete {
                stroke: #ffeb3b;
                stroke-width: 3;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 235, 59, 0.6));
            }
            
            .prerequisite-line.highlight-not-enrolled,
            .corequisite-line.highlight-not-enrolled {
                stroke: #d0d0d0;
                stroke-width: 3;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(208, 208, 208, 0.6));
            }
            
            .prerequisite-arrow {
                fill: #dc3545;
                opacity: 1;
                transition: all 0.3s;
            }
            
            .corequisite-arrow {
                fill: #dc3545;
                opacity: 1;
                transition: all 0.3s;
            }
            
            .prerequisite-arrow.highlight-passed,
            .corequisite-arrow.highlight-passed {
                fill: #ffd700;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 215, 0, 0.6));
            }
            
            .prerequisite-arrow.highlight-failed,
            .corequisite-arrow.highlight-failed {
                fill: #ff4444;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 68, 68, 0.6));
            }
            
            .prerequisite-arrow.highlight-withdrawn,
            .corequisite-arrow.highlight-withdrawn {
                fill: #ff9500;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 149, 0, 0.6));
            }
            
            .prerequisite-arrow.highlight-grade-n,
            .corequisite-arrow.highlight-grade-n {
                fill: #9e9e9e;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(158, 158, 158, 0.6));
            }
            
            .prerequisite-arrow.highlight-incomplete,
            .corequisite-arrow.highlight-incomplete {
                fill: #ffeb3b;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(255, 235, 59, 0.6));
            }
            
            .prerequisite-arrow.highlight-not-enrolled,
            .corequisite-arrow.highlight-not-enrolled {
                fill: #d0d0d0;
                opacity: 1;
                filter: drop-shadow(0 0 2px rgba(208, 208, 208, 0.6));
            }
            
            /* Electives Section */
            .electives-section {
                margin-top: 30px;
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            
            .electives-section h2 {
                text-align: center;
                color: #A73239;
                margin-bottom: 20px;
                font-size: 1.5em;
            }
            
            .electives-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }
            
            .elective-category {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            
            .category-header {
                font-size: 13px;
                font-weight: bold;
                color: white;
                margin-bottom: 12px;
                text-align: center;
                padding: 10px;
                border-radius: 8px;
            }
            
            .category-header.wellness { background: #A73239; }
            .category-header.wellness_PE { background: #c94c54; }
            .category-header.entrepreneurship { background: #d4686f; }
            .category-header.language_communication_thai { background: #6d2932; }
            .category-header.language_communication_foreigner { background: #8a3640; }
            .category-header.language_communication_computer { background: #a7444e; }
            .category-header.thai_citizen_global { background: #5a2229; }
            .category-header.aesthetics { background: #4a1c22; }
            .category-header.technical_electives { background: #2c3e50; }
            .category-header.free_electives { background: #7f8c8d; }
            
            .progress-bar {
                width: 100%;
                height: 24px;
                background: #e9ecef;
                border-radius: 12px;
                overflow: hidden;
                margin: 12px 0;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #28a745, #20c997);
                transition: width 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
                font-weight: bold;
            }
            
            .elective-course-box {
                background: white;
                border: 2px solid #28a745;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 8px;
            }
            
            .elective-course-code {
                font-weight: 600;
                color: #A73239;
                font-size: 0.85em;
            }
            
            .elective-course-name {
                font-size: 0.8em;
                color: #333;
                margin: 4px 0;
            }
            
            .elective-course-info {
                font-size: 0.75em;
                color: #6c757d;
            }
            
            .no-courses-message {
                text-align: center;
                color: #6c757d;
                font-style: italic;
                padding: 10px;
            }
        </style>
        """

    def generate_javascript(self) -> str:
        """Generate JavaScript for interactive flowchart."""
        return """
        <script>
        // Show tooltip on hover
        function showTooltip(event, element) {
            const code = element.dataset.code;
            const name = element.dataset.name;
            const grade = element.dataset.grade;
            const credits = element.dataset.credits;
            const actualSemester = element.dataset.actualSemester;
            const prerequisite = element.dataset.prerequisite || '';
            const corequisite = element.dataset.corequisite || '';
            
            let tooltip = document.getElementById('courseTooltip');
            if (!tooltip) {
                tooltip = document.createElement('div');
                tooltip.id = 'courseTooltip';
                tooltip.className = 'course-tooltip';
                document.body.appendChild(tooltip);
            }
            
            const gradeClass = grade === 'Not Enrolled' ? 'not-enrolled' : 
                               (grade === 'F' || grade === 'W' ? 'failed' : '');
            
            // แสดงเทอมที่เรียนผ่านจริง (เฉพาะวิชาที่ผ่านแล้ว)
            let semesterHtml = '';
            if (actualSemester && grade !== 'Not Enrolled' && grade !== 'F' && grade !== 'W') {
                semesterHtml = `<div class="tooltip-semester">Completed: ${actualSemester}</div>`;
            }
            
            // แสดง Prerequisites
            let prereqHtml = '';
            if (prerequisite && prerequisite.trim()) {
                prereqHtml = `<div class="tooltip-prereq">Prerequisites: ${prerequisite}</div>`;
            }
            
            // แสดง Corequisites
            let coreqHtml = '';
            if (corequisite && corequisite.trim()) {
                coreqHtml = `<div class="tooltip-coreq">Corequisites: ${corequisite}</div>`;
            }
            
            tooltip.innerHTML = `
                <div class="tooltip-code">${code}</div>
                <div class="tooltip-name">${name}</div>
                <div class="tooltip-credits">${credits} credits</div>
                <div class="tooltip-grade ${gradeClass}">Grade: ${grade}</div>
                ${semesterHtml}
                ${prereqHtml}
                ${coreqHtml}
            `;
            
            tooltip.style.display = 'block';
            tooltip.style.visibility = 'hidden';
            
            setTimeout(() => {
                const rect = element.getBoundingClientRect();
                const tooltipWidth = tooltip.offsetWidth;
                const tooltipHeight = tooltip.offsetHeight;
                
                let left = rect.left + (rect.width / 2) - (tooltipWidth / 2);
                if (left < 10) left = 10;
                if (left + tooltipWidth > window.innerWidth - 10) {
                    left = window.innerWidth - tooltipWidth - 10;
                }
                
                let top = rect.top - tooltipHeight - 15 + window.scrollY;
                if (rect.top - tooltipHeight - 15 < 0) {
                    top = rect.bottom + 15 + window.scrollY;
                }
                
                tooltip.style.left = left + 'px';
                tooltip.style.top = top + 'px';
                tooltip.style.visibility = 'visible';
            }, 0);
        }
        
        function hideTooltip() {
            const tooltip = document.getElementById('courseTooltip');
            if (tooltip) tooltip.style.display = 'none';
        }
        
        function getCourseStatus(element) {
            if (element.classList.contains('passed')) return 'passed';
            if (element.classList.contains('grade-f')) return 'failed';
            if (element.classList.contains('grade-w')) return 'withdrawn';
            if (element.classList.contains('grade-n')) return 'grade-n';
            if (element.classList.contains('grade-i')) return 'incomplete';
            return 'not-enrolled';
        }

        function highlightPrerequisitePath(element, event) {
            showTooltip(event, element);
            const code = element.dataset.code;
            const highlightedCourses = new Set();
            const highlightedLines = new Set();
            
            const currentStatus = getCourseStatus(element);
            element.classList.add(`highlight-${currentStatus}`);
            highlightedCourses.add(code);
            
            highlightPrerequisites(code, highlightedCourses, highlightedLines);
            highlightCorequisites(code, highlightedCourses, highlightedLines, currentStatus);
            highlightDependents(code, highlightedCourses, highlightedLines, currentStatus);
        }
        
        function highlightCorequisites(courseCode, highlightedCourses, highlightedLines, currentStatus) {
            const courseBox = document.querySelector(`.course-box[data-code="${courseCode}"]`);
            if (!courseBox) return;
            
            // Highlight corequisites of this course (courses that must be taken together)
            const corequisite = courseBox.dataset.corequisite;
            if (corequisite && corequisite !== '') {
                const coreqCodes = corequisite.replace(/,/g, ' ').split(/\\s+/)
                    .filter(c => c.trim() !== '' && c !== 'nan')
                    .map(c => c.trim().padStart(8, '0'));
                
                coreqCodes.forEach(coreqCode => {
                    const coreqBox = document.querySelector(`.course-box[data-code="${coreqCode}"]`);
                    if (coreqBox) {
                        // Highlight the line from corequisite to this course
                        const connectionKey = `${coreqCode}->${courseCode}`;
                        if (!highlightedLines.has(connectionKey)) {
                            const coreqStatus = getCourseStatus(coreqBox);
                            highlightLine(connectionKey, coreqStatus);
                            highlightedLines.add(connectionKey);
                        }
                        
                        // Highlight the corequisite course box
                        if (!highlightedCourses.has(coreqCode)) {
                            const coreqStatus = getCourseStatus(coreqBox);
                            coreqBox.classList.add(`highlight-${coreqStatus}`);
                            highlightedCourses.add(coreqCode);
                            
                            // Recursively highlight corequisites of this corequisite
                            highlightCorequisites(coreqCode, highlightedCourses, highlightedLines, coreqStatus);
                            // Also highlight prerequisites and dependents of this corequisite
                            highlightPrerequisites(coreqCode, highlightedCourses, highlightedLines);
                            highlightDependents(coreqCode, highlightedCourses, highlightedLines, coreqStatus);
                        }
                    }
                });
            }
            
            // Also check if this course is a corequisite of other courses
            const allCourses = document.querySelectorAll('.course-box');
            allCourses.forEach(box => {
                const boxCode = box.dataset.code;
                const boxCorequisite = box.dataset.corequisite;
                if (!boxCorequisite || boxCorequisite === '') return;
                
                const boxCoreqCodes = boxCorequisite.replace(/,/g, ' ').split(/\\s+/)
                    .filter(c => c.trim() !== '' && c !== 'nan')
                    .map(c => c.trim().padStart(8, '0'));
                
                if (boxCoreqCodes.includes(courseCode)) {
                    // This course is a corequisite of boxCode
                    const connectionKey = `${courseCode}->${boxCode}`;
                    if (!highlightedLines.has(connectionKey)) {
                        highlightLine(connectionKey, currentStatus);
                        highlightedLines.add(connectionKey);
                    }
                    
                    // Highlight the dependent course box
                    if (!highlightedCourses.has(boxCode)) {
                        const boxStatus = getCourseStatus(box);
                        box.classList.add(`highlight-${boxStatus}`);
                        highlightedCourses.add(boxCode);
                        
                        // Recursively highlight corequisites, prerequisites and dependents
                        highlightCorequisites(boxCode, highlightedCourses, highlightedLines, boxStatus);
                        highlightPrerequisites(boxCode, highlightedCourses, highlightedLines);
                        highlightDependents(boxCode, highlightedCourses, highlightedLines, boxStatus);
                    }
                }
            });
        }
        
        function highlightPrerequisites(courseCode, highlightedCourses, highlightedLines) {
            const courseBox = document.querySelector(`.course-box[data-code="${courseCode}"]`);
            if (!courseBox) return;
            
            const prerequisite = courseBox.dataset.prerequisite;
            if (!prerequisite || prerequisite === '') return;
            
            const prereqCodes = prerequisite.replace(/,/g, ' ').split(/\\s+/)
                .filter(c => c.trim() !== '' && c !== 'nan')
                .map(c => c.trim().padStart(8, '0'));
            
            prereqCodes.forEach(prereqCode => {
                const prereqBox = document.querySelector(`.course-box[data-code="${prereqCode}"]`);
                if (prereqBox) {
                    // Always highlight the line, even if course is already highlighted
                    const connectionKey = `${prereqCode}->${courseCode}`;
                    if (!highlightedLines.has(connectionKey)) {
                        const prereqStatus = getCourseStatus(prereqBox);
                        highlightLine(connectionKey, prereqStatus);
                        highlightedLines.add(connectionKey);
                    }
                    
                    // Only highlight the course box if not already highlighted
                    if (!highlightedCourses.has(prereqCode)) {
                        const prereqStatus = getCourseStatus(prereqBox);
                        prereqBox.classList.add(`highlight-${prereqStatus}`);
                        highlightedCourses.add(prereqCode);
                        highlightCorequisites(prereqCode, highlightedCourses, highlightedLines, prereqStatus);
                        highlightPrerequisites(prereqCode, highlightedCourses, highlightedLines);
                    }
                }
            });
        }
        
        function highlightDependents(courseCode, highlightedCourses, highlightedLines, lockedColor) {
            const allCourses = document.querySelectorAll('.course-box');
            
            allCourses.forEach(box => {
                const boxCode = box.dataset.code;
                const prerequisite = box.dataset.prerequisite;
                
                // Check prerequisites
                if (prerequisite && prerequisite !== '') {
                    const prereqCodes = prerequisite.replace(/,/g, ' ').split(/\\s+/)
                        .filter(c => c.trim() !== '' && c !== 'nan')
                        .map(c => c.trim().padStart(8, '0'));
                    
                    if (prereqCodes.includes(courseCode)) {
                        // Always highlight the line, even if course is already highlighted
                        const connectionKey = `${courseCode}->${boxCode}`;
                        if (!highlightedLines.has(connectionKey)) {
                            highlightLine(connectionKey, lockedColor);
                            highlightedLines.add(connectionKey);
                        }
                        
                        // Only highlight the course box if not already highlighted
                        if (!highlightedCourses.has(boxCode)) {
                            const boxStatus = getCourseStatus(box);
                            let useColor, nextLockedColor;
                            
                            if (lockedColor === 'failed' || lockedColor === 'withdrawn') {
                                useColor = lockedColor;
                                nextLockedColor = lockedColor;
                            } else {
                                useColor = boxStatus;
                                nextLockedColor = (boxStatus === 'failed' || boxStatus === 'withdrawn') ? boxStatus : boxStatus;
                            }
                            
                            box.classList.add(`highlight-${useColor}`);
                            highlightedCourses.add(boxCode);
                            highlightCorequisites(boxCode, highlightedCourses, highlightedLines, useColor);
                            highlightDependents(boxCode, highlightedCourses, highlightedLines, nextLockedColor);
                        }
                    }
                }
            });
        }
        
        function highlightLine(connectionKey, status) {
            // Highlight both prerequisite and corequisite lines
            document.querySelectorAll('.prerequisite-line, .corequisite-line').forEach(line => {
                if (line.dataset.connection === connectionKey) {
                    line.classList.add(`highlight-${status}`);
                }
            });
            
            // Highlight both prerequisite and corequisite arrows
            document.querySelectorAll('.prerequisite-arrow, .corequisite-arrow').forEach(arrow => {
                if (arrow.dataset.connection === connectionKey) {
                    arrow.classList.add(`highlight-${status}`);
                }
            });
        }

        function clearHighlight() {
            hideTooltip();
            const highlightClasses = ['highlight-passed', 'highlight-failed', 'highlight-withdrawn', 
                                      'highlight-grade-n', 'highlight-incomplete', 'highlight-not-enrolled'];
            
            document.querySelectorAll('.course-box').forEach(box => {
                highlightClasses.forEach(cls => box.classList.remove(cls));
            });
            document.querySelectorAll('.prerequisite-line, .corequisite-line').forEach(line => {
                highlightClasses.forEach(cls => line.classList.remove(cls));
            });
            document.querySelectorAll('.prerequisite-arrow, .corequisite-arrow').forEach(arrow => {
                highlightClasses.forEach(cls => arrow.classList.remove(cls));
            });
        }
        
        function drawPrerequisiteLines() {
            const svg = document.getElementById('flowchartSvg');
            if (!svg) return;
            svg.innerHTML = '';
            
            const courseBoxes = {};
            document.querySelectorAll('.course-box').forEach(box => {
                courseBoxes[box.dataset.code] = box;
            });
            
            const lineOffsets = {};
            
            // Draw prerequisite lines
            document.querySelectorAll('.course-box').forEach(toBox => {
                const prerequisite = toBox.dataset.prerequisite;
                if (!prerequisite || prerequisite === '') return;
                
                const prereqCodes = prerequisite.replace(/,/g, ' ').split(/\\s+/)
                    .filter(code => code.trim() !== '' && code !== 'nan')
                    .map(code => code.trim().padStart(8, '0'));
                
                prereqCodes.forEach(prereqCode => {
                    const fromBox = courseBoxes[prereqCode];
                    if (fromBox && toBox) {
                        drawLine(svg, fromBox, toBox, lineOffsets, 'prerequisite');
                    }
                });
            });
            
            // Draw corequisite lines
            document.querySelectorAll('.course-box').forEach(toBox => {
                const corequisite = toBox.dataset.corequisite;
                if (!corequisite || corequisite === '') return;
                
                const coreqCodes = corequisite.replace(/,/g, ' ').split(/\\s+/)
                    .filter(code => code.trim() !== '' && code !== 'nan')
                    .map(code => code.trim().padStart(8, '0'));
                
                coreqCodes.forEach(coreqCode => {
                    const fromBox = courseBoxes[coreqCode];
                    if (fromBox && toBox) {
                        // Only draw if toBox is below fromBox (to avoid duplicate lines)
                        const fromRect = fromBox.getBoundingClientRect();
                        const toRect = toBox.getBoundingClientRect();
                        if (toRect.top > fromRect.bottom) {
                            drawLine(svg, fromBox, toBox, lineOffsets, 'corequisite');
                        }
                    }
                });
            });
        }
        
        function drawLine(svg, fromBox, toBox, lineOffsets, lineType = 'prerequisite') {
            const fromRect = fromBox.getBoundingClientRect();
            const toRect = toBox.getBoundingClientRect();
            const svgRect = svg.getBoundingClientRect();
            
            const fromYear = parseInt(fromBox.dataset.year);
            const fromTerm = parseInt(fromBox.dataset.term);
            const toYear = parseInt(toBox.dataset.year);
            const toTerm = parseInt(toBox.dataset.term);
            
            const OFFSET_STEP = 3;
            const ARROW_SIZE = 4;
            const SIDE_OFFSET = 10;
            
            const fromTermIndex = (fromYear - 1) * 2 + fromTerm;
            const toTermIndex = (toYear - 1) * 2 + toTerm;
            const termDistance = Math.abs(toTermIndex - fromTermIndex);
            
            let BOTTOM_CLEARANCE;
            if (termDistance <= 1) BOTTOM_CLEARANCE = 2;
            else if (termDistance === 2) BOTTOM_CLEARANCE = 5;
            else if (termDistance === 3) BOTTOM_CLEARANCE = 7;
            else BOTTOM_CLEARANCE = 12;
            
            let path, arrow;
            
            if (fromYear === toYear && fromTerm === toTerm) {
                // Same semester - draw vertical line from bottom of fromBox to top of toBox
                const x1 = fromRect.left + (fromRect.width / 2) - svgRect.left;
                const y1 = fromRect.bottom - svgRect.top;
                const x2 = toRect.left + (toRect.width / 2) - svgRect.left;
                const y2 = toRect.top - svgRect.top;
                
                // Only draw if toBox is actually below fromBox
                if (y2 > y1) {
                    path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    path.setAttribute('d', `M ${x1} ${y1} L ${x2} ${y2}`);
                    
                    arrow = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                    arrow.setAttribute('points', `${x2},${y2} ${x2-ARROW_SIZE},${y2-ARROW_SIZE} ${x2+ARROW_SIZE},${y2-ARROW_SIZE}`);
                    
                    // Add special styling for corequisite lines
                    if (lineType === 'corequisite') {
                        path.setAttribute('class', 'prerequisite-line corequisite-line');
                        arrow.setAttribute('class', 'prerequisite-arrow corequisite-arrow');
                    } else {
                        path.setAttribute('class', 'prerequisite-line');
                        arrow.setAttribute('class', 'prerequisite-arrow');
                    }
                } else {
                    // If boxes are in wrong order, skip drawing
                    return;
                }
            } else {
                const pathKey = `${fromYear}-${fromTerm}-${toYear}-${toTerm}`;
                if (!lineOffsets[pathKey]) lineOffsets[pathKey] = 0;
                const offset = lineOffsets[pathKey];
                lineOffsets[pathKey] += OFFSET_STEP;
                
                const fromY = fromRect.top + (fromRect.height / 2) - svgRect.top;
                const toY = toRect.top + (toRect.height / 2) - svgRect.top;
                
                const allBoxes = document.querySelectorAll('.course-box');
                let lowestObstacleBottom = 0;
                let willCollide = false;
                
                allBoxes.forEach(box => {
                    if (box === fromBox || box === toBox) return;
                    const boxRect = box.getBoundingClientRect();
                    const boxLeft = boxRect.left - svgRect.left;
                    const boxRight = boxRect.right - svgRect.left;
                    const boxTop = boxRect.top - svgRect.top;
                    const boxBottom = boxRect.bottom - svgRect.top;
                    const fromX = fromRect.right - svgRect.left;
                    const toX = toRect.left - svgRect.left;
                    
                    if (boxRight > fromX && boxLeft < toX) {
                        const lineMinY = Math.min(fromY, toY);
                        const lineMaxY = Math.max(fromY, toY);
                        if (boxBottom > lineMinY && boxTop < lineMaxY) {
                            willCollide = true;
                            lowestObstacleBottom = Math.max(lowestObstacleBottom, boxBottom);
                        }
                        if ((fromY >= boxTop && fromY <= boxBottom) || (toY >= boxTop && toY <= boxBottom)) {
                            willCollide = true;
                            lowestObstacleBottom = Math.max(lowestObstacleBottom, boxBottom);
                        }
                    }
                });
                
                const x1 = fromRect.right - svgRect.left;
                const y1 = fromY;
                
                if (willCollide) {
                    const detourY = lowestObstacleBottom + BOTTOM_CLEARANCE + offset;
                    const x2 = x1 + SIDE_OFFSET;
                    const y2 = y1;
                    const x3 = x2;
                    const y3 = detourY;
                    const x4 = toRect.left - svgRect.left - SIDE_OFFSET;
                    const y4 = detourY;
                    const x5 = x4;
                    const y5 = toY;
                    const x6 = toRect.left - svgRect.left;
                    const y6 = toY;
                    
                    path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    path.setAttribute('d', `M ${x1} ${y1} L ${x2} ${y2} L ${x3} ${y3} L ${x4} ${y4} L ${x5} ${y5} L ${x6} ${y6}`);
                    
                    arrow = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                    arrow.setAttribute('points', `${x6},${y6} ${x6-ARROW_SIZE},${y6-ARROW_SIZE} ${x6-ARROW_SIZE},${y6+ARROW_SIZE}`);
                } else {
                    const x2 = x1 + SIDE_OFFSET + offset;
                    const y2 = y1;
                    const x3 = x2;
                    const y3 = toY;
                    const x4 = toRect.left - svgRect.left;
                    const y4 = toY;
                    
                    path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    path.setAttribute('d', `M ${x1} ${y1} L ${x2} ${y2} L ${x3} ${y3} L ${x4} ${y4}`);
                    
                    arrow = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
                    arrow.setAttribute('points', `${x4},${y4} ${x4-ARROW_SIZE},${y4-ARROW_SIZE} ${x4-ARROW_SIZE},${y4+ARROW_SIZE}`);
                }
                
                // Add styling
                if (lineType === 'corequisite') {
                    path.setAttribute('class', 'prerequisite-line corequisite-line');
                    arrow.setAttribute('class', 'prerequisite-arrow corequisite-arrow');
                } else {
                    path.setAttribute('class', 'prerequisite-line');
                    arrow.setAttribute('class', 'prerequisite-arrow');
                }
            }
            
            path.dataset.connection = `${fromBox.dataset.code}->${toBox.dataset.code}`;
            arrow.dataset.connection = `${fromBox.dataset.code}->${toBox.dataset.code}`;
            
            svg.appendChild(path);
            svg.appendChild(arrow);
        }
        
        // Initialize on load with multiple fallbacks
        function initializeFlowchart() {
            // Clear any existing lines first
            const svg = document.getElementById('flowchartSvg');
            if (svg) svg.innerHTML = '';
            
            // Draw lines
            drawPrerequisiteLines();
        }
        
        // Try multiple times to ensure lines are drawn
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(initializeFlowchart, 100);
            });
        } else {
            setTimeout(initializeFlowchart, 100);
        }
        
        window.addEventListener('load', () => {
            setTimeout(initializeFlowchart, 200);
            // Extra fallback for slow-loading systems
            setTimeout(initializeFlowchart, 500);
        });
        
        window.addEventListener('resize', () => {
            setTimeout(initializeFlowchart, 100);
        });
        </script>
        """

    def generate_header_section(self, student_info: Dict, template: Dict, semesters: List[Dict] = None) -> str:
        """Generate the header section of the flow chart."""
        # Get cumulative GPA from second-to-last semester
        gpa_text = ""
        if semesters and len(semesters) >= 2:
            second_last_semester = semesters[-2]
            cum_gpa = second_last_semester.get('cum_gpa')
            if cum_gpa is not None:
                gpa_text = f" | <strong>Cumulative GPA:</strong> {cum_gpa:.2f}"
        elif semesters and len(semesters) == 1:
            latest_semester = semesters[-1]
            cum_gpa = latest_semester.get('cum_gpa')
            if cum_gpa is not None:
                gpa_text = f" | <strong>Cumulative GPA:</strong> {cum_gpa:.2f}"
        
        return f"""
        <div class="header">
            <h1>IE Curriculum Flow Chart</h1>
            <p><strong>Template:</strong> {template.get('curriculum_name', 'Unknown')} | 
               <strong>Student:</strong> {student_info.get('name', 'N/A')} ({student_info.get('id', 'N/A')}){gpa_text}</p>
        </div>
        """
    
    def generate_legend_section(self) -> str:
        """Generate the legend section."""
        return """
        <div class="flowchart-header">
            <h3 class="flowchart-title">Curriculum Flow Chart</h3>
            <div class="flowchart-legend">
                <div class="legend-item">
                    <div class="legend-box passed"></div>
                    <span>Passed</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box grade-f"></div>
                    <span>F (Failed)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box grade-w"></div>
                    <span>W (Withdrawn)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box grade-n"></div>
                    <span>N (No Grade)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box grade-i"></div>
                    <span>I (Incomplete)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-box not-enrolled"></div>
                    <span>Not Enrolled</span>
                </div>
            </div>
        </div>
        """
    
    def generate_course_box(self, course_code: str, course_name: str, credits: int,
                           status_class: str, grade: str, year: int, term: int,
                           prerequisite: str = "", actual_semester: str = "", corequisite: str = "") -> str:
        """Generate HTML for a single course box."""
        return f"""
        <div class="course-box {status_class}" 
             data-code="{course_code}"
             data-name="{course_name}"
             data-grade="{grade}"
             data-credits="{credits}"
             data-prerequisite="{prerequisite}"
             data-corequisite="{corequisite}"
             data-year="{year}"
             data-term="{term}"
             data-actual-semester="{actual_semester}"
             onmouseenter="highlightPrerequisitePath(this, event)"
             onmouseleave="clearHighlight()">
            <div class="course-box-indicator">{credits}</div>
            <div class="course-box-info">
                <div class="course-box-code">{course_code}</div>
            </div>
        </div>
        """
    
    def generate_year_section(self, year_num: int, first_semester_html: str, second_semester_html: str) -> str:
        """Generate HTML for a year section."""
        return f"""
        <div class="year-group">
            <div class="year-header">Year {year_num}</div>
            <div class="semesters-row">
                <div class="semester-column">
                    <div class="semester-header">First Semester</div>
                    {first_semester_html}
                </div>
                <div class="semester-column">
                    <div class="semester-header">Second Semester</div>
                    {second_semester_html}
                </div>
            </div>
        </div>
        """
    
    def generate_complete_html(self, student_info: Dict, template: Dict, 
                              curriculum_grid_html: str, electives_html: str = "", semesters: List[Dict] = None) -> str:
        """Generate the complete HTML document."""
        css_styles = self.generate_css_styles()
        javascript = self.generate_javascript()
        header_html = self.generate_header_section(student_info, template, semesters)
        legend_html = self.generate_legend_section()
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>IE Curriculum Flow Chart</title>
            <meta charset="utf-8">
            {css_styles}
        </head>
        <body>
            <div class="container">
                {header_html}
                <div class="flowchart-container">
                    <div class="flowchart-wrapper">
                        {legend_html}
                        <div class="flowchart-grid" id="flowchartGrid">
                            {curriculum_grid_html}
                        </div>
                        <svg class="flowchart-svg" id="flowchartSvg"></svg>
                    </div>
                </div>
                {electives_html}
            </div>
            {javascript}
        </body>
        </html>
        """
    
    def generate_electives_section(self, template: Dict, analysis: Dict) -> str:
        """Generate the electives requirements section."""
        html = """
        <div class="electives-section">
            <h2>Elective Requirements Progress</h2>
            <div class="electives-grid">
        """
        
        category_display_map = {
            'wellness': 'Wellness',
            'wellness_PE': 'Wellness & PE',
            'entrepreneurship': 'Entrepreneurship',
            'language_communication_thai': 'Thai Language & Communication',
            'language_communication_foreigner': 'Foreign Language & Communication',
            'language_communication_computer': 'Computer & Digital Literacy',
            'thai_citizen_global': 'Thai Citizen & Global',
            'aesthetics': 'Aesthetics',
            'technical_electives': 'Technical Electives',
            'free_electives': 'Free Electives'
        }
        
        for elective_key, required_credits in template.get('elective_requirements', {}).items():
            analysis_data = analysis['elective_analysis'].get(elective_key, {'required': required_credits, 'completed': 0, 'courses': []})
            completed_credits = analysis_data['completed']
            courses = analysis_data['courses']
            
            progress_percentage = min((completed_credits / required_credits) * 100, 100) if required_credits > 0 else 0
            category_display = category_display_map.get(elective_key, elective_key.replace('_', ' ').title())
            
            html += f"""
            <div class="elective-category">
                <div class="category-header {elective_key}">{category_display}</div>
                <div style="text-align: center; margin-bottom: 8px;">
                    <strong>{completed_credits}/{required_credits} credits</strong>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percentage}%">
                        {progress_percentage:.0f}%
                    </div>
                </div>
            """
            
            if courses:
                for course in courses:
                    html += f"""
                    <div class="elective-course-box">
                        <div class="elective-course-code">{course["code"]}</div>
                        <div class="elective-course-name">{course["name"]}</div>
                        <div class="elective-course-info">{course["credits"]} credits - {course["semester"]}</div>
                    </div>
                    """
            else:
                html += '<div class="no-courses-message">No courses completed yet</div>'
            
            html += '</div>'
        
        html += '</div></div>'
        return html
