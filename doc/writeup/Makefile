REPORT=agent
REFS=$(wildcard *.bib)
LATEX=/usr/texbin/pdflatex
BIBTEX=/usr/texbin/bibtex

SRCS=$(wildcard *.tex)

all: $(REPORT).pdf

$(REPORT).pdf: $(SRCS) $(REFS)
	$(LATEX) $(REPORT)
	$(BIBTEX) $(REPORT)
	$(LATEX) $(REPORT)
	$(LATEX) $(REPORT)

#view: $(REPORT).dvi
# xdvi $(REPORT).dvi

#print: $(REPORT).dvi
# dvips $(REPORT).dvi

clean:
	rm -f *.dvi *.aux *.log *.blg *.bbl $(REPORT).ps $(REPORT).pdf
