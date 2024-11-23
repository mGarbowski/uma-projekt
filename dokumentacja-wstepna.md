## Miary jakości 

W celu oceny jakości klasyfikacji zastosowane zostaną poniższe metryki, które pozwalają na dokładną analizę wyników modeli. Aby zastosować miary jakości recall, precision, f-measure, i specificity w przypadku drzewa decyzyjnego klasyfikującego do więcej niż dwóch klas, zostaną wykorzystane następujące podejścia:

### Binaryzacja problemu wieloklasowego

Dla każdej klasy $k$, miary jakości zostaną obliczone przy zastosowaniu podejścia OvR (One vs Rest)

- klasa $k$ jest traktowana jako pozytywna, a wszystkie inne jako negatywne

### Definicje miar jakości

- TP - liczba próbek poprawnie zaklasyfikowanych do klasy $k$
- FP - liczba próbek błędnie zaklasyfikowanych do klasy $k$
- TN - liczba próbek poprawnie zaklasyfikowanych jako należące do innych klas
- FN - liczba próbek należących do klasy $k$, ale zaklasyfikowanych do innych klas

### Odzysk (Recall)

Współczynnik prawdziwych pozytywnych, określający, jak dobrze klasyfikator potrafi znaleźć wszystkie pozytywne przypadki.

$$ Recall = \dfrac{TP}{TP + FN} $$

Im wyższy współczynnik, tym więcej przypadków pozytywnych zostało prawidłowo wykrytych.

### Precyzja (Precision)

Stosunek liczby prawdziwie pozytywnych wyników do liczby wszystkich przypadków zaklasyfikowanych jako pozytywne.

$$ Precision = \dfrac{TP}{TP + FN} $$

Ocenia jak dobre są wyniki pozytywne, czyli ile spośród nich jest faktycznie prawdziwie pozytywnych.

### Miara F (F-measure)

Średnia harmoniczna precyzji i odzysku. Balansuje oba wskaźniki, szczególnie w przypadku, gdy jeden z nich jest znacznie wyższy od drugiego.

$$ F = \dfrac{2 * Recall * Precision}{Recall + Precision} $$

### Specyficzność (Specificity)

Współcznynnik prawdziwych negatywnych, określający jak dobrze klasyfikator potrafi zidentyfikować negatywne przypadki.

$$ Specificity = \dfrac{TN}{TN + FP} $$

Im wyższa wartość, tym lepsze odróżnienie przypadków negatywnych od fałszywie pozytywnych.

### Uśrednianie wyników

Aby uzyskać jedną wartość podsumowującą wydajność klasyfikatora dla wszystkich klas, zostaną zastosowane dwa podejścia do uśredniania wyników:

- #### Makro-uśrednianie
    - Miary jakości są obliczane osobno dla każdej klasy $k$, a następnie ich wyniki są uśrednianie arytmetycznie
    - Każda klasa ma równą wagę, niezależnie od liczby próbek w danych
    $$ Precision_{makro} = \dfrac{1}{K}\sum_{k=1}^{K}{Precision_k} $$
    Analogicznie jak w powyższym wzorze dla Recall, F-measure i Specificity.

- #### Mikro-uśrednianie
    - Wszystkie wartości TP, FP, FN, TN są sumowane dla wszystkich klas
    - Na podstawie tych zsumowanych wartości obliczane są globalne miary jakości
    - Metoda ta przypisuje wagę klasom proporcjonalnie do liczby próbek
    $$ Precision_{mikro} = \frac{\sum_{k=1}^{K} TP_k}{\sum_{k=1}^{K} (TP_k + FP_k)} $$
    Analogicznie jak w powyższym wzorze dla Recall, F-measure i Specificity.

### Analiza ROC

Analiza ROC zostanie zastosowana w kontekście wieloklasowym poprzez podejście One-vs-Rest:

- Dla każdej klasy zostanie wygenerowana osobna krzywa ROC, traktując tę klasę jako pozytywną, a pozostałe jako negatywne
- Dla każdej krzywej ROC obliczone zostanie pole pod krzywą (Area Under the Curve)


## Wybór i opis zbiorów danych

### Car Evaluation (https://archive.ics.uci.edu/dataset/19/car+evaluation)

#### Cel zbioru:

