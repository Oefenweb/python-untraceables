all: check source deb

init:
	pip install -r requirements.txt

dist: source deb

source:
	python setup.py sdist

deb:
	python setup.py --command-packages=stdeb.command bdist_deb

check:
	find . -name \*.py | xargs pep8 --first
	find bin -type f | xargs pep8 --first

test:
	nosetests -v

clean:
	python setup.py clean
	rm -rf build deb_dist debian dist MANIFEST *.egg-info deb_dist
	find . -name '*.pyc' -print0 | xargs --no-run-if-empty -0 rm
