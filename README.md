### Setup your Python Environment
##### Open your CMD or Command Prompt

##### **Make sure you have installed python and it is updated**
Use `pip --version` to verify if it's working,
If you have already installed it, and it's not updated use 
`pip install --upgrade pip`

##### Creating Environment
`python -m venv courseu`
<p>if Error: [WinError 2] The system cannot find the file specified:</p>
<p>go to your local Python file directory (`User/user/AppData/Loca/Programs/Python/Python<ver>/` or where you installed python), and try to input the command their again.</p>


##### **Activating Environment**
`courseu\Scripts\activate`
your terminal should have the pipenv name in front ex ***(course) C:\\Users\user\folder>***


after successfully activating your environment
create a new folder called course-u <br>
`cd ..` <br>
to step out or up in parent directory folder
then create a folder <br>
`mkdir course-u` <br>
cd to the directory `cd course-u` <br>
now you should be on your folder directory, like so `User/user/AppData/Loca/Programs/Python/Python38/course-u/`

### Connect to GIT
Make sure your `git config user.name` and `git config user.email` is same with your GitHub account
Git initialize folder, 
make sure you are on ***course-u*** folder
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
if you are in main, use `git push --set-upstream origin main`
then use `git pull` to make sure it's working

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
`python manage.py create_database`
<br>
`python manage.py makemigrates`
<br>
`python manage.py createsuperuser`
<br>
(this will prompt you to enter a username, password, password confirmation)
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
