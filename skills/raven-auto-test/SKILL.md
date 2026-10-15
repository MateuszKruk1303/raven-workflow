---
name: raven-auto-test
description: Implementuj i zweryfikuj trwałe testy unit, integration i E2E dla oddanej implementacji Raven. Po uruchomieniu testów automatycznie deleguje niezależne review i poprawki wad testów. Obowiązkowy etap przed PR; kod w repo, dowody w GitHubie.
---

# Raven Auto Test

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [implement](../raven-implement/references/procedures/implement/procedure.md); [e2e-setup](../raven-test/references/procedures/e2e-setup/procedure.md); [e2e](../raven-test/references/procedures/e2e/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


To wykonawca trwałych testów po oddaniu implementacji, przed raven-pr. raven-test-plan ustala strategię; ten skill pisze i uruchamia testy w repo. Nie zastępuj ich raportem browser-review z raven-auto-implement. Etap jest obowiązkowy, ale nie każda zmiana potrzebuje wszystkich trzech warstw ani nowych testów, jeśli istniejące już chronią jej zachowanie.

Przeczytaj [kontrakt GH](../raven-auto-plan/references/github-contract.md) i [adapter](../raven-plan/references/manual-github.md). Wykonuj lokalną procedurę implementacji faz testowych oraz procedury setupu i wykonania E2E wskazane powyżej. Dla już gotowej funkcji nie odtwarzaj implementacji tylko po to, by udawać test-first.

Przeczytaj i stosuj [kontrakt źródeł i niezależnego review](../raven-test/references/test-review.md) przed przekazaniem pracy autorowi oraz reviewerowi.

## Wyjątek brownfield: before-change

Jeżeli zlecono testy zabezpieczające przed refaktorem lub reprodukcję przed bugfixem, przeczytaj [tryb before-change](../raven-test/references/before-change.md). Jego zasady nadpisują poniższe warunki gotowej implementacji, osobistego odbioru i wyłącznie zielonego wyniku; pozostałe zasady manual/auto, niezależności i publikacji obowiązują bez zmian.

## Zakres i plan

Przyjmij change issue/Raven ID, pobierz wymagania, zaakceptowany plan i Progress, raporty review/testera, decyzje i powiązaną strategię raven-test-plan. Czytaj lessons, reguły repo, test-stack i istniejące testy. Ustal branch, bazę i HEAD oraz upewnij się, że implementacja jest oddana i nie jest równolegle edytowana.

Wykorzystaj wydzielone fazy testowe planu. Jeśli ich brak, przygotuj konkretny zakres na podstawie wymagań i ryzyk: zachowanie, niezależne źródło oczekiwanego wyniku, regresja, warstwa, przypadek brzegowy, istniejące pokrycie. Zapisz go jako fazę/task tego samego change oraz nowy snapshot i uzgodnij zakres przed implementacją zgodnie z regułami zmiany planu; nie odhaczaj historycznych faz ponownie. Brak strategii globalnej nie blokuje testów konkretnego dobrze opisanego change.

Dobierz najtańszą skuteczną warstwę: unit dla izolowanej logiki, integration dla granic usług/DB/API, E2E gdy ryzyko wymaga rzeczywistej przeglądarki lub pełnej ścieżki. Nie powielaj tych samych asercji we wszystkich warstwach dla statystyki. Nie zmieniaj wymagań, aby dopasować je do aktualnego outputu.

## Orkiestracja i niezależność

Uruchamiaj po technicznym review implementacji i osobistym sprawdzeniu użytkownika. Nie traktuj samego zielonego przebiegu automatycznego testera jako odbioru użytkownika.

Ten skill jawnie wymaga delegowania: koordynator uruchamia autora testów w osobnym kontekście, a po zakończeniu pisania i uruchomieniu testów NOWEGO reviewera (`fork_turns="none"` lub odpowiednik hosta). Reviewer nie może być autorem testów ani implementatorem produktu i nie dziedziczy ich transkryptów. Koordynator publikuje GH; agenci zwracają artefakty. Poniższa automatyczna pętla review testów nadpisuje zakaz automatycznego review/pętli w manualnym adapterze wyłącznie w tym skillu.

Autor otrzymuje wymagania, zaakceptowany zakres testów, strategię, repo/worktree, artifact_dir i źródłowe instrukcje. Wykonuje kroki poniżej. Podczas review nikt nie edytuje ocenianego kodu. Brak możliwości uruchomienia niezależnego agenta jest blokadą etapu review, nie zgodą na ocenę własnych testów pod inną nazwą roli.

## Wykonanie

1. Sprawdź istniejący runner i wzorce. Uzupełnij wyłącznie brakującą infrastrukturę w uzgodnionym zakresie. Dla E2E wykonaj procedurę e2e-setup przed procedurą e2e, z adapterem GH dla strategii i stanów. Test-stack, seed i konfiguracja są rzeczywistymi plikami repo. Nie instaluj drugiego runnera obok istniejącego ani nie podłączaj CI — to raven-hooks.
2. Unit/integration realizuj dyscypliną raven-implement dla faz testowych. Dla E2E zachowaj PLAN → GENERATE → REVIEW → VERIFY z raven-test, seed, reguły lokatorów, izolację danych, oczekiwanie na stan i cleanup. Używaj odizolowanego środowiska testowego i kont testowych; nie eksportuj prywatnej sesji użytkownika do repo ani CI.
3. Oczekiwane wyniki pochodzą z wymagań/kontraktu, nie z kopiowania implementacji. Kontroluj naiwne asercje, nadmierne mocki i współdzielony stan. Zweryfikuj ochronę regresji zgodnie z Raven, w tym kontrolowanym zepsuciem zachowania w izolacji i bezwarunkowym przywróceniem zmian przed commitem. Błąd składni nie dowodzi skuteczności asercji biznesowej.
4. Uruchom nowe/zmienione testy i właściwe regresje. Dla E2E wykonaj powtórny przebieg, aby sprawdzić izolację i cleanup. Raportuj rzeczywiste polecenia, wyniki i ograniczenia. Stosuj limity napraw bramek z Raven; nie zapętlaj pracy bez postępu.
5. Jeśli test ujawni błąd produktu, zapisz reprodukcję i FAIL w change. Nie osłabiaj asercji. Poprawka produktu wraca do implementacji na zlecenie użytkownika, chyba że już ją jednoznacznie zlecił; po poprawce ponownie sprawdź testy i wskaż potrzebne odświeżenie review.
6. Commituj wyłącznie własny uzgodniony zakres z bramkami Raven, publikuj Progress i dowody. Zaktualizuj cookbook strategii o rzeczywiście dostarczony wzorzec, zachowując historyczne wersje.

## Automatyczne niezależne review testów

Po zakończeniu autora ustal finalny SHA i cały diff etapu testów. Przekaż świeżemu reviewerowi surowe wymagania i decyzje z GH, plan/strategię, lessons, bazę i oceniany SHA, mapę pokrycia i dowody wykonania. Raport autora jest twierdzeniem do sprawdzenia, nie dowodem samym w sobie.

Reviewer ocenia: powiązanie wymagań z asercjami, niezależność oczekiwanych wyników od kodu, skuteczność wykrywania regresji, adekwatność warstwy, granice mocków, przypadki błędów, izolację danych, cleanup, lokatory i oczekiwanie na stan oraz powtarzalność. Obejmuje też konfigurację/helpery i ewentualne zmiany produkcyjne w diffie. Weryfikuje dowody, wykonując potrzebne kontrole w bezpiecznym środowisku. Nie edytuje kodu ani wymagań. Wewnętrzny krok REVIEW źródłowego raven-test nie zastępuje tego świeżego agenta.

Zwraca PASS / REVISE / BLOCKED, stabilne ID T1/T2, kryterium, path:line, dowód, skutek i konkretną poprawkę. Koordynator publikuje osobny niezmienny komentarz `<!-- raven:test-review change=C-03 round=1 -->` z wersją wymagań, base/head SHA i ocenionym zakresem.

Potwierdzone wady testów w uzgodnionym zakresie automatycznie wracają do autora testów, bez pytania o każdą naprawę. Wznów go, jeśli ma aktualny kontekst, w przeciwnym razie uruchom nowego. Po poprawkach autor ponownie uruchamia właściwe testy i regresje, koordynator zapisuje nowy SHA, a niezależny reviewer ponownie ocenia poprawki i ich wpływ. Można wznowić tego samego reviewera, jeśli nigdy nie pisał kodu. Wynik końcowy obejmuje cały dostarczony zakres aktualnej wersji, nie tylko ostatnią poprawkę.

Nie rozszerzaj automatycznie wymagań ani nie poprawiaj produktu pod pozorem naprawy testu. Błąd produktu, sprzeczne wymagania lub decyzja architektoniczna wracają do użytkownika zgodnie z krokiem 5. Po dwóch nieskutecznych naprawach tego samego problemu zatrzymaj pętlę z dowodami; zapisuj liczniki i otwarte ID w checkpointcie GH, także przy zmianie agenta. Brak narzędzi/danych lub niewykonana kontrola oznacza BLOCKED, nie PASS.

Etap jest ukończony po zielonych wymaganych testach i PASS niezależnego review na tej samej wersji. Uwagi pozostawione na świadome zlecenie użytkownika zapisuj jako wyjątek, nie naprawę ani pełny PASS. Jeśli nowych testów nie potrzeba, reviewer ocenia zasadność tej decyzji i istniejące pokrycie. Po przerwie odtwórz checkpoint, nie restartuj wykonanych prac ani nie przenoś review na zmieniony kod.

## Raport i zakończenie

Publikuj komentarz `<!-- raven:test-report change=C-03 round=1 -->`: wersja planu/strategii, base/head SHA, mapa kryterium/ryzyko → plik testu → warstwa → wynik, polecenia, dowody ochrony regresji, nowe i wykorzystane testy, luki i uzasadnione nieadekwatne warstwy. Brak wykonania to NOT VERIFIED/BLOCKED, nie PASS. Dla zmiany niewymagającej nowych testów podaj dowody istniejącej ochrony albo konkretne uzasadnienie nieadekwatności testów; nie dodawaj pustego testu.

Po ukończeniu oddaj wynik użytkownikowi wraz z raportem niezależnego review, chronionymi ryzykami, naprawionymi uwagami i pozostałymi ograniczeniami. Nie twórz PR ani nie ustawiaj Done. raven-pr jest osobno zlecany po tym etapie. CI uruchomi te testy po publikacji PR, jeśli repo ma konfigurację raven-hooks; wynik lokalny nie jest wynikiem CI. Po zmianie kodu oceń wpływ na pokrycie i odśwież potrzebne dowody zamiast przenosić PASS na nowy SHA.
