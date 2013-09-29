APP_NAME=github
PACKAGE_NAME=django-octocat

develop:
	python setup.py develop

release:
	python setup.py sdist upload

clean:
	find . -name '*.pyc' | xargs rm -f

test-py:
	django-admin.py test $(APP_NAME) --settings=$(APP_NAME).tests.settings

test: install-test-requirements test-py

install-test-requirements:
	pip install "file://`pwd`#egg=$(PACKAGE_NAME)[tests]"

coverage: install-test-requirements
	coverage run --source=$(APP_NAME) `which django-admin.py` test $(APP_NAME) --settings=$(APP_NAME).tests.settings
