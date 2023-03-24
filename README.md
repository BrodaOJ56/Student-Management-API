# Student-Management-API
<p align="center">
  <img src="https://img.favpng.com/24/15/7/school-information-management-system-education-png-favpng-JVitNTht5EYkhT5fB2EsqtY2Z.jpg" width="300">
</p>

<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>


<div align="center">
  <h1>Flask REST API For School Student Management System And Its Deployment To Heroku</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/BrodaOJ56/Student-Management-API#readme"><strong>Explore the Docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/BrodaOJ56/Student-Management-API/issues">Report Bug</a>
    ·
    <a href="https://github.com/BrodaOJ56/Student-Management-API/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#About-Flask-REST-API-for-School-Student-Management-System">About Flask REST API for Student Management System</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#Deployed-With">Deployed With</a></li>
      </ul>
    </li>
    <li><a href="#Endpoints">Endpoints</a></li>
    <li><a href="#Error-Handling">Error Handling</a></li>
    <li><a href="#What-I-learnt">What I learnt</a></li>
    <li><a href="#How-to-run-the-project-on-Local-on-Live-Server">How to run the project on Local and on Live Server</a></li>
    <li><a href="#Conclusion">Conclusion</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#Connect-With-Me">Connect With Me</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Blog -->
## About Flask REST API for Student Management System

This is a Flask-RESTX API for managing student information and performance. The API includes endpoints for onboarding students, updating student's information, viewing student performance, and administrative functions such as adding new students, enrolling students to courses, adding performance and viewing all students.
The API has two roles: teacher and student. The teacher role has the full access to all the endpoints, which means, a teacher can perform all CRUD operation on course and student namespaces, while the student role can only register as a student, update personal information, view their own information and course performance.


<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]

### Deployed With:

![Heroku][heroku]

<p align="right"><a href="#readme-top">back to top</a></p>


<!-- Project Endpoints -->
## Endpoints 

Here are the some of the endpoints for this project;

Onboard a new User (Student and Teacher) 

```
POST /auth/register/student

Request body:
# Register as a Student
    {
        "email": "student@gmail.com",
        "first_name": "Olubunmi",
        "last_name": "Oluwatobi",
         "password": "password"
    }

```

```
POST /auth/register/teacher

Request body:
# Register as a Teacher
    {
        "email": "teacher@gmail.com",
        "first_name": "Adekunle",
        "last_name": "Olayinka",
         "password": "password"
    }

```

Update a student's information

```
PUT /students/<student_id>

Request body:
{
     "email": "adewale@gmail.com",
     "first_name": "Adewale",
     "last_name": "John"
}
```

View a student's grade

```
GET /students/<student_id>/courses/grade

Response body:
[
	{
		"name": "BCH103",
		"score": 80.0,
		"grade": "B"
	},
	{
		"name": "BCH102",
		"score": 50.0,
		"grade": "E"
	},
	{
		"name": "BCH104",
		"score": 89.0,
		"grade": "B"
	},
	{
		"name": "BCH105",
		"score": 88.0,
		"grade": "B"
	},
	{
		"name": "BCH106",
		"score": 81.0,
		"grade": "B"
	}
]

```

View all students

