# MS Teams Notification Lambda
Notification for AWS CloudWatch Alarms on Microsoft Teams. Check my [other projects](https://linktr.ee/michal_baron)

Stack:
- Python
- AWS Cloud Development Kit
## Introduction

**TODO: describe your project in one or two sentences.**

## Structure

This repository consists of the following elements:

 - `infrastructure` - contains the CDK code for the project
 - `.pre-commit-config.yaml` - parent configuration used by `pre-commit`
 - `tests` - AWS stack unit tests - It will be developed in future.
 - `requirements*.txt` - requirements used in project

## Local setup

### Installing requirements

Create and activate a virtual environment:

```commandline
python3 -m venv .venv
source .venv/bin/activate
```

Assuming that the `virtualenv` is activated, install the dependencies in the following way:

```commandline
pip install -r requirements.txt
```

### Running unit tests manually

Assuming that the `virtualenv` is activated, and the dependencies are installed, run the following command:

```commandline
pip install -r requirements-dev.txt
pytest infrastructure/tests/
```

### Static code analysis

> **_NOTE_:** This step applies locally. You have to repeat it for every project.

This project uses `pre-commit` to run various static code checks.
To make use of `pre-commit` locally, run:

    # In your git repo
    $ pre-commit install

This creates a .git/hooks/pre-commit script which will check your git config and run checks that are enabled.

To run the checks, type in:

    # In your git repo
    $ pre-commit run -a

> **_NOTE_:**   Using `pre-commit` script means that a number of code formatters and code quality checks will be
executed once you create a commit. **If any of these checks fail, your commit will not be created!**.
Some of these failures are resolved by `pre-commit` by reformatting the code, but some may require manual action.
Once the changes are applied either by you, or by pre-commit, add the affected files to staging again (`git add -u`)
and try to create a commit again.

It may happen that you will need to repeat this step 2 times. The basic flow is:

1. `git commit -m ...`
2. Git commit fails due to errors reported by pre-commit
3. Errors are fixed manually or by pre-commit
4. Files are added to git staging again (`git add -u`)
5. `git commit -m ...`
