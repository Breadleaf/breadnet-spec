# BreadNet Domain Name Server

## Setup

Make sure you have a postgres database running and configured somewhere...

Run the following commands

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 generate.py
```

Finally edit the generated `.env` file with the relevant fields.
