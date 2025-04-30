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
	uv run flake8 page_analyzer

check:
	make lint

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app