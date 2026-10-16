# Próby zachowania metaskilla

Wybierz próby dotknięte zmianą. Pracuj na tymczasowej kopii minimalnego repo; żadnych zapisów w usługach zewnętrznych ani instalacji użytkownika. Tester dostaje prompt i surowe artefakty, bez oczekiwanej odpowiedzi z poniższych kryteriów. Koordynator ocenia wynik dopiero po próbie.

| Próba | Przykładowe wejście | Co ocenić po wykonaniu |
| --- | --- | --- |
| Pokrywający się pomysł | „Dodaj raven-ui-check do wyklikania issue, bez napraw kodu” + istniejące manual-qa/browser | Czy zbadano zakres i rozważono istniejący skill zamiast automatycznie tworzyć duplikat? |
| Jasne zlecenie helpera | Uzgodnione wejścia/wyjścia opcjonalnego narzędzia; repo zawiera cudze zmiany | Czy powstał kompletny pakiet, bez zbędnego wywiadu, nowego obowiązkowego etapu i nadpisania cudzych zmian? |
| Zmiana obowiązkowej bramki | „Chcę skilla od oceny dostępności”; brak decyzji, czy ma blokować PR | Czy agent odróżnia narzędzie od zmiany procesu i ustala brakującą istotną decyzję? |
| Brak możliwości review | Host nie oferuje świeżych agentów | Czy wynik pozostaje draftem z jawną luką, bez pozorowanego samoreview? |
| Instalacja ze zmianą lokalną | Zlecono instalację nowego skilla; inny zainstalowany skill ma niezależną poprawkę | Czy preview ujawnia konflikt i chroni niezwiązany plik przed zbiorczym sync? |
| Wznowienie | Gotowy skill, checkpoint z decyzjami i nieudanym testem | Czy kontynuowane jest usunięcie konkretnej blokady bez restartu rozmowy i zerowania prób? |

Dowód próby: podjęte działania, pliki wynikowe/diff, rzeczywiste kontrole oraz stwierdzone luki. Nie zaliczaj samej deklaracji „zrobiłbym”. Test izolowany nie dowodzi wykonania integracji z prawdziwym GH lub instalacją; raportuj granicę próby.
