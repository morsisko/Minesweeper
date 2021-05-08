# Minesweeper
https://pl.wikipedia.org/wiki/Saper_(gra_komputerowa)

*tekst* - Treść wykreślona z pierwotnej specyfikacji

__tekst__ - Treść dodana do pierwotnej specyfikacji

## Opis zadania
* *Główne okno* **Okno pomocnicze** zawiera dwa pola *tekstowe* **numeryczne** do wprowadzania rozmiaru planszy (n na m pól), pole *tekstowe* **numeryczne** na wprowadzenie liczby min na planszy. **Okno główne** - planszę o wymiarach n na m pól (np. siatka przycisków), , liczbę oznaczonych pól, liczbę min na planszy, oraz przycisk rozpoczęcia nowej gry.
* Wprowadzenie mniejszego rozmiaru planszy niż 2x2 lub większego niż 15x15, liczby min mniejszej niż 0 lub większej niż m\*n **-1** powoduje wyświetlenie komunikatu o błędzie. Nie można rozpocząć gry dopóki te parametry nie są poprawne. Walidacja danych powinna wykorzystywać mechanizm wyjątków.
* *Na początku gry* **Po kliknięciu przez graczna na pierwsze pole** na losowych polach umieszczane jest tyle min ile wskazano w polu tekstowym (każde możliwe rozłożenie min jest równie prawdopodobne), **ma to zapobiec sytuacji, w której gracz przegrałby natychmiastowo po odkryciu pierwszego pola.**
* Po kliknięciu lewym przyciskiem na pole:
  * Jeśli jest tam mina, wyświetlana jest wiadomość o przegranej i gra się kończy,
  * Jeśli w sąsiedztwie pola są miny, na przycisku wyświetlana jest ich liczba a pole dezaktywuje się,
  * W przeciwnym razie sąsiednie pola są sprawdzane tak jakby zostały kliknięte a pole dezaktywuje się.
* Po kliknięciu prawym przyciskiem pole może zostać oznaczone “tu jest mina", po ponownym kliknięciu oznaczenie zmienia się na “tu może być mina”, a po kolejnym kliknięciu oznaczenie znika.
* Gra kończy się po kliknięciu wszystkich pól bez min, lub oznaczeniu “tu jest mina” wszystkich pól z minami (i żadnych innych).
* Po naciśnięciu kolejno klawiszy x, y, z, z, y, pola pod którymi są miny stają się ciemniejsze (https://en.wikipedia.org/wiki/Xyzzy_(computing)#Other_computer_games_and_media).
## Testy
1.	Próba rozpoczęcia gry z rozmiarem planszy i liczbą min: (1 na 1; 1), (5 na 1; 2), (4 na 1; 2), (20 na 500; 12), (5 na 6; -4), (3 na 3; 10), (1 na 10; 5) - oczekiwane komunikaty o błędzie. Wprowadzenie rozmiarów planszy 8 na 8 i liczby min równej 12 na potrzeby kolejnych testów.
2.	Kliknięcie pola, wyświetla się liczba min w sąsiedztwie pola,
3.	Kliknięcie pola, wyświetla się mina, gra się kończy,
4.	Kliknięcie pola, brak min w sąsiedztwie - oczekiwane automatyczne sprawdzenie sąsiadów aż do wyznaczenia obszaru wyznaczonego przez pola sąsiadujące z minami lub krawędzie planszy,
5.	Oznaczenie pola jako “tu jest mina" - licznik oznaczonych powinien *wzrosnąć* **zmaleć** o 1,
6.	Oznaczenie innego pola jako “tu może być mina",
7.	Oznaczenie pola, odznaczenie go, ponowne oznaczenie i ponowne odznaczenie - licznik oznaczonych powinien się odpowiednio aktualizować,
8.	Wygranie gry przez kliknięcie wszystkich pól bez min,
9.	Wygranie gry przez oznaczenie wszystkich pól z minami (można skorzystać z kodu xyzzy),
10.	Próba oznaczenia sprawdzonego pola - oczekiwane niepowodzenie,
11.	Sprawdzenie kilku pól bez min, oznaczenie pól "tu jest mina”, rozpoczęcie nowej gry -licznik min powinien się zaktualizować, a pola zresetować.
12.	Wpisanie kodu xyzzy, zresetowanie gry - wszystkie pola powinny odzyskać standardowy kolor.
