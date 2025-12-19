# Makefile pour la compilation de la présentation LaTeX Beamer

# Nom du fichier principal (sans extension)
MAIN = presentation

# Compilateur LaTeX
LATEX = pdflatex
LATEXFLAGS = -interaction=nonstopmode -shell-escape

# Fichiers à nettoyer
CLEAN = *.aux *.log *.nav *.out *.snm *.toc *.vrb *.fls *.fdb_latexmk *.synctex.gz

# Cible par défaut
all: $(MAIN).pdf

# Compilation du PDF
$(MAIN).pdf: $(MAIN).tex
	@echo "Compilation de $(MAIN).tex..."
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	$(LATEX) $(LATEXFLAGS) $(MAIN).tex
	@echo "Compilation terminée: $(MAIN).pdf"

# Générer les graphiques avant la compilation
charts:
	@echo "Génération des graphiques..."
	python generate_presentation_charts.py
	@echo "Graphiques générés."

# Compilation complète (graphiques + LaTeX)
full: charts $(MAIN).pdf

# Nettoyer les fichiers temporaires
clean:
	@echo "Nettoyage des fichiers temporaires..."
	rm -f $(CLEAN)
	@echo "Nettoyage terminé."

# Nettoyer tout (y compris le PDF)
cleanall: clean
	@echo "Suppression du PDF..."
	rm -f $(MAIN).pdf
	@echo "Nettoyage complet terminé."

# Nettoyer les graphiques
cleancharts:
	@echo "Suppression des graphiques..."
	rm -rf presentation_charts/*.png
	@echo "Graphiques supprimés."

# Aide
help:
	@echo "Makefile pour la compilation de la présentation LaTeX"
	@echo ""
	@echo "Cibles disponibles:"
	@echo "  make          - Compile le PDF (nécessite que les graphiques existent)"
	@echo "  make charts   - Génère les graphiques Python"
	@echo "  make full     - Génère les graphiques puis compile le PDF"
	@echo "  make clean    - Supprime les fichiers temporaires LaTeX"
	@echo "  make cleanall - Supprime tout (y compris le PDF)"
	@echo "  make cleancharts - Supprime les graphiques"
	@echo "  make help     - Affiche cette aide"

.PHONY: all charts full clean cleanall cleancharts help

