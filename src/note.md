to run pipenv on command prompt,
`pipenv shell`
then to run server
`python manage.py runserver`
then open your browser and go to
`http://localhost:8000/`
to stop runserver `ctrl + c`
to exit pipenv shell `exit`

switch python interpreter
to get your pipenv path use `pipenv --venv`
then go to your visual studio code, press `ctrl + shift + p` then type `python: select interpreter` then paste your pipenv path

to create .vscode folder and settings.json file
`mkdir .vscode`
`cd .vscode`
`touch settings.json`
then open settings.json file and paste this
`{
    "python.pythonPath": "C:\\Users\\<username>\\AppData\\Local\\Programs\\Python\\Python39\\python.exe"
}`
then save
