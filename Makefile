check:
	pep8 untokenize.py setup.py
	pep257 untokenize.py setup.py
	pylint --report=no --include-ids=yes --disable=C0103,R0913,R0914,W0622 --rcfile=/dev/null untokenize.py setup.py
	check-manifest --ignore=.travis.yml,Makefile,test_acid.py,tox.ini
	python setup.py --long-description | rst2html --strict > /dev/null
	scspell untokenize.py setup.py test_untokenize.py README.rst

coverage:
	@rm -f .coverage
	@coverage run test_untokenize.py
	@coverage report
	@coverage html
	@rm -f .coverage
	@python -m webbrowser -n "file://${PWD}/htmlcov/index.html"

mutant:
	@mut.py -t untokenize -u test_untokenize -mc

readme:
	@restview --long-description --strict