init:
	git init
	pre-commit install
	poetry install
	git add .
	git commit -m ":tada: Initial commit."

lint:
	pre-commit run --all-files

test:
	poetry install
	poetry run pytest

freeze:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

freeze_dev:
	poetry export -f requirements.txt --dev --output requirements.txt --without-hashes

update:
	poetry update
	pre-commit autoupdate
