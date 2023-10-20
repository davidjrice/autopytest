build:
	@hatch build .

install:
	@pip install autopytest*.tar.gz

test: # Run tests
	@python3 setup.py pytest