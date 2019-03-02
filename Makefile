PROJECT := pyloc
REQS := "requirements.txt"
TEST_REQS := "test-requirements.txt"

.PHONY: clean validate test

env-setup:
	pip install -r ${REQS}

test-setup:
	pip install -r ${TEST_REQS}

test: clean validate
	tox

clean:
	find ./test/ -name '*.py[co]' -exec rm {} \;
	rm -rf build dist $(PROJECT).egg-info

validate:
	flake8 setup.py $(PROJECT)/ test/
