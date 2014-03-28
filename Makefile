check:
	pep8 untokenize.py setup.py test_acid.py
	pep257 untokenize.py setup.py test_acid.py
	pylint \
		--rcfile=/dev/null \
		--reports=no \
		--disable=invalid-name \
		untokenize.py setup.py test_acid.py
	check-manifest
	rstcheck README.rst
	scspell untokenize.py setup.py test_untokenize.py test_acid.py README.rst

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
