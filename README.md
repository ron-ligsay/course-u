### Setup your Python Environment
##### Open your CMD or Command Prompt

##### **Make sure you have installed python and it is updated**
`pip install --upgrade pip`

##### Creating Environment
`python -m venv courseu`
<p>if Error: [WinError 2] The system cannot find the file specified:</p>
<p>go to your local Python file directory (`User/user/AppData/Loca/Programs/Python/Python<ver>/` or where you installed python), and try to input the command their again.</p>


##### **Activating Environment**
`courseu\Scripts\activate`
<p>your terminal should have the pipenv name in front ex: `(course) C:\\Users\user\folder>`</p>


<p>after successfully activating your environment</p>
<p>create a new folder called course-u</p>
`cd ..`
to step out or up in parent directory folder
then create a folder
`mkdir course-u` 
<p>cd to the directory `cd course-u`</p>
now you should be on your folder directory, like so `User/user/AppData/Loca/Programs/Python/Python38/course-u/`

### Connect to GIT
Git initialize folder

`git init`

add remote repo

`git remote add origin https://github.com/ron-ligsay/course-u.git`

pull

`git pull origin main`

check your current branch if its in main

`git branch`

if its not in main, change your branch and pull again

`git checkout main`

`git pull` then push `git push`

### Installing Pre-requisites
(note: your should install this when your python environment is activated)
`pip install -r requirements.txt`
this might take a while

### Setting up MySQL Database
(make sure you have mysql 8.0 or higher)
now open course_u/settings.py 
then on DABATASES, change the user and password corresponding to your database info

Markup : ```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'CourseU_DB',
        'USER': '<change to your user name>',
        'PASSWORD': '<change to your password>',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
      ```

<br>

(if your not sure of your user name and password open your MySQL workbench)
<br>

then on website/management/commands/create_database.py
change also the user and the password
---
Markup : ```
dataBase = mysql.connector.connect(
    host="localhost",
    user = "<change to your user>",
    passwd = "<change to your password>",
    auth_plugin='mysql_native_password'
)
    ```

---
### Setting up DJango
in your command prompt again, enter this commands:
<br>
`python manage.py makemigrates`
<br>
`python manage.py createsuperuser`
(this will prompt you to enter a username, password, password confirmation)
<br>
`python manage.py create_database`
<br>
`python manage.py migrate`
<br>
### then to run server
`python manage.py runserver`

<br><br>
then, you will see this:
    Django version 4.2.4, using settings 'course_u.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.

copy the HTTP, then open it on your browser.
to stop runserver `ctrl + c`
