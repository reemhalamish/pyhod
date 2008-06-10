DOC = egpaper_final.tex
#SUBDOCS =
#FIGURES = 
#FIGURES_DEL =
GRAPHS = laser_high.eps laser_low.eps distance_estimation.eps fuzzy.eps

LATEX = pdflatex
BIBTEX = bibtex
FIG2DEV = fig2dev
FIG2DEV_OPTS = -L eps
DVIPS = dvips
DVIPS_OPTS = -t letter -Pcmz -q
PS2PDF = ps2pdf
PS2PDF_OPTS = -dPDFSETTINGS=/prepress
RERUN = "(There were undefined references|Rerun to get (cross-references|the bars) right)"
RERUNBIB = "No file.*\.bbl|Citation.*undefined"

.PHONY: dvi ps pdf clean

all: ${GRAPHS} ${FIGURES} pdf ${SUBDOCS}

pdf: $(DOC:.tex=.pdf)


laser_low.eps: graphs/laser_low.plot graphs/laser_low.txt
	gnuplot graphs/laser_low.plot
	ps2pdf -dEPSCrop laser_low.eps

laser_high.eps: graphs/laser_high.plot graphs/laser_high.txt
	gnuplot graphs/laser_high.plot
	ps2pdf -dEPSCrop laser_high.eps

distance_estimation.eps: graphs/distance_estimation.plot graphs/distance_estimation.txt
	gnuplot graphs/distance_estimation.plot
	ps2pdf -dEPSCrop distance_estimation.eps

fuzzy.eps: graphs/fuzzy.plot
	gnuplot graphs/fuzzy.plot
	ps2pdf -dEPSCrop fuzzy.eps


%.eps: %.fig
	${FIG2DEV} ${FIG2DEV_OPTS} $< > $@

%.pdf: %.tex
	pdflatex  $*
	bibtex  $*
	pdflatex  $*
	pdflatex  $*

clean:
	@\rm -f \
        $(DOC:.tex=.aux) \
        $(DOC:.tex=.log) \
        $(DOC:.tex=.out) \
        $(DOC:.tex=.dvi) \
        $(DOC:.tex=.pdf) \
        $(DOC:.tex=.ps)  \
        $(DOC:.tex=.bbl) \
        $(DOC:.tex=.blg) \
	$(GRAPHS:.eps=.pdf) \
        ${FIGURES_DEL}
	rm -f ${GRAPHS}

veryclean: clean
	@\rm -f *~
