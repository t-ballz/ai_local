.PHONY: install serve build deploy

install:
	pip install mkdocs-material

serve:
	mkdocs serve

build:
	mkdocs build --strict

deploy:
	mkdocs gh-deploy --force
