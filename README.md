# Contenuto
Questi script permettono l'analisi degli abstract degli articoli delle Special Section della rivista scientifica Transaction on Industrial Informatics, abstract elaborati con `slr-kit`. 
Ogni script può essere eseguito in maniera indipendente dagli altri.
Gli script sono presentati nel corretto ordine di esecuzione che ci si aspetta durante il workflow.

## `Scopus2csv.py`
- AZIONE: converte un file CSV scaricato da Scopus in un file CSV compatibile con `slr-kit`
- INPUT: file CSV scaricato da Scopus
- OUTPUT: file CSV denominato `slr-kit_abstracts.csv`

Argomenti posizionali:
* `input_file`: CSV scaricato da Scopus

### Esempio di utilizzo
```
python Scopus2csv.py Scopus.csv
```

## `PreprocBySpecSec.py`
- AZIONE: divide gli articoli preprocessati da `slr-kit` in base alla Special Section di appartenenza
- INPUT: file CSV contenente articoli e nomi delle Special Section; file CSV contenente gli articoli preprocessati da `slr-kit`
- OUTPUT: insieme di cartelle contenenti gli articoli preprocessati divisi per Special Section; file eseguibile denominato `run_all_process.bat` per poter eseguire il postprocessamento degli articoli e successivamente LDA (postprocessamneto e LDA sono forniti da `slr-kit`)

Argomenti posizionali:
* `spec_sec_csv`: file CSV contenente articoli e nomi delle Special Section
* `preproc_file`: file CSV contenente gli articoli preprocessati di tutte le Special Section

### Esempio di utilizzo
```
python PreprocBySpecSec.py Spec_Sec.csv SpecSec_preproc.csv
```

## `SpecSecFake.py`
- AZIONE: crea Special Section fake (di test) a partire dagli articoli postprocessati da `slr-kit`
- INPUT: cartelle contenenti gli articoli postprocessati divisi per Special Section; file CSV contenente gli articoli postprocessati di tutte le Special Section
- OUTPUT: cartelle contenenti gli articoli postprocessati delle Special Section fake

Argomenti posizionali:
* `directories_special_section`: cartelle contenenti tutti gli articoli postprocessati divisi per Special Section
* `postprocess_file`: file CSV contenente gli articoli postprocessati di tutte le Special Section

Argomenti opzionali:
* `-fake`: numero di Special Section fake che si vogliono creare (se non specificato impostato di default a 200)

### Esempio di utilizzo
```
python SpecSecFake.py (Get-ChildItem -Path "SpecSec\SpecSec*").FullName SpecSec_postproc.csv
```

## `SpecSecHist.py`
- AZIONE: crea un istogramma che illustra il numero di articoli presenti in ogni Special Section o Special Section fake
- INPUT: cartelle contenenti gli articoli postprocessati divisi per Special Section o Special Section fake
- OUTPUT: istrogramma in formato png

Argomenti posizionali:
* `directories`: elenco di cartelle di Special Section o Special Section fake

### Esempio di utilizzo
```
python SpecSecHist.py (Get-ChildItem -Path "SpecSec\SpecSec*").FullName
python SpecSecHist.py (Get-ChildItem -Path "SpecSecFake\SpecSecFake*").FullName
```
## `SpecSecGraph.py`
- AZIONE: crea un grafo per ogni Special Section o Special Section fake
- INPUT: cartelle contenenti gli articoli postprocessati divisi per Special Section o Special Section fake
- OUTPUT: grafi in formato png

Il peso dei lati dei grafi è dato dal numero di parole che hanno in comune gli abstract postprocessati di due articoli.

Argomenti posizionali:
* `directories`: elenco di cartelle contenenti gli articoli postprocessati divisi per Special Section o Special Section fake

### Esempio di utilizzo
```
python SpecSecGraph.py (Get-ChildItem -Path "SpecSec\SpecSec*").FullName
python SpecSecGraph.py (Get-ChildItem -Path "SpecSecFake\SpecSecFake*").FullName
```

## `SpecSecElab.py`
- AZIONE: calcola i parametri di coerenza tra gli articoli di Special Section e Special Section fake
- INPUT: cartelle contenenti gli articoli postprocessati divisi per Special Section; cartelle contenenti gli articoli postprocessati divisi per Special Section fake
- OUTPUT: file CSV denominato `Spec_Sec_metrics.csv` contenente i parametri di coerenza tra gli articoli delle Special Section; file CSV denominato `Spec_Sec_fake_metrics.csv` contenente i parametri di coerenza tra gli articoli delle Special Section fake

Argomenti posizionali:
* `--spec_sec`: elenco di cartelle delle Special Section
* `--spec_sec_fake`: elenco di cartelle delle Special Section fake

Argomenti opzionali:
* `-th`: valore (numero intero) della soglia (numero di parole che devono almeno avere in comune due articoli all'interno del loro abstract postprocessato) per il calcolo della coerenza (se non specificato impostato di default a 10)

### Esempio di utilizzo
```
python SpecSecElab.py --spec_sec (Get-ChildItem -Path "SpecSec\SpecSec*").FullName --spec_sec_fake (Get-ChildItem -Path "SpecSecFake\SpecSecFake*").FullName
```

## `SpecSecBoxPlot.py`
- AZIONE: crea un box plot per le Special Section e un box plot per le Special Section fake
- INPUT: file CSV per le Special Section generato da `SpecSecElab.py`; file CSV per le Special Section fake generato da `SpecSecElab.py`
- OUTPUT: box plot denominati `SpecSec_BoxPlot.png` e `SpecSecFake_BoxPlot.png`

Argomenti posizionali:
* `spec_sec_metrics`: file CSV con i parametri di coerenza delle Special Section
* `spec_sec_fake_metrics`: file CSV con i parametri di coerenza delle Special Section fake

### Esempio di utilizzo
```
python SpecSecBoxPlot.py Spec_Sec_metrics.csv Spec_Sec_fake_metrics.csv
```

## `SpecSecPlot.py`
- ACTION: crea un grafico con due curve che mettono a confronto i valori medi di coerenza di Special Section e Special Section fake
- INPUT: file CSV per le Special Section generato da `SpecSecElab.py`; file CSV per le Special Section fake generato da `SpecSecElab.py`
- OUTPUT: grafico denominato `Plot.png`

Argomenti posizionali:
* `spec_sec_metrics`: file CSV con i parametri di coerenza delle Special Section
* `spec_sec_fake_metrics`: file CSV con i parametri di coerenza delle Special Section fake

### Esempio di utilizzo
```
python SpecSecPlot.py Spec_Sec_metrics.csv Spec_Sec_fake_metrics.csv
```