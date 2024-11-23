This application is a web app that is targeted for high school or low level collegiate baseball programs that would like to track and scout season long stats for all teams on the application. 

To start using this application. Know that it runs in django. First build your virtual environment of your choosing. Next run the following code snippit to pull in required modules:
`pip install -r /path/to/requirements.txt`

After the environment is fully set up, you will then need to run `py manage.py runserver` to run the server.

In order to have access to all of the features you must be an admin. 
Our preloaded admin login:

Username:  `admin` 

Password: `admin`

Once logged in as an admin account you will now see clickable buttons such as add team on the standing page, edit player in a teams page, edit games in the scuedule page. 

The clickable links are self explanatory and does what the link says. 

In the scueudle page when trying to sumbit game stats, click on the "Submit Game stats" button. You will then be brought to the game page where you will see you can edit the scores and the player stats for the game. You must click the "submit" button to submit the game.

Once submitted you will be brought back to the home page. Go to the "Standings" page and you will see the teams Wins and Losses updated from the game you just submitted. 
