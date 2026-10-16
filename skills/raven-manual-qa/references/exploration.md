# Heurystyki eksploracyjnego QA

Dobieraj próby do funkcji, dostępnych danych i ryzyka. Najpierw ustal, jaki skutek użytkownik chce osiągnąć oraz co nie może zostać utracone, zdublowane lub ujawnione. Z każdej istotnej kategorii wybierz rozróżniający przypadek; pomijaj nieadekwatne. To inspiracje, nie obowiązkowa macierz wszystkich kombinacji.

| Obszar | Pomysły na próby | Obserwowany skutek |
| --- | --- | --- |
| Granice danych | Puste pole, same spacje, zero, wartość ujemna, granica limitu i tuż za nią, długi tekst, Unicode, wklejanie | Walidacja, czytelność komunikatu, brak utraty poprawnych pól |
| Zbiory | Brak rekordów, jeden, wiele w rozsądnym rozmiarze, duplikaty, podobne nazwy, brak pól opcjonalnych | Puste stany, selekcja właściwego rekordu, sortowanie i paginacja |
| Daty i liczby | Koniec miesiąca, zakres od/do, taka sama data, separator dziesiętny, strefa czasowa zgodna z zakresem funkcji | Zgodność widoku z zapisanym wynikiem i ustaloną regułą |
| Kolejność działań | Zapis dwa razy, Enter i kliknięcie, anulowanie i ponowne otwarcie, powrót do poprzedniego kroku | Duplikaty, blokady przycisków, resztki stanu |
| Nawigacja | Odświeżenie w połowie, Wstecz/Dalej, bezpośredni link, nowa karta, ponowne wejście | Utrata danych, błędny routing, niespójny stan |
| Współbieżność | Ten sam własny rekord w dwóch kartach, zapis starego formularza po zmianie w drugiej | Nadpisanie zmian, brak komunikatu konfliktu, pozorny sukces |
| Filtry i wyszukiwanie | Brak wyników, wyczyszczenie, kombinacja filtrów, zmiana filtra na dalszej stronie | Zgubiona selekcja, błędne liczniki, nieaktualne wyniki |
| Uprawnienia | Dostępne konta testowe o różnych rolach, dozwolone przełączenie organizacji, stary link do własnego rekordu | Ujawnienie danych, akcja niedozwolona przez kontrakt |
| Pliki i import | Dozwolony plik, pusty plik, błędny format, duplikat, przerwanie wyboru; realistyczne małe próbki | Częściowy zapis, mylący sukces, brak informacji o błędzie |
| Przerwanie | Anulowanie, utrata połączenia w kontrolowanej sesji, ponowienie po błędzie | Odzyskanie kontroli, brak zdublowanej operacji, zachowanie danych |
| Obsługa UI | Tab/Shift+Tab, Enter/Escape, fokus po dialogu, rozsądny mały ekran, zoom | Zablokowana akcja, niewidoczny błąd, zasłonięte kontrolki |
| Trwałość i integracja | Ponowne otwarcie, sprawdzenie listy i szczegółów, odczyt po ponownym wejściu | Rozbieżność zapisu i widoku, nieaktualne podsumowanie |

Łącz dwie powiązane próby, gdy ujawniają nowe ryzyko: np. filtr + paginacja, dwie karty + edycja, nieudany zapis + ponowienie. Zmieniaj jedną rzecz naraz podczas zawężania reprodukcji.

Nie myl kreatywności z przypadkowym klikaniem. Każda próba ma hipotezę i obserwowalny rezultat. „Użytkownik robi głupotki” oznacza realistyczną pomyłkę, powtórzenie, złą kolejność lub próbę użycia danych niezgodnie z oczekiwaniem formularza. Nie oznacza DoS, masowej wysyłki, realnych zakupów ani testowania cudzych kont.

Jeśli scenariusz wymaga niedostępnej funkcji narzędzia (np. symulacji sieci), sprawdź inny wykonalny wariant lub odnotuj ograniczenie. Nie deklaruj wykonania symulacji na podstawie samej analizy kodu.
