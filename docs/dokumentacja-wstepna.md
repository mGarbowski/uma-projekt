# Projekt UMA - dokumentacja wstępna

* Mikołaj Garbowski
* Michał Pałasz

## Temat
Tematem projektu jest implementacja klasyfikatora dla problemów wieloklasowych, opartego o algorytm ID3 oraz porównanie jego jakości z dwoma wariantami.

Wariant pierwszy polega na stworzeniu dla każdej klasy klasyfikatora binarnego (dla klasy A - klasa pozytywna to A, 
klasa negatywna to wszystkie pozostałe z oryginalnego problemu). Wynikiem predykcji będzie ta klasa, dla której klasyfikator binarny 
przypisze klasę pozytywną z największym stopniem pewności.

Wariant drugi polega na stworzeniu osobnego klasyfikatora binarnego dla każdej pary klas, gdzie jedna jest traktowana jako klasa pozytywna, 
a druga jako negatywna. Model dokonuje predykcji przez głosowanie.

## Opis algorytmu

### Algorytm ID3

Opracowane na podstawie wykładów z przedmiotów UMA (2024Z, Paweł Cichosz) i WSI (2023Z, Paweł Zawistowski)

Algorytm ID3 jest metodą indukcji drzew decyzyjnych.
Drzewo budowane jest rekurencyjnie zaczynając od korzenia.
Węzły nieterminalne odpowiadają podziałowi zbioru uczącego na podstawie wartości wybranego atrybutu.
Gałęzie odpowiadają konkretnej wartości atrybutu użytego do podziału.
Liście zawierają klasę (predykcję) i stopień pewności (rozkład prawdopodobieństwa klas).

Proces predykcji dla wybranego przykładu polega na przejściu od korzenia drzewa do liścia, w każdym węźle wybierając
gałąź, która odpowiada wartości atrybutu użytego do podziału w przykładzie, wynikiem predykcji jest klasa w liściu.

#### Pseudokod
```
Wejścje: 
    Y - zbiór klas
    D - zbiór atrybutów wejściowych
    U - zbiór par uczących

jeśli jednakowa klasa y dla wszystkich przykładów
    zwróć liść z klasą y

jeśli D jest pusty
    zwróć liść zawierający klasę większościową w T

d = argmax InfGain(d, T)
{T_1, T_2, ...} = podział zbioru T po atrybucie d
węzły potomne = {ID3(Y, D-{d}, T_1), ID3(Y, D-{d}, T_2), ...}

zwróć drzewo z korzeniem d i gałęziami prowadzącymi do węzłów potomnych

```


#### Podział zbioru uczącego w węźle
Algorytm ID3 stosuje podziały wielowartościowe na podstawie wartości atrybutu - z węzła (nieterminalnego) 
wychodzi po 1 gałęzi dla każdej wartości atrybutu dyskretnego.

Do podziału zbioru atrybutów w węźle wybiera się ten atrybut, który daje największą zdobycz informacyjną przy podziale definiowaną jako:

$$ InfGain(d, T) = I(T) - Inf(d, T) $$

$$ Inf(d, T) = \sum_j \frac{|T_j|}{|T|} \cdot I(T_j) $$

$$ I(T) = - \sum_i f_i \cdot \log(f_i) $$

Gdzie:

* $d$ - atrybut użyty do podziału
* $T$ - zbiór trenujący
* $T_j$ - podzbiór $T$, gdzie każdy przykład ma $j$-tą wartość atrybutu $d$
* $f_i$ - częstość $i$-tej klasy w zbiorze
* $InfGain$ - zdobycz informacyjna
* $Inf$ - entropia zbioru $T$ podzielonego na podzbiory przez atrybut $d$
* $I$ - entropia zbioru $T$

#### Kryterium stopu
W kroku algorytmu tworzony jest liść jeśli wszystkie przykłady podzbioru zbioru uczącego mają jednakową klasę (wybierana jest ta klasa z pewnością 1) lub jeśli nie ma już atrybutów do kolejnego podziału - wybierana jest klasa większościowa z pewnością równą częstości występowania tej klasy w podzbiorze uczącym ($f_i$).

W przypadku, kiedy w przykładzie dla którego wyznaczana jest predykcja pojawia się wartość atrybutu, dla której nie istnieje gałąź w drzewie, wynikiem predykcji będzie klasa większościowa w węźle nieterminalnym (tym z którego brakuje gałęzi).

#### Przykładowe obliczenia

**Jednolita klasa**

Dla zbioru trenującego

| $x_1$ | $x_2$ | $y$ |
|-------|-------|-----|
| A     | 1     | 0   |
| B     | 2     | 0   |
| C     | 3     | 0   |

