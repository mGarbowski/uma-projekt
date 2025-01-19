# uma-projekt

Projekt semestralny z przedmiotu Uczenie Maszynowe (UMA 2024Z)

## Autorzy

* Mikołaj Garbowski
* Michał Pałasz

## Temat projektu

Implementacja drzewa decyzyjnego, porównanie sposobu radzenia sobie z problemami wieloklasowymi,
czyli porównanie jakości wyników typowej implementacji ID3 z jakością wyników dwóch podejść:

1) tworzymy osobny model binarny dla każdej klasy (jedna klasa traktowana jako pozytywna, wszystkie pozostałe jako
   negatywne),
   predykcja przez wybór klasy o maksymalnej wartości funkcji decyzyjnej (wymaga posiadania przez każdy klasyfikator
   „stopnia pewności siebie”, co można zdefiniować na wiele sposobów).
2) tworzymy osobny model binarny dla każdej pary klas (jedna klasa traktowana jako pozytywna, druga jako negatywna),
   predykcja przez głosowanie.

Przed rozpoczęciem realizacji projektu proszę zapoznać się z
zawartością: https://staff.elka.pw.edu.pl/~rbiedrzy/UMA/index.html.

## Linki

* [wytyczne prowadzącego](https://staff.elka.pw.edu.pl/~rbiedrzy/UMA/index.html)
* [zasady realizacji projektu](http://elektron.elka.pw.edu.pl/~pcichosz/uma/uma-projekt-zasady.html)

## Uruchomienie i instalacja

### Utworzenie środowiska wirtualnego

Wymagana wersja Pythona: 3.12

```bash
python3 -m venv .venv
```

### Aktywacja środowiska wirtualnego

```bash
source .venv/bin/activate
```

### Instalacja zależności

```bash
pip install -r requirements.txt
```

### Uruchomienie

```bash
python -m src.main
```

### Uruchomienie testów

```bash
python -m pytest
```

### Raport pokrycia kodu testami

```bash
coverage run -m pytest
coverage report -m
```

## Wykorzystane zbiory danych

* Bohanec, M. (1988). Car Evaluation [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5JP48.
* Siegler, R. (1976). Balance Scale [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5488X.
* Zwitter, M. & Soklic, M. (1987). Primary Tumor [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5WK5Q.
