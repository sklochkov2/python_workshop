# How to prepare

## Activate virtual environment.

Use whichever means your IDE / tools provide, or run:

```shell
python3 -m venv .venv
. .venv/bin/activate
```

## Install dependencies

```shell
pip install fastapi "uvicorn[standard]" httpx requests
```

## Generate practice data

```shell
python src/generate_events.py
```

## Run practice API

Execute the following command in a separate tab, navigating to the directory where the virtual environment is located:
```
. .venv/bin/activate
uvicorn src.user_service:app --host 127.0.0.1 --port 8000
```

This will run our practice API, which will be available to serve requests on port 8000. Let's test it:
```shell
curl -s http://127.0.0.1:8000/user/user_00001 
```

# Concurrency modes we will explore

## Threading

Doc: [Python threading library](https://docs.python.org/3/library/threading.html)

## Asynchronous operation

Doc: [Python asyncio library](https://docs.python.org/3/library/asyncio.html)

## Multiprocessing

Doc: [Python multiprocessing library](https://docs.python.org/3/library/multiprocessing.html)
