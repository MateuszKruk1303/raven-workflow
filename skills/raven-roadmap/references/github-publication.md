# Kontrakt publikacji roadmapy

## Tożsamość i źródła prawdy

Czytaj `context/foundation/github.json` utworzony przez `raven-github-setup`. Korzystaj z rzeczywistych ID repozytorium, Project, kanonicznego statusu i opcji, pól `Raven Order`/`Raven ID` oraz etykiety `raven:change`. Nie zakładaj nazwy pola Status ani nie wpisuj ID z innego projektu. Nie dopisuj kolejki do manifestu.

Change = issue z `raven:change`; task = issue z `raven:task` i natywną relacją sub-issue. Roadmapa publikuje changes, nie szczegółowe taski. Współistnienie tych issues w Project nie zmienia ich hierarchii.

Dla nowych changes bez konwencji użyj `C-01`, `C-02` itd.; następny numer jest wyższy od najwyższego użytego w GitHubie i lokalnym kontekście, włącznie z archiwami. W brownfield zachowaj istniejące ID (także nazwy tekstowe). Numer issue `#17`, REST numeric ID, GraphQL node ID, Project item ID i `Raven ID` są różnymi identyfikatorami.

Zachowaj istniejącą nazwę folderu change. Jeśli różni się od Raven ID, zapisz jej rzeczywistą względną ścieżkę w issue. Jeśli folder jeszcze nie powstał, oznacz kontekst jako „powstanie podczas przygotowania”; roadmapa nie tworzy pustych planów. Przyszłe taski mają ID z zakresem rodzica, np. `C-01/T-01`.

## Treść change issue

Tytuł: `[C-01] Konkretny rezultat` (lub istniejący identyfikator).

```markdown
<!-- raven:change id=C-01 -->
## Rezultat
Jednoznaczne zachowanie dostępne po zakończeniu change.

## Zakres
- Uzgodnione zachowania.

## Poza zakresem
- Wyłączenia istotne dla granic tego change.

## Kryteria odbioru
- [ ] Obserwowalny rezultat i warunki jego sprawdzenia.

## Źródła i kontekst
- Raven ID: C-01
- PRD: context/foundation/prd.md, wersja/data, FR-001, US-01.
- Kontekst change: istniejąca ścieżka względna albo „powstanie podczas przygotowania”.

## Zależności
- Odsyłacze do wymaganych issues albo „brak”. Natywne relacje GitHuba są kanoniczne.

## Otwarte decyzje i przeszkody
- Pytanie/przeszkoda, wpływ, potrzebna akcja; albo „brak”.
```

Marker i jawny Raven ID pozwalają odzyskać issue po przerwaniu publikacji przed dodaniem do Project. Przy istniejących issues zachowaj treść, notatki, checkboxy odbioru i identyfikatory; aktualizuj tylko uzgodnione fragmenty. Nie zastępuj całego opisu szablonem bez odczytania aktualnego tekstu. Nie dopisuj checkboxów udających sub-issues. Nie kopiuj do issue pełnego PRD ani planu.

W ścieżkach nie ujawniaj absolutnych ścieżek komputera ani sekretów. Link do pliku na GitHubie dawaj tylko, jeśli plik rzeczywiście jest opublikowany; inaczej jawnie wskaż lokalny kontekst.

## Odczyt przed zapisem

Używaj dostępnego connectora lub `gh`. Sprawdzaj bieżące `--help`, schemat API lub oficjalne dokumenty przed poleganiem na szczegółach mutacji. Odczytaj z pełną paginacją:

- Repo, jego Issues i uprawnienia; Project, jego prywatność, powiązanie, pola i opcje.
- Otwarte i zamknięte issues Ravena, wszystkie itemy Project oraz istniejące ID. Uwzględnij issue z markerem, nawet jeśli częściowy zapis nie nadał etykiety/pól.
- Dla dotkniętych changes: aktualną treść, status, taski, natywne zależności oraz odbiór odnotowany w kontekście.

