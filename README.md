# Content

The scripts in this repository allow the analysis of the abstracts of conference track. (in this README "track" and "Special Section" are used as synonyms)
The abstracts are processed with the [`slr-kit`](https://github.com/robolab-pavia/slr-kit) tool.
Each script can be run independently of the others.
The scripts are presented in the order of execution expected during the workflow.

## `cleaningETFACsv.py`

Removes papers we are not interested for.

- INPUT: CSV file containing all papers
- OUTPUT: CSV file containing the papers we are interested for

Positional arguments:

* `file`: CSV file containing all papers

Example of usage:

```
python3 cleaningETFACsv.py "conference file".csv
```

## `cleaningINDINCsv.py`

Removes papers we are not interested for.

- INPUT: CSV file containing all papers
- OUTPUT: CSV file containing the papers we are interested for

Positional arguments:

* `file`: CSV file containing all papers

Example of usage:

```
python3 cleaningINDINCsv.py "conference file".csv
```

## `PreprocBySpecSec.py`

Splits the articles postprocessed by `slr-kit` according to the track they belong to.

- INPUT: CSV file containing the items postprocessed by `slr-kit`
- OUTPUT: set of folders containing the postprocessed articles divided by Special Section

Positional arguments:

* `spec_sec_csv`: CSV file containing the postprocessed articles of all the Special Sections

Example of usage:

```
python3 PreprocBySpecSec.py "conference name"_postproc.csv
```

## `SpecSecFake.py`

Create fake (test) Special Sections from articles postprocessed by `slr-kit`.

* INPUT: folders containing the postprocessed articles divided by Special Section; CSV file containing the postprocessed articles of all the Special Sections
* OUTPUT: folders containing the postprocessed articles of the fake Special Sections

Positional arguments:

* `directories_special_section`: folders containing all postprocessed articles divided by Special Section
* `postprocess_file`: CSV file containing the postprocessed articles of all the Special Sections

Positional arguments:

* `-fake`: number of fake Special Sections to be created; default = 200

Example of usage:

```
python3 SpecSecFake.py SpecSec/SpecSec* "conference name"_postproc.csv
```

## `SpecSecHist.py`

Creates a histogram illustrating the number of items in each Special Section or fake Special Section.

- INPUT: folders containing the postprocessed articles divided by Special Section or Special Section fake
- OUTPUT: histogram in PNG format

Positional arguments:

* `directories`: list of directories of Special Sections or fake Special Sections

Example of usage:

```
python3 SpecSecHist.py SpecSec/SpecSec*
python3 SpecSecHist.py SpecSecFake/SpecSecFake*
```

## `SpecSecGraph.py`

Creates a graph for each Special Section or Special Section fake.

- INPUT: folders containing the postprocessed articles divided by Special Section or Special Section fake
- OUTPUT: graphs in png format

The weight of the sides of the graphs is given by the number of words that the postprocessed abstracts of two articles have in common.

Positional arguments:

* `directories`: list of folders containing postprocessed articles divided by Special Section or Special Section fake

Example of usage:

```
python3 SpecSecGraph.py SpecSec/SpecSec*
python3 SpecSecGraph.py SpecSecFake/SpecSecFake*
```

## `SpecSecElab.py`

Calculates the parameters of coherence between the articles of Special Section and Special Section fake.

* INPUT: folders containing the postprocessed articles divided by Special Section; folders containing the postprocessed articles divided by Special Section fake
* OUTPUT: CSV file called `Spec_Sec_metrics.csv` containing the parameters of coherence between the articles of the Special Sections; CSV file called `Spec_Sec_fake_metrics.csv` containing the parameters of coherence between the articles of the fake Special Sections

Positional arguments:

* `--spec_sec`: list of Special Section folders
* `--spec_sec_fake`: directory listing of fake Special Sections

Positional arguments:

* `-th`: integer value of the threshold for calculating the coherence, i.e., number of words that two articles must have at least in common within their postprocessed abstract (if not specified, set to 10 by default)

Example of usage:

```
python3 SpecSecElab.py --spec_sec SpecSec/SpecSec* --spec_sec_fake SpecSecFake/SpecSecFake*
```

## `SpecSecBoxPlot.py`

Creates a box plot for the Special Sections and a box plot for the fake Special Sections.

- INPUT: CSV file for the Special Sections generated by `SpecSecElab.py`; CSV file for fake Special Sections generated by `SpecSecElab.py`
- OUTPUT: box plots named `SpecSec_BoxPlot.png` and `SpecSecFake_BoxPlot.png`

Positional arguments:

* `spec_sec_metrics`: CSV file with the coherence parameters of the Special Sections
* `spec_sec_fake_metrics`: CSV file with the coherence parameters of the fake Special Sections

Example of usage:

```
python3 SpecSecBoxPlot.py Spec_Sec_metrics.csv Spec_Sec_fake_metrics.csv
```

## `SpecSecPlot.py`

Creates a graph with two curves comparing the average coherence values of Special Section and fake Special Section.

* INPUT: CSV file for the Special Sections generated by `SpecSecElab.py`; CSV file for fake Special Sections generated by `SpecSecElab.py`
* OUTPUT: graph named `Plot.png`

Positional arguments:

* `spec_sec_metrics`: CSV file with the coherence parameters of the Special Sections
* `spec_sec_fake_metrics`: CSV file with the coherence parameters of the fake Special Sections

Example of usage:

```
python3 SpecSecPlot.py Spec_Sec_metrics.csv Spec_Sec_fake_metrics.csv
```

## `TrackAsPaper.py`

Merges every paper under a track in a single "track paper" and puts every "track paper" in a CSV file.

* INPUT: folders containing the postprocessed articles divided by Special Section
* OUTPUT: CSV file called `Biggest_Paper.csv` containing track papers (only 'id' and 'abstract_filtered' columns)

Positional arguments:

* `directories_special_section`: list of Special Section folders

Example of usage:

```
python3 TrackAsPaper.py SpecSec/SpecSec*
```

## `TrackCluster.py`

Creates clusters between track papers and an histogram of the intersections between track papers.

* INPUT: CSV file containing track papers generated by `TrackAsPaper.py`
* OUTPUT: graph named `BiggestPaper_graph.png` and histogram named `intersection_histogram.png`

Positional arguments:

* `file`: CSV file containing track papers

Example of usage:

```
python3 TrackCluster.py Biggest_Paper.csv
```

## `matrix.py`

Creates a CSV file which has in the first column every unique words among every track paper and in the others columns the frequency of that word in each track

* INPUT: CSV file containing track papers generated by `TrackAsPaper.py`
* OUTPUT: CSV file called `matrix.csv` which has in the first column every unique words among every track paper and in the others columns the frequency of that word in each track

Positional arguments:

* `file`: CSV file containing track papers

Example of usage:

```
python3 matrix.py Biggest_Paper.csv
```