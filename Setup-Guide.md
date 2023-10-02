# Course-University - Recommender System
A Recommender System for the College of Computer in Information and Sciences (CCIS), provide recommended courses and jobs based on their soft and tech skills.

## Requirements:
* MySQL version 8 or higher
* Python 3.6 or higher
* Github/Git
<br>Optional:
* VS Code

<!-- ### Setup your Python Environment -->
##### Open your CMD or Command Prompt

##### **Make sure you have installed python and it is updated**
Use `pip --version` to verify if it's working,
If you have already installed it, and it's not updated use 
`pip install --upgrade pip`

<!-- ##### Creating Environment
`python -m venv courseu`
<p>if Error: [WinError 2] The system cannot find the file specified:</p>
<p>go to your local Python file directory (`User/user/AppData/Loca/Programs/Python/Python<ver>/` or where you installed python), and try to input the command their again.</p>


##### **Activating Environment**
`courseu\Scripts\activate`
your terminal should have the pipenv name in front example ***(course) C:\\Users\user\folder>*** -->


<!-- after successfully activating your environment -->
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
now open .env
then on DABATASES, change the user and password corresponding to your database info

Markup : ```
DB_NAME=courseu_db <br>
DB_USER=<replace_this_to_your_username> <br>
DB_PASS=<replace_this_to_your_password> <br>
DB_HOST=localhost   <br>
DB_PORT=3306    <br>
      ```
<br>
**note: on text with < >, replace it with the corresponding info**

<br>

(if your not sure of your user name and password open your MySQL workbench)
<br>


---
### Setting up DJango
in your command prompt again, enter this commands:
<br>
`python manage.py create_database`
<br>
`python manage.py load_csv_data3`
<br>
`python manage.py makemigrations`
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

----

once you have completed this setup once, you can follow these steps to run from start again:
<!-- ##### Activate Python Environment -->

<!--on you command prompt, locate your python environment that you have created (courseu), then go to that directory and enter command `courseu/Scripts/activate`-->
<!-- go to your project folder, right-click the folder (course-u) to open your visual studio

on your terminal, activate your python environment, by using command `courseu/Scripts/activate`

once your python environment is activated

make sure your project files are updated by using `git pull`

then once it is pulled, you are now ready to make your changes! -->

at first make sure you use `git pull` in order to synchronize your files with the remote repo


then you can use `python manage.py load_dump_file` to synchronize sql data on your database

after that you can start editing again and use `python manage.py runserver` to run your server

if you made changes the  databse, use `mysql -u <username> -p courseu_db < dump_file.sql` to update the sql file

.