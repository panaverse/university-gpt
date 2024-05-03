Initially we created this quiz-api fully using SQLAlchemy ASYNC Engine. On top of engine we
were using SQLModel for all the ORM & Data sanitization needs.

But do we really need this approach:

- FastAPI is already optimized for Async
- SQLModel is created by the same author
- There are some performance issues with current implementation
- Online there are scattered resources but none of them give the most satisfactory answer
- In SQLModel roadmap there's plan for async engine for long but no implementation yet.

And recently FastAPI Template new version was announced. In LinkedIn discussion there's
a particular comment:

```
~ Christoph Lins’ comment
Any plans for an async backend?


~ Sebastián Ramírez Montaño
Creator of FastAPI, Typer, SQLModel, Asyncer and other open source tools.

Not for this project, the idea is to keep it super simple and easy to extend. But SQLModel supports async, so you could use it in the endpoints for the hot paths.
```

There are many new version releases for FastAPI & SQLModel since our last implementation and
I decided to test latency after cold start in this template.

Quick Raw Tests After Cold Start:
Testing Endpoint: http://localhost:8080/quiz/api/v1/topics/
Tool: PostMan
Results: - Async Query was taking about 1.4 second & Sync Query took 2.1 Seconds.

Using SQLModel with Async Engine:
https://github.com/tiangolo/sqlmodel/issues/626

-> For Best Async Engine + Session Configuration refer to quiz-gpt branch.

-> In main branch we are using sqlmodel engine and session.