# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 -m flask run

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

test:
	python -m pytest --capture=no

cov:
	coverage run -m pytest
	coverage report -m

lint:
	pylint *.py

init_db:
	flask db init

migrations:
	flask db migrate

upgrade:
	flask db upgrade

.PHONY: all venv run clean
