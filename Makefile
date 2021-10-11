include envs/dev.env
export

deps:
	if ! command -v pipenv &> /dev/null; then pip install pipenv; fi
	pipenv install

migrate:
	pipenv run ./manage.py migrate

seed_users:
	pipenv run ./manage.py seed_users

seed_contacts:
	pipenv run ./manage.py seed

lint:
	pipenv run pylama

test:
	pipenv run ./manage.py test

run:
	pipenv run ./manage.py runserver localhost:8000

zip:
	git archive --format zip --output $(shell pwd)/contacts.zip master

init_no_deps: migrate seed_users seed_contacts test

init: deps init_no_deps
