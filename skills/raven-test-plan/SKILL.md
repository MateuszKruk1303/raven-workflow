---
name: raven-test-plan
description: Twórz, wznawiaj i odświeżaj strategię testowania oraz etapowe wdrożenie testów. Pełny plan, ryzyka, cookbook i stan rollout przechowuje w GitHubie; nie implementuje testów.
---

# Raven Test Plan

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [test-plan](references/procedures/test-plan/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Wykonaj pełny lokalny [test-plan](references/procedures/test-plan/procedure.md) i jego referencje, w szczególności `references/test-plan-schema.md`.  Nie zastępuj źródłowego procesu skróconą checklistą. Brak zależności zgłoś. Zachowaj fazy 0–6, warunki wstępne, discovery, profil none/sparse/meaningful, potwierdzany zakres hot-spotów, wywiad, challenger, akceptację briefu, pełny schemat §1–§7, Risk Response Guidance, cookbook, negative space, --status, --refresh i zatrzymanie na handoffie.

Przeczytaj [kontrakt GitHub](../raven-auto-plan/references/github-contract.md). Poniższe zmiany dotyczą transportu i powiązania z Raven workflow; merytoryczne zasady Raven, w tym koszt × sygnał, obawy użytkownika i sygnał ≠ wiedza, pozostają bez zmian. Ten skill nie pisze testów ani konfiguracji CI.

## Kanoniczny plan w GitHubie

Z github.json ustal repo i Project. Wyszukaj we wszystkich stanach issues marker `<!-- raven:test-plan -->`, używając paginacji; nie wnioskuj z braku lokalnego test-plan.md, że plan nie istnieje. Jeśli kilka planów pasuje, ustal właściwy, nie wybieraj najnowszego. Brak dostępu nie upoważnia do lokalnego zastępstwa ani duplikatu.

Gdy planu brak, po źródłowym wywiadzie i akceptacji briefu utwórz jedno issue strategii z markerem i dodaj je do właściwego Project. Nie przedstawiaj go jako zwykłego change do zamknięcia przez najbliższy PR. Pełne §1–§7 zapisuj w oznaczonym bloku `<!-- raven:test-plan:start -->` … `<!-- raven:test-plan:end -->`, zachowując ręczne fragmenty. Zachowaj dosłowny boilerplate schematu. Kolumna Change-folder w §3 staje się Change issue (URL + Raven ID); merytoryczna reszta schematu pozostaje identyczna.

Plan strategii ma kolejne wersje. Po publikacji zapisz niezmienny snapshot w komentarzu `<!-- raven:test-plan-snapshot version=N -->` z pełną treścią i SHA-256 UTF-8. Przy limicie rozmiaru użyj ponumerowanych części i manifestu z hashem; nie ucinaj treści. Postęp rollout to widok wyprowadzany z powiązanych issues, a nie drugie niezależne źródło statusów. Każdą zmianę treści dokumentuj; nie nadpisuj snapshotów.

Testy, konfiguracja, fixture'y i test-stack.md opisujący techniczne uruchamianie pozostają w repo. Kanoniczna strategia i cookbook §6 pozostają w issue, bez drugiej edytowalnej kopii lokalnej. Na potrzeby lokalnych procedur renderuj cały test-plan.md w artifact_dir poza śledzonym repo. Ścieżki źródłowe do niego oznaczają tę kopię. Zwracane zmiany cookbooka publikuj do strategii z dowodami i odczytem zwrotnym.

## Wejścia i wykrywanie stanu

Roadmapę i archiwalne changes czytaj z GH, PRD/tech-stack/lessons/instrukcje z repo; respektuj też jawne źródła użytkownika. Każde ryzyko ma stabilne ID i źródło zgodne z Raven. Nie zastępuj dowodów ryzyka kotwicami implementacji. Rozpoznawanie stanu plików lokalnej procedury zastąp odczytem GH:

- brak strategii → pełne discovery i wywiad;
- not started → brak powiązanego change; po źródłowym potwierdzeniu utwórz zwykły change Raven z wymaganiami fazy, linkiem do strategii/wersji i ID ryzyk;
- change opened → potwierdzony zapis issue; researched → rzeczywiście opublikowane ustalenia researchu;
- planned → kompletny snapshot planu; osobno sprawdź review i akceptację, zanim zaproponujesz wykonanie;
- implementing → rzeczywisty checkpoint rozpoczętej realizacji lub częściowy Progress, nie sam fakt istnienia planu;
- complete → pełny Progress z dowodami i uzupełniony cookbook. To ukończenie wykonania rollout, nie Done w Project: pokaż osobno merge/dostarczenie. Zależności wymagające wdrożonej pracy czekają na jej dostarczenie.

Nie oznaczaj etapu jako otwartego przed potwierdzonym utworzeniem issue. Zachowaj natywne relacje tasków, kolejność i zależności wspólnego kontraktu. Etap rollout to change; jego fazy wykonania są taskami. Nie zakładaj, że zwykłe zamknięcie issue dowodzi realizacji. --status jest wyłącznie odczytem: pokazuje rozbieżności, nie naprawia ich.

## Handoff i odświeżanie

Zachowaj źródłowe payloady handoffów: ryzyka, intencję ochrony, kontekst do ustalenia, przypadki brzegowe i antywzorce. Zamień ścieżki na URL strategii/change/raportu i wskazanie wersji. Nie wywołuj kolejnych skilli automatycznie. Kopiuj komendę do schowka tylko jeśli faktycznie dostępny; nie deklaruj fikcyjnego skopiowania.

Mapowanie: new → utworzenie tożsamości GH; research → raven-research; plan → raven-plan (lub raven-auto-plan na wybór użytkownika); review → raven-plan-review. Dla zatwierdzonych faz pisania testów przekaż raven-test; dla budowy brakującej funkcji lub infrastruktury raven-implement; dla GitHub Actions raven-hooks. Dobór auto pozostaje decyzją użytkownika. Research rekomenduj zgodnie z Raven, lecz nie wymuszaj osobnego skilla, jeśli użytkownik dostarczył już wystarczające ustalenia; nie fabrykuj stanu researched.

--refresh otwiera osobny change odświeżenia z linkiem do bieżącej wersji, przechodzi źródłowe discovery/wywiad i przekazuje pracę dalej. Nie nadpisuje od razu strategii. Zachowaj źródłową regułę przenoszenia korekt researchu dopiero po decyzji użytkownika oraz ograniczenia edycji §1/§2. Przy ponowieniu odczytaj markery i istniejący change, nie twórz duplikatu.

Handoff zawiera URL strategii, wersję, bieżący rollout, dowody stanu i jedną konkretną następną komendę. Nie deklaruj wszystkich faz jako shipped, jeśli jedynie wykonano je lokalnie. Brak lokalnego folderu nie oznacza braku postępu w GH.

Etap trwałych testów ma dwa warianty: raven-test → osobno raven-test-review (manual) albo raven-auto-test (pisanie, uruchomienie, niezależne review i poprawki wad testów w jednym cyklu). Oba używają tego samego change i źródeł; wybór należy do użytkownika. Samo ukończenie manualnego raven-test nie oznacza ukończenia review testów.
