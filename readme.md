# Nullchan

Federated anonymous communication platform.

## Run dev server
```bash
# For the first time
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

# After initial setup
python manage.py runserver
```

## Authors
- Ivan Reshetnikov <ordinarydev@protonmail.com>
