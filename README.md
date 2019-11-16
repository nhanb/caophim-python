```sh
pyenv virtualenv 3.7.5 caophim
pyenv activate caophim
poetry install

# spin up postgres container
docker-compose up -d

make dev
```
