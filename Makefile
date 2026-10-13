prepare:
	cd astro && npm install

run:
	cd astro && npm run dev

build:
	cd astro && npm run build

preview: build
	cd astro && npm run preview

clean:
	rm -rf astro/dist astro/.astro
