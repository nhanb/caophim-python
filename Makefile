dev:
	manage runserver

test: lint djangotest

djangotest:
	manage test  # `manage` is a script provided by the `caophim` package

lint:
	flake8
	black --check .
	isort --check-only --recursive .

localconfig:
	generate-config > caophim.conf.json
