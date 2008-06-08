DOC = egpaper_final.tex
#SUBDOCS =
#FIGURES = 
#FIGURES_DEL =
GRAPHS = laser_high.eps laser_low.eps


LATEX = latex
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
ps:  $(DOC:.tex=.ps)
dvi: $(DOC:.tex=.dvi)


laser_low.eps: graphs/laser_low.plot graphs/laser_low.txt
	gnuplot graphs/laser_low.plot

laser_high.eps: graphs/laser_high.plot graphs/laser_high.txt
	gnuplot graphs/laser_high.plot

%.dvi: %.tex ${FIGURES} ${GRAPHS}
	$(LATEX) $<
	egrep -c $(RERUNBIB) $*.log && ($(BIBTEX) $*;$(LATEX) $<) ; true
	egrep $(RERUN) $*.log && ($(LATEX) $<) ; true
	egrep $(RERUN) $*.log && ($(LATEX) $<) ; true
	egrep -i "(Reference|Citation).*undefined" $*.log ; true

%.eps: %.fig
	${FIG2DEV} ${FIG2DEV_OPTS} $< > $@

%.ps: %.dvi
	${DVIPS} ${DVIPS_OPTS}  $< -o $@

%.pdf: %.ps
	${PS2PDF} ${PS2PDF_OPTS}  $<

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
        ${FIGURES_DEL}
	rm -f ${GRAPHS}

veryclean: clean
	@\rm -f *~
