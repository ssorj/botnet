.PHONY: build
build:
	docker build -t ngircd -f Containerfile

.PHONY: run
run: build
	docker run -p 6667:6667 ngircd
