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




#### For urls
When creating URL patterns in Django, you define a `path` or `re_path` (regular expression path) with one or more parameters. Here's an explanation of the common parameters you might use:

1. `route` (required): This is the main part of the URL path that you want to match. It's a string without a leading slash. For example, if you want to match `myapp/somepage/`, the `route` would be `"somepage/"`.

2. `view` (required): This is the Python function or class-based view that should be called when the URL pattern is matched. You typically reference your view function or class here.

3. `kwargs` (optional): A dictionary of keyword arguments to pass to the view function. These arguments can be used to pass additional data to the view. For example, you might pass a specific `pk` value from the URL to identify a specific database record.

4. `name` (optional): A unique name for the URL pattern. You can use this name to reverse-resolve URLs in your templates or views. It's a good practice to name your URL patterns for better maintainability.

5. `converter` (optional): You can specify a converter to control the data type of a captured URL parameter. For example, you can use `int` to capture an integer value from the URL. Django provides various built-in converters like `int`, `slug`, `uuid`, etc.

Here's an example of a URL pattern definition in Django's `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
]
```

In this example:

- `route`: `'articles/'` and `'articles/<int:article_id>/'` are the URL patterns.
- `view`: `views.article_list` and `views.article_detail` are the Python functions that handle these URL patterns.
- `kwargs`: In the second pattern, `<int:article_id>` captures an integer value and passes it as a keyword argument to the `article_detail` view.

You can also use regular expressions and more complex patterns with `re_path` if needed.

When you define URL patterns in your project's `urls.py`, Django's URL dispatcher will use these patterns to route incoming requests to the appropriate view functions based on the matching URL.






Organizing a Django project with multiple apps can greatly improve maintainability and code organization. Based on the modules you've mentioned, here's how you could structure your Django project:

```plaintext
myproject/              # Main project directory
    myproject/          # Project settings and configuration
        __init__.py
        settings.py
        urls.py
        wsgi.py
    users/              # App for user management
        __init__.py
        admin.py
        models.py
        views.py
    student_test/       # App for student tests
        __init__.py
        admin.py
        models.py
        views.py
    student_recommender/  # App for student recommender
        __init__.py
        admin.py
        models.py
        views.py
    student_jobs/       # App for student jobs
        __init__.py
        admin.py
        models.py
        views.py
    student_learning_modules/  # App for student learning modules
        __init__.py
        admin.py
        models.py
        views.py
    instructor_test_maker/  # App for instructor test creation
        __init__.py
        admin.py
        models.py
        views.py
    instructor_student_test_reports/  # App for instructor's test reports
        __init__.py
        admin.py
        models.py
        views.py
    templates/          # Templates for rendering views
    static/             # Static files (CSS, JavaScript, etc.)
    manage.py           # Django management script
```

In this structure:

- Each app (e.g., `users`, `student_test`, `student_recommender`, etc.) contains its own `models.py`, `views.py`, and other app-specific files.
- The project-wide settings and configuration are in the `myproject` directory.
- Templates and static files are stored in their respective directories.
- The `manage.py` script is used for various Django management tasks.

This structure separates your project into different apps, making it easier to manage and maintain each module independently. Each app can have its own models, views, templates, and URLs related to its functionality. You can create more apps as needed for additional functionality.

Remember to update the project settings (`INSTALLED_APPS`) to include each app you create. Additionally, you can define user models, permissions, and groups as needed based on your project's requirements.

Finally, make sure to configure the project's URLs (`urls.py`) to route requests to the appropriate app views.