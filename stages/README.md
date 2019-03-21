# OLA Scriptable Lighting

This project is currently in a very not-even-alpha state.

Expect lots of things to change in lots of ways.

## Intro

Drive OLA (Open Lighting Architecture) with an API

## Big TODOs
 * Tests, tests, tests
 * DMX Previewer
 * Command Line Args
 * Refactor into a library
 * Web API

## Install

You will need OLA installed (ideally, for ease of setup, on the same machine), on many systems this is as easy as `sudo apt/yum install ola`.

You will then need to navigate to the web UI at http://localhost:9090 and create a Universe with ID 1 and the appropriate device.

This has been developed with Python 3.7, which is the recommended version but Python 3.6 & 3.5 may work.

Replace `python3.7` with the name of the Python 3.7 binary on your system. It could be `python3.7`, `python37`, `python3` or `python`. Check with `python --version`.

Make sure you have pip

```
python3.7 -m ensurepip
```

Install `pipenv`

```
pip install pipenv
```

Install the app

```
pipenv install
```

Run it

```
pipenv run python main.py
```

or

```
pipenv shell
python main.py
```
