from abc import ABC, abstractmethod
from university_gpt.user import Student

# class QuestionBank:
#     def __init__(self, questionBankID:str, student: Student, subpath: str, questionBankTitle:str) -> None:
#         self.questionBankID:str = questionBankID
#         self.user: Student = student
#         self.subpath: str = subpath
#         self.questionBankTitle : str = questionBankTitle
#         self.topics: list[Topic]= []

class Content(ABC):
    def __init__(self) -> None:
        self

class Topic:
    def __init__(self, str, topicID:str, title: str, desc: str) -> None:
        self.topicID: str = topicID
        self.title: str = title
        self.desc : str = desc
        self.subtopics : list[Topic] = []
        self.questions : list[Question] = []
        self.contents: list[Content] = []


class Question(ABC):
    def __init__(self, topicID: str, questionID:str, title:str, text: str, points: int = 1) -> None:
        self.topicID: str = topicID
        self.questionID: str = questionID
        self.title: str = title
        self.text: str = text
        self.points: int = points

    def getPoints(self)-> int:
        return self.points

    def getQuestionCount(self)-> int:
        return 1

class Option:
    def __init__(self, questionID: str, optionID: str, text: str, correct:bool) -> None:
        self.questionID = questionID
        self.optionID = optionID
        self.text = text
        self.correct: bool = correct

class MCQ(Question):
    def __init__(self, questionBankID: str, topicID: str, questionID: str, title:str, text: str) -> None:
        super().__init__(questionBankID, topicID, questionID, title, text)
        self.options: list[Option]= []

    def getOptions(self)-> list[Option]:
        return self.options
    
class SingleSelectMCQ(MCQ):
    def __init__(self, topicID: str, questionID:str, title:str, text: str) -> None:
        super().__init__( topicID, questionID, title, text)

class MultipleSelectMCQ(MCQ):
    def __init__(self, topicID: str, questionID: str, title:str, text: str) -> None:
        super().__init__(topicID, questionID, title, text)

class CaseStudy(Question):
    def __init__(self, topicID: str, questionID: str, title:str, text: str) -> None:
        super().__init__(topicID, questionID, title, text)
        self.text: str = text
        self.mcqs: list[Question]= []

    def getQuestions(self)-> list[Question]:
        return self.mcqs

    def getPoints(self)-> int:
        points: int = 0
        for q in self.mcqs:
            points += q.getPoints()
        return points
    
    def getQuestionCount(self)-> int:
        return len(self.mcqs)

class FreeTextQuestion(Question):
    def __init__(self,  topicID: str, questionID: str, title:str, text: str, points: int, correctAnswer: str) -> None:
        super().__init__( topicID, questionID, title, text, points)
        self.correctAnswer = correctAnswer
    
    
class CodingQuestion(Question):
    def __init__(self, topicID: str, questionID: str, title:str, text: str, points: int, correctAnswer: str) -> None:
        super().__init__(topicID, questionID, title, text, points)
        self.correctAnswer = correctAnswer
