# ExchangeP2pAPI
python version: 3.12.2
pip version: 24.1

## Installation
``` bash
pip install -r requirements.txt
```

### Installation django-cryptography 
``` bash
pip install "git+https://github.com/saurav-codes/django-cryptography"
```

## Run dev server
``` bash
python manage.py runserver
```

## Run periodic tasks
``` bash
# executive worker:
celery -A djangoP2pExchangeApi.celery worker --loglevel=info --concurrency 1 -P solo
```

# this command doesn't work on Windows
# celery -A djangoP2pExchangeApi.celery worker --beat -l info 

```bash
# run celery task from shell
python manage.py shell
from djangoP2pExchangeApi.tasks import call_endpoint1_task
call_endpoint1_task.delay()
```

