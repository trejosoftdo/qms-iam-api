start:
	uvicorn main:app --reload

lint:
	pylint ./app  --extension-pkg-whitelist='pydantic'

unit-tests:
	nosetests -c ./app/setup.cfg

integration-tests:
	behave ./app/features
