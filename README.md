# Data Engineering Onboarding & Learning Plan

Welcome to Optimus! This repository is designed to guide you through a set of topics and exercises to get you up to speed with essential concepts and tools. Each section contains learning material, links to external resources, and practical exercises. The goal is for you to complete this onboarding program within a specific timeline while also engaging with the hands-on exercises.

---

## Table of Contents
1. [Git](#1-git)
2. [Clean Code](#2-clean-code)
3. [Web Scraping](#3-web-scraping)
4. [Threading and MultiProcessing](#4-threading-and-multiprocessing)
5. [Databases](#5-databases)  
  5.1. [PostgreSQL](#51-postgres)  
  5.2. [MongoDB](#52-mongodb)  
  5.3. [S3](#53-s3)  
  5.4. [Redis](#54-redis)  
6. [Building API](#6-api)  
  6.1 [FastAPI](#61-fastapi)  
  6.2 [SQLAlchemy](#62-sqlalchemy)  
7. [Testing](#7-testing)
8. [Useful Python Libraries](#8-python-libraries)
9. [Rolling Exercise](#9-rolling-exercise)
10. [Data Engineering](#10-data-engineering)
11. [Kafka](#11-kafka)
12. [Splunk](#12-splunk)
13. [Trino](#13-trino)
   
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

### Duration: 0.5 Day

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

## 8. Useful Python Libraries

### Duration: 1 Day

- [NumPy Cheat Sheet](https://www.dataquest.io/cheat-sheet/numpy-cheat-sheet/)
- [NumPy Exercises](https://www.w3schools.com/python/numpy/default.asp)
- [Python Tutorial](https://www.w3schools.com/python/pandas/default.asp)

---

## 9. Rolling Exercise

### Duration: 5 Days

There is an exercise in the `rolling_exercise/` folder where you'll need to build an API. Follow the instructions provided in the folder.

---

## 10. Data Engineering

### Duration: 1 Hour

**DE Explanation**

- [DE Introduction](https://docs.google.com/document/d/1ZOsylqaWftkHFjnqHi_d3As8c_ifI8EOHQZhfscUdGo/edit?tab=t.0#heading=h.udg0q6xlt4mv)
- [DE Introduction Video](https://www.youtube.com/watch?v=qWru-b6m030)
If you feel that you don't understand it enough, you are more than welcome to read more about it.

---

## 11. Kafka🩷

### Duration: 1 Hour

- [Kafka Introduction](https://www.youtube.com/watch?v=Ch5VhJzaoaI&t=284s)
- [Get To Know the Terms](https://kafka.apache.org/intro#)

---

## 12. Splunk

### Duration: 1 Hour

- [Splunk Introduction and Cheat Sheet](https://www.stationx.net/splunk-cheat-sheet/)
- [Basic Splunk Searching](https://www.youtube.com/watch?v=GWl-TuAAF-k&t=102s)
- [Creating a Splunk Dashboard](https://www.youtube.com/watch?v=uQUAvY5M3RU)

---

## 13. Trino

### Duration: 0.5 Hour

- [Trino Introduction](https://www.youtube.com/watch?v=SKNJObdGCsY)
- [Trino Concepts](https://trino.io/docs/current/overview/concepts.html)
  
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

Happy learning!🤍
