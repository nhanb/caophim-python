dev:
	caophim-manage runserver

test: lint djangotest

djangotest:
	caophim-manage test

shell:
	caophim-manage shell

lint:
	flake8
	black --check .
	isort --check-only --recursive .

localconfig:
	caophim-generate-config > caophim.conf.json

clean:
	rm -r dist
	rm -r src/caophim.egg-info
	rm caophim.conf.json

startdb:
	docker-compose up -d

destroydb:
	docker-compose down
	sudo rm -rf ../pgdata
