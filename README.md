# thefaablab
Python 3.10 Node JS 16 On Mac OS X: brew install postgresql

Install pipenv

Django Local Development
pipenv shell python manage.py runserver --settings=code_breaker.local_settings

React Local Development
npm run dev

Production: How to Deploy to Heroku (while automatic deployments are not working)
Heroku had a security issue with GitHub and has turned off GitHub integrations.

Install the Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

heroku git:remote -a code-breaker-proj git push heroku main

If you want to run on Heroku, you need to set all environment variables documented in the Environment Variables section using "heroku config:set ENVIRONMENT_VARIABLE_NAME=value"

Heroku Deployment
You need access to Heroku in order to deploy our application: https://dashboard.heroku.com/apps/code-breaker-proj

Dyno formation is set in the Procfile

This app requires the Heroku Postgres add-on.

This app requires the heroku/nodejs and heroku/python buildpacks.

EndToEnd Testing
Make sure chromedriver is install on your machine

In one terminal:

pipenv shell python manage.py runserver --settings=code_breaker.local_settings

another terminal: npm run dev

third terminal: python manage.py test --settings=code_breaker.local_settings

**updating week issue is probably because you need run the npm run dev then redeploy (possibly in debug mode) **


# How it works
in HomePage.js redirects to the correct week, the week is based what you put in the state of HomePage.js and in views with "current_week"
if current week in views is more than current week in the homePage.js it will automatically show results
the there is an if statement based on whether or not the the user based of their session token has already submitted
it shows either the bid page if they havent submitted yet or the show results if they have submitted
next year yo umight have to add a year column to the table 