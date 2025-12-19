# 🚀 Démarrage Rapide - Présentation LaTeX

## Étape 1: Générer les Graphiques

```bash
python generate_presentation_charts.py
```

Cela crée le dossier `presentation_charts/` avec tous les graphiques PNG nécessaires.

## Étape 2: Compiler le LaTeX

### Option A: Avec Makefile (Recommandé)
```bash
make full
```

### Option B: Compilation Manuelle
```bash
pdflatex presentation.tex
pdflatex presentation.tex
```

## Étape 3: Ouvrir le PDF

Le fichier `presentation.pdf` est créé. Ouvrez-le avec votre lecteur PDF préféré.

---

## ⚡ Commandes Rapides

```bash
# Tout faire en une fois
make full

# Nettoyer les fichiers temporaires
make clean

# Regénérer les graphiques
make charts
```

---

## 📋 Checklist

- [ ] Python installé
- [ ] Matplotlib, NumPy, Pandas, Seaborn installés
- [ ] LaTeX installé (MiKTeX, TeX Live, ou MacTeX)
- [ ] Graphiques générés (`presentation_charts/*.png` existe)
- [ ] PDF compilé (`presentation.pdf` existe)

---

## 🆘 Problèmes Courants

### "ModuleNotFoundError: No module named 'matplotlib'"
```bash
pip install matplotlib numpy pandas seaborn
```

### "pdflatex: command not found"
- Windows: Installez [MiKTeX](https://miktex.org/)
- Linux: `sudo apt-get install texlive-full`
- macOS: Installez [MacTeX](https://www.tug.org/mactex/)

### "File not found: slide2_performance_comparison.png"
- Vérifiez que `python generate_presentation_charts.py` a bien fonctionné
- Vérifiez que le dossier `presentation_charts/` contient les fichiers PNG

---

**C'est tout!** Votre présentation est prête. 🎉

