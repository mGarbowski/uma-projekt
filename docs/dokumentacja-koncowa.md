# UMA - Projekt

Semestr 2024Z

* Mikołaj Garbowski
* Michał Pałasz

## Temat Projektu

Implementacja drzewa decyzyjnego, porównanie sposobu radzenia sobie z problemami wieloklasowymi,
czyli porównanie jakości wyników typowej implementacji ID3 z jakością wyników dwóch podejść:

1) tworzymy osobny model binarny dla każdej klasy (jedna klasa traktowana jako pozytywna, wszystkie pozostałe jako
   negatywne),
   predykcja przez wybór klasy o maksymalnej wartości funkcji decyzyjnej (wymaga posiadania przez każdy klasyfikator
   „stopnia pewności siebie”, co można zdefiniować na wiele sposobów).
2) tworzymy osobny model binarny dla każdej pary klas (jedna klasa traktowana jako pozytywna, druga jako negatywna),
   predykcja przez głosowanie.

## Opis Rozwiązania

### Algorytm ID3

Przy tworzeniu liścia, poza klasą większościową zapamiętujemy również częstość występowania przykładów klasy
większościowej
w zbiorze przykładów rozważanym w danym liściu.
W przypadku jednakowej klasy dla wszystkich przykładów - wartość 1, w pozostałych przypadkach - wartość z
przedziału $(0,1)$.
Częstość potraktujemy jako stopień pewności modelu co do decyzji.

### Wariant One vs Rest

Dla problemu klasyfikacji z liczbą klas równą $n$ powstanie $n$ modeli klasyfikacji binarnej według algorytmu ID3.

Dla pojedynczego modelu dla klasy $c$ modyfikujemy etykiety w zbiorze danych - przypisujemy klasę pozytywną w miejsce
klasy $c$,
przypisujemy klasę negatywną w miejsce wszystkich pozostałych.

Przy tworzeniu liścia, poza klasą większościową zapamiętujemy również częstość występowania przykładów klasy
większościowej
w zbiorze przykładów rozważanym w danym liściu.
W przypadku jednakowej klasy dla wszystkich przykładów - wartość 1, w pozostałych przypadkach - wartość z
przedziału $(0,1)$.
Częstość potraktujemy jako stopień pewności modelu co do decyzji.

Wynikiem predykcji zespołu modeli będzie ta klasa, którą model binarny zaklasyfikował pozytywnie z największą pewnością.

Przykładowo, dla klas A, B, C, D

| Model binarny dla klasy | A   | B   | C   | D   |
|-------------------------|-----|-----|-----|-----|
| Predykcja (0/1)         | 1   | 0   | 1   | 0   |
| Pewność                 | 0,8 | 0,7 | 0,7 | 0,9 |

Predykcją zespołu modeli będzie klasa A, ponieważ zarówno model binarny dla klasy A i C dał pozytywny wynik
klasyfikacji, ale model dla klasy A miał większą pewność.

Jeśli wszystkie modele binarne dadzą predykcję negatywną, predykcją zespołu modeli będzie ta klasa, która została
zaklasyfikowana negatywnie z najmniejszą pewnością. Przykład:

| Model binarny dla klasy | A   | B   | C   | D   |
|-------------------------|-----|-----|-----|-----|
| Predykcja (0/1)         | 0   | 0   | 0   | 0   |
| Pewność                 | 0,9 | 0,7 | 0,8 | 0,5 |

Predykcją zespołu modeli będzie klasa D, ponieważ wszystkie predykcje dają klasę negatywną, ale model dla klasy D ma
najmniejszą pewność.

### Wariant One vs One

Dla problemu klasyfikacji z liczbą klas równą $n$ powstanie $n(n-1)/2$ modeli klasyfikacji binarnej - po 1 dla każdej
pary klas.
Klasyfikator binarny rozstrzyga, do której klasy z pary należy przykład.

