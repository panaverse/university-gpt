# University GPT: Personalizing Education with Generative Artificial Intelligence

**Imagine a university that adapts to your individual learning style and pace.** That's the vision behind University GPT, a revolutionary **conversational tool and AI app** that personalizes education for each student.

University GPT is a conversational tool and a Generative AI app which personalizes education for each and every student. Students can access it using two kinds of interfaces: Graphic User Interface (GUI) and Conversational User Interface (Conversational UI).

The GUI will be built by using the OpenAI Assistant APIs and Conversational UI by using OpenAI GPTs. Both will be interacting with our University APIs. We will build both but first we will build the University Custom GPT.

## Microservices Overview

This repository contains the source code for the following microservices:

### 1. Assessment Evals

- Folder Name: assessment-evals
- Description: This service is responsible for managing assessments and evaluations within the system. It handles the recording of student attempts, grading, and providing feedback on assessments.
- Purpose: To facilitate the assessment process by ensuring accurate recording, grading, and feedback mechanisms for student evaluations.

### 2. Question Bank

- Folder Name: quiz-engine
- Description: The Question Bank service acts as a central repository for storing and managing questions and their respective answers. It provides functionalities for adding, updating, and retrieving questions.
- Purpose: To maintain a comprehensive database of questions and answers, ensuring easy access and management for quiz creation and assessment purposes.

### 3. Quiz Management

- Folder Name: quiz-management
- Description: This service oversees the management of quizzes, including their creation, configuration, and association with questions from the Question Bank service. It also handles the lifecycle of quizzes, such as activation and deactivation.
- Purpose: To provide a platform for creating and managing quizzes efficiently, allowing instructors to configure and administer quizzes seamlessly.

### 4. Educational Program

- Folder Name: educational-program
- Description: The Educational Program service manages educational programs, courses, topics, and related content. It facilitates the organization and structuring of educational materials.
- Purpose: To offer a structured approach to educational content delivery by managing programs, courses, and topics, aiding in effective learning management.

### 5. User Management

- Folder Name: user-management
- Description: User Management service handles user registrations, authentication, and role management across the system. It ensures secure access to the platform and assigns appropriate roles to users.
- Purpose: To manage user accounts and access permissions, providing a secure and personalized experience for students, instructors, and administrators.
