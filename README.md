# Caophim

[![builds.sr.ht status](https://builds.sr.ht/~nhanb/caophim/debian-master.yml.svg)](https://builds.sr.ht/~nhanb/caophim/debian-master.yml?)

Is yet another (WIP) attempt at a futaba-style (e.g. 4chan) imageboard, using
django + postgres.

Goals:

- Replicate the minimalistic UI and UX. Should take advantage of modern browser
  features, using javascript when and only when necessary.

- Simplest backend setup that works, but no simpler.
  A webmaster's installation runlist should be as simple as:
  + pip install caophim
  + caophim-generate-config > caophim.conf.json
  + [edits caophim.conf.json: db credentials etc.]
  + caophim-run


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

# need to activate again so pyenv can make shims for installed entrypoints:
# (see [tool.poetry.scripts] in pyproject.toml)
pyenv deactivate && pyenv activate

# generate initial config for local dev - should work out of the box with the
# db provided docker-compose above.
make localconfig

make dev
```

# Env-specific configs

This project uses [goodconf](https://github.com/lincolnloop/goodconf).
See what options are available at **src/caophim/conf.py**.

# Installation for actual use

```sh
pip install caophim
```

To be expanded.
