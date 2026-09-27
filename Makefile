.PHONY: dev test eval demos build run help

help:
	@echo "PetCare India AI - Commands:"
	@echo "  make dev      Start local development server"
	@echo "  make test     Run pytest suite"
	@echo "  make eval     Run automated evaluation benchmark"
	@echo "  make demos    Run 10 required demo scenarios"
	@echo "  make build    Build docker image"

dev:
	python3 -m app.main

test:
	pytest -v tests/

eval:
	python3 -m app.evaluation.runner

demos:
	python3 run_demos.py

build:
	docker build -t petcare-india-ai .

run:
	docker run -p 8000:8000 --env-file .env petcare-india-ai
