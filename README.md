# Async nbgrader

A jupyter extension which adds async capabilities to nbgrader's auto-grading service.

## Installation

1. Install this setup directly from GitHub using `pip install`:

```bash
pip install git+ssh://git@github.com/IllumiDesk/async-nbgrader.git
cd async-nbgrader
```

> **NOTE**: future versions will publish the `async-nbgrader` package to PyPi.

2. Create and activate your virtual environment:

```bash
virtualenv -p python3 venv
source venv/bin/activate
```

3. Install and Activate Extensions

Install and activate all extensions (assignment list, create assignment, formgrader, and validate):

```bash
jupyter nbextension install --sys-prefix --py async_nbgrader --overwrite
jupyter nbextension enable --sys-prefix --py async_nbgrader
jupyter serverextension enable --sys-prefix --py async_nbgrader
```

## Run the Auto-Grader

This package leverages the same Python API available with `nbgrader`. Therefore no additional changes are required to run the auto-grader for submitting assignments.

## Contributing

For general contribution guidelines, please refer to IllumiDesk's [contributing guidelines](https://github.com/IllumiDesk/illumidesk/blob/main/CONTRIBUTING.md).

The `async_nbgrader` package installs the `nbgrader` package as a required dependency, therefore you should not have to install it explicitly.

> The `async_nbgrader` package overrides `nbgrader`'s default auto-grading service (included with the `Formgrader` extension) by converting the grading service from a `syncronous` service to an `asyncronous` service. Thefore it's a good idea to get familiar with the `nbgrader` documentation (although not a must) to setup your local environment [by following these instructions](https://nbgrader.readthedocs.io/en/latest/contributor_guide/installation_developer.html).

Use `pytest` to run tests:

```bash
pytest -v
```

## License

Apache 2.0
