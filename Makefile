lint:
	# stop the build if there are Python syntax errors or undefined names
	@pdm run flake8 pyswitch --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	@pdm run flake8 pyswitch --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics


test:
	@cat codecov_ats/tests_to_run.txt | xargs pdm run pytest --verbose --cov=pyswitch --cov-report=term-missing && pdm run python -m coverage xml

install:
	@pdm install

start:
	@python main.py

.PHONY: lint test install start
