import enum
from sqlmodel import SQLModel, Field
from datetime import datetime

# Enum for QuestionDifficulty
class UserRole(str, enum.Enum):
    student = "student"
    experienced_student = "experienced_student"
    section_leader = "section_leader"
    section_leader_mentor = "section_leader_mentor"
    head_ta = "head_ta"
    instructor = "instructor"
    admin = "admin"