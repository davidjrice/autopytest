env:
	@pyenv local 3.12.0 3.11.5 3.10.13

deps:
	@pip install .[dev]

build:
	@hatch build .

install:
	@pip install .

autotest:
	@autopytest .

coverage:
	@pytest --cov=autopytest --cov-report=html --cov-report=lcov

test: # Run tests
	@tox --parallel=all

lint:
	@black --color .
	@ruff check .
	@codespell .
	@mypy .
	@refurb .
