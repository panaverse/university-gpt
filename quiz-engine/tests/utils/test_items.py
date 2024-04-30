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

mock_course = {
  "name": "Quarter 3: API Design, Development, and Deployment using FastAPI, Containers, and OpenAPI Specifications",
  "description": " An API-as-a-Product is a type of Software-as-a-Service that monetizes niche functionality, typically served over HTTP.\n    OpenAI APIs are themselves this kind of service. An application programming interface economy, or API economy, refers to the business structure\n    where APIs are the distribution channel for products and services. In this quarter we will learn to develop APIs not just as a backend for our\n    frontend but also as a product itself. In this model, the API is at the core of the business's value. We will be using Python-based FastAPI as\n    our core library and Pedantic, SQLAlchemy, and Postgresql databases for API development. Docker Containers will be our fundamental building block\n    for development, testing, and deployment. For local development, we will be using Docker Compose and DevPod which is Dev-Environments-As-Code,\n    for testing Pytest and Testcontainers, and for deployment Google Cloud Run, Azure Container Service, and Kubernetes. We will be using Terraform\n    as our Infrastructure as Code (IaC) tool. OpenAI Chat GPT 4, Google Gemini APIs, and Langchain will be used to build these API-as-a-Product. ",
  "id": 1,
  "program_id": 1
}