develop:
	python setup.py develop

release:
	python setup.py sdist upload

clean:
	find . -name '*.pyc' | xargs rm -f
