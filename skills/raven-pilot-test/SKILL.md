---
name: raven-pilot-test
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Zabezpiecz zaakceptowany przez użytkownika chunk Raven Pilot dobranymi do ryzyk testami unit, integration i E2E. Wykorzystuj scenariusze Playwright z implementacji i uzupełniaj pokrycie oraz konfigurację bez duplikowania testów."
---

# Raven Pilot Test

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

Wejście: `accepted` z jawną akceptacją aktualnego zachowania albo wznowienie `testing`. Przeczytaj plan, AC, acceptance, handoff, istniejące testy i konfigurację, w tym verification.md oraz wykonywalne scenariusze Playwright i wyniki z implementacji. Nie uruchamiaj tego etapu na szkielecie ani na podstawie review agenta.

1. Porównaj spec_revision i manifest zaakceptowanego kodu z aktualnym stanem. Wyjaśnij istotne rozbieżności; zmiana zachowania po akceptacji wraca do ludzkiego review. Nie blokuj z powodu niezwiązanej edycji dokumentacji lub innego chunka.
2. Zapisz w `test-report.md` mapę AC/ryzyk → właściwy poziom testu. Unit dla istotnej logiki, integration dla kontraktów/usług/uprawnień, E2E dla krytycznych podróży użytkownika. Zacznij od oceny istniejącego pokrycia, w tym scenariuszy Playwright z implementacji: zachowaj przydatne, popraw niestabilne i uzupełnij luki na właściwym poziomie. Nie przepisuj działających scenariuszy do drugiego zestawu. Nie wymuszaj trzech poziomów dla każdego chunka ani duplikacji tych samych asercji.
3. Wykorzystaj istniejący runner i package manager. Jeśli infrastruktury brakuje, skonfiguruj wyłącznie potrzebne minimum teraz. Używaj aktualnej dokumentacji narzędzi tam, gdzie jest potrzebna.
4. Twórz testy obserwowalnego zachowania, istotnych niepowodzeń i izolacji uprawnień, nie kopie implementacji. Zadbaj o izolowane dane, deterministyczny setup/cleanup, brak sekretów w repozytorium i brak modyfikacji danych rzeczywistych użytkowników. E2E sprawdzają działający produkt, nie zastępują całego backendu mockami.
5. Uruchom testy i odpowiednie istniejące kontrole. Napraw błędy implementacji względem już zaakceptowanego kontraktu oraz ponownie sprawdź wynik. Nie osłabiaj asercji, nie pomijaj trudnych scenariuszy i nie zmieniaj wymagania, żeby uzyskać green. Nowa decyzja produktowa wymaga powrotu do review; do tego czasu brak gotowości do archiwizacji.
6. Możesz delegować niezależny przegląd testów albo oddzielne zakresy testów, zgodnie z modelami i granicami kontraktu. Nie twórz konkurujących zapisów tych samych plików. Przy regresji istniejących testów rozróżnij problem zastany od wprowadzonego przez chunk; ujawnij oba.
7. Zapisz rzeczywiste polecenia i wyniki, pokryte AC/ryzyka, uzasadnienie doboru poziomów, pozostałe luki oraz manifest końcowego kodu. Testy skipped/nieuruchomione to brak dowodu, nie sukces. Zapisz wznowienie w `state.json`; przerwanie nie może zgubić postępu.

`ready_to_archive` wymaga zaakceptowanego zachowania, przejścia wymaganych kontroli i braku nierozwiązanych blokujących problemów. Zachowaj oryginalny manifest akceptacji i zapisz osobny końcowy manifest weryfikacji; poprawki zgodności odnotuj w raporcie. Zasugeruj `$raven-pilot-archive <id>`; wykonaj go tylko jeśli zamknięcie zostało już zlecone.

Na wejściu po spełnieniu bramek ustaw testing w state i `in-progress` / `testing` w roadmapie. Po sukcesie zapisz `in-progress` / `ready_to_archive`, nigdy Done przed archiwizacją. Synchronizuj według protokołu z kontraktu; sam raport w czacie nie zastępuje zapisanych artefaktów.
