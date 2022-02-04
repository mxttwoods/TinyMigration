init:
	pip install -r requirements.txt

package: clean-build build install

test:
	python -m unittest

build:
	python3 -m pip install --upgrade build
	python3 -m build

install:
	pip3 install dist/*.whl

lint:
	pylint sample

format:
	black .

clean-build:
	rm -rf *.egg-info
	rm -rf dist

clean-venv:
	rm -rf venv

homestead:
	pip3 install virtualenv
	virtualenv venv
	pip3 install -r requirements.txt
	source venv/bin/activate