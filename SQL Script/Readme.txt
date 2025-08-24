We are using MySQL workbench for the project.

There are two options to setup the database with its current data:

Option1: Because we integrate the user_auth into our code so to setup the database correctly we need to run two script.

The steps should be:

	.Step 1: run queries of the script: option1_PhaseIII_Team 7_SQL script Submission.sql

	.Step 2: Inside folder BeautyNailProject, open the terminal to run the command: python manage.py migrate

	.Step 3: run queries of the script: option1_PhaseIII_Team 7_Script run after running python migration.sql

Option2: Just run a single SQL script file that was exported by MYSQL Workbench

	 Run the queries of the script: option2_Run only this file without the python migrate command.sql