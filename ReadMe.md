# About

I've met some problem with running tests using FastAPI+SQLAlchemy and PostgreSQL,
which leads to lots of errors (however, it works well on SQLite).
So I created a repo with MVP app and Pytest on Docker Compose testing.

The basic error is `InterfaceError('cannot perform operation: another operation is in progress')`.
This may be related to the app/DB initialization, though I checked that all the operations
get performed sequentially.
Also I tried to use single instance of `TestClient` for the all tests, but got no results.

Feel free to tell a solution `:)`

## Run tests

```bash
docker-compose -f docker-compose.test.yml up --build
```

Or:

```bash
pip install -r requirements.txt
pytest tests.py
# But this will use SQLite by default 
```
