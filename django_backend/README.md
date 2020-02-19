## Table of Contents

- [Basic Commands](#basic-commands)
- [Creating Admin Privileges](#creating-admin-privileges)
- [Creating a Table](#creating-a-table)
- [Migrations](#migrations)
- [Querying](#querying)
- [Media in Dev](#media-in-dev)
- [Adding Context Processor](#adding-context-processor)
- [Sending data to DOM in HTML](#sending-data-to-dom-in-html)
- [Pagination](#pagination)
- [Worklog](#work-log)

---

## Basic Commands

__Running the server__
```
python3 manage.py runserver
```

## Creating a Database

To kickstart the initial migration we use
```
python3 manage.py migrate
```

## Creating Admin Privileges

Before you create a user for admin, you need to create a database.

See [__Creating a database__](#creating-a-database)

The user details are stored in `auth_user` table.

```{bash}
python3 manage.py createsuperuser
```

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

__Adding a new field with data__

In order to actually populate the new column, you'll need to update the existing schema in `models.py` before running a data migration.

## Querying

To check your database migrations, you want to load a Python interpreter using
```{bash}
python3 manage.py shell
```
Your normal Python interpreter won't be able to locate your models.

The official docs for querying is [here](https://docs.djangoproject.com/en/3.0/topics/db/queries/).

A quicke example
```{python}
from tracker.models import Fund

print(Fund.objects.all())
print(Fund.objects.filter())
print(Fund.objects.get(ticker="IOZ.AX"))
```

## Media in Dev

In order to render images, one must make a few adjustments. First is to set the `MEDIA_ROOT` and `MEDIA_URL` in the project `settings.py` file.
```{python}
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```
Then we have to add the url patterns in `urls.py` of the project as well.
```{python}
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

Note: In production this will be different.

Finally to actually render the image you have just specify the url like below
```{html}
<img src="{{MEDIA_URL}}about_page_dp.jpg" alt="Placeholder image">
```

## Adding Context Processor

According to the [Django docs](https://docs.djangoproject.com/en/3.0/ref/templates/api/), you need to specify a dictionary of variables in a `context_processors.py` file to augment to the context and allow them to be seen by adding it into the 'context_processors' in the `settings.py` file.
```{python}

def add_context_var(request):
    return {
        'var1': var1,
        'var2': var2,
    }
```
```{python}
'context_processors': [
    ...
    'tracker.context_processors.add_context_var'
],
```

## Sending data to DOM in HTML

So, QuerySet objects aren't too good for converting to JSON format, and so we first

```{python}
import datetime as dt
import json
from django.core.serializers.json import DjangoJSONEncoder

cutoff_date = dt.datetime.today() - dt.timedelta(days=n)

prices = list(FundPrices.objects.filter(date__gte=cutoff_date).values_list("fund", "freq_type", "date", "price"))

# You can reformat it however much you want before passing it through.
prices_json = json.dumps(prices, cls=DjangoJSONEncoder)

context["prices_json"] = prices_json
```

See [here](https://stackoverflow.com/questions/7165656/passing-objects-from-django-to-javascript-dom?noredirect=1&lq=1)

To get javascript to grab the data, you want to use the `json_script` template builtin function (see docs [here](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#json-script))
```{python}
{{ prices_json | json_script:"id-name" }}
```
which can be retrieved with

```{javascript}
var value = JSON.parse(document.getElementById('id-name').textContent);
```

## Pagination

```{python}
from django.core.paginator import Paginator

items = ['a', 'b', 'c', 'd', 'e']
p = Paginator(items, 2)

# Now for some methods and attributes
print(p.page(1))
print(p.page(1).number) # returns page number

print(p.num_pages)
print(p.page(1).object_list)
print(p.page(1).has_previous))
print(p.page(1).has_next))
print(p.page(1).next_page_number))

for page in p.page_range:
    print(page)
```

## Worklog

See [WORKLOG](../README.md) in parent directory