Dopasowuj po trwałym ID i tożsamości repo, nie tylko po tytule. Konflikt dwóch issues o tym samym ID wymaga wyjaśnienia; nie łącz ani nie usuwaj automatycznie. Niepełny odczyt, brak scope albo 403/404 nie dowodzą nieistnienia zasobu.

## Publikacja i wznowienie

1. Przygotuj konkretny zestaw mutacji wynikający z ustalonego PRD i zlecenia. Dla zwykłego tworzenia roadmapy nie wymagaj osobnej akceptacji tego zestawu. Bezpośrednio przed mutacją ponownie odczytaj zmieniane issues/pola; przy konflikcie z nowszą edycją uzgodnij zmianę zamiast nadpisywać.
2. Najpierw utwórz brakujące issues z markerem i etykietą albo zmień uzgodnione sekcje istniejących. Po każdej operacji zachowaj zwrócone ID/URL w bieżącej sesji. Nie twórz komentarzy.
3. Dodaj brakujące issues do właściwego Project. Link repo–Project sam nie dodaje itemów.
4. Ustaw `Raven ID`, uzgodniony `Raven Order` oraz status według prawdziwych ID opcji z manifestu. Nowe changes domyślnie Backlog; istniejące statusy zachowaj, chyba że zlecona aktualizacja jawnie je obejmuje. Numer kolejności nie zastępuje grafu zależności.
5. Gdy znane są ID wszystkich końców, dodaj brakujące natywne zależności. Jeśli B wymaga A, B jest **blocked by A**. Usuń tylko relacje jawnie wskazane w jawnie zleconym zakresie zmian. Nie twórz sub-issue między changes tylko po to, by wyrazić zależność.
6. Uzupełnij odsyłacze w opisach na podstawie rzeczywistych URL-i. Nie używaj słów automatycznie zamykających issue w przyszłym PR jako substytutu odbioru.
7. Odczytaj issues, membership, wartości pól i krawędzie grafu. Porównaj z przygotowanym zestawem mutacji. Potwierdź też, że nie zmieniono niezwiązanych itemów.

Wielowierszowe opisy przekazuj strukturalnie albo przez plik tymczasowy i `--body-file`, nigdy przez niebezpieczną interpolację shellową. Plik tymczasowy jest transportem, nie drugą roadmapą w repo.

API nie daje jednej transakcji dla całej publikacji. Po timeout lub niejednoznacznym błędzie odczytaj stan przed ponowieniem. Wznowienie wyszukuje markery/ID również poza Project i uzupełnia brakujące kroki zamiast tworzyć duplikaty. Nie usuwaj udanych zapisów w ramach automatycznego rollbacku.

Jeżeli nie można zapisać natywnej zależności, opis tekstowy nie oznacza sukcesu. Zgłoś częściową publikację, konkretne issues/relacje i wymagane działanie. Nie pozostawiaj nowego zależnego change jako Ready. Przy trwałym błędzie dostępu zatrzymaj zależne mutacje; wykonaj niezależną część ustalonego zakresu tylko, jeśli nie powoduje mylącego stanu. Nie ponawiaj odmowy uprawnień bez końca.

Po utracie kontekstu odczytaj GitHub i aktualne źródła, odtwórz brakujące kroki w ramach zlecenia i ustalonego zakresu. Jeśli źródła się zmieniły lub są sprzeczne, pokaż różnicę i zapytaj tylko o nierozstrzygniętą decyzję. Częściowa publikacja nie upoważnia do resetowania istniejącej pracy.

## Aktualne źródła API

Przy publikacji odczytaj potrzebne oficjalne źródło, jeśli dostępne narzędzie nie wyjaśnia operacji:

- Issues i opisy: https://docs.github.com/en/rest/issues/issues
- Natywne zależności: https://docs.github.com/en/rest/issues/issue-dependencies
- Sub-issues (odczyt istniejących tasków): https://docs.github.com/en/rest/issues/sub-issues
- Project item: https://cli.github.com/manual/gh_project_item-add
- Pola itemu: https://cli.github.com/manual/gh_project_item-edit

Nie twórz próbnych issues/relacji w prawdziwym repo w celu sprawdzenia skilla.