Do trenowania klasyfikatora binarnego dla pary klas A i B użyjemy takiego podzbioru zbioru trenującego, który zawiera
tylko przykłady klas A i B.

Predykcja zespołu klasyfikatorów będzie wyznaczana przez głosowanie.
Ze względu na możliwość remisu przy zliczaniu głosów jako liczby modeli, które przewidują daną klasę, proponujemy
poniższy sposób obliczania głosów ważonych stopniem pewności predykcji
(stopień predykcji definiowany jak w poprzednim wariancie).

Przykład dla klas A, B i C:

| Model binarny dla pary | A vs B | B vs C | C vs A |
|------------------------|--------|--------|--------|
| Predykcja              | A      | B      | C      |
| Pewność                | 0,99   | 0,8    | 0,7    |

| Klasa | Ważony głos           |
|-------|-----------------------|
| A     | 1,29 = 0,99 + (1-0,7) |
| B     | 0,81 = (1-0,99) + 0,8 |
| C     | 0,9 = (1-0,8) + 0,7   |

Dla powyższego przykładu predykcją zespołu klasyfikatorów byłaby klasa A, ponieważ choć wszystkie uzyskały po 1 głosie,
dla każdej klasy obliczamy sumę pewności głosów *za* i dopełnienia do 1 pewności głosów *przeciw*.

### Prawidłowość implementacji

O poprawności zaimplementowanych algorytmów zapewniają testy jednostkowe w katalogu `tests`.

```
Name                                               Stmts   Miss  Cover   Missing
--------------------------------------------------------------------------------
src/__init__.py                                        0      0   100%
src/classifiers/__init__.py                            0      0   100%
src/classifiers/classifier.py                         17      3    82%   12, 17, 26
src/classifiers/id3.py                                77      0   100%
src/classifiers/one_vs_one.py                         31      0   100%
src/classifiers/one_vs_rest.py                        21      0   100%
src/dataset/__init__.py                                0      0   100%
src/dataset/dataset.py                               116     14    88%   48, 160-174
...
--------------------------------------------------------------------------------
TOTAL                                                644     54    92%

```

## Zbiory danych

### [Primary tumor](https://archive.ics.uci.edu/dataset/83/primary+tumor)

