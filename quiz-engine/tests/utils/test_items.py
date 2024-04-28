from app.init_data import init_course_id
temp_topic = {
  "contents": [
    {
      "content_text": "OOP is a programming paradigm based on classes and objects rather."
    },
    {
      "content_text": "OOP Pillars: Encapsulation, Inheritance and Polymorphism, and Abstraction."
    }
  ],
  "course_id": init_course_id,
  "description": "Learn OOPS in Python12",
  "title": "OOP"
}

temp_question = {
  "difficulty": "easy",
  "is_verified": True,
  "options": [
    {
      "is_correct": True,
      "option_text": "Missing BaseImage"
    },
    {
      "is_correct": False,
      "option_text": "Add COPY "
    }
  ],
  "points": 1,
  "question_text": "DevContainer common cause of syntax errors?",
  "question_type": "single_select_mcq",
  "topic_id": 1
}

temp_quiz_data = {
  "add_topic_ids": [
    1
  ],
  "course_id": 1,
  "difficulty_level": "easy",
  "quiz_title": "TypeScript Quiz",
  "random_flag": True
}