```
GET /students


Response body:
[
	{
		"id": "1",
		"identifier": "8831",
		"email": "s@gmail.com",
		"first_name": "David",
		"last_name": "Daniel",
		"admission_no": "STD/23/8831"
	},
	{
		"id": "3",
		"identifier": "9317",
		"email": "s1@gmail.com",
		"first_name": "Odumade",
		"last_name": "Babajide",
		"admission_no": "STD/23/9317"
	},
	{
		"id": "4",
		"identifier": "2306",
		"email": "s2@gmail.com",
		"first_name": "Ogunmola",
		"last_name": "Kayode",
		"admission_no": "STD/23/2306"
	},
	{
		"id": "5",
		"identifier": "3415",
		"email": "s3@gmail.com",
		"first_name": "Iterogba",
		"last_name": "Adeolu",
		"admission_no": "STD/23/3415"
	}
    ]

```
![Screenshot_20230319-000742~2](https://user-images.githubusercontent.com/82912148/226144960-7dc3315d-ee0f-4647-bf5d-35817ebc562c.png)


## Error Handling

The API includes error handling for the following scenarios:

- Invalid request body: The API will return a 400 Bad Request response with a message indicating the issue with the request body.
- Student not found: The API will return a 404 Not Found response with a message indicating that the student with the specified ID was not found.
- Unauthorized access: The API will return a 401 Unauthorized response if the user attempts to access an endpoint that requires authentication without providing valid credentials.
- Internal server error: The API will return a 500 Internal Server Error response if an unexpected error occurs.

---

<!-- Lessons from the Project -->
## What I learnt 
- How to set up a Flask API with Flask-RESTX
- Databases with Flask-SQLAlchemy
- JWT Authentication with Flask-JWT-Extended
- Environment variables with Python-Decouple
- Database migrations with Flask-Migrate
- How to write Unit Tests with Unittest and PyTest
- Documenting REST APIs with SwaggerUI and Flask-RESTX
- Error Handling
- Flask API Deployment via Heroku

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- GETTING STARTED -->
## How to run the project on Local and on Live Server

Clone the project Repository
```
git clone https://github.com/BrodaOJ56/Student-Management-API/
```

Enter the project folder
``` 
$ cd Student-Management-API
 
```

Install all requirements

```
$ pip install -r requirements.txt
```
Export to run the project in development environment

```
export FLASK_APP=api/
```
```
echo FLASK_APP
```

Create database

```
flask db init
```

```
flask db migrate -m "your description"
```

``` 
flask run
``` 


To use this API, on live server:

- Open the web API on your browser: https://student-management-flask-api.herokuapp.com/

Create a student or teacher account:

- Click 'auth' to reveal a dropdown menu of auth routes, then register as either as a student or teacher.
- Sign in via the '/auth/login' route to generate a JWT token. Copy this access token without the quotation marks

- Scroll up to click 'Authorize' at top right. Enter the JWT token in the given format, Bearer <token> for example:

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3OTE1NTM5MywianRpIjoiMGQ1MGFlNWUtZTAyMy00ZDI3LTg3MjAtNTFmMzg0NWJkZGRkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjc5MTU1MzkzLCJleHAiOjE2NzkyNDE3OTN9.Mr-uZ2Ne6H-RAGgooQq0jOuORCmdRnCqa3K1nCUlHQA

```

- Click 'Authorize' and then 'Close'

- Now authorized as either a student or teacher, you now perform various operations via the many routes in 'students', 'courses' endpoints'.

- When you're done, click 'Authorize' at top right again to then 'Logout'
---

## Conclusion
<!-- Conclusion -->

This Flask-RESTX API provides a basic framework for managing student information and performance. With the endpoints provided, a teacher can onboard new students and view all students in the system, while students can update their basic information and view their performance. The API is extensible and could be expanded to include additional functionality as needed.

---

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/BrodaOJ56/Student-Management-API/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Connect With Me

OLUBUNMI OLUWATOBI JAMES - [@ItzOfficialOJ](https://twitter.com/ItzOfficialOJ)


<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's Flask Lessons](https://github.com/CalebEmelike)
* [GitHub Student Pack](https://education.github.com/globalcampus/student)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/BrodaOJ56/Student-Management-API.svg?style=for-the-badge
[contributors-url]: https://github.com/BrodaOJ56/Student-Management-API/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BrodaOJ56/Student-Management-API.svg?style=for-the-badge
[forks-url]: https://github.com/BrodaOJ56/Student-Management-API/network/members
[stars-shield]: https://img.shields.io/github/stars/BrodaOJ56/Student-Management-API.svg?style=for-the-badge
[stars-url]: https://github.com/BrodaOJ56/Student-Management-API/stargazers
[issues-shield]: https://img.shields.io/github/issues/BrodaOJ56/Student-Management-API.svg?style=for-the-badge
[issues-url]: https://github.com/BrodaOJ56/Student-Management-APIissues
[license-shield]: https://img.shields.io/github/license/BrodaOJ56/Student-Management-API.svg?style=for-the-badge
[license-url]: https://github.com/BrodaOJ56/Student-Management-API/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@ItzOfficialOJ-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/ItzOfficialOJ
[twitter-url]: https://twitter.com/ItzOfficialOJ
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[Heroku]: https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white

