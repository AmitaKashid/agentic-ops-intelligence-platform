.PHONY: install seed index run test eval docker-build docker-up docker-down clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt

seed:
	python -m app.db.seed

index:
	python -m app.retrieval.build_index

run:
	uvicorn app.main:app --reload

test:
	pytest

eval:
	python -m evaluation.run_evaluation

docker-build:
	docker compose build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	rm -rf .pytest_cache
	rm -rf app/data/vector_index
	rm -f agentic_ops.db
	rm -f evaluation/results.csv
	rm -f evaluation/metrics_summary.json
	rm -f evaluation/error_analysis.md