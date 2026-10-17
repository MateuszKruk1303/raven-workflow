# Obowiązkowe wykonawcze QA w auto-implement

Ta procedura jest bramką `raven-auto-implement`, również bez UI. Manualne `raven-implement` nie dostaje przez nią obowiązkowego testera. Osobno wywołane [raven-manual-qa](../../raven-manual-qa/SKILL.md) nadal raportuje bez automatycznych napraw; tutaj koordynator prowadzi pętlę do PASS lub uzasadnionej blokady. Korzystaj z podlinkowanych zasad QA, nie uruchamiaj całego samodzielnego skilla z jego odmiennym zakresem.

## Świeży tester i ustalony zakres

Po implementacji i review uruchom osobnego testera Astra/high z `fork_turns="none"`. Otrzymuje pełny kontrakt/fingerprint, wersje źródeł i publiczne decyzje, base/head/tree z dirty diffem, instrukcje uruchomienia, środowisko/URL, rolę testową, ścieżki danych, istniejących testów i dowodów. Nie dostaje transkryptu autora ani jego wniosków jako Expected. Brak wskazówek autora nie zwalnia z celowego znalezienia tych danych w repo; nie czytaj całego repo na zapas.

Tester ustala Expected z kryteriów i źródeł przed wykonaniem. Stosuje [heurystyki manual QA](../../raven-manual-qa/references/exploration.md): pełny cel użytkownika, istotne błędy/granice, trwałość wyniku i uprawnienia, gdy dotyczą funkcji. Kod i istniejące testy wskazują ryzyka, lecz nie definiują poprawnego zachowania. Niejednoznacznej reguły biznesowej nie rozstrzygaj przez skopiowanie implementacji.

Tester zapisuje `qa-plan.md` i `qa-report.md` obok planu, ale nie edytuje produktu, trwałych testów ani ich konfiguracji. Może tworzyć i poprawiać własne tymczasowe skrypty/config QA w zweryfikowanym ignorowanym katalogu lub poza repo. Implementator nie zmienia scenariuszy testera, żeby uzyskać PASS. Zatrzymaj zapisy produktu podczas przebiegu; po zmianie sprawdzanej wersji wynik wymaga oceny aktualności.

## Przygotuj raz, wykonuj ponownie

1. Zapisz macierz według [formatu qa-plan](../../raven-manual-qa/references/qa-plan.md): stabilne S-ID, każde AC/istotne ryzyko i źródło, warunki, konkretne kroki, niezależne Expected i początkowe NOT RUN. W auto obejmij także kryteria spoza UI odpowiednim kanałem. Dopisz sposób uruchomienia i lokalizację każdego scenariusza.
2. Najpierw sprawdź dostępne adekwatne scenariusze i fixtures. Jeśli istniejący test wykonuje rzeczywistą wymaganą ścieżkę z właściwymi asercjami i izolacją, tester może go uruchomić po niezależnym ustaleniu Expected. Nie przepisuj dobrego testu tylko dla drugiego autorstwa. Sam wynik sprzed wejścia testera nie spełnia obowiązku wykonawczego QA; brakującą obserwację lub ryzyko uzupełnij celowo.
3. **UI:** zastosuj [raven-browser](../../raven-browser/SKILL.md), domyślnie Playwright w izolowanej sesji. Po krótkim rozpoznaniu strony przygotuj brakujące scenariusze jako tymczasowy wykonywalny kod Playwright z jawnymi asercjami skutku, np. zapis i ponowny odczyt, walidacja, brak duplikatu. Użyj dostępnego wykonania kodu CLI albo istniejącej biblioteki/runnera Playwright z osobnym tymczasowym configiem; nie wdrażaj nowego frameworka do produktu. Zachowaj wybór przeglądarki użytkownika i granice raven-browser. Używaj stabilnych locatorów z zaobserwowanego UI, nie zapisanych referencji snapshotu jako trwałych selektorów. Nie zastępuj wymaganych interakcji UI samym API.
4. **Bez UI:** uruchom adekwatny scenariusz API/CLI z asercjami rezultatu i skutków, również negatywny gdy wynika z ryzyka. Zmianę dokumentacyjną sprawdź konkretnie: np. wykonaj opisane polecenia w izolowanym fixture, sprawdź odsyłacze i zgodność instrukcji ze źródłami. Nie twórz fikcyjnego browser smoke ani nie utożsamiaj braku UI z brakiem QA.
5. Uruchom scenariusze na potwierdzonej wersji. Sprawdź realny skutek, nie sam exit code runnera bez asercji. Przy zmianach wyglądu obejrzyj render/screenshot; asercje tekstu nie dowodzą layoutu. Jeśli nie można potwierdzić wersji wdrożenia, zapisz identyfikację/czas i ograniczenie; nie przypisuj mu lokalnego HEAD.

