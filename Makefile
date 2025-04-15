install:
	uv sync

dev:
	uv run flask --app page_analyzer:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	uv run flake8 hexlet-code

check:
	make lint

test-coverage:
	uv run pytest --cov=??? --cov-report xml

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app