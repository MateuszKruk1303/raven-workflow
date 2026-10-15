---
name: raven-test
description: Implementuj i zweryfikuj trwałe testy unit, integration i E2E dla oddanej implementacji Raven. Manualny etap pisania i uruchamiania testów; niezależne review wywołuje użytkownik przez raven-test-review. Obowiązkowy etap przed PR; kod w repo, dowody w GitHubie.
---

# Raven Test

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [implement](../raven-implement/references/procedures/implement/procedure.md); [e2e-setup](references/procedures/e2e-setup/procedure.md); [e2e](references/procedures/e2e/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


To wykonawca trwałych testów po oddaniu implementacji, przed raven-pr. raven-test-plan ustala strategię; ten skill pisze i uruchamia testy w repo. Nie zastępuj ich raportem browser-review z raven-auto-implement. Etap jest obowiązkowy, ale nie każda zmiana potrzebuje wszystkich trzech warstw ani nowych testów, jeśli istniejące już chronią jej zachowanie.

Przeczytaj [kontrakt GH](../raven-auto-plan/references/github-contract.md) i [adapter](../raven-plan/references/manual-github.md). Wykonuj lokalną procedurę implementacji faz testowych oraz procedury setupu i wykonania E2E wskazane powyżej. Dla już gotowej funkcji nie odtwarzaj implementacji tylko po to, by udawać test-first.

Przeczytaj i stosuj [kontrakt źródeł i niezależnego review](../raven-test/references/test-review.md) przed przekazaniem pracy autorowi oraz reviewerowi.

## Wyjątek brownfield: before-change

Jeżeli zlecono testy zabezpieczające przed refaktorem lub reprodukcję przed bugfixem, przeczytaj [tryb before-change](../raven-test/references/before-change.md). Jego zasady nadpisują poniższe warunki gotowej implementacji, osobistego odbioru i wyłącznie zielonego wyniku; pozostałe zasady manual/auto, niezależności i publikacji obowiązują bez zmian.

## Zakres i plan

Przyjmij change issue/Raven ID, pobierz wymagania, zaakceptowany plan i Progress, raporty review/testera, decyzje i powiązaną strategię raven-test-plan. Czytaj lessons, reguły repo, test-stack i istniejące testy. Ustal branch, bazę i HEAD oraz upewnij się, że implementacja jest oddana i nie jest równolegle edytowana.

Wykorzystaj wydzielone fazy testowe planu. Jeśli ich brak, przygotuj konkretny zakres na podstawie wymagań i ryzyk: zachowanie, niezależne źródło oczekiwanego wyniku, regresja, warstwa, przypadek brzegowy, istniejące pokrycie. Zapisz go jako fazę/task tego samego change oraz nowy snapshot i uzgodnij zakres przed implementacją zgodnie z regułami zmiany planu; nie odhaczaj historycznych faz ponownie. Brak strategii globalnej nie blokuje testów konkretnego dobrze opisanego change.

Dobierz najtańszą skuteczną warstwę: unit dla izolowanej logiki, integration dla granic usług/DB/API, E2E gdy ryzyko wymaga rzeczywistej przeglądarki lub pełnej ścieżki. Nie powielaj tych samych asercji we wszystkich warstwach dla statystyki. Nie zmieniaj wymagań, aby dopasować je do aktualnego outputu.

## Tryb manualny

Uruchamiaj po technicznym review implementacji i osobistym odbiorze użytkownika. Zachowaj interaktywny tryb wykonania Raven i zapis źródeł test_sources. Nie uruchamiaj końcowego review ani pętli reviewer–autor automatycznie. Samokontrola testów i naprawy błędów ich uruchomienia pozostają częścią implementacji. Zlecone poprawki T1/T2 realizuj tylko w wskazanym zakresie, uruchom właściwe testy i oddaj wynik do osobnego review.

## Wykonanie

1. Sprawdź istniejący runner i wzorce. Uzupełnij wyłącznie brakującą infrastrukturę w uzgodnionym zakresie. Dla E2E wykonaj procedurę e2e-setup przed procedurą e2e, z adapterem GH dla strategii i stanów. Test-stack, seed i konfiguracja są rzeczywistymi plikami repo. Nie instaluj drugiego runnera obok istniejącego ani nie podłączaj CI — to raven-hooks.
2. Unit/integration realizuj dyscypliną raven-implement dla faz testowych. Dla E2E zachowaj PLAN → GENERATE → REVIEW → VERIFY z raven-test, seed, reguły lokatorów, izolację danych, oczekiwanie na stan i cleanup. Używaj odizolowanego środowiska testowego i kont testowych; nie eksportuj prywatnej sesji użytkownika do repo ani CI.
3. Oczekiwane wyniki pochodzą z wymagań/kontraktu, nie z kopiowania implementacji. Kontroluj naiwne asercje, nadmierne mocki i współdzielony stan. Zweryfikuj ochronę regresji zgodnie z Raven, w tym kontrolowanym zepsuciem zachowania w izolacji i bezwarunkowym przywróceniem zmian przed commitem. Błąd składni nie dowodzi skuteczności asercji biznesowej.
4. Uruchom nowe/zmienione testy i właściwe regresje. Dla E2E wykonaj powtórny przebieg, aby sprawdzić izolację i cleanup. Raportuj rzeczywiste polecenia, wyniki i ograniczenia. Stosuj limity napraw bramek z Raven; nie zapętlaj pracy bez postępu.
5. Jeśli test ujawni błąd produktu, zapisz reprodukcję i FAIL w change. Nie osłabiaj asercji. Poprawka produktu wraca do implementacji na zlecenie użytkownika, chyba że już ją jednoznacznie zlecił; po poprawce ponownie sprawdź testy i wskaż potrzebne odświeżenie review.
6. Commituj wyłącznie własny uzgodniony zakres z bramkami Raven, publikuj Progress i dowody. Zaktualizuj cookbook strategii o rzeczywiście dostarczony wzorzec, zachowując historyczne wersje.

## Raport i zakończenie

Publikuj komentarz `<!-- raven:test-report change=C-03 round=1 -->`: wersja planu/strategii, base/head SHA, mapa kryterium/ryzyko → plik testu → warstwa → wynik, polecenia, dowody ochrony regresji, nowe i wykorzystane testy, luki i uzasadnione nieadekwatne warstwy. Brak wykonania to NOT VERIFIED/BLOCKED, nie PASS. Dla zmiany niewymagającej nowych testów podaj dowody istniejącej ochrony albo konkretne uzasadnienie nieadekwatności testów; nie dodawaj pustego testu.

Po ukończeniu oddaj raport wykonania, chronione ryzyka i ograniczenia użytkownikowi. Wskaż raven-test-review jako osobno wywoływany kolejny etap przed PR; sam raport wykonania nie oznacza niezależnego review. Nie twórz PR ani nie ustawiaj Done. raven-pr jest osobno zlecany po tym etapie. CI uruchomi te testy po publikacji PR, jeśli repo ma konfigurację raven-hooks; wynik lokalny nie jest wynikiem CI. Po zmianie kodu oceń wpływ na pokrycie i odśwież potrzebne dowody zamiast przenosić PASS na nowy SHA.
