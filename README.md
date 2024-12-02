# Data Engineering Onboarding & Learning Plan

Welcome to Optimus! This repository is designed to guide you through a set of topics and exercises to get you up to speed with essential concepts and tools. Each section contains learning material, links to external resources, and practical exercises. The goal is for you to complete this onboarding program within a specific timeline while also engaging with the hands-on exercises.

---

## Table of Contents
1. [Git](#git)
2. [Clean Code](#clean-code)
3. [Web Scraping](#web-scraping)
4. [Threading and MultiProcessing](#threading-and-multiprocessing)
5. [Databases](#databases)
  5.1. [PostgreSQL](#postgres)
  5.2. [MongoDB](#mongo)
  5.3. [S3](#s3)
  5.4. [Redis](#redis)
6. [Building API](#api)
  6.1 [FastAPI](#fastapi)
  6.2 [SQLAlchemy](#sqlalchemy)
7. [Testing](#testing)
8. [Rolling Exercise](#rolling-exercise)
   
---

## 1. Git

### Duration: 1 Day

**Learning Material**:  
- Interactive Git learning: [Learn Git Branching](https://learngitbranching.js.org/)

**Notes**:  
- **Do not** cover the following topics:
  - Main: "Advanced Topics"
  - Remote: "To Origin And Beyond -- Advanced Git Remotes!"

---

## 2. Clean Code

### Duration: 1 Day

**Reference Material**:  
- [Clean Code Python](https://github.com/zedr/clean-code-python)  
This github page includes Python best practices to write clean and maintainable code.

**Exercise**:  
- In the `clean_code/` folder, you will find a `main.py` file that requires refactoring. Apply the principles described in the reference material to improve the code quality.

---

## 3. Web Scraping

### Duration: 1 Day

**Exercise**:  
In the `web_scraping/` folder, there is an exercise with instructions to perform web scraping on a websites.

---

## 4. Threading and MultiProcessing

### Duration: 2 Days

**Learning Material**:  
- [Practical Guide to Asyncio, Threading & Multiprocessing](https://itnext.io/practical-guide-to-async-threading-multiprocessing-958e57d7bbb8)
- [Multiprocessing VS Threading VS AsyncIO in Python](https://leimao.github.io/blog/Python-Concurrency-High-Level/)

**Exercise**:  
There is an exercise in the `threading_multiprocessing/` folder where you'll need to implement a multi-threaded solution to process data efficiently. Follow the instructions provided in the folder.

---

## 5. Databases

### Duration: 1 Day

**Learning Material**:

#### 5.1. PostgreSQL
A tutorial on postgreSQL (We know you've learnt it already, but go over it quickly)
- [Postgresql Tutorial](https://www.w3schools.com/postgresql/postgresql_exercises.php)

#### 5.2. MongoDB
- [Mongo Interactive Tutorial](https://www.mongodb.com/docs/manual/tutorial/getting-started/)

#### 5.3. S3
Quick overview about s3
- [S3 Guide](https://youtu.be/tfU0JEZjcsg?si=ch-W6mPULHn79Ars)

#### 5.4. Redis
Inroduction to Redis and learning the syntax
- [Redis Introduction](https://youtu.be/G1rOthIU-uo?si=jhEWzfj59GZrHBg7)
- [Redis Begginers' Guide](https://daily.dev/blog/redis-basics-for-new-developers)

---

## 6. Building API

### Duration: 1 Day

**Learning Material**:

#### 6.1. FastAPI
- [FastAPI Explanation](https://youtu.be/iWS9ogMPOI0?si=HPv_xetY7HGfOxPK)
- [FastAPI Syntax Guide](https://fastapi.tiangolo.com/tutorial/first-steps/)

**Notes**:  
- **Only** cover the following topics:
  - From "First Steps" to "Request Body"
  - "Handling Errors"
  - "Debugging"

#### 6.2. SQLAlchemy
- [SQLAlchemy Documentation](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_introduction.htm)

---

## 7. Testing

### Duration: 0.5 Days

**Learning Material**:
- [Begginers' Guide to Python Testing](https://medium.com/@sachinsoni600517/unit-testing-in-python-a-comprehensive-guide-for-beginners-985eec71bb4d)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [Mocking in Python](https://medium.com/@moraneus/the-art-of-mocking-in-python-a-comprehensive-guide-8b619529458f)

---

## 8. Rolling Exercise

### Duration: 5 Days

There is an exercise in the `rooling_exercise/` folder where you'll need to build an API. Follow the instructions provided in the folder.

---

## 9. Data Engineering

### Duration: 0.5 Days

- [DE Introduction](https://docs.google.com/document/d/1ZOsylqaWftkHFjnqHi_d3As8c_ifI8EOHQZhfscUdGo/edit?tab=t.0#heading=h.udg0q6xlt4mv)
- [DE Introduction Video](https://www.youtube.com/watch?v=qWru-b6m030)
  
---
## Submitting Your Exercises

1. Fork this repository to your own GitHub account.
2. Clone your fork locally:  
   `git clone <your-fork-url>`
3. Work on the exercises in their respective folders.
4. Work on a seperate branch for each exercise.
5. When you're ready, create a pull request for an exercise and inform your superior for a CR.
6. The pull request should be to your forked repository.

---

## Questions and Support

If you have any questions or need support, feel free to reach out to the team.

Happy learning!
