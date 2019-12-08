dev:
	caophim-manage runserver

test: lint djangotest

djangotest:
	caophim-manage test --settings=caophim.test_settings

shell:
	caophim-manage shell

lint:
	flake8
	black --check .
	isort --check-only --recursive .

localconfig:
	caophim-generate-config > caophim.conf.json

clean:
	rm -rf dist
	rm -rf src/caophim.egg-info
	rm -rf test_media

startdb:
	docker-compose up -d

destroydb:
	docker-compose down
	sudo rm -rf ../pgdata
