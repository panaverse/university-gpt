from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, email:str, mobile_number:str, name: str)->None:
        self.email = email
        self.mobile_number = mobile_number
        self.name = name

class Student(User):
    def __init__(self, studentID: str,  email: str, mobile_number: str, name: str) -> None:
        super().__init__(email, mobile_number, name)
        self.studentID = studentID

class Instructor(User):
    def __init__(self, instructorID: str, email: str, mobile_number: str, name: str) -> None:
        super().__init__(email, mobile_number, name)
        self.instructorID = instructorID
        