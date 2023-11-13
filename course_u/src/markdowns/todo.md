# TODO

check if tables exists
else, load_csv_data

on load_csv_data
import db_connection from different file
create a connection
import zip csv table files
if table not exits, create table
if table is empty, load csv data
else, do nothing


## High Priority
- [ ]: Maintenance
    - [X]: Loggers
    - [X]: Handlers
- [ ]: Unit Tests
    - [X]: Sample Unit Test
    - [ ]: Integration Tests
- [ ]: Transactions
    - [ ]: Create a transaction for every database operation
- [ ]: Reports
    - [ ]: Report Page for Admin/Instructors
    - [ ]: Report Email for Admin/Instructors
    - [ ]: Create a report for every database operation
    - [X]: Students
    - [X]: Grades
    - [ ]: Jobs
    - [ ]: Jobs_Applied
    - [ ]: Student_Career
    - [ ]: Feedbacks
    - [ ]: Instructors/Faculty
- [ ]: Track Page
    - [ ]: Courses 
## Medium Priority
- [ ]: # Path: todo.
- [ |-|x]: something
- [X]: git rm <files> that are on the [.gitignore]
- [X]: utils folder, for recommendation system model, job_post_scrapy, static_website
- [ ]: create submodules
    - [ ]: for recommender system model
    - [ ]: for job_post_scrapy
- [ ]: Debugger
    - [-]: on .env file, set DEBUG=True
    - [ ]: on codes, add a line calling the debugger passing on if DEBUG=True, debug this code and the message will be printed on the terminal
- [ ]: add dropdown group on nav bar
- [ ]: make nave bar foldable
- [ ]: update home page

- [ ]: Create a email verification
    - [ ]: Create a email verification for students
    - [ ]: Create a email verification for instructors
    - [ ]: Create a email verification for admin
    - [ ]: Create a email for password reset
    - [ ]: Email Templates
    - [ ]: Report Email for Admin/Instructors
- [ ]: Create a notification system
    - [ ]: Create a notification system for students
    - [ ]: Create a notification system for instructors
    - [ ]: Create a notification system for admin
    - [ ]: Create a notification system for password reset
    - [ ]: Notification Templates
    - [ ]: Report Notification for Admin/Instructors
- [ ]: Create a logging report w/email
- [ ]: Use Instructor domain, (using regex to identify it) and send confirmation email for verification.
    - This automatically creates an Instructor account

## Setups
-[-]: Create a virtual environment [Course-u]

## Home Section
- []: @ron-ligsay On Home Create a filter for Specialization on Page # Path: website/views.py
    - []: Create A Filter Buttons # Path: templates/home.html
    - []: Create A Filter Function # Path: website/views.py
    - []: Create A Filter URL # Path: website/urls.py
    - []: Create A Filter View # Path: website/views.py

## User Section
- [ ]: On user Sign up or Registration, verify if username and email is unique.
    - [ ]: send email verification
- [ ]: User Profiles:
    - Enhance the user profile functionality to allow students to input information about their academic interests, career aspirations, and preferences. This data will be valuable for making personalized recommendations.
- [ ]: Enhance the user profile functionality to allow students to input information about their academic interests, career aspirations, and preferences. This data will be valuable for making personalized recommendations.
- [ ]: creating a new users
- [ ]: Instructor Home Page
    - Has a list of all the students
    - Has a list of all the tests
    - Has a list of all the jobs


## Test Section
- [X]: User Grade Form
- [X]: User Year Level Form
- [ ]: Test Division, test should get only 1/4 set from the test, then when it wants to get again, it will get the next 1/4 set of the test. test should be randomized, test should not be repeated
- [ ]: Test Session # Path:
    - [X]: test session working properly
    - [X]: test session continous unfinished task of the user, else create new one
    - [X]: if test is complited for the year, it will prompt user if he/she finished the school year
    - [X]: if no, and user is superuser, use can either erase test set or delete entire set and create new one
    - [ ]: Create Notification or Pop up windows
        - user cannot exit test session when test is not finished
        - if user was forced or unintentionally exit test session, user will be redirected to test session page
    - [ ]: After test is completed and submitted, go to result page
    - [ ]: On result page record the User's Skills

## Personlaity


## Job Section

## Report Section

## Recommender Section

- [ ]: After every assessment, personality and grade inputs, update the user skill database
    - [x]: add subject-skills
    - [x]: add and update skill database with new skill sets from nakuri
    - [X]: model for specialization skills with level
    - [X]: reorganize the specialization skills data's fields
    - [X]: complete skills for test, subject, mbti, specialization (jobs are generated per scrape events)
    - [X]: Modify User Skill database to have a level field
    - [X]: fix acad subject skill id (note reset index, then recreate id)
    - [ ]: load csv data using management commands load_data
    - [ ]: views that would initiate or start the recommendation process
        - [ ]: crete a normalized data, from specialization (the database that would be recommended)
        - [ ]: create a normalized data, from user skills
        - [ ]: load the data to the recommendation system
        - [ ]: get the recommendation
        - [ ]: display the recommendation (with detailed information including the skills)
        - [ ]: save the recommendation

- [ ]: Create recommendation for job post
    - [ ]: use existing skill lists to get job post skills
    - [ ]: save data of jobs - csv/model/database for job_skills
    - [ ]: use recommendation system to recommend jobs

- [ ]: Recommendatioon algorithms
    - Develop algorithms that take into account a student's assessment history, academic preferences, and career goals to recommend academic tracks, specializations, and job postings.
- [ ]: Job Recommendations
    - Implement a recommendation system for job postings based on a student's academic background, preferences, and career goals. You can use techniques like content-based filtering or collaborative filtering for this purpose.
- [ ]: User Skills with count database
    - user_id, skill_id, count

## Others
- [ ]: Testing and Refinement:
    - Test your recommendation algorithms thoroughly to ensure they provide meaningful and accurate recommendations. Continuously refine the algorithms based on user feedback and data analysis.
- [ ]: User-Friendly Interface:
    - Design a user-friendly interface that presents recommendations in an understandable and engaging way.
- [ ]: Notifications:
    - Consider implementing notifications to alert students about new job postings, assessment opportunities, or updates related to their academic track.
- [ ]: Privacy and Security:
    - Ensure that user data, especially assessment results and personal information, is handled securely and with respect to privacy regulations.
- [ ]: Documentation and User Support:
    - Provide clear documentation to guide students on how to use the recommendation system and offer user support as needed.
- [ ]: Feedback Loop:
    - Establish a feedback loop with students to collect their input on the recommendations and continuously improve the system.
- [ ]: Configuration - database
    - Records variables such as number of questions per field
- [ ]: User Interaction - database



## Field/Specialization Section
- [ ]: Add Field/Specialization Table List on Admin_home
    - [ ]: View Field Page
      - [X]: View for Specialization
      - [ ]: CRUD for Specialization
    - [ ]: View for Test per Field

# BACKLOG


# DONE
- [x] Test System #bug
- [x] Create a Guide
- [-] Declined  #feat @ron-ligsay 2023-01-01


