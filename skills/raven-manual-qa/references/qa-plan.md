# Lokalny plan i przebieg QA

Jeden lokalny plan aktualizowany w trakcie wykonania. Retest zapisuje nową rundę w tym pliku; Git zachowuje wcześniejszą historię. Użyj rzeczywistych wartości zamiast placeholderów.

```markdown
<!-- raven:manual-qa-plan change=ID round=N -->
## Raven Manual QA — plan i przebieg

Tester: raven-manual-qa
Ticket: URL
Źródła: kontrakt/wersja wymagań i decyzje, PR/diff + SHA; brak dostępu do kodu, jeśli dotyczy
Środowisko: URL, build/SHA lub nieustalona wersja, przeglądarka, rola
Dane: ścieżka datasetu/fixture albo identyfikatory własnych rekordów testowych
Zakres: testowana funkcja i istotne warianty
Poza zakresem: kryteria nieweryfikowalne w UI, jeśli występują
Aktualizacja: data i czas

| ID | Kryterium lub ryzyko i źródło | Warunki i dane | Kroki | Expected | Wynik | Actual / dowód / build / problem |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | AC1 — link do wymagania | Rola i rekord testowy | 1. Otwórz formularz; 2. Zapisz; 3. Odśwież | Dane zgodne z wymaganiem pozostają zapisane | NOT RUN | — |

Luki i blokady: konkretne niesprawdzone scenariusze oraz powód, jeśli występują.
Raport końcowy: odsyłacz do qa-report.md po zapisie.
```

Statusy mają ścisłe znaczenie:

- **NOT RUN** — zaplanowany scenariusz jeszcze niewykonany.
- **PASS** — rzeczywiście wykonane kroki i zaobserwowany Expected na wskazanej wersji.
- **FAIL** — zaobserwowana rozbieżność; link do QA-ID w końcowym raporcie, gdy potwierdzona.
- **BLOCKED** — próba niemożliwa lub przerwana przez konkretną przeszkodę; nie oznacza automatycznie defektu produktu.
- **INCONCLUSIVE** — wykonano próbę, ale dowód lub Expected nie pozwala rozstrzygnąć wyniku; opisz brak i sposób rozstrzygnięcia.

Jeśli po zmianie builda wynik traci aktualność, zachowaj poprzednią obserwację z jej wersją, a bieżący wynik ustaw na NOT RUN do ponownej próby. Nie chowaj nieudanej próby pod późniejszym PASS: dopisz rezultat powtórzenia i częstość występowania. Nierozstrzygnięte wyniki i istotne NOT RUN/BLOCKED wykluczają komunikat o ukończonym QA bez problemów.

Dla długich scenariuszy użyj osobnych sekcji S1, S2 poniżej tabeli. Plan ma być czytelny, bez dumpów danych, sekretów i pełnych logów. Krótki dowód obserwacji wystarczy; dołącz screenshot tylko gdy pomaga i można go bezpiecznie udostępnić. Zachowaj wszystkie scenariusze w lokalnym planie; obszerniejsze dowody linkuj zamiast kopiować pełne logi.

Plan zawiera również udane próby. Raport końcowy testera zawiera wyłącznie problemy lub krótki komunikat sukcesu oraz ewentualne ograniczenie, z linkiem do planu. Publikacja raportu nie jest zgodą na merge, zmianą statusu Project ani osobistym odbiorem użytkownika.
