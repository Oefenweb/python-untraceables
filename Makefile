all: check test source

init:
	pip install -r requirements.txt

init-dev:
	pip install -r requirements-dev.txt

source:
	python setup.py sdist

check:
	find . -name \*.py | xargs pycodestyle --first
	find bin -type f | xargs pycodestyle --first

test:
	nosetests -v

clean:
	python setup.py clean
	rm -rfv build deb_dist debian dist MANIFEST *.egg-info deb_dist
	find . -name '*.pyc' -print0 | xargs --no-run-if-empty -0 rm -v