Zwitter, M. & Soklic, M. (1987). Primary Tumor [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5WK5Q.

TODO

### [Car evaluation](https://archive.ics.uci.edu/dataset/19/car+evaluation)

Bohanec, M. (1988). Car Evaluation [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5JP48.

TODO

### [Balance scale](https://archive.ics.uci.edu/dataset/12/balance+scale)

Siegler, R. (1976). Balance Scale [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5488X.

TODO

## Wyniki

W ramach eksperymentu porównujemy działanie trzech klasyfikatorów: ID3, One vs Rest, One vs One na zbiorach danych
opisanych powyżej.

Do porównania jakości klasyfikacji modeli wykorzystujemy metryki:
dokładność, odzysk, precyzja, miara F, specyficzność, TP rate, FP rate.

Dla zastosowania standardowych metryk klasyfikacji binarnej do problemu klasyfikacji wieloklasowej stosujemy
podejście makro-uśredniania i mikro-uśredniania. Wyniki dla obu wariantów przedstawiono w tabelach.

Stosujemy 5-krotną walidację krzyżową.

Dla każdej metryki podajemy wartość średnią i odchylenie standardowe uzyskane przy walidacji krzyżowej.

W każdym eksperymencie prezentujemy wyniki w 2 tabelach

* Wartości średnie metryk dla poszczególnych modeli przy uśrednianiu mikro i makro
* Wartości odchylenia standardowego metryk dla poszczególnych modeli przy uśrednianiu mikro i makro



### Zbiór Primary tumor

| Model       | Uśrednianie   | Dokładność (avg) | Odzysk (avg) | Precyzja (avg) | Miara F (avg) | Specyficzność (avg) | TP rate (avg) | FP rate (avg) |
|:------------|:--------------|-----------------:|-------------:|---------------:|--------------:|--------------------:|--------------:|--------------:|
| ID3         | macro         |            0,854 |        0,231 |          0,235 |         0,217 |               0,911 |         0,231 |         0,089 |
| One-vs-Rest | macro         |            0,822 |        0,207 |          0,215 |         0,194 |               0,896 |         0,207 |         0,104 |
| One-vs-One  | macro         |            0,863 |        0,267 |          0,263 |         0,258 |               0,917 |         0,267 |         0,083 |
| ID3         | micro         |            0,843 |        0,392 |          0,392 |         0,392 |               0,909 |         0,392 |         0,091 |
| One-vs-Rest | micro         |            0,807 |        0,333 |          0,333 |         0,333 |               0,887 |         0,333 |         0,113 |
| One-vs-One  | micro         |            0,854 |        0,413 |          0,413 |         0,413 |               0,916 |         0,413 |         0,084 |

| Model       | Uśrednianie   | Dokładność (std) | Odzysk (std) | Precyzja (std) | Miara F (std) | Specyficzność (std) | TP rate (std) | FP rate (std) |
|:------------|:--------------|-----------------:|-------------:|---------------:|--------------:|--------------------:|--------------:|--------------:|
| ID3         | macro         |            0,046 |        0,056 |          0,081 |         0,064 |               0,031 |         0,056 |         0,031 |
| One-vs-Rest | macro         |            0,040 |        0,049 |          0,056 |         0,050 |               0,022 |         0,049 |         0,022 |
| One-vs-One  | macro         |            0,026 |        0,081 |          0,073 |         0,071 |               0,017 |         0,081 |         0,017 |
| ID3         | micro         |            0,052 |        0,090 |          0,090 |         0,090 |               0,032 |         0,090 |         0,032 |
| One-vs-Rest | micro         |            0,049 |        0,073 |          0,073 |         0,073 |               0,032 |         0,073 |         0,032 |
| One-vs-One  | micro         |            0,029 |        0,063 |          0,063 |         0,063 |               0,018 |         0,063 |         0,018 |

Wnioski TODO

### Zbiór Car evaluation

| Model       | Uśrednianie   | Dokładność (avg) | Odzysk (avg) | Precyzja (avg) | Miara F (avg) | Specyficzność (avg) | TP rate (avg) | FP rate (avg) |
|:------------|:--------------|-----------------:|-------------:|---------------:|--------------:|--------------------:|--------------:|--------------:|
| ID3         | micro         |            0,960 |        0,922 |          0,922 |         0,922 |               0,973 |         0,922 |         0,027 |
| ID3         | macro         |            0,960 |        0,847 |          0,829 |         0,836 |               0,963 |         0,847 |         0,037 |
| One-vs-Rest | micro         |            0,967 |        0,936 |          0,936 |         0,936 |               0,978 |         0,936 |         0,022 |
| One-vs-Rest | macro         |            0,967 |        0,855 |          0,868 |         0,859 |               0,967 |         0,855 |         0,033 |
| One-vs-One  | micro         |            0,977 |        0,956 |          0,956 |         0,956 |               0,985 |         0,956 |         0,015 |
| One-vs-One  | macro         |            0,978 |        0,953 |          0,946 |         0,948 |               0,977 |         0,953 |         0,023 |

| Model       | Uśrednianie   | Dokładność (std) | Odzysk (std) | Precyzja (std) | Miara F (std) | Specyficzność (std) | TP rate (std) | FP rate (std) |
|:------------|:--------------|-----------------:|-------------:|---------------:|--------------:|--------------------:|--------------:|--------------:|
| ID3         | macro         |            0,001 |        0,021 |          0,019 |         0,013 |               0,007 |         0,021 |         0,007 |
| One-vs-Rest | macro         |            0,005 |        0,046 |          0,036 |         0,037 |               0,004 |         0,046 |         0,004 |
| One-vs-One  | macro         |            0,005 |        0,028 |          0,014 |         0,016 |               0,008 |         0,028 |         0,008 |
| ID3         | micro         |            0,001 |        0,003 |          0,003 |         0,003 |               0,001 |         0,003 |         0,001 |
| One-vs-Rest | micro         |            0,005 |        0,010 |          0,010 |         0,010 |               0,004 |         0,010 |         0,004 |
| One-vs-One  | micro         |            0,005 |        0,009 |          0,009 |         0,009 |               0,003 |         0,009 |         0,003 |

Wnioski TODO

### Zbiór balance scale

| Model       | Uśrednianie   | Dokładność (avg) | Odzysk (avg) | Precyzja (avg) | Miara F (avg) | Specyficzność (avg) | TP rate (avg) | FP rate (avg) |
|:------------|:--------------|-----------------:|-------------:|---------------:|--------------:|--------------------:|--------------:|--------------:|
| ID3         | macro         |            0,791 |        0,515 |          0,487 |         0,500 |               0,809 |         0,515 |         0,191 |
| One-vs-Rest | macro         |            0,784 |        0,508 |          0,483 |         0,494 |               0,802 |         0,508 |         0,198 |
| One-vs-One  | macro         |            0,751 |        0,481 |          0,478 |         0,477 |               0,778 |         0,481 |         0,222 |
| ID3         | micro         |            0,786 |        0,710 |          0,710 |         0,710 |               0,830 |         0,710 |         0,170 |
| One-vs-Rest | micro         |            0,779 |        0,702 |          0,702 |         0,702 |               0,825 |         0,702 |         0,175 |
| One-vs-One  | micro         |            0,748 |        0,664 |          0,664 |         0,664 |               0,798 |         0,664 |         0,202 |

| Model       | Uśrednianie   | Dokładność (std) | Odzysk (std) | Precyzja (std) | Miara F (std) | Specyficzność (std) | TP rate (std) | FP rate (std) |
|:------------|:--------------|-----------------:|-------------:|---------------:|--------------:|--------------------:|--------------:|--------------:|
| ID3         | macro         |            0,018 |        0,013 |          0,029 |         0,018 |               0,020 |         0,013 |         0,020 |
| One-vs-Rest | macro         |            0,027 |        0,026 |          0,027 |         0,025 |               0,024 |         0,026 |         0,024 |
| One-vs-One  | macro         |            0,026 |        0,016 |          0,020 |         0,016 |               0,020 |         0,016 |         0,020 |
| ID3         | micro         |            0,020 |        0,024 |          0,024 |         0,024 |               0,016 |         0,024 |         0,016 |
| One-vs-Rest | micro         |            0,029 |        0,036 |          0,036 |         0,036 |               0,024 |         0,036 |         0,024 |
| One-vs-One  | micro         |            0,026 |        0,030 |          0,030 |         0,030 |               0,022 |         0,030 |         0,022 |

Wnioski TODO

### Inne przebadane zbiory
Nie zaobserwowano istotnych różnic w miarach jakości dla zbiorów danych

* [Nursery](https://archive.ics.uci.edu/dataset/76/nursery)
* [NPHA](https://archive.ics.uci.edu/dataset/936/national+poll+on+healthy+aging+(npha))

### Wnioski końcowe

TODO

## Odstępstwa od dokumentacji wstępnej

Uzupełnienie: przy obliczaniu miar jakości klasyfikacji stosujemy k-krotną walidację krzyżową z $k = 5$ (średnie i
odchylenia standardowe).

Zrezygnowaliśmy z wykreślania krzywych ROC i wyliczania AUC ze względu na problem ze zdefiniowaniem progu odcięcia dla
rozważanych modeli klasyfikacji.

Zbiór danych **nursery** zastąpiliśmy zbiorem **Primary tumor**.