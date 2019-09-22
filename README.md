# Django-uikit Blueprint

**version: 1.0.0**

Simple boilerplate for Django project. with full authentication system
and a blog app fully functional using Uikit CSS framework

---
## Contributors:
- Hicham Gamany

## Licence and Copyright:
&copy; Hicham Gamany, hgamany@gmail.com


## Documentation:
For developement:
- `git clone <repository> <your-project-name>`
- `cd ~/<your-project-name>`
- `virtualenv env`
- `source env/bin/activate`
- `pip install -r requirements.txt`
- create a secret key for the app(google search: django secret key generator)
- change .env_copy to .env
- setup .env variables (SECRET_KEY, Email config)
- `python manage.py rename <your-project-name>`
- `python manage.py migrate`
- `python makemigrations users blog pages`
- `python manage.py migrate`
- `python manage.py collectstatic`
- `python manage.py createsuperuser`
- `python manage.py runserver`
- `rm-rf .git`
- you can now create your own repository

#
 For production:

 I have tested it in Digital Ocean and Digital Ocean Spaces (for static files)
 checkout <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04>
 for the instructions, it's very detailed.
 
 ### notes:
 - instead of creating a new django project, pull your project from github using:
 - `git init`
 - `git remote add origin <your-github-repository>`
 - `git pull origin master`
 




