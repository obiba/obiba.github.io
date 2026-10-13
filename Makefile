prepare:
	npm install

run:
	npm run dev

build:
	npm run build

preview: build
	npm run preview

clean:
	rm -rf dist .astro
