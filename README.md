# Test task for WifiMap

## Installation (Linux)

- Clone the repository.
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
