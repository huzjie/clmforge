.PHONY: test bench doctor train serve install

install:
	pip install -e .

test:
	python -m unittest discover -s tests -t .

doctor:
	python -m clmforge doctor

train:
	python -m clmforge train --epochs 10

bench:
	python -m clmforge bench --n 200

speedup:
	python -m clmforge speedup --n 500

serve:
	python -m clmforge serve --host 0.0.0.0 --port 8765
