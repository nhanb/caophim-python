# Dev

On Arch Linux:

```sh
sudo pacman -S postgresql-libs python-poetry

# spin up postgres container, because manually creating databases for dev
# purposes is fiddly and annoying.
docker-compose up -d

# assuming pyenv and pyenv-virtualenv are already installed:
pyenv virtualenv 3.7.5 caophim
pyenv activate caophim
poetry install

# need to activate again so pyenv can make a shim for our `manage` script:
pyenv deactivate && pyenv activate

# generate initial config for local dev - should work out of the box with the
# db provided docker-compose above.
make localconfig

make dev
```

# Env-specific configs

This project uses [goodconf](https://github.com/lincolnloop/goodconf).
See what options are available at **src/caophim/conf.py**.
```
