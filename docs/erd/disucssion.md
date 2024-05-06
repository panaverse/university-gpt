Most of the Modules in ERD have been inspired from Model Schema. It's among the most comprehensive and successful open source project. The Quiz Engine Microservice Schema is mostly taken and developed on top of the Moddle implementation.

We have 4 Microservice each have it's own DataBase. It's an implementation to make it headless so 
any organization can the desired microservices easily.

- Auth is separate Microservice - Use it for Quiz or just change it with your organization Auth Microservice.
- Educational Program can be used as it is and for existing educational institutes they can just Change it.
- Quiz-Engine is the Core Quiz Service that have Topic, Content, Quiz Engine (A set of 5 quiz tables) and QuestionBank.
- Assessment-Evals that is used to attempt Quizzes