PYTHON = python
PIP = pip
APP = astranotes.main:app
PORT = 8000

install:
	$(PIP) install -r requirements.txt

run:
	uvicorn $(APP) --reload --port $(PORT)

test:
	pytest tests

lint:
	$(PYTHON) -m py_compile src/astranotes/*.py

docs:
	@echo "Documentation available in docs/"

clean:
	rm -rf __pycache__ .pytest_cache .venv
