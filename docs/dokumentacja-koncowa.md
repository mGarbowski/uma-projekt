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

### Zbiór 1

Tabelka
Wnioski
TODO

### Zbiór 2

Tabelka
Wnioski
TODO

### Zbiór 3

Tabelka
Wnioski
TODO

### Wnioski końcowe

TODO

## Odstępstwa od dokumentacji wstępnej

Uzupełnienie: przy obliczaniu miar jakości klasyfikacji stosujemy k-krotną walidację krzyżową z $k = 5$ (średnie i
odchylenia standardowe).

Zrezygnowaliśmy z wykreślania krzywych ROC i wyliczania AUC ze względu na problem ze zdefiniowaniem progu odcięcia dla
rozważanych
modeli klasyfikacji.

Zbiór danych **nursery** zastąpiliśmy zbiorem **NPHA**, ponieważ wszystkie modele osiągały na nim dokładność zbliżoną
do $100%$