presentation.pdf: presentation.pymd
	stitch $< -o presentation.md
	pandoc -t beamer -V theme=metropolis \
		-o presentation.pdf \
		presentation.md
