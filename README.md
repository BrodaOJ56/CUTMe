# CUTMe - URL Shortener
<p align="center">
  <img src="https://www.sms-magic.com/wp-content/uploads/2021/01/Shorten-URL-1024x635.png" width="300">
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
  <h1>CUTMe URL Shortener And Its Deployment To Render</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/BrodaOJ56/CUTMe#readme"><strong>Explore the Docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/BrodaOJ56/CUTMe/issues">Report Bug</a>
    ·
    <a href="https://github.com/BrodaOJ56/CUTMe/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#About-CUTMe-URL-Shortener">About CUTMe URL Shortener </a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#Features">Features</a></li>
    <li><a href="#What-I-learnt">What I learnt</a></li>
    <li><a href="#How-to-run-the-project-on-Local">How to run the project on Local</a></li>
    <li><a href="#Conclusion">Conclusion</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#Connect-With-Me">Connect With Me</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Blog -->
## About CUTMe URL Shortener

CUTMe is a URL shortening service developed using Flask and SQLAlchemy. It allows users to create shortened URLs for their long URLs, making them more convenient to share and remember.




<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]


<p align="right"><a href="#readme-top">back to top</a></p>


<!-- Features -->
## Features  

User Registration and Login: Users can create an account and log in to the application.

URL Shortening: Users can enter a long URL and generate a shortened URL.
Custom Short URLs: Users can customize the generated short URL by providing their preferred short code.

URL Analytics: Users can view analytics data for each shortened URL, including the number of clicks and user agents.

Account Dashboard: Users have access to a dashboard where they can manage their created URLs and view their account information.



## How to run the project on Local and on Live Server

1. Clone the repository:
```
git clone https://github.com/your-username/CUTMe.git
```
2. Create and activate a virtual environment (optional but recommended):
 ```
  python3 -m venv venv
  ```

```
source venv/bin/activate
```

3. Install the dependencies:
```
pip install -r requirements.txt
```
4. Set up the database:

- Create a PostgreSQL database.
- Update the database configuration in the config.py file.

5. flask run

6. Access the application in your web browser:

```
http://localhost:5000
```
---

<!-- Lessons from the Project -->
## What I learnt 
- Flask Web Framework
- Database Management
- User Authentication and Authorization
- Form Handling
- Database migrations with Flask-Migrate
- Debugging
- Error Handling

<p align="right"><a href="#readme-top">back to top</a></p>

---


## Conclusion
<!-- Conclusion -->

In conclusion, CUTMe is a URL shortener web application built with Flask. It provides users with the ability to shorten long URLs into shorter, more manageable links. The application also offers features such as customizing short URLs, tracking analytics for each shortened URL, and user registration/authentication.

By using CUTMe, users can easily share shortened URLs that redirect to the original long URLs. The application allows for personalized and user-specific URL management, giving users control over their shortened links.

The technology stack used in this project includes Python, Flask, SQLAlchemy, PostgreSQL, HTML, CSS, and JavaScript. The application is easy to install and configure, thanks to the provided installation instructions and configuration options.

Contributions to the project are welcome, and users are encouraged to report any issues or provide suggestions for improvement. The project is open-source and licensed under the MIT License, allowing for further development and customization.

Overall, CUTMe is a convenient and user-friendly URL shortener that simplifies the sharing and management of URLs, making it an ideal choice for anyone looking for a streamlined solution.

---

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/BrodaOJ56/CUTMe/blob/main/LICENSE">LICENSE</a> for more information.

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
[contributors-shield]: https://img.shields.io/github/contributors/BrodaOJ56/CUTMe.svg?style=for-the-badge
[contributors-url]: https://github.com/BrodaOJ56/CUTMe/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BrodaOJ56/CUTMe.svg?style=for-the-badge
[forks-url]: https://github.com/BrodaOJ56/CUTMe/network/members
[stars-shield]: https://img.shields.io/github/stars/BrodaOJ56/CUTMe.svg?style=for-the-badge
[stars-url]: https://github.com/BrodaOJ56/CUTMe/stargazers
[issues-shield]: https://img.shields.io/github/issues/BrodaOJ56/CUTMe.svg?style=for-the-badge
[issues-url]: https://github.com/BrodaOJ56/CUTMe/issues
[license-shield]: https://img.shields.io/github/license/BrodaOJ56/CUTMe.svg?style=for-the-badge
[license-url]: https://github.com/BrodaOJ56/CUTMe/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@ItzOfficialOJ-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/ItzOfficialOJ
[twitter-url]: https://twitter.com/ItzOfficialOJ
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white


