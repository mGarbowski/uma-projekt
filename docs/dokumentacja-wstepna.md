# Dokumentacja wstępna

Dokumentacja wstępna
W założeniach wstępnych projektu należy doprecyzować temat zadania, a oprócz tego:

* Zawrzeć precyzyjny opis algorytmów, które będą wykorzystane, wraz z przykładowymi obliczeniami. Na podstawie tego opisu nie znający tematyki przedmiotu programista powinien być w stanie wykonać poprawną implementację.
* Przedstawić plan eksperymentów.
* Określić jakie miary jakości zostaną wykorzystane. Dla zadań klasyfikacji nie wolno zapomnieć o podaniu dokładności i tabeli pomyłek ("confusion matrix").
* Tam gdzie ma to sens (np. w zdaniach związanych z klasyfikacją) należy wybrać i opisać zbiory danych (w tym podać liczbę przykładów poszczególnych klas), które będą używane do badań, należy określić jak zostanie wyłoniony i użyty zbiór trenujący.
* Im bardziej ogólne wnioski, tym więcej zbiorów danych potrzeba. Zalecam badania na min. 3 nietrywialnych, sensownych zbiorach danych. Jeśli po przemyśleniu nie czują Państwo czy zbiór jest sensowny to na kolejnym etapie, mając już implementację, proponuję wykonać klasyfikację - jeśli dokładność oscyluje w pobliżu 100%, lub w pobliżu dokładności klasyfikatora losowego, to zbiór nie jest sensowny (do Państwa badań). Jeśli zmiana badanych komponentów/parametrów nie wpływa na wyniki, to zbiór nie jest odpowiedni do Państwa badań. (należy wtedy wspomnieć, że dany zbiór przebadano i wyniki nie były wrażliwe na zmiany w badanym algorytmie)
* Sensowny zbiór nie może być zbyt mały. Nie można się opierać tylko na sztucznie wygenerowanych zbiorach.
* Tematy są różne - im mniej kodu stworzył dany zespół, tym więcej badań musi wykonać.
* Nie potrzebuję strony tytułowej i spisu treści. Zawartość merytoryczną należy rozpocząć przywołaniem treści zadania, dokładnie w takiej postaci w jakiej podałem, po czym powinna nastąpić interpretacja treści zadania, doprecyzowanie.
* Proszę nie zamieszczać rozwlekłych wywodów erudycyjnych, zwłaszcza tych nie związanych z treścią zadania, np. algorytmy ... są inspirowane ... Ich początki sięgają lat ...
* Proszę zapoznać się z radami z sekcji: Sposób oceny. 
* Dokumentację wstępną należy wysłać e-mailem. W temacie proszę napisać UMA, a załącznik proszę nazwać tak jak imię i nazwisko autora, np. JanKowalski.pdf. 

## Temat
Tematem projektu jest implementacja klasyfikatora dla problemów wieloklasowych, opartego o algorytm ID3 oraz porównanie jego jakości z dwoma wariantami.

Wariant pierwszy polega na stworzeniu dla każdej klasy klasyfikatora binarnego (dla klasy A - klasa pozytywna to A, 
klasa negatywna to wszystkie pozostałe z oryginalnego problemu). Wynikiem predykcji będzie ta klasa, dla której klasyfikator binarny 
przypisze klasę pozytywną z największym stopniem pewności.

Wariant drugi polega na stworzeniu osobnego klasyfikatora binarnego dla każdej pary klas, gdzie jedna jest traktowana jako klasa pozytywna, 
a druga jako negatywna. Model dokonuje predykcji przez głosowanie.

## Precyzyjny opis algorytmu

### Algorytm ID3
...

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
