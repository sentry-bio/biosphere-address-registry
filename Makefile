.PHONY: install test examples validate clean

install:
	python3 -m pip install -e ".[dev]"

test:
	python3 -m pytest -q
	python3 scripts/run_local_conformance.py

examples:
	python3 examples/build_examples.py

validate: examples
	python3 -m biosphere_registry.cli validate --require-id --schema examples/observation.example.json
	python3 -m biosphere_registry.cli validate --require-id --schema examples/map-edition.example.json
	python3 -m biosphere_registry.cli validate --require-id --schema examples/evidence.example.json
	python3 -m biosphere_registry.cli validate --require-id --schema examples/address.example.json
	python3 -m biosphere_registry.cli validate --require-id --schema examples/organism-record.example.json

clean:
	rm -rf .pytest_cache src/*.egg-info src/biosphere_registry/__pycache__ tests/__pycache__
