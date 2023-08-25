# Alert Producer v0.1.0

An application used to analyze new postings on the Kenny U-Pull website which will then notify all subscribers.

## Usage

See the [usage](./docs/usage.md) document for more information.

## Development

### Getting Started

    # install golang
    brew install golang

    # install the golangci linter
    # more details: https://golangci-lint.run/
    brew install golangci-lint

    # install pre-commit
    pip install pre-commit
    pre-commit install

You will also need to set up MySQL locally. You can do this with the following command:

    brew install mysql

Once installed, you can start the MySQL server with the following command:

    brew services start mysql

You will find the SQL scripts to create the database and tables in the `./sql/` directory named `create_tables.sql`. Run this script to create the database and tables locally by connecting to your local MySQL server and running the script.

Downloading dependencies
    go mod download

### Environment Variables
Make a copy of the `.env.example` file and rename it to `.env`. This file contains all the environment variables needed to run the application locally.

### Pre-commit

A number of pre-commit hooks are set up to ensure all commits meet basic code quality standards.

If one of the hooks changes a file, you will need to `git add` that file and re-run `git commit` before being able to continue.


### Git Workflow

This repo is configured for trunk-based development. When adding a new fix or feature, create a new branch off of `main`.

Merges into main *must always be rebased and squashed*. This can be done manually or with GitHub's "Squash and Merge" feature.

### Testing

All test files are kept in ./test/ and named *_test.go.

You can run all tests with the following command:

    go test ./...

### Running server

    # run the server
    go run .

### Running via Docker

To make it easier to test you can also run the application via Docker. For now the table creation is manual and you will need to run the SQL scripts in the `./sql/` directory named `create_tables.sql` to create the database and tables locally by connecting to your image's MySQL server and running the script.

This can be done by opening a terminal in the container and running the following command:

    mysql -u root -p

You will be prompted for a password. The password is set in the `./.env` file and is `password` by default.

A key thing to do before building is ensure the .env file values are set correctly and set up in the environment variables.

Build the images

    docker compose build

Run the containers

    docker compose up
