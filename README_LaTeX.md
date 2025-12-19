# Guide de Compilation - Présentation LaTeX Beamer

## 📋 Prérequis

### Logiciels Requis
1. **LaTeX Distribution**:
   - Windows: [MiKTeX](https://miktex.org/) ou [TeX Live](https://www.tug.org/texlive/)
   - Linux: `sudo apt-get install texlive-full` ou `sudo yum install texlive-scheme-full`
   - macOS: [MacTeX](https://www.tug.org/mactex/)

2. **Packages LaTeX Requis**:
   - beamer (inclus dans la plupart des distributions)
   - tikz, pgfplots
   - graphicx
   - babel (pour le français)

3. **Graphiques**:
   - Générer les graphiques avec `generate_presentation_charts.py`
   - Les graphiques doivent être dans `presentation_charts/`

## 🚀 Compilation

### Méthode 1: Compilation Directe

```bash
# Compiler le fichier LaTeX
pdflatex presentation.tex

# Compiler à nouveau pour les références (si nécessaire)
pdflatex presentation.tex
```

### Méthode 2: Utiliser le Makefile

```bash
# Compiler
make

# Nettoyer les fichiers temporaires
make clean

# Nettoyer tout (y compris le PDF)
make cleanall
```

### Méthode 3: Compilation avec BibTeX (si vous ajoutez des références)

```bash
pdflatex presentation.tex
bibtex presentation
pdflatex presentation.tex
pdflatex presentation.tex
```

## 📁 Structure des Fichiers

```
.
├── presentation.tex              # Fichier principal LaTeX
├── generate_presentation_charts.py  # Script Python pour générer les graphiques
├── presentation_charts/         # Dossier contenant les graphiques PNG
│   ├── slide2_performance_comparison.png
│   ├── slide4_linear_grid_search.png
│   ├── slide5_softmax_radar.png
│   └── ...
├── Makefile                     # Makefile pour compilation automatique
└── README_LaTeX.md              # Ce fichier
```

## 🎨 Personnalisation

### Changer les Couleurs

Modifier dans `presentation.tex`:
```latex
\definecolor{paperred}{RGB}{231, 76, 60}
\definecolor{ourgreen}{RGB}{39, 174, 96}
\definecolor{bestgreen}{RGB}{30, 132, 73}
```

### Changer le Thème

Remplacer `\usetheme{Madrid}` par:
- `Berlin`
- `Darmstadt`
- `Warsaw`
- `Singapore`
- etc.

### Changer l'Aspect Ratio

Remplacer `aspectratio=169` par:
- `aspectratio=43` (4:3)
- `aspectratio=1610` (16:10)

## 📊 Génération des Graphiques

1. **Générer tous les graphiques**:
   ```bash
   python generate_presentation_charts.py
   ```

2. **Vérifier que les graphiques sont créés**:
   ```bash
   ls presentation_charts/*.png
   ```

3. **Si des graphiques manquent**, le LaTeX affichera une erreur. Vérifiez:
   - Que le script Python a bien généré tous les graphiques
   - Que les noms de fichiers correspondent exactement

## ⚠️ Résolution de Problèmes

### Erreur: "File not found" pour les graphiques
- Vérifiez que `presentation_charts/` existe
- Vérifiez que tous les graphiques sont générés
- Vérifiez les noms de fichiers (sensible à la casse)

### Erreur: "Package babel Error"
- Installez le package babel-french:
  ```bash
  # MiKTeX: Package Manager
  # TeX Live:
  tlmgr install babel-french
  ```

### Erreur: "Package pgfplots Error"
- Installez pgfplots:
  ```bash
  tlmgr install pgfplots
  ```

### Compilation lente
- Utilisez `pdflatex -interaction=nonstopmode presentation.tex`
- Ou compilez seulement les slides nécessaires

## 📝 Notes

- Les graphiques doivent être en format PNG
- Résolution recommandée: 300 DPI minimum
- Les graphiques sont générés par le script Python
- Vous pouvez remplacer les graphiques par vos propres versions

## 🎯 Compilation Rapide

```bash
# 1. Générer les graphiques
python generate_presentation_charts.py

# 2. Compiler le LaTeX
pdflatex presentation.tex
pdflatex presentation.tex

# 3. Ouvrir le PDF
# Windows: start presentation.pdf
# Linux: xdg-open presentation.pdf
# macOS: open presentation.pdf
```

## 📦 Export vers PowerPoint

Si vous voulez exporter vers PowerPoint:

1. Compilez le PDF
2. Utilisez un convertisseur PDF → PPTX:
   - [Adobe Acrobat](https://www.adobe.com/acrobat/)
   - [Online converters](https://www.ilovepdf.com/pdf-to-ppt)
   - [LibreOffice Impress](https://www.libreoffice.org/) (ouvre les PDF)

Ou utilisez `beamer2pptx` (outil Python):
```bash
pip install beamer2pptx
beamer2pptx presentation.pdf
```

---

**Version**: 1.0  
**Date**: 2024

