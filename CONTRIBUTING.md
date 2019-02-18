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

Finally, run migrations and start the server:

```bash
$ pipenv run python manage.py migrate
$ pipenv run python manage.py runserver
```

If you want a functional data filled app, download [budget data](https://github.com/prefeiturasp/SME-Livro-Aberto/wiki/dev-data.tar.gz) from the [project wiki](https://github.com/prefeiturasp/SME-Livro-Aberto/wiki), unarchive it, and then load it to the database:

```bash
$ curl https://github.com/prefeiturasp/SME-Livro-Aberto/wiki/dev-data.tar.gz -o dev-data.tar.gz
$ tar -xvzf dev-data.tar.gz
$ pipenv run python manage.py loaddata data/budget_execution.json
```

To run tests:
```bash
$ python manage.py test
```
