# Django 4.2 app for servers

### Starting by creating poetry envirenment.
We will start with creating the poetry envirenment. First of all we'll have to install poetry. ***Look at the prevews link if you want to install poetry:*** https://python-poetry.org/docs/

If you allredy have poetry:
`poetry init`
Than you'll choose the package name, version, author name, description and licence. Latter you'll select the versions of python, django and other dependences.

We have:
- python 3.10
- django 4.2
- django-browser-reload 1.11
- Markdown 3.4.4
- ipdb 0.13.13
- cryptography 41.0.4

###### If you want to create latter the packeges you can use the prevews comande
`poetry init --no-interaction --dependency django`

Than we'll create the django project via the poetry:
`poetry run django-admin startproject primarilink_serveur`
This wi'll create the project. With `manage.py` and the `primarilink_serveur`, in the last one we'll find alsow the 'settings.py'

#### Creating the application 'cryptographie'
In this app we'll manage the creation and the exploitation of the 'url', 'pin code' and rsa public keys.

CCreating the app:
```bash=
poetry bash
poetry lock
./manage.py startapp cryptographie
```

### Creating the models and the url-s
