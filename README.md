# Developer Quick Start
This project uses Poetry for dependency management, so ensure you've added poetry to your Python environment. 

`python -m pip install poetry`

To install project dependencies, cd into the project's root directory and call `poetry install`. 
To add dependencies, use `poetry add [name-of-package]`. 
To remove dependencies, use `poetry remove [name-of-package]`


# Unit Testing Report
Pytest is used as main lib for unit test. To export the report, use the command below
`python -m pytest --html=<report_name>.html --self-contained-html`
Pytest-cov is used for export code coverage report. To export the HTML coverage report, use the command below
`python -m pytest --cov --cov-report=html`