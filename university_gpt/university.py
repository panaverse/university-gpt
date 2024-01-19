from topic import Topic
from user import Student, Instructor


class University():
    def __init__(self, id: str, name:str):
        self.id = id
        self.name = name
        self.programs: list[Program]  = []
        

class Program():
    def __init__(self, id:str, name:str):
        self.id = id
        self.name = name
        self.courses: list[Course]  = []

class Course():
    def __init__(self, id:str, name:str):
        self.id = id
        self.name = name
        self.topics: list[Topic] = []
        self.students: list[Student] = []
        self.instructors: list[Instructor] = []


