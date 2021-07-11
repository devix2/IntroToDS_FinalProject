SocialPulse
==============================

Repository for the creation of the final project of the Uni-Trento course "Introduction to data science for physicist" (held by Luca Tubiana)


DESCRIPTION:
Consegna finale elaborato "Social Pulse".
Questo progetto è stato realizzato da Davide Micheli e da Lorenzo Beltrame.

Non abbiamo preparato un make_file perchè farlo su Windows è altamente impratico e fuori lo scopo del corso, speriamo che questo non risulti essere un problema.
Per ottenere l'env su cui lavorare, si può usare il file della dir ./PythonEnv e usando anaconda.

I dati necessari sono parte di quelli forniti nella cartella lezione_24 (tendenzialmente tutti importabili dalla reference del paper, sebbene separatamente) e i dati della mappa della circoscrizione di TN (vedi references). Per sicurezza, includo una copia dei dati della circoscrizione nella cartella raw
Per svolgere questo progetto bisogna aprire la sezione ./src runnare:

python make_dataset_run.py			-> Ci impiega ~5 mins
python ML_run.py				-> Ci impiega ~3 mins (C'è dentro un plot nella parte classificazione (che potrebbe buggare), potrebbe essere necessario dare un comando di avanzata)


Più realisticamente, ha senso svolgere lo studio attraverso notebooks nella directory ./notebooks, da eseguire nell'ordine:

- import.ipynb
- EDA.ipynb
- machine_learning.ipynb

I file sono completamente commentati con i nostri appunti e le nostre osservazioni.

La roadmap standardizzata fornita dal Prof. Tubiana è stata seguita in maniera sparsa, quindi il resto di questo file è piuttosto misleading





Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be im
    │
    └─ src                <- Source code for use in this project.
       ├── __init__.py    <- Makes src a Python module
       │
       ├── data           <- Scripts to download or generate data
       │   └── make_dataset.py
       │
       ├── features       <- Scripts to turn raw data into features for modeling
       │   └── build_features.py
       │
       ├── models         <- Scripts to train models and then use trained models to make
       │   │                 predictions
       │   ├── predict_model.py
       │   └── train_model.py
       │
       └── visualization  <- Scripts to create exploratory and results oriented visualizations
           └── visualize.py


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
