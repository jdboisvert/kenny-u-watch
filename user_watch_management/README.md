# User Watch Management v0.0.0
This application handles the auth and admin of the user management API along with the tables to track a user's info and alert data.

## Features

- Manage a user's alert
- Create an alert
- Admin portal functionality
- API to authenticate via JWT

## Usage

## Development

### Getting started

```shell
# install pyenv (if necessary)
brew install pyenv pyenv-virtualenv
echo """
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
""" > ~/.zshrc
source ~/.zshrc

# create a virtualenv
pyenv install 3.9.11
pyenv virtualenv 3.9.11 user_watch_management
pyenv activate user_watch_management

# install dependencies
pip install -U pip
pip install requirements.txt
pip install requirements_dev.txt
```

### Pre-commit

A number of pre-commit hooks are set up to ensure all commits meet basic code quality standards.

If one of the hooks changes a file, you will need to `git add` that file and re-run `git commit` before being able to continue.

#### Initialize pre-commit
```bash
pre-commit install
```


### Git Workflow

This repo is configured for trunk-based development. When adding a new fix or feature, create a new branch off of `main`.

Merges into main _must always be rebased and squashed_. This can be done manually or with GitHub's "Squash and Merge" feature.

### Testing

This project simply uses the built in testing provided by the Django web framework.

1. `test`

    We write unit tests for each piece of functionality we add. You can simply run all the tests with the following command:

    ```
    python manage.py test
    ```

    To run all tests for a specific app (ex: alerts) run the following command:

    ```
    python manage.py test alerts.tests
    ```

    To preserve test database run the following command:

    ```
    python manage.py test alerts.tests --keepdb
    ```

    To run tests and ignore warnings (ex: datetime warnings)

    ```
    python -Wignore manage.py test alerts.tests
    ```

### PRs and Releases

GitHub Actions is configured to perform unit tests against MacOS and Linux runners using both Python 3.8, 3.9, and 3.10 for all new PRs.

It will also check if the version has been bumped. To do that, use `bumpver update`. This will bump the version number everywhere and create a new commit.

After merging in a PR, GitHub Actions will package the module and create a new release for it on GitHub.

## Credits

- Jeffrey Boisvert ([jdboisvert](https://github.com/jdboisvert)) [info.jeffreyboisvert@gmail.com](mailto:info.jeffreyboisvert@gmail.com)
