prepare:
	pip install --upgrade pip
	pip install -r requirements.txt --break-system-packages

build:
	mkdocs build

run:
	mkdocs serve

clean:
	rm -rf site
