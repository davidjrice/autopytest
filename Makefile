build:
	@hatch build .

install:
	@pip install autopytest*.tar.gz

test: # Run tests
	@tox