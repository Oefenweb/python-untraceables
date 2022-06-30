all: check test source

init:
	pip install -r requirements.txt

init-dev:
	pip install -r requirements-dev.txt

source:
	python setup.py sdist

pycodestyle:
	find . -type f -name \*.py | xargs --no-run-if-empty pycodestyle --first
	find bin -type f | xargs --no-run-if-empty pycodestyle --first

pylint:
	find . -type f -name \*.py | xargs --no-run-if-empty pylint
	find bin -type f | xargs --no-run-if-empty pylint

check: pycodestyle

test:
	nosetests -v

clean:
	python setup.py clean
	rm -rfv build deb_dist debian dist MANIFEST *.egg-info deb_dist
	find . -name '*.pyc' -print0 | xargs --no-run-if-empty -0 rm -v
