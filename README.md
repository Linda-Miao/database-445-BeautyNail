=== PROJECT OVERVIEW ===
A comprehensive web-based management system for nail and spa salons.
Replaces manual paper-based operations with digital solutions for
customer booking, staff management, and business operations.

=== SYSTEM REQUIREMENTS ===
- Python 3.9 or higher
- Django 4.2+
- MySQL 8.0 or SQLite for development
- Modern web browser (Chrome, Firefox, Safari, Edge)

=== INSTALLATION & SETUP ===

1. Python and Django setup:
   - Install Python: https://www.python.org/downloads/
   - install dependencies by running this command in terminal: pip install django mysqlclient pillow virtualenv

1. Database Setup:
   -There are two options to setup the database with its current data:

   -Option1: Because we integrate the user_auth into our code so to setup the database correctly we need to run two script.

    The steps should be:

	.Step 1: run queries of the script: option1_PhaseIII_Team 7_SQL script Submission.sql

	.Step 2: Inside folder BeautyNailProject, open the terminal to run the command: python manage.py migrate

	.Step 3: run queries of the script: option1_PhaseIII_Team 7_Script run after running python migration.sql

   -Option2: Just run a single SQL script file that was exported by MYSQL Workbench

	 Run the queries of the script: option2_Run only this file without the python migrate command.sql

   Note: For older MacBook Air i5 devices:
   - Install Docker + phpMyAdmin as alternative to MySQL Workbench

3. Update settings.py in folder BeautyNailProject\BeautyNail
   - Currently the user and password we use to connect to database is: user: root, password: root.
   - If your user and password are different than that, you should update the file settings.py in folder BeautyNailProject\BeautyNail
   - Go to database section and update this:
	DATABASES = {
    	'default': {
        'ENGINE'  : 'django.db.backends.mysql',  
        'NAME'    : 'beautynailnet',                 
        'USER'    : 'root',                     # <-- UPDATE line if you use another username
        'PASSWORD': 'root',              	# <-- UPDATE line if you user another password
        'HOST'    : 'localhost',                
        'PORT'    : '3306',
    		}
	}

4. Run the server:
   - Navigate to project directory: BeautyNailProject
   - Run migrations: python manage.py migrate
   - Create superuser: python manage.py createsuperuser 
   - You can also use the current admin account in database; username: admin; password: team7admin
   - Start server: 
			.open a terminal from project folder (BeautyNailProject)

			.run this command: python manage.py runserver

			(Note: on Window if you want to run the server inside virtual environment(venv)	
			you should run this first in terminal: venv\Scripts\activate)

5. Access Application:
   - Open browser: http://localhost:8000/
   - Login using admin account described above to access admin pages
   - The Django also provides a built-in admin page at: http://localhost:8000/admin

=== USER ROLES & FEATURES ===

BACKEND FUNCTIONALITY:

Customer Interface:
- Browse available services and pricing
- Book appointments online
- View booking history
- Submit reviews and ratings

Staff Interface:
- View appointment schedules
- Access customer information
- Track customer feedback

Admin Interface:
- Manage customers, staff, and services
- Monitor appointments and payments
- Check reviews and inventory

FRONTEND INTERFACE:

Homepage:
- Welcome message
- Popular services for client reference
- Events for company promotion
- Navigation to all sections

Customer Portal:
- Customer feedback system
- Rewards for special clients
- View button to return to homepage

Booking Appointment Interface:
- Simple and fast appointment booking for clients
- Confirm or cancel scheduled appointments
- Use email and phone login to check appointment status

Service Catalog Interface:
- Browse all services with pricing
- Each service includes "Book Now" button
- Direct navigation to booking interface

=== TECHNICAL FEATURES ===
- 10+ database tables normalized to BCNF
- Comprehensive SQL queries demonstrating joins, subqueries, and aggregations
- Model-View-Controller (MVC) architecture
- Responsive web design
- User authentication and role-based access control

=== CONTACT INFORMATION ===
Team 7 - TCSS445 Summer 2025
- Bao Thinh Diep
- Linda Miao

Course: TCSS445 Database Systems Design
Instructor: Tom Capaul
University of Washington Tacoma