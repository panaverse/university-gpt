## Deployment

Now the Quiz API Module have been tested in Deployment Environment.

We have optimized Docker Files for Deployment for:
- All FastAPI Microservices
- And NextJS as well

## Backend Microservices
You can build and deploy all of them using Dockerfile - in future we will setup and add
comprehensive deployment infrastructure and guidelines using kubernetes and terraform

## Frontend - Quiz Attempt Platform
In `next.config.js` uncomment the line `output: "standalone",`

Now deploy it just like the backend microservices. 

P.S: Each microservice production image is from 200 - 300 MB - this includes the nextjs as well.