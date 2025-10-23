.PHONY: help test run demo stats export clean docker-build docker-run install dev-install

help:
	@echo "Champions League Draw Simulator - Available Commands:"
	@echo ""
	@echo "  make run          - Run the main draw program"
	@echo "  make demo         - Run complete demonstration"
	@echo "  make test         - Run unit tests"
	@echo "  make stats        - Generate statistics"
	@echo "  make export       - Export draw to JSON"
	@echo "  make clean        - Remove generated files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run in Docker container"
	@echo "  make install      - Install as Python package"
	@echo "  make dev-install  - Install in development mode"

run:
	python3 champions_league_draw.py

demo:
	python3 demo.py

test:
	python3 test_draw.py

stats:
	python3 statistics.py

export:
	python3 export_json.py

clean:
	rm -f *.json
	rm -rf __pycache__
	rm -rf *.egg-info
	rm -rf build dist
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

docker-build:
	docker build -t champions-league-draw:latest .

docker-run:
	docker run --rm champions-league-draw:latest

docker-compose-up:
	docker-compose up

docker-compose-demo:
	docker-compose --profile demo up

docker-compose-test:
	docker-compose --profile test up

install:
	pip install .

dev-install:
	pip install -e .

lint:
	python -m py_compile *.py

check-syntax:
	@echo "Checking Python syntax..."
	@python -c "import ast; [ast.parse(open(f).read()) for f in ['champions_league_draw.py', 'test_draw.py', 'statistics.py', 'export_json.py', 'demo.py']]"
	@echo "All files have valid syntax ✓"

