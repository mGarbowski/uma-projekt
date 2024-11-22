## Miary jakości 

W celu oceny jakości klasyfikacji zastosowane zostaną poniższe metryki, które pozwalają na dokładną analizę wyników modeli.

- TP - true positive
- TN - true negative
- FN - false negative
- FP - false positive

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

### Analiza ROC

Analiza ROC to uniwersalne narzędzie do oceny i porównywania klasyfikatorów, szczególnie w sytuacjach z nierównymi klasami lub gdy potrzebne jest ustalenie odpowiedniego progu decyzyjnego.

Charakterystyka krzywej ROC:
- Oś X: False Positive Rate – im niższa wartość, tym mniejsza liczba błędnych przypadków.
- Oś Y: True Positive Rate (czyli Recall) – im wyższa wartość, tym więcej prawdziwie pozytywnych przypadków jest poprawnie wykrywanych.

AUC - Pole pod krzywą (Area Under the Curve):
- AUC to wartość liczbowa reprezentująca pole pod krzywą ROC. Jest to wskaźnik zdolności modelu do odróżniania klas pozytywnej i negatywnej.


## Wybór i opis zbiorów danych

### Wine Quality (https://archive.ics.uci.edu/dataset/186/wine+quality)

Zbiór danych Wine Quality zawiera informacje o fizykochemicznych właściwościach portugalskich win "Vinho Verde" oraz ich ocenach jakości.


### Estimation of Obesity Levels Based On Eating Habits and Physical Condition (https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)

Zbiór danych Estimation of Obesity Levels Based On Eating Habits and Physical Condition zawiera informacje dotyczące nawyków żywieniowych i kondycji fizycznej osób z Meksyku, Peru i Kolumbii. Jego celem jest ocena poziomu otyłości na podstawie tych danych.


### Iris (https://archive.ics.uci.edu/dataset/53/iris)

Zbiór danych Iris z repozytorium UCI Machine Learning jest jednym z najbardziej znanych i często używanych zestawów danych w dziedzinie uczenia maszynowego. Został wprowadzony przez Ronalda A. Fishera w 1936 roku i służy do klasyfikacji trzech gatunków irysów na podstawie czterech cech morfologicznych.