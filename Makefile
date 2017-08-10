presentation.pdf: presentation.md
	pandoc -t beamer -V theme=metropolis -o $@ $<
