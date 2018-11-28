After cloning the repository, install all dependencies:

```bash
$ pipenv install
```

Set required environment variables (using `.env` file is a [nice idea](https://pipenv.readthedocs.io/en/latest/advanced/#automatic-loading-of-env)):

```bash
SECRET_KEY='your-secret-key'
DEBUG=True
ALLOWED_HOSTS='*'
STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage'
DATABASE_URL=postgres://postgres:postgres@localhost:5432/livro-aberto
```

Finally, you run migrations and start the server

```bash
$ pipenv shell # or prefix the following commands with `pipenv run`
$ python manage.py migrate
$ python manage.py runserver
```

To run tests:
```bash
$ python manage.py test
```
