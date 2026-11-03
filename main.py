import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Set

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, Image as ReportImage

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices, QAction, QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QStackedWidget, QFrame,
    QScrollArea, QCheckBox, QMessageBox, QSizePolicy, QFileDialog, QProgressBar
)

APP_NAME = "JobFinder"
APP_VERSION = "3.4.0"


def resource_path(relative_path):
    """Resolve bundled assets in source and PyInstaller builds."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base_path / relative_path)


SUBJECTS = {
    "Math": {
        "color": "#3977B8",
        "subtitle": "Numbers, patterns and puzzles",
        "question": "What parts of math do you enjoy?",
        "options": [
            "Solving puzzles and tricky problems",
            "Finding patterns in numbers",
            "Measuring, designing and building",
            "Working with money",
            "Using computers and logic",
        ],
    },
    "Science": {
        "color": "#27866A",
        "subtitle": "Experiments, nature and discovery",
        "question": "Which areas of science interest you?",
        "options": [
            "Animals and wildlife",
            "The human body and health",
            "Space, planets and stars",
            "Chemistry and experiments",
            "Inventions, machines and technology",
            "Plants, oceans and the environment",
        ],
    },
    "Reading": {
        "color": "#8B5BB2",
        "subtitle": "Stories, language and ideas",
        "question": "What do you enjoy most about reading and language?",
        "options": [
            "Stories, books and adventures",
            "Learning facts about real topics",
            "Writing stories or creating characters",
            "Explaining ideas and teaching",
            "Solving mysteries and finding clues",
            "Learning new languages",
        ],
    },
    "Social Studies": {
        "color": "#C17A35",
        "subtitle": "People, places and the past",
        "question": "Which topics would you like to explore?",
        "options": [
            "History and how people lived",
            "Different countries and cultures",
            "Maps, cities and geography",
            "Helping people and communities",
            "Government, laws and fairness",
            "How businesses and money work",
        ],
    },
}

GENERAL_QUESTIONS = [
    {
        "eyebrow": "YOUR INTERESTS · ACTIVITIES",
        "title": "What do you like doing?",
        "subtitle": "Choose up to three activities you would enjoy doing often.",
        "multi": True,
        "limit": 3,
        "options": [
            ("Building or fixing things", {"hands_on", "engineering", "mechanical"}),
            ("Creating art, designs or stories", {"creative", "communication"}),
            ("Solving mysteries or problems", {"analysis", "research"}),
            ("Helping or taking care of people", {"helping", "people"}),
            ("Working with animals or nature", {"animals", "environment"}),
            ("Using computers or technology", {"technology", "analysis"}),
            ("Leading a team or organizing a project", {"leadership", "organization"}),
            ("Exploring, traveling or being outdoors", {"outdoors", "environment"}),
        ],
    },
    {
        "eyebrow": "YOUR PERSONALITY · TEAMWORK",
        "title": "How do you like to work?",
        "subtitle": "Pick the option that feels most like you.",
        "multi": False,
        "options": [
            ("I like working with a group", {"people", "teamwork"}),
            ("I prefer working independently", {"independent", "focus"}),
            ("I enjoy a mix of both", {"teamwork", "independent"}),
        ],
    },
    {
        "eyebrow": "YOUR PERSONALITY · PROBLEM SOLVING",
        "title": "When something is difficult, what do you do?",
        "subtitle": "There is no right or wrong answer.",
        "multi": False,
        "options": [
            ("Try different ideas until something works", {"persistence", "analysis"}),
            ("Ask questions and learn more first", {"research", "curiosity"}),
            ("Ask someone to work through it with me", {"teamwork", "people"}),
            ("Try a creative approach nobody has tried", {"creative", "innovation"}),
        ],
    },
    {
        "eyebrow": "YOUR STRENGTHS",
        "title": "What are you good at?",
        "subtitle": "Choose the strengths that sound like you. You can choose several.",
        "multi": True,
        "options": [
            ("Understanding how things work", {"analysis", "mechanical", "engineering"}),
            ("Explaining things to others", {"communication", "teaching"}),
            ("Noticing small details", {"detail", "science", "research"}),
            ("Coming up with new ideas", {"creative", "innovation"}),
            ("Staying organized", {"organization", "leadership"}),
            ("Being patient and caring", {"helping", "people", "animals"}),
            ("Remembering facts and information", {"research", "history"}),
            ("Working with my hands", {"hands_on", "mechanical"}),
        ],
    },
    {
        "eyebrow": "YOUR WORK STYLE",
        "title": "Where would you enjoy working?",
        "subtitle": "Choose any places that sound interesting.",
        "multi": True,
        "options": [
            ("In an office or studio", {"office", "creative"}),
            ("Outside in nature", {"outdoors", "environment", "animals"}),
            ("In a hospital, clinic or care center", {"health", "helping", "people"}),
            ("In a lab or research center", {"science", "research", "analysis"}),
            ("In a workshop or on a job site", {"hands_on", "engineering", "mechanical"}),
            ("In a school or community", {"teaching", "helping", "people"}),
            ("Traveling or visiting different places", {"travel", "people", "geography"}),
        ],
    },
]

CAREERS = [
    ("Veterinarian", "Cares for animals, finds out what is making them sick, and helps them stay healthy.", {"animals", "health", "science", "helping", "people"}),
    ("Wildlife Biologist", "Studies wild animals and their habitats to help protect nature.", {"animals", "environment", "outdoors", "science", "research"}),
    ("Doctor", "Works with patients to understand health problems and provide treatment.", {"health", "science", "helping", "people", "detail"}),
    ("Nurse", "Cares for patients, supports families and works with a healthcare team.", {"health", "helping", "people", "teamwork", "science"}),
    ("Engineer", "Designs, tests and improves products, machines, buildings or systems.", {"engineering", "math", "analysis", "hands_on", "mechanical"}),
    ("Architect", "Plans buildings and spaces that are useful, safe and interesting.", {"creative", "math", "design", "engineering", "detail"}),
    ("Software Developer", "Creates computer programs, apps and tools that solve problems.", {"technology", "analysis", "math", "creative", "independent"}),
    ("Game Designer", "Plans how a video game works, feels and keeps players interested.", {"creative", "technology", "story", "analysis", "math"}),
    ("Data Scientist", "Looks for patterns in information to help answer important questions.", {"math", "analysis", "research", "technology", "detail"}),
    ("Teacher", "Helps students understand new ideas and build skills.", {"teaching", "communication", "people", "helping", "organization"}),
    ("Author", "Creates books, stories, articles or other written work for readers.", {"creative", "communication", "story", "independent", "reading"}),
    ("Journalist", "Researches events, interviews people and explains what is happening.", {"communication", "research", "history", "people", "curiosity"}),
    ("Lawyer", "Studies laws, builds arguments and helps people work through legal problems.", {"communication", "analysis", "research", "history", "people"}),
    ("Historian", "Studies the past using documents, objects and other evidence.", {"history", "research", "reading", "detail", "communication"}),
    ("Geographer", "Studies places, maps, people and how the world is changing.", {"geography", "environment", "research", "outdoors", "analysis"}),
    ("Social Worker", "Helps people and families find support and work through challenges.", {"helping", "people", "communication", "community", "teamwork"}),
    ("Environmental Scientist", "Studies the environment and works on ways to protect it.", {"environment", "science", "research", "outdoors", "analysis"}),
    ("Forensic Scientist", "Uses science and careful observations to help investigate evidence.", {"science", "detail", "analysis", "research", "problem"}),
    ("Entrepreneur", "Starts a business by turning an idea into a product or service.", {"leadership", "creative", "organization", "math", "people"}),
    ("Urban Planner", "Helps design neighborhoods, streets, parks and public spaces.", {"geography", "organization", "community", "creative", "math"}),
    ("Mechanical Technician", "Builds, tests, maintains and repairs machines and equipment.", {"hands_on", "mechanical", "analysis", "technology", "detail"}),
    ("Graphic Designer", "Creates visual designs for websites, products, signs and publications.", {"creative", "design", "technology", "communication"}),
    ("Museum Curator", "Cares for collections and creates exhibits that help people learn.", {"history", "research", "organization", "communication"}),
    ("Park Ranger", "Protects parks, helps visitors and cares for natural places.", {"outdoors", "environment", "helping", "animals", "communication"}),
]


# Career profiles are written for exploration, not as promises about a person's
# future. Pay is shown as a broad U.S. annual estimate and varies by location,
# experience, employer, and specialty. Use the BLS link in each profile for
# current occupation-specific information.
CAREER_DETAILS = {
    "Veterinarian": {
        "day": "A veterinarian may examine pets, ask owners questions, run tests, give vaccines, perform procedures, and explain how to keep animals healthy. Some veterinarians work with farm animals or wildlife.",
        "skills": "Science, careful observation, communication, patience, problem-solving, and compassion for animals.",
        "education": "Usually a bachelor's degree with science prerequisites, followed by a Doctor of Veterinary Medicine (DVM) degree and a state license. The path often takes about 8 years after high school.",
        "pay": "$75,000–$160,000+",
        "setting": "Animal hospitals, veterinary clinics, farms, laboratories, zoos, or wildlife facilities.",
    },
    "Wildlife Biologist": {
        "day": "A wildlife biologist observes animals, studies habitats, collects field data, analyzes results, and helps protect species and ecosystems. Some days are outdoors; others are spent in a lab or writing reports.",
        "skills": "Biology, curiosity, data collection, patience, writing, and comfort working outdoors.",
        "education": "A bachelor's degree in wildlife biology, zoology, ecology, or a related field is common. Research leadership roles may require a master's or doctoral degree.",
        "pay": "$45,000–$100,000+",
        "setting": "Field sites, parks, government agencies, universities, conservation groups, and laboratories.",
    },
    "Doctor": {
        "day": "Doctors meet with patients, ask about symptoms, perform exams, review tests, make diagnoses, recommend treatments, and work with other healthcare professionals.",
        "skills": "Science, critical thinking, communication, decision-making, empathy, and attention to detail.",
        "education": "Typically a bachelor's degree, medical school (MD or DO), and residency training. Some specialties require additional fellowship training and a medical license.",
        "pay": "$150,000–$300,000+",
        "setting": "Hospitals, clinics, medical offices, laboratories, and other healthcare settings.",
    },
    "Nurse": {
        "day": "Nurses check on patients, measure vital signs, give treatments and medications, explain care instructions, update records, and coordinate with doctors and families.",
        "skills": "Communication, teamwork, organization, science, calm decision-making, and compassion.",
        "education": "Registered nurses commonly complete an approved nursing diploma, associate degree, or bachelor's degree and pass the NCLEX-RN licensing exam. Advanced nursing roles require more education.",
        "pay": "$60,000–$125,000+",
        "setting": "Hospitals, clinics, schools, community health centers, and patients' homes.",
    },
    "Engineer": {
        "day": "Engineers identify problems, plan designs, build or test prototypes, use math and computer tools, and improve products, structures, or systems. The exact work depends on the type of engineering.",
        "skills": "Math, science, creative problem-solving, teamwork, communication, and attention to detail.",
        "education": "A bachelor's degree in an engineering specialty is common. Some roles require professional licensure or graduate study.",
        "pay": "$65,000–$150,000+",
        "setting": "Offices, design studios, laboratories, factories, construction sites, and field locations.",
    },
    "Architect": {
        "day": "Architects talk with clients, sketch ideas, create digital building plans, choose materials, coordinate with engineers, and visit construction sites to see how a design is coming together.",
        "skills": "Design, creativity, math, spatial thinking, communication, and organization.",
        "education": "Typically an accredited architecture degree, supervised experience, and passing licensing exams. Requirements vary by state and degree path.",
        "pay": "$55,000–$130,000+",
        "setting": "Architecture firms, design studios, construction sites, and government offices.",
    },
    "Software Developer": {
        "day": "Software developers plan how an app or program should work, write code, test features, fix bugs, and work with designers and other developers to improve the product.",
        "skills": "Logic, problem-solving, patience, creativity, math, and clear communication.",
        "education": "A bachelor's degree in computer science or a related field is common, but some developers enter through other education, projects, or work experience.",
        "pay": "$80,000–$210,000+",
        "setting": "Offices, technology companies, government, schools, or remote work environments.",
    },
    "Game Designer": {
        "day": "Game designers develop ideas for game worlds, rules, challenges, characters, and player experiences. They test games and adjust designs based on how people play.",
        "skills": "Creativity, storytelling, communication, collaboration, problem-solving, and understanding players.",
        "education": "There is no single required path. Employers may look for a degree in game design, computer science, art, or a related area, plus a portfolio of projects.",
        "pay": "$50,000–$150,000+",
        "setting": "Game studios, software companies, independent teams, and remote studios.",
    },
    "Data Scientist": {
        "day": "Data scientists ask questions, collect and organize information, use statistics and computer code to find patterns, and explain what the results might mean.",
        "skills": "Math, statistics, coding, curiosity, critical thinking, and explaining complex ideas clearly.",
        "education": "A bachelor's degree in math, statistics, computer science, or a related field is common. Some positions prefer a master's or doctoral degree.",
        "pay": "$75,000–$180,000+",
        "setting": "Technology companies, businesses, hospitals, research organizations, and government agencies.",
    },
    "Teacher": {
        "day": "Teachers plan lessons, explain ideas, lead activities, check student progress, give feedback, and work with families and other educators.",
        "skills": "Communication, patience, creativity, organization, leadership, and understanding how people learn.",
        "education": "Public school teachers generally need a bachelor's degree and state teaching certification. Requirements differ by grade level and state.",
        "pay": "$40,000–$90,000+",
        "setting": "Schools, classrooms, online learning programs, museums, and community education programs.",
    },
    "Author": {
        "day": "Authors develop ideas, research topics, plan and write drafts, revise their work, and work with editors or publishers. Some write books; others create articles, scripts, or digital content.",
        "skills": "Writing, imagination, research, persistence, editing, and curiosity.",
        "education": "There is no required degree. Many authors study English, journalism, communications, or a subject they write about; strong writing samples matter.",
        "pay": "Varies widely; freelance income can be unpredictable",
        "setting": "Home offices, publishing companies, media organizations, and freelance environments.",
    },
    "Journalist": {
        "day": "Journalists find story ideas, research facts, interview people, check information, write or produce stories, and share news with the public.",
        "skills": "Writing, curiosity, listening, research, fairness, accuracy, and communication.",
        "education": "A bachelor's degree in journalism, communications, or a related subject is common. Internships and published work can be helpful.",
        "pay": "$35,000–$100,000+",
        "setting": "Newsrooms, studios, field locations, websites, radio, television, and remote work.",
    },
    "Lawyer": {
        "day": "Lawyers research laws, meet with clients, prepare documents, negotiate, and may represent people or organizations in court.",
        "skills": "Reading, writing, careful reasoning, research, public speaking, and listening.",
        "education": "Usually a bachelor's degree, a law degree (JD), and passing the bar exam in the state where they practice.",
        "pay": "$70,000–$240,000+",
        "setting": "Law firms, businesses, government agencies, courts, and nonprofit organizations.",
    },
    "Historian": {
        "day": "Historians study documents, photographs, objects, and other evidence; compare sources; write about what happened; and help people understand the past.",
        "skills": "Research, reading, writing, curiosity, careful analysis, and attention to detail.",
        "education": "A bachelor's degree may lead to some related roles. Historian and research positions often prefer a master's or doctoral degree.",
        "pay": "$40,000–$110,000+",
        "setting": "Museums, archives, universities, government agencies, libraries, and historical sites.",
    },
    "Geographer": {
        "day": "Geographers study places and how people and the environment interact. They may use maps, satellite images, surveys, and computer mapping tools to answer questions.",
        "skills": "Geography, data analysis, mapping, research, communication, and curiosity about the world.",
        "education": "A bachelor's degree in geography or a related field is common. Technical mapping roles may value GIS training; research roles may require graduate study.",
        "pay": "$45,000–$120,000+",
        "setting": "Government agencies, planning offices, research organizations, universities, and field locations.",
    },
    "Social Worker": {
        "day": "Social workers listen to people, help them find services, support families, connect clients with resources, and work with schools, hospitals, or community organizations.",
        "skills": "Listening, empathy, communication, organization, problem-solving, and teamwork.",
        "education": "A bachelor's degree in social work is common for many entry-level roles. Clinical social workers need a master's degree, supervised experience, and a license.",
        "pay": "$35,000–$90,000+",
        "setting": "Schools, hospitals, community agencies, government, and nonprofit organizations.",
    },
    "Environmental Scientist": {
        "day": "Environmental scientists collect samples, study air, water, soil, or wildlife, analyze results, and help organizations understand and reduce environmental problems.",
        "skills": "Science, research, data analysis, observation, writing, and problem-solving.",
        "education": "A bachelor's degree in environmental science, biology, chemistry, or a related field is common. Some specialties require graduate study.",
        "pay": "$45,000–$120,000+",
        "setting": "Laboratories, offices, field sites, consulting firms, and government agencies.",
    },
    "Forensic Scientist": {
        "day": "Forensic scientists examine evidence, use laboratory tests, document results, and explain scientific findings to investigators or courts. Different specialists study different kinds of evidence.",
        "skills": "Science, careful observation, accuracy, patience, critical thinking, and clear writing.",
        "education": "A bachelor's degree in chemistry, biology, forensic science, or a related natural science is common. Specialized roles may require additional training.",
        "pay": "$40,000–$110,000+",
        "setting": "Crime laboratories, government agencies, medical examiner offices, and research facilities.",
    },
    "Entrepreneur": {
        "day": "Entrepreneurs notice a need, develop a product or service, plan a business, talk with customers, manage money, and solve the many problems involved in running something new.",
        "skills": "Creativity, leadership, communication, organization, persistence, and financial understanding.",
        "education": "There is no single required degree. Business, finance, technology, or industry training can help, along with experience and learning from customers.",
        "pay": "Varies widely; income may be low or negative while starting",
        "setting": "Small businesses, offices, stores, workshops, online businesses, and many other places.",
    },
    "Urban Planner": {
        "day": "Urban planners help communities decide where homes, parks, roads, shops, and public services should go. They review plans, study data, meet with residents, and make recommendations.",
        "skills": "Geography, design, communication, research, organization, and understanding communities.",
        "education": "A bachelor's degree in planning or a related field may lead to some jobs. A master's degree in urban or regional planning is common for planner roles.",
        "pay": "$50,000–$130,000+",
        "setting": "City and regional government, planning firms, community organizations, and public meetings.",
    },
    "Mechanical Technician": {
        "day": "Mechanical technicians help build, test, inspect, maintain, and repair machines or equipment. They may use tools, read technical drawings, and run tests.",
        "skills": "Hands-on problem-solving, mechanical ability, math, safety awareness, and attention to detail.",
        "education": "Many roles require a high school diploma plus technical training. Some employers prefer a certificate or associate degree in mechanical or engineering technology.",
        "pay": "$35,000–$90,000+",
        "setting": "Factories, repair shops, laboratories, manufacturing plants, and field service locations.",
    },
    "Graphic Designer": {
        "day": "Graphic designers create visual materials such as logos, posters, websites, packaging, and advertisements. They talk with clients, develop concepts, and refine designs.",
        "skills": "Creativity, visual communication, design software, listening, and attention to detail.",
        "education": "A bachelor's degree in graphic design or a related field is common, though a strong portfolio and practical experience are important.",
        "pay": "$35,000–$100,000+",
        "setting": "Design studios, advertising agencies, businesses, publishing, and freelance work.",
    },
    "Museum Curator": {
        "day": "Curators care for collections, research objects and their history, plan exhibits, write descriptions, and help visitors learn from the collection.",
        "skills": "Research, organization, communication, history or art knowledge, and careful attention to objects.",
        "education": "A master's degree is common for curator roles, often in museum studies, history, art history, or a related subject.",
        "pay": "$35,000–$110,000+",
        "setting": "Museums, galleries, historic sites, universities, and cultural organizations.",
    },
    "Park Ranger": {
        "day": "Park rangers help visitors, explain nature and history, protect park resources, maintain safe public spaces, and may assist with conservation or emergency response.",
        "skills": "Communication, outdoor skills, public service, observation, teamwork, and knowledge of nature or history.",
        "education": "Requirements vary. Some positions accept a high school diploma with relevant experience; others prefer a degree in parks, natural resources, biology, or a related field.",
        "pay": "$30,000–$90,000+",
        "setting": "National, state, and local parks, historic sites, forests, and visitor centers.",
    },
}

BLS_CAREER_URL = "https://www.bls.gov/ooh/occupation-finder.htm"


STYLE = """
QMainWindow, QWidget#page { background: #F5F7FA; }
QLabel { color: #203047; }
QLabel#title { font-size: 29px; font-weight: 750; color: #172D49; }
QLabel#subtitle { font-size: 15px; color: #617186; }
QLabel#eyebrow { color: #3977B8; font-size: 11px; font-weight: 800; letter-spacing: 1px; }
QPushButton, QCheckBox#choice {
    background: white; border: 1px solid #DCE4ED; border-radius: 13px;
    padding: 14px; color: #203047; font-size: 14px; font-weight: 650;
}
QPushButton:hover, QCheckBox#choice:hover { border: 1px solid #7899BE; background: #F8FBFF; }
QPushButton#primary {
    background: #244D78; color: white; border: none;
    padding: 13px 22px; border-radius: 12px; font-size: 14px;
}
QPushButton#primary:hover { background: #326596; }
QPushButton#back { background: transparent; border: none; color: #52657C; padding: 7px; text-align: left; }
QCheckBox#choice { spacing: 10px; }
QCheckBox#choice::indicator { width: 19px; height: 19px; }
QCheckBox#choice::indicator:unchecked { border: 1px solid #AAB8C8; border-radius: 5px; background: white; }
QCheckBox#choice::indicator:checked { border: 1px solid #3977B8; border-radius: 5px; background: #3977B8; }
QFrame#panel { background: white; border: 1px solid #E1E8F0; border-radius: 14px; }
QLabel#muted { color: #6B7C91; font-size: 12px; }
"""

class JobFinder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"JobFinder {APP_VERSION}")
        self.resize(1020, 760)
        self.setMinimumSize(720, 560)
        self.create_menus()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.answers: Dict[str, Set[str]] = {}
        self.selected_subjects: Set[str] = set()
        self.flow = []
        self.flow_index = 0
        self.current_profile = set()
        self.current_scored = []
        self.home = self.build_home()
        self.stack.addWidget(self.home)

    def create_menus(self):
        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction("&About JobFinder", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        privacy_action = QAction("&Privacy", self)
        privacy_action.triggered.connect(self.show_privacy)
        help_menu.addAction(privacy_action)

    def show_about(self):
        self.show_notice(
            "About JobFinder",
            f"JobFinder {APP_VERSION}\n\n"
            "Explore your interests, strengths, and possible career paths.\n\n"
            "JobFinder is an educational exploration tool, not a career aptitude test. "
            "Its suggestions are conversation starters, not predictions or limits."
        )

    def show_privacy(self):
        self.show_notice(
            "JobFinder Privacy",
            "JobFinder does not create an online account, send answers to a server, "
            "or collect analytics. Your answers stay in the app while you use it.\n\n"
            "Nothing is saved automatically. If you choose Save Results, JobFinder "
            "creates a PDF report at the location you select. The report may contain the "
            "subjects, answers, and career suggestions from the session. Keep it "
            "somewhere private if it includes a child's information.\n\n"
            "The app only opens an external website when you choose a career-information link."
        )


    def save_results(self):
        if not self.flow or not self.answers or not self.current_scored:
            self.show_notice("Nothing to save", "Complete the career questions and view your career matches before saving a report.")
            return

        default_name = f"JobFinder_Career_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save JobFinder Career Report", default_name, "PDF report (*.pdf)"
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        try:
            self.create_pdf_report(file_path)
            self.show_notice("Report saved", f"Your JobFinder career report was saved to:\\n{file_path}")
        except Exception as exc:
            self.show_notice("Could not save report", f"An error occurred while creating the PDF:\\n{exc}", QMessageBox.Warning)

    def create_pdf_report(self, file_path):
        """Create a polished PDF showing the user's choice path and career matches."""
        page_width, _ = letter
        doc = SimpleDocTemplate(
            file_path, pagesize=letter, rightMargin=.62*inch, leftMargin=.62*inch,
            topMargin=.62*inch, bottomMargin=.62*inch,
            title="JobFinder Career Discovery Report", author="JobFinder"
        )
        navy = colors.HexColor("#203047")
        blue = colors.HexColor("#3977B8")
        teal = colors.HexColor("#27866A")
        pale = colors.HexColor("#EAF1F8")
        pale_teal = colors.HexColor("#EAF5F1")
        muted = colors.HexColor("#607087")
        line = colors.HexColor("#D8E1EA")

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="JFTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                                  fontSize=24, leading=29, textColor=navy, alignment=1, spaceAfter=5))
        styles.add(ParagraphStyle(name="JFSub", parent=styles["Normal"], fontSize=9, leading=13,
                                  textColor=muted, alignment=1, spaceAfter=15))
        styles.add(ParagraphStyle(name="JFSection", parent=styles["Heading2"], fontName="Helvetica-Bold",
                                  fontSize=15, leading=19, textColor=navy, spaceBefore=13, spaceAfter=8))
        styles.add(ParagraphStyle(name="JFNode", parent=styles["Normal"], fontSize=9, leading=13,
                                  textColor=navy))
        styles.add(ParagraphStyle(name="JFSmall", parent=styles["Normal"], fontSize=8, leading=11,
                                  textColor=muted))
        styles.add(ParagraphStyle(name="JFCareer", parent=styles["Normal"], fontName="Helvetica-Bold",
                                  fontSize=12, leading=15, textColor=navy))
        styles.add(ParagraphStyle(name="JFBody", parent=styles["Normal"], fontSize=8.3, leading=11.5,
                                  textColor=navy))
        styles.add(ParagraphStyle(name="JFWhite", parent=styles["Normal"], fontName="Helvetica-Bold",
                                  fontSize=8, leading=10, textColor=colors.white, alignment=1))

        logo_path = resource_path("assets/jobfinder_logo.png")
        report_logo = ReportImage(logo_path, width=2.55*inch, height=1.60*inch)
        report_logo.hAlign = "CENTER"
        story = [Spacer(1, .02*inch), report_logo,
                 Paragraph("CAREER DISCOVERY REPORT  |  " + datetime.now().strftime("%B %d, %Y"),
                           styles["JFSub"])]

        intro = ("Your answers create a path through subjects, interests, activities, strengths, "
                 "and work preferences. This report shows the choices you made and careers worth exploring.")
        box = Table([[Paragraph(intro, styles["BodyText"])]], colWidths=[7.2*inch])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), pale), ("BOX", (0,0), (-1,-1), .7, line),
            ("LEFTPADDING", (0,0), (-1,-1), 11), ("RIGHTPADDING", (0,0), (-1,-1), 11),
            ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)
        ]))
        story += [box, Paragraph("Your choice path", styles["JFSection"])]

        def node_table(content, header=None, fill=pale_teal):
            rows = []
            if header:
                rows.append([Paragraph(header, styles["JFWhite"])])
            rows.append([Paragraph(content, styles["JFNode"])])
            t = Table(rows, colWidths=[6.9*inch])
            cmds = [
                ("BACKGROUND", (0,0), (-1,-1), fill), ("BOX", (0,0), (-1,-1), .6, line),
                ("LINEBEFORE", (0,0), (0,-1), 3, teal),
                ("LEFTPADDING", (0,0), (-1,-1), 11), ("RIGHTPADDING", (0,0), (-1,-1), 11),
                ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)
            ]
            if header:
                cmds.append(("BACKGROUND", (0,0), (-1,0), blue))
                cmds.append(("LINEBEFORE", (0,0), (0,0), 0, blue))
            t.setStyle(TableStyle(cmds))
            return t

        subjects = "  •  ".join(sorted(self.selected_subjects)) or "No subjects recorded"
        story.append(node_table("<b>Favorite subjects</b><br/>" + self._pdf_escape(subjects),
                                "STARTING POINT", pale))
        story.append(Paragraph("<font color='#27866A'>↓</font>",
                               ParagraphStyle("JFArrow", parent=styles["Normal"], fontSize=14,
                                              alignment=1, leading=17)))

        for idx, question in enumerate(self.flow):
            selected = sorted(self.answers.get(question.get("key"), set()))
            if not selected:
                continue
            eyebrow = question.get("eyebrow", "")
            prefix = (f"<font color='#27866A'><b>{self._pdf_escape(eyebrow)}</b></font><br/>"
                      if eyebrow else "")
            content = prefix + "<b>" + self._pdf_escape(question.get("title", "Your choices")) + "</b><br/>"
            content += "<br/>".join("• " + self._pdf_escape(choice) for choice in selected)
            story.append(node_table(content, fill=pale_teal if idx % 2 == 0 else colors.HexColor("#F5F7FA")))
            story.append(Paragraph("<font color='#27866A'>↓</font>",
                                   ParagraphStyle("JFArrow" + str(idx), parent=styles["Normal"],
                                                  fontSize=11, alignment=1, leading=14)))

        story += [
            Paragraph("Career matches to explore", styles["JFSection"]),
            Paragraph("These are the strongest matches from this exploration. You can explore any career "
                      "that catches your interest, even if it is not listed here.", styles["JFSmall"]),
            Spacer(1, 6)
        ]

        for rank, (score, title, description, matched) in enumerate(self.current_scored, 1):
            detail = CAREER_DETAILS.get(title, {})
            parts = [
                Paragraph(f"{rank}. {self._pdf_escape(title)}", styles["JFCareer"]),
                Paragraph(self._pdf_escape(description), styles["JFBody"]),
                Paragraph("<b>Why it matched:</b> " + self._pdf_escape(", ".join(sorted(matched))),
                          styles["JFBody"])
            ]
            for label, key in [
                ("A typical day", "day"), ("Helpful skills", "skills"),
                ("Education and training", "education"), ("Work settings", "setting"),
                ("Approximate U.S. pay", "pay")
            ]:
                if detail.get(key):
                    parts.append(Paragraph(f"<b>{label}:</b> {self._pdf_escape(detail[key])}", styles["JFBody"]))
            card = Table([[parts]], colWidths=[6.9*inch])
            card.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                ("BOX", (0,0), (-1,-1), .7, line), ("LINEBEFORE", (0,0), (0,0), 3, blue),
                ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
                ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)
            ]))
            story.append(KeepTogether([card, Spacer(1, 7)]))

        disclaimer = ("<b>Remember:</b> JobFinder is an educational exploration tool, not a career aptitude test. "
                      "These matches are ideas to investigate—not predictions or limits on what you can become. "
                      "Salary information is a broad U.S. estimate and varies by location, experience, employer, "
                      "specialty, and hours.")
        endbox = Table([[Paragraph(disclaimer, styles["JFSmall"])]], colWidths=[7.2*inch])
        endbox.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), pale), ("BOX", (0,0), (-1,-1), .6, line),
            ("LEFTPADDING", (0,0), (-1,-1), 9), ("RIGHTPADDING", (0,0), (-1,-1), 9),
            ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)
        ]))
        story += [Spacer(1, 8), endbox]

        def footer(canvas, document):
            canvas.saveState()
            canvas.setStrokeColor(line)
            canvas.line(.62*inch, .45*inch, page_width-.62*inch, .45*inch)
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(muted)
            canvas.drawString(.62*inch, .28*inch, "JobFinder • Career discovery")
            canvas.drawRightString(page_width-.62*inch, .28*inch, f"Page {document.page}")
            canvas.restoreState()

        doc.build(story, onFirstPage=footer, onLaterPages=footer)

    @staticmethod
    def _pdf_escape(value):
        value = str(value)
        return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def show_notice(self, title, message, icon=QMessageBox.Information):
        # Use an explicitly styled dialog so text remains readable in Windows
        # light mode, dark mode, and when the system theme differs from the app.
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(message)
        box.setIcon(icon)
        box.setStandardButtons(QMessageBox.Ok)
        box.setStyleSheet("""
            QMessageBox { background-color: #F5F7FA; }
            QMessageBox QLabel { color: #203047; font-size: 14px; }
            QMessageBox QPushButton {
                background: #244D78; color: white; border: none;
                border-radius: 8px; padding: 8px 20px; min-width: 72px;
            }
            QMessageBox QPushButton:hover { background: #326596; }
        """)
        box.exec()

    def shell(self):
        page = QWidget()
        page.setObjectName("page")
        layout = QVBoxLayout(page)
        layout.setContentsMargins(24, 20, 24, 22)
        layout.setSpacing(12)
        return page, layout

    def header(self, layout, eyebrow, title, subtitle):
        e = QLabel(eyebrow.upper())
        e.setObjectName("eyebrow")
        layout.addWidget(e)
        t = QLabel(title)
        t.setObjectName("title")
        t.setWordWrap(True)
        layout.addWidget(t)
        s = QLabel(subtitle)
        s.setObjectName("subtitle")
        s.setWordWrap(True)
        layout.addWidget(s)

    def progress(self, layout, step, total):
        row = QHBoxLayout()
        label = QLabel(f"STEP {step} OF {total}")
        label.setObjectName("muted")
        row.addWidget(label)
        row.addStretch()
        row.addWidget(QLabel(f"{int(step / total * 100)}%"))
        layout.addLayout(row)
        bar = QProgressBar()
        bar.setRange(0, total)
        bar.setValue(step)
        bar.setTextVisible(False)
        bar.setFixedHeight(8)
        bar.setStyleSheet(
            "QProgressBar { background:#E1E8F0; border:0; border-radius:4px; }"
            "QProgressBar::chunk { background:#3977B8; border-radius:4px; }"
        )
        layout.addWidget(bar)

    def build_home(self):
        page, outer = self.shell()
        top_row = QHBoxLayout()
        top_row.addStretch()
        privacy_button = QPushButton("Privacy")
        privacy_button.clicked.connect(self.show_privacy)
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        top_row.addWidget(privacy_button)
        top_row.addWidget(about_button)
        outer.addLayout(top_row)
        outer.addSpacing(8)

        # Integrated brand header: transparent logo artwork sits beside the name
        # and tagline, rather than inside a separate image card.
        eyebrow = QLabel("INTERESTS · STRENGTHS · POSSIBILITIES")
        eyebrow.setObjectName("eyebrow")
        outer.addWidget(eyebrow)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(18)
        logo = QLabel()
        logo.setAlignment(Qt.AlignCenter)
        logo.setMinimumWidth(225)
        logo.setMaximumWidth(285)
        logo_pixmap = QPixmap(resource_path("assets/jobfinder_logo.png"))
        if not logo_pixmap.isNull():
            logo.setPixmap(logo_pixmap.scaled(
                275, 172, Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        brand_row.addWidget(logo, 0)

        brand_copy = QVBoxLayout()
        brand_copy.setSpacing(5)
        brand_copy.addStretch()
        brand_title = QLabel("JobFinder")
        brand_title.setObjectName("title")
        brand_copy.addWidget(brand_title)
        brand_tagline = QLabel("Discover what interests you.\nExplore what you could become.")
        brand_tagline.setObjectName("subtitle")
        brand_tagline.setWordWrap(True)
        brand_copy.addWidget(brand_tagline)
        brand_copy.addStretch()
        brand_row.addLayout(brand_copy, 1)
        outer.addLayout(brand_row)
        outer.addSpacing(9)
        prompt = QLabel("Which subjects do you enjoy?")
        prompt.setStyleSheet("font-size:19px; font-weight:750;")
        outer.addWidget(prompt)
        note = QLabel("Choose one or more. You can explore different paths along the way.")
        note.setObjectName("subtitle")
        outer.addWidget(note)

        grid = QGridLayout()
        grid.setSpacing(12)
        self.subject_checks = {}
        self.subject_count_label = QLabel("0 subjects selected")
        self.subject_count_label.setObjectName("muted")
        for i, (name, data) in enumerate(SUBJECTS.items()):
            card = QFrame()
            card.setObjectName("panel")
            card.setStyleSheet(f"QFrame#panel {{ border-left: 6px solid {data['color']}; }}")
            card_layout = QVBoxLayout(card)
            cb = QCheckBox(name)
            cb.setObjectName("choice")
            cb.setStyleSheet("QCheckBox#choice { border:0; font-size:17px; padding:5px; }")
            cb.stateChanged.connect(lambda state, n=name: self.subject_changed(n, state))
            card_layout.addWidget(cb)
            sub = QLabel(data["subtitle"])
            sub.setObjectName("muted")
            card_layout.addWidget(sub)
            grid.addWidget(card, i // 2, i % 2)
            self.subject_checks[name] = cb
        outer.addLayout(grid)
        outer.addWidget(self.subject_count_label)
        privacy_note = QLabel(
            f"Version {APP_VERSION}  ·  Your answers stay on this device unless you choose to save or share them."
        )
        privacy_note.setObjectName("muted")
        privacy_note.setWordWrap(True)
        outer.addWidget(privacy_note)
        outer.addStretch()
        bottom = QHBoxLayout()
        bottom.addStretch()
        start = QPushButton("Start exploring  →")
        start.setObjectName("primary")
        start.clicked.connect(self.start_flow)
        bottom.addWidget(start)
        outer.addLayout(bottom)
        return page

    def subject_changed(self, name, state):
        if state:
            self.selected_subjects.add(name)
        else:
            self.selected_subjects.discard(name)
        count = sum(1 for checkbox in self.subject_checks.values() if checkbox.isChecked())
        self.subject_count_label.setText(
            f"{count} subject{'s' if count != 1 else ''} selected"
        )

    def start_flow(self):
        # Read the live checkbox states directly. This avoids stale selection
        # state if Qt emits a tri-state value differently across platforms.
        self.selected_subjects = {
            name for name, checkbox in self.subject_checks.items()
            if checkbox.isChecked()
        }
        if not self.selected_subjects:
            self.show_notice("Choose a subject", "Select at least one subject to get started.")
            return
        self.answers = {}
        self.flow = []
        for subject in SUBJECTS:
            if subject in self.selected_subjects:
                data = SUBJECTS[subject]
                self.flow.append({
                    "key": f"subject_{subject}",
                    "eyebrow": f"SUBJECT EXPLORATION · {subject.upper()}",
                    "title": data["question"],
                    "subtitle": "Choose all the topics that interest you.",
                    "options": [(x, set(self.subject_tags(subject, x))) for x in data["options"]],
                    "multi": True,
                    "limit": 0,
                })
        # Give every general question a stable key. Subject questions already
        # receive keys above; without these, advancing to the first general
        # question raises KeyError in show_question().
        self.flow.extend(
            {**question, "key": f"general_{index}_{question['title']}"}
            for index, question in enumerate(GENERAL_QUESTIONS, start=1)
        )
        self.flow_index = 0
        self.show_question()

    def subject_tags(self, subject, option):
        tags = set()
        s = subject.lower()
        if s == "math":
            tags.update({"math", "analysis"})
            if "building" in option: tags.update({"engineering", "hands_on", "mechanical"})
            if "computer" in option: tags.update({"technology"})
            if "money" in option: tags.update({"business"})
        elif s == "science":
            tags.update({"science", "research"})
            if "animal" in option: tags.update({"animals", "environment", "outdoors"})
            if "body" in option: tags.update({"health", "helping", "people"})
            if "space" in option: tags.update({"space", "physics", "analysis"})
            if "technology" in option: tags.update({"technology", "engineering"})
            if "environment" in option or "Plants" in option: tags.update({"environment", "outdoors"})
        elif s == "reading":
            tags.update({"reading", "communication"})
            if "Stories" in option or "Writing" in option: tags.update({"creative", "story"})
            if "teaching" in option: tags.update({"teaching", "people"})
            if "mysteries" in option: tags.update({"analysis", "research"})
            if "languages" in option: tags.update({"language", "communication"})
        elif s == "social studies":
            tags.update({"social", "people"})
            if "History" in option: tags.update({"history", "research"})
            if "countries" in option: tags.update({"geography", "travel", "culture"})
            if "maps" in option: tags.update({"geography", "environment"})
            if "Helping" in option: tags.update({"helping", "community"})
            if "government" in option: tags.update({"law", "communication"})
            if "businesses" in option: tags.update({"business", "math"})
        return tags

    def show_question(self):
        q = self.flow[self.flow_index]
        total = len(self.flow)
        page, outer = self.shell()
        back = QPushButton("←  Back")
        back.setObjectName("back")
        back.clicked.connect(self.go_back)
        outer.addWidget(back)
        self.progress(outer, self.flow_index + 1, total)
        self.header(outer, q["eyebrow"], q["title"], q["subtitle"])
        outer.addSpacing(5)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget()
        choices = QVBoxLayout(content)
        choices.setContentsMargins(4, 4, 12, 8)
        choices.setSpacing(9)
        self.current_checks = []
        old = self.answers.get(q["key"], set())
        for label, tags in q["options"]:
            cb = QCheckBox(label)
            cb.setObjectName("choice")
            cb.setMinimumHeight(48)
            cb.setChecked(label in old)
            choices.addWidget(cb)
            self.current_checks.append((cb, label, tags))

        # For questions with a maximum, prevent selecting beyond the limit
        # and explain the rule rather than allowing a confusing late error.
        limit = q.get("limit", 0)
        if limit:
            def enforce_limit(changed_cb):
                selected_count = sum(1 for check, _, _ in self.current_checks if check.isChecked())
                if selected_count > limit:
                    changed_cb.blockSignals(True)
                    changed_cb.setChecked(False)
                    changed_cb.blockSignals(False)
                    self.show_notice("Selection limit", f"Choose up to {limit} options for this question.")
            for check, _, _ in self.current_checks:
                check.toggled.connect(lambda checked, current=check: enforce_limit(current) if checked else None)
        choices.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        hint = "Select up to three" if q.get("limit") else ("Select any that apply" if q["multi"] else "Choose one")
        hint_row = QHBoxLayout()
        hint_label = QLabel(hint)
        hint_label.setObjectName("muted")
        hint_row.addWidget(hint_label)
        hint_row.addStretch()
        self.selection_count_label = QLabel("")
        self.selection_count_label.setObjectName("muted")
        hint_row.addWidget(self.selection_count_label)
        outer.addLayout(hint_row)

        def update_selection_count():
            count = sum(1 for check, _, _ in self.current_checks if check.isChecked())
            self.selection_count_label.setText(
                f"{count} selected" if q["multi"] else ("1 selected" if count else "No answer selected")
            )

        for check, _, _ in self.current_checks:
            check.toggled.connect(update_selection_count)
        update_selection_count()

        bottom = QHBoxLayout()
        bottom.addStretch()
        next_btn = QPushButton("Continue  →" if self.flow_index < total - 1 else "Find my career ideas  ✨")
        next_btn.setObjectName("primary")
        next_btn.clicked.connect(self.save_and_continue)
        bottom.addWidget(next_btn)
        outer.addLayout(bottom)

        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        self.current_page = page

    def save_and_continue(self):
        q = self.flow[self.flow_index]
        chosen = [(label, tags) for cb, label, tags in self.current_checks if cb.isChecked()]
        if len(chosen) == 0:
            self.show_notice("Choose an answer", "Pick at least one option to continue.")
            return
        limit = q.get("limit", 0)
        if limit and len(chosen) > limit:
            self.show_notice("Choose fewer options", f"Please choose no more than {limit} options.")
            return
        self.answers[q["key"]] = {label for label, tags in chosen}
        if self.flow_index < len(self.flow) - 1:
            self.flow_index += 1
            self.show_question()
        else:
            self.show_results()

    def go_back(self):
        if self.flow_index == 0:
            self.stack.setCurrentWidget(self.home)
            return
        self.flow_index -= 1
        self.show_question()

    def show_results(self):
        profile = set()
        for q in self.flow:
            key = q["key"]
            selected = self.answers.get(key, set())
            for label, tags in q["options"]:
                if label in selected:
                    profile.update(tags)

        scored = []
        for title, description, tags in CAREERS:
            overlap = profile.intersection(tags)
            score = len(overlap)
            if score:
                scored.append((score, title, description, overlap))
        scored.sort(key=lambda x: (-x[0], x[1]))
        scored = scored[:8]
        self.current_profile = profile
        self.current_scored = scored

        page, outer = self.shell()
        back = QPushButton("←  Back to questions")
        back.setObjectName("back")
        back.clicked.connect(lambda: self.stack.setCurrentWidget(self.current_page))
        outer.addWidget(back)
        self.header(outer, "YOUR JOBFINDER PROFILE", "Career paths to explore",
                    "These suggestions are based on the interests and preferences you selected. They are possibilities, not limits.")
        summary = QLabel("Subjects: " + " · ".join(sorted(self.selected_subjects)))
        summary.setStyleSheet("background:#E8EFF8; padding:12px; border-radius:10px; font-weight:650;")
        summary.setWordWrap(True)
        outer.addWidget(summary)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget()
        listing = QVBoxLayout(content)
        if not scored:
            listing.addWidget(QLabel("Try selecting a few more interests to see career ideas."))
        for rank, (score, title, description, matched) in enumerate(scored, 1):
            card = QFrame()
            card.setObjectName("panel")
            card_layout = QVBoxLayout(card)
            row = QHBoxLayout()
            name = QLabel(f"{rank}.  {title}")
            name.setStyleSheet("font-size:17px; font-weight:800;")
            row.addWidget(name)
            row.addStretch()
            match = QLabel(f"{score} interest matches")
            match.setObjectName("muted")
            row.addWidget(match)
            card_layout.addLayout(row)
            desc = QLabel(description)
            desc.setWordWrap(True)
            desc.setStyleSheet("color:#607087;")
            card_layout.addWidget(desc)
            why = QLabel("Why it appeared: " + ", ".join(sorted(matched)))
            why.setWordWrap(True)
            why.setStyleSheet("color:#3977B8; font-size:12px;")
            card_layout.addWidget(why)
            detail_btn = QPushButton("Explore this career  →")
            detail_btn.setObjectName("primary")
            detail_btn.clicked.connect(
                lambda checked=False, career=title, why_tags=matched, rank_score=score:
                    self.show_career_detail(career, why_tags, rank_score)
            )
            card_layout.addWidget(detail_btn)
            listing.addWidget(card)
        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        bottom = QHBoxLayout()
        save_button = QPushButton("Save results  ↓")
        save_button.clicked.connect(self.save_results)
        bottom.addWidget(save_button)
        again = QPushButton("Start a new exploration")
        again.setObjectName("primary")
        again.clicked.connect(self.reset)
        bottom.addWidget(again)
        bottom.addStretch()
        outer.addLayout(bottom)
        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)
        self.results_page = page

    def show_career_detail(self, career, matched_tags=None, match_score=None):
        """Show a readable, kid-friendly profile for one recommended career."""
        description = next(
            (item[1] for item in CAREERS if item[0] == career),
            "Explore this career and learn what the work involves."
        )
        info = CAREER_DETAILS.get(career, {
            "day": description,
            "skills": "Curiosity, communication, problem-solving, and a willingness to keep learning.",
            "education": "Training depends on the specific role. Explore local schools, training programs, and professional requirements.",
            "pay": "Varies by role, location, experience, and employer.",
            "setting": "Work settings vary depending on the specialty and employer.",
        })

        page, outer = self.shell()
        back = QPushButton("←  Back to career matches")
        back.setObjectName("back")
        back.clicked.connect(lambda: self.stack.setCurrentWidget(self.results_page))
        outer.addWidget(back)

        self.header(
            outer,
            "CAREER PROFILE",
            career,
            description
        )

        if matched_tags is None:
            matched_tags = set()
        if match_score is None:
            match_score = 0

        match_panel = QFrame()
        match_panel.setObjectName("panel")
        match_layout = QVBoxLayout(match_panel)
        match_title = QLabel(f"Why JobFinder suggested this  ·  {match_score} matching interests")
        match_title.setStyleSheet("font-size:15px; font-weight:750;")
        match_layout.addWidget(match_title)
        if matched_tags:
            match_text = "This career connects with: " + ", ".join(sorted(matched_tags)) + "."
        else:
            match_text = "Explore this career because it may connect with interests you selected."
        match_desc = QLabel(match_text)
        match_desc.setWordWrap(True)
        match_desc.setStyleSheet("color:#607087;")
        match_layout.addWidget(match_desc)
        outer.addWidget(match_panel)

        sections = [
            ("A TYPICAL DAY", info["day"]),
            ("SKILLS THAT CAN HELP", info["skills"]),
            ("EDUCATION & TRAINING", info["education"]),
            ("WHERE THEY WORK", info["setting"]),
            ("PAY INFORMATION", info["pay"]),
        ]
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(2, 2, 10, 8)
        content_layout.setSpacing(10)

        for heading, body in sections:
            panel = QFrame()
            panel.setObjectName("panel")
            panel_layout = QVBoxLayout(panel)
            title_label = QLabel(heading)
            title_label.setObjectName("eyebrow")
            body_label = QLabel(body)
            body_label.setWordWrap(True)
            body_label.setStyleSheet("font-size:14px; color:#34465D;")
            panel_layout.addWidget(title_label)
            panel_layout.addWidget(body_label)
            content_layout.addWidget(panel)

        pay_note = QLabel(
            "Pay is a broad U.S. estimate for exploration, not a promise or starting salary. "
            "Actual earnings can be lower or higher depending on location, experience, specialty, "
            "hours, and employer."
        )
        pay_note.setWordWrap(True)
        pay_note.setObjectName("muted")
        content_layout.addWidget(pay_note)

        related = []
        current_tags = next((tags for title, _, tags in CAREERS if title == career), set())
        for title, short_description, tags in CAREERS:
            if title == career:
                continue
            shared = current_tags.intersection(tags)
            if shared:
                related.append((len(shared), title, short_description, shared))
        related.sort(key=lambda item: (-item[0], item[1]))
        if related:
            related_panel = QFrame()
            related_panel.setObjectName("panel")
            related_layout = QVBoxLayout(related_panel)
            related_heading = QLabel("RELATED CAREERS TO EXPLORE")
            related_heading.setObjectName("eyebrow")
            related_layout.addWidget(related_heading)
            for _, related_title, _, _ in related[:3]:
                related_button = QPushButton(f"{related_title}  →")
                related_button.clicked.connect(
                    lambda checked=False, name=related_title:
                        self.show_career_detail(name, set(), 0)
                )
                related_layout.addWidget(related_button)
            content_layout.addWidget(related_panel)

        scroll.setWidget(content)
        outer.addWidget(scroll, 1)

        bottom = QHBoxLayout()
        source_btn = QPushButton("Open U.S. Bureau of Labor Statistics career data")
        source_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(BLS_CAREER_URL))
        )
        bottom.addWidget(source_btn)
        bottom.addStretch()
        outer.addLayout(bottom)

        self.stack.addWidget(page)
        self.stack.setCurrentWidget(page)

    def reset(self):
        self.selected_subjects.clear()
        for cb in self.subject_checks.values():
            cb.setChecked(False)
        self.answers.clear()
        self.stack.setCurrentWidget(self.home)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
    window = JobFinder()
    window.show()
    sys.exit(app.exec())
