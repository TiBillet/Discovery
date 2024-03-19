# Server to link the Cashless Android app to the server

Requierement :
- python 3.10
- poetry
- django 4.2


## Usage

```bash
poetry install
poetry shell
# Create super user
poetry run python manage.py createsuperuser
# Run server
poetry run python manage.py runserver
```