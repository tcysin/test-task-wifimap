# Test task for WifiMap

## Installation (Linux)

- Clone the repository and navigate there.
- (optional) Create a *virtual environment* and activate it:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
- Install the required packages:
    ```bash
    pip install -r requirements/base.txt
    ```

Run the tests with `unittest`:
```bash
python3 -m unittest
```

## Quickstart

Run the analysis using `analysis.py` script:
```bash
user_id="1118"
python src/analysis.py \
    $user_id  \
    conns.csv  \
    hotspots.csv  \
    users.csv  \
    --loglevel=info
```

For usage, check out the docs:
```bash
python src/analysis.py -h
```

## Flask app

There is a simple Flask application that mirrors the functionality of the script. It is ok for demo purposes, but is rough.

### Setup

To set up the app, create the `data/` folder inside the project root directory, then copy CSV files **with names** `conns.csv`, `hotspots.csv`, `users.csv` inside this newly created folder:
```bash
mkdir data
cp ${somedir}/conns_test.csv data/conns.csv
cp ${somedir}/hotspots_test.csv data/hotspots.csv
cp ${somedir}/users_test.csv data/users.csv
```

> Note that the names *must match* - CSV imports are hard-coded inside the `db.py` module.

The final layout of the root folder should look like so:
```
data/
    conns.csv
    hotspots.csv
    users.csv
requirements/
src/
...
```

Run the Flask development server:
```bash
flask --app src/app --debug run
```

### API

There are 2 URL endpoints of interest:
- `/users/<user_id>/hotspots` provides the counts of hotspots for a particular user.
    - Accepts `location`, `since`, `lower`, `upper` query args.
- `/users/<user_id>/hotspots/unique_connections` provides the counts of unique connections to user's hotspots.
    - Accepts `since`, `min_unique_conns` query args.

Both are controlled through *query parameters*.
