---
title: Présentation du langage Python
subtitle:  pour des applications scientifiques
author: V. Choqueuse
date: 
fontsize: 10pt
output:
beamer_presentation:
#    keep_tex: true
#    toc: true
slide_level: 3

---

# Des langages pour communiquer

## Objectifs: Communiquer, échanger de l'information

* entre individus 
* entre l'homme et la machine
* entre objets connectés

## Cahier des charges d'un "bon" langage.

* Etre relativement général & polyvalent
* Etre populaire 
* Etre conscis


# Programmation d'applications scientifiques

## Objectifs

* Illustrer, Simuler, Tester

## Les besoins

* Fonctionalités mathématiques (complexes, matrices, lois aléatoires, analyse spectrale, ...)
* Fonctionalités graphiques et interactivité (zoom, marqueurs, export)
* Fonctionnalités multimédia (import/export, lecture)
* Langage Multiplateforme (Windows, Linux, OSX)


# Les Langages de Programmation [TIOBE]


Classement |  Langage | Utilisation | Changement | 
--- | --- | --- | --- |
1        |	Java	| 18.236%	| -1.33%   | 
2		 |	C	| 10.955%	| -4.67% | 
3		 |	C++	| 6.657%	| -0.13% | 
4		 |	C#	| 5.493%	| +0.58% | 
5		 |	Python	| 4.302%	| +0.64% | 
6        |  JavaScript	| 2.929%	| +0.59% | 
7        |  PHP		| 2.847%	| +0.32% | 
8        |  Assembly language |	2.417%		|  +0.61% | 
9		 |	Visual Basic |	2.343%	| +0.28% | 
10		 |	Perl |	2.333%	| +0.43%	| 
...		 |	... |	...	| ... | 
15	     | MATLAB	| 1.826%	| +0.65% | 


# Matlab Vs Scilab Vs Python


Langage | Prix (euros) | TIOBE | Indeed | APEC |
--- | --- | --- | --- | --- |
Python | $0$ | 5 | 3190 | 768 |
Matlab | $>3000$ | 15 | 997 | 271 |
Scilab | $0$ | $>100$ | 11 | 48 |


# Installation et Configuration

## Installation

* De base certains OS embarque déja une distribution de python (Python 2 ou 3)
* Certaines distributions sont spécifiquement dédiés aux applications scientifiques
    * Anaconda  (Numpy, Scipy, Matplotlib, ...)
    


# Les bases du Langage

## Différences par rapport au Langage c

* Python=Script (pas de compilation).
* Paradigme de programmation: procédural et objet.
* Pas de point virgule.
* Structures de contrôle délimités par des indentations.

```
res=0
for indice in [1,2,3]
    res=res+indice
    print(res)
    
```



One big disadvantage to Markdown: compiling.

\bigskip Here's what it would look like from Terminal \medskip


\bigskip Nobody got time for that.

### One Alternative: Rstudio




### Another Alternative: Rscript

Another option: noninteractive \texttt{Rscript}

- I prefer this option since I tend to not like GUIs.
- Assumes you're on a Linux/Mac system.

Save this to a .R script (call it whatever you like)

- Note that the "s" in "utils" package is cut off in verbatim environment below.


```
#! /usr/bin/Rscript --vanilla --default-packages=base,stats,utils
library(knitr)
library(rmarkdown)
file <- list.files(pattern='.Rmd')
rmarkdown::render(file)
```



Make it executable. Double click or run in Terminal.

- Keep a copy in each directory, but keep only one .Rmd per directory.


# Conclusion
### Conclusion

Beamer markup is messy. Markdown is much more elegant.

- Incorporating R with Markdown makes Markdown that much better.
- Rendering Markdown $\rightarrow$ Beamer requires minimal Rscript example.
- I provide such a script to accompany this presentation.