Wszystkie przykłady mają jednakową klasę więc tworzony jest liść z klasą 0 i pewnością 1.

**Brak atrybutów do podziału**

| | $y$ |
|-|-----|
| | 0   |
| | 1   |
| | 1   |

Nie ma atrybutów do dalszego podziału, tworzony jest liść z klasą większościową 1 i pewnością $2/3$

**Obliczanie zdobyczy informacyjnej**

Dla $T$:

| $x_1$ | $x_2$ | $y$ |
|-------|-------|-----|
| A     | 1     | 0   |
| B     | 1     | 1   |
| B     | 2     | 1   |
| B     | 2     | 0   |
| B     | 3     | 1   |

Podział po atrybucie $x_1$

$T_A$:

| $x_1$ | $x_2$ | $y$ |
|-------|-------|-----|
| A     | 1     | 0   |

$T_B$:

| $x_1$ | $x_2$ | $y$ |
|-------|-------|-----|
| B     | 1     | 1   |
| B     | 2     | 1   |
| B     | 2     | 0   |
| B     | 3     | 1   |



$$I(T) = -2/5 \log(2/5) - 3/5 \log(3/5) \simeq 0.67$$

$$I(T_A) = 0$$

$$I(T_B) = -1/4 \log(1/4) - 3/4 \log(3/4) \simeq 0.56$$

$$InfGain(x_1, T) = I(T) - \frac{|T_A|}{|T|}I(T_A) - \frac{|T_B|}{|T|}I(T_B)$$

$$InfGain(x_1, T) \simeq 0.67 - 0.2 \cdot 0 - 0.8 \cdot 0.56 \simeq 0.22$$


### Wariant z n klasyfikatorów binarnych

Dla problemu klasyfikacji z liczbą klas równą $n$ powstanie $n$ modeli klasyfikacji binarnej według algorytmu ID3.

Dla pojedynczego modelu dla klasy $c$, modyfikujemy etykiety w zbiorze danych - przypisujemy klasę pozytywną w miejsce klasy $c$, 
przypisujemy klasę negatywną w miejsce wszystkich pozostałych.

Przy tworzeniu liścia, poza klasą większościową zapamiętujemy również częstość występowania przykładów klasy większościowej 
w zbiorze przykładów rozważanym w danym liściu. 
W przypadku jednakowej klasy dla wszystkich przykładów - wartość 1, w pozostałych przypadkach - wartość z przedziału $(0,1)$. 
Częstość potraktujemy jako stopień pewności modelu co do decyzji.

Wynikiem predykcji zespołu modeli będzie ta klasa, którą model binarny zaklasyfikował pozytywnie z największą pewnością.

Przykładowo, dla klas A, B, C, D

| Model binarny dla klasy | A   | B   | C   | D   |
|-------------------------|-----|-----|-----|-----|
| Predykcja (0/1)         | 1   | 0   | 1   | 0   |
| Pewność                 | 0,8 | 0,7 | 0,7 | 0,9 |

Predykcją zespołu modeli będzie klasa A, ponieważ zarówno model binarny dla klasy A i C dał pozytywny wynik klasyfikacji, ale model dla klasy A miał większą pewność.

Jeśli wszystkie modele binarne dadzą predykcję negatywną, predykcją zespołu modeli będzie ta klasa, która została zaklasyfikowana negatywnie z najmniejszą pewnością. Przykład:

| Model binarny dla klasy | A   | B   | C   | D   |
|-------------------------|-----|-----|-----|-----|
| Predykcja (0/1)         | 0   | 0   | 0   | 0   |
| Pewność                 | 0,9 | 0,7 | 0,8 | 0,5 |

Predykcją zespołu modeli będzie klasa D, ponieważ wszystkie predykcje dają klasę negatywną, ale model dla klasy D ma najmniejszą pewność

### Wariant z głosowaniem

Dla problemu klasyfikacji z liczbą klas równą $n$ powstanie $n(n-1)/2$ modeli klasyfikacji binarnej - po 1 dla każdej pary klas.
Klasyfikator binarny rozstrzyga do której klasy z pary należy przykład.

Do trenowania klasyfikatora binarnego dla pary klas A i B użyjemy takiego podzbioru zbioru trenującego, który zawiera tylko przykłady klas A i B.

Predykcja zespołu klasyfikatorów będzie wyznaczana przez głosowanie. 
Ze względu na możliwość uzyskania jednakowej liczby głosów przez wiele klas przy zliczaniu głosów jako liczby modeli które przewidują daną klasę, proponujemy poniższy sposób obliczania głosów ważonych stopniem pewności predykcji
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


## Plan eksperymentów
Mikołaj

## Miary jakości
Michał

## Wybór i opis zbiorów danych
Michał
