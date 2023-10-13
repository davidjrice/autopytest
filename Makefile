build:
	@hatch build .

install:
	@pip3 install autotest*.tar.gz

test: # Run tests
	@python3 setup.py pytest