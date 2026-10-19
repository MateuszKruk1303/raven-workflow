# Dyscyplina wykonania

- Oczekiwane zachowanie wyprowadzaj z wymagań; kod i aktualny output nie zmieniają wymagań.
- Poznaj wzorce przed edycją. Wykonuj najmniejszą poprawkę domykającą wymagany rezultat, z jego błędami i gwarancjami. Nie dodawaj infrastruktury na zapas.
- Przed niechronionym refaktorem zabezpiecz zachowanie. Test błędu powinien ujawnić regresję na starej wersji, jeśli jest to praktyczne. EXPECTED_RED przed bugfixem nie jest końcowym PASS.
- Testy, konfiguracja i dokumentacja potrzebna do działania są częścią implementacji. Dobierz najtańszą skuteczną warstwę i wykorzystaj istniejące testy; nie sprawdzaj obowiązkowo tego samego zachowania na unit + integration + E2E. Nie powielaj implementacji w asercjach.
- Dowody odnoszą się do konkretnego drzewa, konfiguracji i środowiska. Zmiana unieważnia dotknięty wynik, niekoniecznie wszystkie niezależne kontrole.
- Zachowaj cudze zmiany/staging, wykonuj celowy staging i przegląd diffu. Commity grupuj logicznie.
- Drobna korekta mieści się w zakresie; zmiana istotnej decyzji lub wymagań wraca do użytkownika. Odróżniaj defekt od nowego życzenia.
- Dwie nieskuteczne próby jednego problemu zatrzymują zależną pętlę. Zgłoś oczekiwane i obserwowane zachowanie oraz próby.

- Nie osłabiaj asercji ani nie wyłączaj testów dla PASS. Aktualizuj nieaktualny test po zaakceptowanej zmianie zachowania tylko z uzasadnieniem i Expected z nowego wymagania.
