init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests tests

clean:
	rm mosaic/*.pyc tests/*.pyc
