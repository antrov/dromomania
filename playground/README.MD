# Playground
Poszukujemy metody na połączenie zdjęc porónych obróbakch w jedną grupę, która reprezentuję tę samą ofertę.

Wybrana została róznica pomiędzy percepcyjnymi hashami, wynoszą maksymalnie 14.

Wartość ta została wybrana empirycznie na próbce zdjęc pobranych z róznych portali. Nie zawsze łączy wszystkie zdjęcia (przez np. crop) ale nie ma błędnych połączeń, które były przy wyzszych wartościach róznicy lub przy innych metodach hashowania.

Testy grupowania widać na dwóch stronach:
* families.html - gdzie jest pokazana rónice hasha kazdego zdjęcia z kazdym
* grouped_images.html - gdzie są ju tylko gotowe zbiory zdjęć