Scenariusze muszą nadawać się do powtórzenia: jawny setup, własne identyfikowalne dane, izolacja kont/organizacji i bezpieczny cleanup także po błędzie. Korzystaj z istniejącego testowego auth, bez osobistych cookies i sekretów w raportach. Nie wykonuj rzeczywistych płatności, wysyłek, publikacji ani operacji na cudzych danych. Nie resetuj współdzielonej bazy. Zapisz pozostałe rekordy, jeśli cleanup zawiedzie.

Zachowaj pliki scenariuszy, komendę, zależności/config, dane początkowe i krótkie wyniki do końca pętli. Nie eksploruj od nowa po każdej poprawce; ponawiaj ten sam kod i uzupełniaj go tylko o nowe istotne ryzyko lub konieczną adaptację z zachowaniem Expected. Nie twórz trwałej suite z tymczasowego QA bez potrzeby — trwała ochrona regresji należy do implementatora. Artefakty lokalne nie są publicznymi linkami; przy przekazaniu sesji potwierdź ich dostępność. Gdy zniknęły, odtwórz je z zachowanego planu i jawnie ponów kontrolę.

Zwykły PASS raportuj zwięźle: S-ID, wynik i wersja. Szczegółowe logi, trace i diagnostyczne screenshoty zachowuj przy awarii; screenshot potrzebny do oceny wyglądu wykonaj niezależnie od tego. Nie wklejaj pełnych snapshotów i logów do kontekstu. Oszczędność dotyczy ponownego odkrywania i nadmiarowych artefaktów, nie wymaganych asercji ani zakresu.

## Defekt, naprawa, ponowna próba

Wyniki zapisuj po grupach prób. `qa-report.md` zawiera fingerprint, środowisko/build, ocenione drzewo, rzeczywistą konfigurację testera, link do macierzy i konkretne defekty QA-ID: S-ID, Expected ze źródłem, Actual, najkrótsza reprodukcja, wpływ i dowód. Rozdziel defekt produktu, skryptu QA i blokadę środowiska. Nie kończ na pierwszym błędzie, jeśli pozostałe kontrole są niezależne.

Koordynator przekazuje potwierdzone defekty produktu w zakresie implementatorowi, który naprawia produkt i potrzebną trwałą ochronę. Po kontroli autora i odświeżeniu dotkniętego review **ten sam niezależny tester** uruchamia zachowane reprodukcje i adekwatne regresje. Nie potrzebuje nowego kontekstu od zera w każdej rundzie. Nowy tester przy rzeczywistym handoffie otrzymuje źródła, plan QA, scenariusze, wyniki i liczniki bez transkryptu implementatora.

Zachowuj S-ID, QA-ID i historię rund; nie zmieniaj Expected dla zielonego wyniku. Błąd własnego skryptu tester poprawia z wyjaśnieniem i ponawia scenariusz. Po dwóch nieskutecznych próbach naprawy tego samego problemu zatrzymaj zależną pętlę. Zmiana roli, sesji lub ID nie zeruje licznika. Brak narzędzia/uprawnień lub nierozstrzygnięte wymaganie oznacza konkretną blokadę; wykonaj możliwe niezależne kontrole i zapisz brak.

PASS wymaga wykonania wszystkich wymaganych kryteriów i dobranych istotnych ryzyk z oczekiwanym wynikiem na aktualnej wersji, bez nierozwiązanych defektów w zakresie. NOT RUN/BLOCKED/INCONCLUSIVE/NOT VERIFIED nie są PASS. Po zmianie kodu lub środowiska zachowaj poprzednie obserwacje z wersją, a dotknięte wyniki ponów; niedotknięte dowody wykorzystuj tylko po uzasadnionej ocenie zależności. Do checkpointu dopisz ścieżki raportów/scenariuszy, wynik QA, sprawdzoną wersję, otwarte defekty, liczniki i następny krok. Koordynator nie może zastąpić brakującego raportu własną deklaracją sukcesu.

Gotowe QA nie stanowi odbioru człowieka ani zgody merge. Issue pozostaje In progress do potwierdzonego raven-merge.