Celem zbioru jest klasyfikacja samochodów na podstawie ich cech, takich jak cena, koszty utrzymania czy pojemność pasażerska, do jednej z czterech kategorii akceptowalności:
- `unacc` (nieakceptowalny),
- `acc` (akceptowalny),
- `good` (dobry),
- `vgood` (bardzo dobry).

#### Charakterystyka zbioru danych:

- **Liczba próbek:** 1 728  
- **Liczba cech:** 6 atrybutów wejściowych + 1 cecha docelowa  
- **Typy danych:** kategoryczne  

#### Opis cech:

1. **buying** (cena zakupu):  
    - Możliwe wartości: `vhigh`, `high`, `med`, `low`

2. **maint** (koszty utrzymania):  
    - Możliwe wartości: `vhigh`, `high`, `med`, `low`

3. **doors** (liczba drzwi):  
    - Możliwe wartości: `2`, `3`, `4`, `5more`

4. **persons** (liczba miejsc dla pasażerów):  
    - Możliwe wartości: `2`, `4`, `more`

5. **lug_boot** (wielkość bagażnika):  
    - Możliwe wartości: `small`, `med`, `big`

6. **safety** (poziom bezpieczeństwa):  
    - Możliwe wartości: `low`, `med`, `high`


### Nursery (https://archive.ics.uci.edu/dataset/76/nursery)

#### Cel zbioru:

Celem zbioru jest klasyfikacja wniosków o przyjęcie dzieci do przedszkola na podstawie różnych kryteriów, takich jak sytuacja finansowa rodziny, liczba dzieci w rodzinie czy zdrowie dziecka. Każdy wniosek jest przypisywany do jednej z trzech kategorii akceptowalności:
- `not_recom` (niezalecany),
- `recommended` (zalecany),
- `priority` (priorytetowy).

#### Charakterystyka zbioru danych:

- **Liczba próbek:** 12 960  
- **Liczba cech:** 8 atrybutów wejściowych + 1 cecha docelowa  
- **Typy danych:** kategoryczne  

#### Opis cech:

1. **parents** (sytuacja rodziców):  
    - Możliwe wartości: `usual`, `pretentious`, `great_pret`

2. **has_nurs** (potrzeba opieki pielęgniarskiej):  
    - Możliwe wartości: `proper`, `less_proper`, `improper`, `critical`, `very_crit`

3. **form** (forma opieki):  
    - Możliwe wartości: `complete`, `completed`, `incomplete`, `foster`

4. **children** (liczba dzieci w rodzinie):  
    - Możliwe wartości: `1`, `2`, `3`, `more`

5. **housing** (warunki mieszkaniowe):  
    - Możliwe wartości: `convenient`, `less_conv`, `critical`

6. **finance** (sytuacja finansowa rodziny):  
    - Możliwe wartości: `convenient`, `inconv`

7. **social** (sytuacja społeczna):  
    - Możliwe wartości: `nonprob`, `slightly_prob`, `problematic`

8. **health** (zdrowie dziecka):  
    - Możliwe wartości: `recommended`, `priority`, `not_recom`


### Balance Scale (https://archive.ics.uci.edu/dataset/12/balance+scale)

#### Cel zbioru:

Celem zbioru jest klasyfikacja stanu równowagi szalki wagi na podstawie masy i odległości obiektów umieszczonych na jej lewym i prawym ramieniu. Każda próbka jest przypisywana do jednej z trzech kategorii:
- `L` (szalka przechylona w lewo),
- `B` (szalka w równowadze),
- `R` (szalka przechylona w prawo).

#### Charakterystyka zbioru danych:

- **Liczba próbek:** 625  
- **Liczba cech:** 4 atrybuty wejściowe + 1 cecha docelowa  
- **Typy danych:** kategoryczne  

#### Opis cech:

1. **Left-Weight** (waga na lewym ramieniu):  
    - Możliwe wartości: liczby całkowite od `1` do `5`

2. **Left-Distance** (odległość na lewym ramieniu):  
    - Możliwe wartości: liczby całkowite od `1` do `5`

3. **Right-Weight** (waga na prawym ramieniu):  
    - Możliwe wartości: liczby całkowite od `1` do `5`

4. **Right-Distance** (odległość na prawym ramieniu):  
    - Możliwe wartości: liczby całkowite od `1` do `5`

**Żaden z powyższych zestawów danych nie posiada brakujących danych.**