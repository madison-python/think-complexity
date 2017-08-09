presentation.pdf: presentation.md

small-world-graphs.pdf: small-world-graphs.md
small-world-graphs.md: small-world-graphs.pymd

%.md: %.pymd
	stitch $< -o $@

%.pdf: %.md
	pandoc -t beamer -V theme=metropolis -o $@ $<
