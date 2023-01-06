# Nullchan

Anonymous communication platform.

[Learn more](https://github.com/alt-web/nullchan)

## Run dev server

1. Make sure the local IPFS server is running ([docker instructions](https://docs.ipfs.tech/how-to/run-ipfs-inside-docker/))

2. Prepare the environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

3. Run the server
```bash
python manage.py runserver
```

## Authors
- Ivan Reshetnikov <ordinarydev@protonmail.com>
