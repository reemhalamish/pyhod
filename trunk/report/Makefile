all: egpaper_final.pdf

egpaper_final.pdf: egpaper_final.tex
	pdflatex egpaper_final.tex

view: egpaper_final.pdf
	evince egpaper_final.pdf

clean:
	rm egpaper_final.pdf 
	rm egpaper_final.log
	rm egpaper_final.aux
	rm egpaper_final.brf

