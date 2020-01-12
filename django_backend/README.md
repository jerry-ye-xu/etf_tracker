## Table of Contents

- [Migrations](#migrations)
- [Worklog](#work-log)

---

## Migration

For this app we'll need to do an initial data migration in addition to the usual schema migration.

Before all of that, we will need to actually create the database first. So run these commands
```{bash}
python3 manage.py makemigrations
python3 manage.py migrate
```
now create another migration that is empty
```{bash}
python3 manage.py makemigrations --empty tracker
```
which we can then customise to serve our needs.

## Querying

To check your database migrations, you want to load a Python interpreter using
```{bash}
python3 manage.py shell
```
Your normal Python interpreter won't be able to locate your models.

The official docs for querying is [here](https://docs.djangoproject.com/en/3.0/topics/db/queries/).

## Worklog

See [WORKLOG](../README.md) in parent directory