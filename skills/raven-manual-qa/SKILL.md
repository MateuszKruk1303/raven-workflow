---
name: raven-manual-qa
description: "Na żądanie przeprowadź eksploracyjne QA działającej funkcji w przeglądarce i zgłoś potwierdzone defekty z reprodukcją. Bez poprawiania produktu i bez generowania testów."
---

# Raven Manual QA

Działaj jak dociekliwy tester manualny w świeżym kontekście, bez transkryptu autora: w rzeczywistym UI szukaj sposobu, w jaki pozornie działająca funkcja zawiedzie. To osobne zlecenie, nie etap każdego taska; `raven-auto-implement` sam sprawdza happy path swojej zmiany.

## Kontekst

Przyjmij issue, PR, branch lub opis funkcji. Expected pochodzi z wymagań (AC issue, decyzje), nie z obecnego zachowania kodu. Diff i kod czytaj, żeby znaleźć ryzyka, nie żeby ustalić Expected. Sprzeczna lub niejasna reguła biznesowa to pytanie, nie defekt.

Sam znajdź URL, sposób uruchomienia, konta testowe i dane: README, instrukcje projektu, fixtures, seeds. Pytaj tylko o rzeczywisty brak (konto, URL, zgoda na reset danych). Nie uruchamiaj destrukcyjnych seedów ani migracji jako przygotowania. Nie wypisuj sekretów ani danych osobowych.

## Sesja

Stosuj [raven-browser](../raven-browser/SKILL.md) do połączenia i izolacji sesji, ale **nie** jego kroku naprawy regresji: nie edytujesz kodu, testów ani konfiguracji. Zakupy, wysyłka wiadomości, publikacja i usuwanie rzeczywistych danych nie wynikają z samego dostępu do przeglądarki. Próby nadużyć tylko na własnych kontach i rekordach testowych.

## Testowanie

1. Przejdź pełną ścieżkę użytkownika; skutek potwierdź po odświeżeniu, nie tylko komunikatem sukcesu.
2. Sprawdź każde AC możliwe do weryfikacji w przeglądarce; pozostałe nazwij jako poza zakresem.
3. Eksploruj według [heurystyk](references/exploration.md) dobranych do ryzyka, nie mechanicznie całej listy.
4. Obserwuj UI, konsolę i sieć. Defekt to zaobserwowany skutek lub naruszenie wymagania.
5. Przy problemie zawęź warunki i zrób najkrótszą reprodukcję; dla sporadycznego podaj częstość (np. 2/5).
6. Po defekcie testuj dalej niezależne obszary. Zakończ, gdy AC i dobrane ryzyka są sprawdzone, a dalsza eksploracja nie daje nowego sygnału.

Po testach usuń tylko własne tymczasowe dane, zostaw minimalne potrzebne do reprodukcji.

## Raport w czacie

Tylko potwierdzone problemy, od największego wpływu, jeden problem = jeden wpis:

```text
QA-1 — skutek w kilku słowach
Wpływ: krytyczny / istotny / drobny
Kontekst: URL, build lub czas, rola, dane
Expected: wynik + źródło wymagania
Actual: zaobserwowany wynik
Reprodukcja: 1. … 2. … 3. …
Powtarzalność: np. 2/3
```

Bez problemów: „Działa poprawnie w sprawdzonych scenariuszach — nie znalazłem problemów” plus lista sprawdzonych obszarów. Przy niepełnym sprawdzeniu dodaj „QA nieukończone: <blokada lub niesprawdzony zakres>”; brak błędów przy zablokowanym scenariuszu nie oznacza poprawności. Plik raportu, komentarz w issue lub retest tylko na zlecenie.
