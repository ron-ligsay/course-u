# Djanago Build Guide
This is the build guide for the Django project.


## Django Structure
The django projects in our systems are:
- **course_u**      - contains the main settings of the project, this is the main project app of a django
- **assessment**    - contains the test system, this creates the test session and the test questions
- **jobs**          - contains the job section, this displays the job sections
- **recommender**   - contains the recommender system, this creates the recommendation for the user
- **websites**      - contains the home section, contains login, register, home, about, contact, etc.


## When creating a page
This is the step you should follow:
1. Create a new html file in the templates folder
    * create a html as normally you do
    <br>Other notes:
    * you could use the base.html for visitors and base_user.html for users such as students, instructor, admin
    * when you use the base.html or base_user.html, you can use the block content
    * when you login as students, instructor, admin required for that page, use the base_user.html
    * when you use base_user.html you can use another block content called block header, then specify the scripts you need to add for this page.
    * when adding css, js, images, etc. use the static folder and also add `{% load static %}` for static files to load
2. Create a new function in the views.py
    * create a function that will render the html file you created
    * 
3. Create a new url in the urls.py
    * create a url that will call the function you created in the views.py
    * this will serves as your link to the page you created

### For other notes
Watch youtube tutorials for django, there are a lot of tutorials out there.

#### Recommended Tutorials
- [Django Tutorial for Beginners](https://www.youtube.com/watch?v=UmljXZIypDc)
- [Django Tutorial for Beginners - Full Course in 3 Hours [2021]](https://www.youtube.com/watch?v=sm1mokevMWk)
- [Django Crash Course 2021 | Python Web Development Tutorial](https://www.youtube.com/watch?v=D6esTdOLXh4)
- [Django 3.2 Tutorial (2021) - Learn Django for Beginners](https://www.youtube.com/watch?v=6ManltU_8iU)
