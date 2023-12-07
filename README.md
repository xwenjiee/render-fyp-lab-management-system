# render-fyp-lab-management-system
My final year project lab management system with online feature. Database and site successfully hosted on Render.

Installation and Setup Instructions:

1. Go to command prompt
Run these commands: 
2. git clone https://github.com/xwenjiee/render-fyp-lab-management-system.git
3. cd render-fyp-lab-management-system
4. cd LabWise
5. python -m venv venv
6. venv\Scripts\activate
7. python -m pip install -r requirements.txt
8. python manage.py migrate
9. python manage.py runserver

The website will be running on localhost http://127.0.0.1:8000/ 
The website will be connected to the database which is hosted on Render. Refer to settings.py file for database connection details.

Login with these credentials
Admin account----
username: admin
password: MyPassword123

Customer account----
username: customer1
password: MyPassword123
