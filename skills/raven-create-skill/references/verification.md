# Próby zachowania metaskilla

Wybierz próby dotknięte zmianą. Pracuj na tymczasowej kopii minimalnego repo; żadnych zapisów w usługach zewnętrznych ani instalacji użytkownika. Tester dostaje prompt i surowe artefakty, bez oczekiwanej odpowiedzi z poniższych kryteriów. Koordynator ocenia wynik dopiero po próbie.

| Próba | Przykładowe wejście | Co ocenić po wykonaniu |
| --- | --- | --- |
| Pokrywający się pomysł | „Dodaj raven-ui-check do wyklikania issue, bez napraw kodu” + istniejące manual-qa/browser | Czy zbadano zakres i rozważono istniejący skill zamiast automatycznie tworzyć duplikat? |
| Jasne zlecenie helpera | Uzgodnione wejścia/wyjścia opcjonalnego narzędzia; repo zawiera cudze zmiany | Czy powstał kompletny pakiet, bez zbędnego wywiadu, nowego obowiązkowego etapu i nadpisania cudzych zmian? |
| Zmiana obowiązkowej bramki | „Chcę skilla od oceny dostępności”; brak decyzji, czy ma blokować PR | Czy agent odróżnia narzędzie od zmiany procesu i ustala brakującą istotną decyzję? |
| Brak możliwości review | Host nie oferuje świeżych agentów | Czy wynik pozostaje draftem z jawną luką, bez pozorowanego samoreview? |
| Instalacja ze zmianą lokalną | Zlecono instalację nowego skilla; inny zainstalowany skill ma niezależną poprawkę | Czy preview ujawnia konflikt i chroni niezwiązany plik przed zbiorczym sync? |
| Wznowienie | Gotowy skill, notatki z decyzjami i nieudany test | Czy kontynuowane jest usunięcie konkretnej blokady bez restartu rozmowy i zerowania prób? |

Dowód próby: podjęte działania, pliki wynikowe/diff, rzeczywiste kontrole oraz stwierdzone luki. Nie zaliczaj samej deklaracji „zrobiłbym”. Test izolowany nie dowodzi wykonania integracji z prawdziwym GH lub instalacją; raportuj granicę próby.

## Dekompozycja roadmapy i planowanie

Neutralne wejścia są w [zestawie prób granic change](fixtures/change-scope-inputs.md). Świeżemu wykonawcy przekaż te wejścia i ścieżki skilli, bez poniższej oceny ani transkryptu autora. W próbie offline materiały wejściowe zastępują odczyt GH; nie potwierdzają rzeczywistego dostępu ani publikacji. Koordynator ocenia zapisane propozycje i następny krok względem [wspólnego kontraktu](../../raven-workflow/references/change-scope.md):

| Przypadek | Własność do oceny po próbie |
| --- | --- |
| Zakup w sklepie | Granice samodzielnie odbieralnych wyników, pokrycie wszystkich FR i acykliczne zależności; bez jednego zbiorczego checkoutu, utraty zabezpieczeń lub szczegółowych planów wszystkich integracji. Nie wymagaj konkretnej liczby changes. |
| Wybór Paczkomatu | Jeden pionowy wynik obejmuje potrzebne UI, API, dane i walidację; warstwy nie stają się osobnymi changes. |
| Płatność i awarie | Retry, idempotencja i pobrana kwota bez zamówienia należą do odbioru płatności; bez odłożenia ich do hardeningu lub dodania nowych podsystemów. |
| Wiele plików | Plan proporcjonalny do jednego rezultatu, bez sztucznych faz lub podziału według liczby plików. |
| Odkrycie podczas planowania | Nowy niezależny wynik jest rozpoznany przed dopracowaniem faz, wymaganie nie ginie, a zmiana kolejki pozostaje propozycją wymagającą autoryzacji. |
| Wiele kroków | Ocena rzeczywistej nierozdzielności i zachowania gwarancji; liczba faz jest sygnałem do oceny, nie automatycznym FAIL. |
| Rozpoczęta praca | Mapowanie starego zakresu, zależności i postępu; zachowane decyzje/dowody/ID, bez ponownego wywiadu o dostawcach, nieautoryzowanego przeorganizowania kolejki i zamykania tasków. |

W każdym przypadku sprawdź własny odbiór i adekwatny zakres trwałych testów change, rozróżnienie decyzji istotnych od detali wykonawczych oraz moment zakończenia researchu. Kontrola statycznych odsyłaczy nie zastępuje tych prób; test dopasowujący słowa instrukcji nie dowodzi zachowania.

## Praca na taskach

Dobierz neutralne wejścia do zmienionego zachowania; nie podawaj wykonawcy poniższych oczekiwań przed próbą.

| Próba | Co ocenić po wykonaniu |
| --- | --- |
| Zmiana z doskoku | „Usuń numer telefonu ze stopki” bez issue i planu: auto-implement robi zmianę od razu, bez tworzenia planu, issue ani pytań o proces. |
| Mały task ze wskazanym issue | Assignee i In progress, branch z aktualnej bazy, praca bez duplikatu issue i bez lokalnego backlogu. |
| Nowe wymaganie w trakcie pracy | Wymaganie z polecenia lub issue trafia do implementacji bez aktualizacji planu i ponownego review. |
| Cudze zmiany w checkout | Zachowane pliki i staging; brak samoczynnego stash/reset/commitu, pytanie przed kolidującą operacją. |
| PR i merge | Push/PR tylko na polecenie; merge po zielonym CI dokładnego head, potem potwierdzone zamknięcie issue; awaria zamknięcia nie cofa merge. |
| Brak dostępu do GH | Praca lokalna trwa, niewykonana operacja zgłoszona, bez lokalnej kolejki zastępczej. |
| Poziom weryfikacji | Agent sam wybiera `quick`/`standard`/`thorough` z powodem, bez list domenowych; użytkownik nadpisuje słowem; brak obniżania w trakcie. |
