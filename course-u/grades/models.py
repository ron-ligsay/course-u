#from django.contrib.auth.models import User
from django.db import models

# Define the course and year choices
COURSE_CHOICES = [
    ('CS', 'Computer Science'),
    ('IT', 'Information Technology'),
]

YEAR_CHOICES = [
    ('1', '1st Year'),
    ('2', '2nd Year'),
    ('3', '3rd Year'),
    ('4', '4th Year'),
]

SUBJECT_CHOICES = [
('1', 'Introduction to Computing'),
('2', 'Computer Programming 1'),
('3', 'Computer Programming 2'),
('4', 'Discrete Structures 1'),
('5', 'Modeling and Simulation'),
('6', 'Data Structures and Algorithms'),
('7', 'Discrete Structures 2'),
('8', 'Object Oriented Programming'),
('9', 'Logic Design and Digital Computer Circuits'),
('10', 'Design and Analysis of Algorithms'),
('11', 'Information Management'),
('12', 'Operating Systems'),
('13', 'Technical Documentation and Presentation Skills in ICT'),
('14', 'Fundamentals of Research'),
('15', 'Application Development and Emerging Technologies'),
('16', 'Computer Organization and Assembly Language'),
('17', 'Automata and Language Theory'),
('18', 'Principles of Programming Languages'),
('19', 'Human Computer Interaction'),
('20', 'Information Assurance and Security'),
('21', 'Software Engineering 1'),
('22', 'Web Development'),
('23', 'CS Thesis Writing 1'),
('24', 'Introduction to Artificial Intelligence'),
('25', 'Data Communications and Networking'),
('26', 'CS Thesis Writing 2'),
('27', 'Software Engineering 2'),
('28', 'Professional Ethics for Computer Scientist'),
('29', 'IT Social and Professional Issues'),
('30', 'Programming 3 (Structured Programming)'),
('31', 'Network Administration'),
('32', 'Quantitative Methods with Modeling and Simulation'),
('33', 'Integrative Programming and Technology'),
('34', 'Systemm Integration and Architecture 1'),
('35', 'Multimedia'),
('36', 'Database Administration'), 
('37', 'Principles of Management and Organization'),
('38', 'Technopreneurship'),
('39', 'Systems Analysis and Design'),
('40', 'Applications Development and Emerging Technologies'),
('41', 'Information Assurance and Security 2'),
('42', 'Systems Administration and Maintenance'),
('43', 'Social and Professional Issues in IT')
]

# Define possible grades
GRADE_CHOICES = [
    ('1', '1'),
    ('1.25', '1.25'),
    ('1.5', '1.5'),
    ('1.75', '1.75'),
    ('2', '2'),
    ('2.25', '2.25'),
    ('2.5', '2.5'),
    ('2.75', '2.75'),
    ('3', '3'),
    ('3.25', '3.25'),
    ('3.5', '3.5'),
    ('3.75', '3.75'),
    ('4', '4'),
    ('4.25', '4.25'),
    ('4.5', '4.5'),
    ('4.75', '4.75'),
    # ... Add all other grade choices up to 5.0
    ('5', '5.0'),
]

class Grade(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjectname = models.CharField(max_length=150, choices=SUBJECT_CHOICES)
    grade = models.CharField(max_length=4, choices=GRADE_CHOICES)
    course = models.CharField(max_length=150, choices=COURSE_CHOICES)
    year = models.CharField(max_length=150, choices=YEAR_CHOICES)
    