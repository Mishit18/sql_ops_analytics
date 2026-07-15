.PHONY: install build validate test dashboard

install:
	python -m pip install -r requirements.txt

build:
	python build_project.py

validate:
	python scripts/validate_project.py

test:
	pytest

dashboard:
	streamlit run dashboard/app.py
