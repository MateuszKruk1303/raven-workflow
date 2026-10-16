# Wewnętrzna procedura Raven

To część implementacji skilla Raven, nie osobna komenda. Czytaj ją wraz z nadrzędnym SKILL.md, który określa tryb manual/auto i uprawnienia. Wszystkie szablony, referencje i skrypty są dostarczone lokalnie w tym katalogu. Nie wyszukuj ani nie instaluj innych pakietów workflow.

**Obowiązujące zasady wykonania:** [kontrakt GitHub](../../../../raven-auto-plan/references/github-contract.md). Ścieżki change/plan/research/review i strategii testów w tej procedurze oznaczają kopie robocze w artifact_dir poza repo, odtwarzane z GitHuba. Kod i testy pozostają w repo_root. Lokalne wykrywanie stanu zastąp odczytem issues, snapshotów i checkpointów. Pomijaj lokalną synchronizację roadmapy, archiwizację, staging kontekstu i commit epilogu dokumentacji; nie wykonuj ich także przez helpery. Status Done wymaga potwierdzonego merge i odczytu właściwego Project; osobno zlecony raven-merge jawnie finalizuje board zgodnie ze wspólnym kontraktem GitHub. Odwołania do publikacji PR nie upoważniają do audytu, zamykania issues ani automatycznego wywołania tego etapu. Zakończenie procedury oddaje wynik nadrzędnemu skillowi; jego reguły decydują o dalszym review i handoffie. Osobny research jest decyzją użytkownika. Tryb before-change i aktualne zasady review testów mają pierwszeństwo przed domyślną kolejnością testów.

# Przegląd implementacji

Porównaj rzeczywistą pracę implementacyjną z oryginalnym planem, aby wychwycić odchylenia, niebezpieczne decyzje, naruszenia architektury i niewłaściwe użycie wzorców, zanim się skumulują.

Dwa poziomy szczegółowości:
- **Przegląd fazy**: po pojedynczej fazie — szybki, skupiony na zmianach z tej fazy
- **Przegląd pełnego planu**: po wszystkich fazach — kompleksowe sprawdzenie

Dwa tryby:
- **Nowy przegląd**: analiza → ustalenia → interaktywny triage
- **Wznowienie triage**: wczytaj zapisany raport i przejdź do triage dla poszczególnych problemów

## Rozwiązywanie wejścia

1. Argument wskazuje zapisany plik przeglądu (zawiera `<!-- IMPL-REVIEW-REPORT -->`) → **wznów triage** (przejdź do Kroku 5)
2. Argument jest `<change-id>` i istnieje `context/changes/<change-id>/plan.md` → nowy przegląd tego planu
3. Podano ścieżkę planu (np. `@context/changes/<change-id>/plan.md`) → nowy przegląd tego planu
4. Podano numer fazy (np. „phase 3”) → przegląd tylko tej fazy
5. Brak argumentu → wylicz `context/changes/*/change.md`; wybierz zmianę z najnowszym `updated` i `status` w `{implementing, implemented}`, a następnie poproś użytkownika o potwierdzenie.

Jeśli rozwiązana ścieżka planu zaczyna się od `context/archive/`, odmów: wypisz „Ta zmiana jest zarchiwizowana. Przeglądy nie są dodawane do zarchiwizowanych planów.” i ZATRZYMAJ SIĘ.

## Krok 1: Wczytaj plan i wykryj zakres zmiany

Utwórz zadanie: „Przegląd implementacji” z aktywnym statusem „Wczytywanie kontekstu”.

1. **Przeczytaj cały plik planu** — bez limitu/offsetu.
2. **Przeczytaj `context/foundation/lessons.md`, jeśli istnieje**, i użyj zaakceptowanych reguł jako priorytetów podczas skanowania ustaleń — odstępstwo naruszające znaną powtarzającą się regułę jest silniejszym sygnałem niż ogólna uwaga stylistyczna.
3. **Odczytaj stan kanoniczny z sekcji `## Progress` planu** (zobacz `references/progress-format.md`): ukończenie = `count([x]) / count([ ] + [x])`; bieżąca faza = faza zawierająca pierwsze `- [ ]` (lub ostatnia faza, jeśli wszystko jest ukończone). Przeczytaj także sąsiedni `change.md` dla `status` i `updated`.
4. **Zakres**: wskazana faza → ta faza i jej zależności; w przeciwnym razie wszystkie dostarczone fazy oraz cały ustalony diff. Oczekujące pola Manual lub późniejsze testy nie wykluczają dostarczonego kodu z review. Wymień dokładne numery ocenionych faz, a niewykonane kontrole raportuj oddzielnie.
5. **Wyodrębnij** z faz objętych przeglądem: ścieżki plików z „Changes Required”, decyzje architektoniczne, kryteria sukcesu (punkty Automated/Manual w blokach Phase + ich odzwierciedlenie `[ ]`/`[x]` w Progress) oraz listę „What We're NOT Doing” (bariery zakresu).
6. **Zakres Git**: odczytaj zapisane base_sha i reviewed_sha z przekazania/checkpointu GH, zweryfikuj je i odczytaj pełny diff. Nie wyznaczaj bazy z daty dokumentu lub komunikatów commitów. Gdy baza jest nieznana, ustal ją z historią brancha/PR i zgłoś niejednoznaczność przed werdyktem kompletności.

Porównaj listę zmienionych plików z listą plików planu:
- **W planie I w diffie** → oczekiwana zmiana, zweryfikuj, czy treść odpowiada intencji
- **W diffie, ale NIE w planie** → nieplanowana zmiana, zbadaj i oznacz
- **W planie, ale NIE w diffie** → potencjalnie brakująca implementacja

Nie wczytuj wcześniej każdego zmienionego pliku do głównego kontekstu — pozwól równoległym agentom przeglądu czytać to, czego potrzebują. Główny kontekst powinien zawierać plan i podsumowanie diffu, a nie pełne źródła 20 plików.

## Krok 2: Równoległy przegląd przez agentów przeglądu

Zaktualizuj status zadania na „Zbieranie dowodów”.

Świeży reviewer Astra ocenia oba poniższe wymiary. Dodatkowych reviewerów uruchamiaj tylko dla odrębnych istotnych ryzyk lub dużego zakresu; każdy również używa Astry i dostaje wymagania oraz kontrakty potrzebne do swojej oceny. Mała zmiana nie wymaga dwóch kolejnych agentów.

**Agent 1 — Wykrywanie odchyleń od planu** (`general-purpose`)

Przekaż mu: tekst „Changes Required” dla sprawdzanych faz, listę ścieżek plików do przeczytania.

Instrukcje: dla każdej planowanej zmiany przeczytaj rzeczywisty plik i zweryfikuj, czy implementacja odpowiada intencji. Sprawdź:
- Zmiany zaimplementowane inaczej niż planowano (niezgodność intencji, nie formatowania)
- Planowane elementy pominięte bez dokumentacji
- Dodatki nieopisane w planie (rozrastanie się zakresu)

Raportuj dla każdego: ścieżkę pliku, co mówił plan, co istnieje, werdykt (MATCH / DRIFT / MISSING / EXTRA).

**Agent 2 — Bezpieczeństwo, jakość i zgodność ze wzorcami** (`general-purpose`)

Przekaż mu: pełną listę zmienionych plików do przeczytania, ścieżkę głównego katalogu projektu.

Instrukcje:

1. **Skan bezpieczeństwa i jakości** dla każdego zmienionego pliku. Oznacz:
   - **Bezpieczeństwo**: ryzyka wstrzyknięć (SQL, command, XSS), zakodowane na stałe sekrety, brakujące authn/authz na granicach systemu, zbyt liberalne CORS/uprawnienia.
   - **Wydajność**: zapytania N+1, nieograniczona iteracja/rekursja, brak paginacji, niepotrzebne synchroniczne I/O.
   - **Niezawodność**: brak obsługi błędów na zewnętrznych granicach (wywołania API, file I/O, DB), warunki wyścigu, wycieki zasobów.
   - **Bezpieczeństwo danych**: niszczące operacje DB bez wycofania, zmiany schematu bez ścieżki migracji, możliwość utraty danych.

2. **Zgodność ze wzorcami** — dla każdego zmienionego pliku znajdź 1–2 podobne istniejące pliki i porównaj nazewnictwo, podejście do obsługi błędów, strukturę modułu, importy/eksporty, strukturę testów, wzorce konfiguracji. **Raportuj wyłącznie istotne niezgodności** (np. nowy moduł używa camelCase, gdy sąsiednie używają snake_case; nowy endpoint pomija wzorzec middleware uwierzytelniania, którego używa reszta API). Pomijaj trywialne różnice stylistyczne — jeśli kod działa i realizuje plan, drobne formatowanie nie jest ustaleniem.

3. **Dostosuj nakład pracy nad wzorcami do zakresu** — jeśli diff zmienił ≤3 pliki, poświęć minimalny czas na wzorce (niewiele jest do porównania). Skaluj głębokość analizy wzorców wraz z zakresem zmiany.

Raportuj każde ustalenie z: plikiem, numerem linii, kategorią, ważnością (CRITICAL / WARNING / OBSERVATION), opisem, rekomendacją.

## Krok 3: Zweryfikuj kryteria sukcesu

Zaktualizuj status zadania na „Weryfikowanie kryteriów sukcesu”.

Dla każdej sprawdzanej fazy:

**Automatyczne**: oceń dowody wszystkich wymaganych kontroli według wspólnej polityki dowodów Raven. Uruchom brakujące, nieaktualne i potrzebne do niezależnego rozstrzygnięcia ryzyk kontrole. Zapisz, co uruchomiono, a co wykorzystano ponownie, wraz z poleceniem, wersją, wynikiem i źródłem dowodu.

**Ręczne**: w sekcji `## Progress` sprawdź elementy Manual jako `- [x]` względem `- [ ]`. Oznacz elementy oznaczone jako ukończone, którym brakuje obserwowalnych dowodów w diffie (możliwe pozorne odhaczenie); uznaj nieodhaczone elementy za oczekujące.

## Krok 4: Skompiluj ustalenia i przedstaw raport

Zaktualizuj status zadania na „Kompilowanie ustaleń”.

Każde ustalenie zawiera:
- **ID**: F1, F2, F3…
- **Ważność**: CRITICAL / WARNING / OBSERVATION (jak poważne są skutki zignorowania)
- **Wpływ**: LOW / MEDIUM / HIGH (ile uwagi wymaga decyzja)
- **Wymiar**: Plan Adherence / Scope Discipline / Safety & Quality / Architecture / Pattern Consistency / Success Criteria
- **Tytuł**: jedna linia
- **Lokalizacja**: `file:line` (lub „N/A” dla brakujących elementów)
- **Szczegóły**: co jest nie tak wraz z dowodami — plan vs. stan faktyczny albo kod vs. oczekiwany
- **Opcje naprawy**: 1 lub 2 (zobacz poniżej)

### Wpływ

Niezależny od ważności. CRITICAL z LOW impact (oczywista jednolinijkowa poprawka) jest tani; WARNING z HIGH impact (przebudowa architektoniczna) zasługuje na uważne rozważenie.

| Wpływ | Znaczenie |
|---|---|
| 🏃 **LOW** | Szybka decyzja. Poprawka jest oczywista i wąsko ograniczona zakresem. Bezpieczna do grupowania. |
| 🔎 **MEDIUM** | Warto się zatrzymać. Rzeczywisty kompromis lub nietrywialna zmiana — pomyśl przed podjęciem decyzji. |
| 🔬 **HIGH** | Stawka architektoniczna. Szeroki zasięg skutków, strategiczne implikacje lub niejasna najlepsza ścieżka. |

### Opcje naprawy

Domyślnie stosuj **jedną** poprawkę. Oferuj dwie tylko wtedy, gdy istnieje rzeczywisty kompromis, który rozsądny recenzent chciałby rozważyć (np. „załataj miejsce wywołania” vs. „napraw u źródła”). Jeśli zauważysz, że wymyślasz słabą drugą opcję, nie rób tego — przedstaw jedną i przejdź dalej.

**Ustalenia o LOW-impact**: tylko `Fix: [one line]`. Szum nie jest pomocny, gdy odpowiedź jest oczywista.

**Ustalenia o MEDIUM/HIGH-impact**: każda opcja otrzymuje:
```
[1-sentence approach] · Strength: [advantage, ideally grounded in code/plan evidence] · Tradeoff: [cost or risk] · Confidence: HIGH|MED|LOW — [1-line why] · Blind spot: [what we haven't verified, or "None significant"]
```

Gdy oferujesz dwie opcje, oznacz dokładnie jedną jako `⭐ Recommended`.

### Werdykty wymiarów

PASS / WARNING / FAIL dla każdego wymiaru:
- **Plan Adherence** — zaplanowane zmiany wdrożone zgodnie z opisem? FAIL przy MISSING lub poważnym DRIFT.
- **Scope Discipline** — granice „not doing” zachowane? WARNING, jeśli istnieją zmiany EXTRA, ale są nieszkodliwe.
- **Safety & Quality** — bezpieczeństwo, wydajność, niezawodność, bezpieczeństwo danych. FAIL przy każdym ustaleniu CRITICAL.
- **Architecture** — granice modułów, kierunek zależności, uzasadnienie abstrakcji. FAIL przy naruszeniach.
- **Pattern Consistency** — zgodność z istniejącymi konwencjami. WARNING przy drobnych niespójnościach.
- **Success Criteria** — automatyczne kontrole przechodzą, ręczne kontrole obsłużone. FAIL przy błędach kontroli automatycznych.

### Werdykt ogólny

- **APPROVED** — wszystkie PASS albo PASS z ≤2 drobnymi ostrzeżeniami
- **NEEDS ATTENTION** — wiele ostrzeżeń lub 1 niekrytyczny FAIL
- **REJECTED** — dowolny krytyczny FAIL (bezpieczeństwo, poważne odchylenie, bezpieczeństwo danych, nieprzechodzące testy)

Sortuj ustalenia według ważności: CRITICAL → WARNING → OBSERVATION. Ogranicz do 10 — jeśli jest ich więcej, skonsoliduj powiązane ustalenia.

### Format raportu

Zwykły tekst, znaki ramek. Wymiary PASS pojawiają się wyłącznie w tabeli werdyktów, nigdy jako ustalenia. Pomiń grupy ważności z zerową liczbą ustaleń.

```
═══════════════════════════════════════════════════════════
  IMPLEMENTATION REVIEW: [Plan Title]
  Scope: Phase [N] of [Total]  |  Date: YYYY-MM-DD
  Findings: [N critical] [N warnings] [N observations]
═══════════════════════════════════════════════════════════

  Plan Adherence        PASS    ✅
  Scope Discipline      WARNING ⚠️   (1 finding)
  Safety & Quality      FAIL    ❌   (1 finding)
  Architecture          PASS    ✅
  Pattern Consistency   WARNING ⚠️   (1 finding)
  Success Criteria      PASS    ✅

  ► Overall: NEEDS ATTENTION

═══════════════════════════════════════════════════════════
  CRITICAL FINDINGS ❌
═══════════════════════════════════════════════════════════

  F1 — SQL injection in auth handler
  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    Severity:  ❌ CRITICAL
    Impact:    🔎 MEDIUM — real tradeoff; pause to reason through it
    Dimension: Safety & Quality
    Location:  src/auth/handler.ts:42

    Detail:
    SQL query built with string concatenation. Plan specified
    parameterized queries but implementation uses template literals.

    Fix: Replace the template literal with a parameterized query using
         db.query($1, [value]).
      Strength:   Matches the pattern in src/users/query.ts and removes
                  the injection class entirely.
      Tradeoff:   Minor — one call site, a few-line change.
      Confidence: HIGH — identical pattern used elsewhere in this repo.
      Blind spot: None significant.

═══════════════════════════════════════════════════════════
  WARNING FINDINGS ⚠️
═══════════════════════════════════════════════════════════

  F2 — Unplanned /api/status endpoint
  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    Severity:  ⚠️ WARNING
    Impact:    🔬 HIGH — architectural stakes; think carefully before deciding
    Dimension: Scope Discipline
    Location:  src/api/routes.ts:18

    Detail:
    New GET /api/status endpoint not in plan. Functionality is
    related to planned work but extends public API surface.

    Fix A ⭐ Recommended: Document in the plan as an addendum
      Strength:   Preserves the work already done; updates the source of
                  truth before future reviews use the plan as ground truth.
      Tradeoff:   Plan becomes a slightly moving target.
      Confidence: HIGH — this repo's plan updates regularly pick up
                  discovered scope through addenda.
      Blind spot: Stakeholders who reviewed the original scope aren't
                  notified.

    Fix B: Remove and add to follow-up work
      Strength:   Keeps scope discipline strict.
      Tradeoff:   Loses implemented work; another PR needed later.
      Confidence: MEDIUM — depends whether anything already depends on it.
      Blind spot: Haven't checked for callers of /api/status.

  ···

  F3 — camelCase vs. snake_case
  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
    Severity:  ⚠️ WARNING
    Impact:    🏃 LOW — quick decision; fix is obvious and narrowly scoped
    Dimension: Pattern Consistency
    Location:  src/utils/format.ts

    Detail:
    Uses camelCase (formatDate, parseInput) while existing utils use
    snake_case (format_date, parse_input).

    Fix: Rename exports to snake_case to match src/utils/.

═══════════════════════════════════════════════════════════
```

### Zasady formatowania raportu

- **Linia tytułu ustalenia** zawiera wyłącznie ID i krótki tytuł — nic więcej. Wszystko inne znajduje się niżej jako oznaczone pola, aby każdy wiersz był krótki i łatwy do przeskanowania.
- **Zawsze łącz ikony ze słowem.** Nigdy nie używaj samej ikony jako jedynego sygnału — `❌ CRITICAL`, nie tylko `❌`. Dzięki temu raport pozostaje czytelny podczas szybkiego przeglądania i użytkownik nie musi pamiętać znaczenia każdej ikony.
- **Wpływ zawsze zawiera swoje jednoliniowe znaczenie** (skopiuj z tabeli Impact — „architectural stakes; think carefully before deciding” / „real tradeoff; pause to reason through it” / „quick decision; fix is obvious and narrowly scoped”). Dzięki temu LOW/MEDIUM/HIGH są zrozumiałe w miejscu użycia, zamiast wymagać od użytkownika pamiętania tabeli.
- Ważność, Wpływ, Wymiar, Lokalizacja są każdorazowo w osobnej linii z wyrównanymi etykietami. Szczegóły zaczynają się w osobnej linii pod etykietą `Detail:`, aby mogły naturalnie się zawijać.

### Zapisywanie raportu (zawsze)

Zachowaj `Reviewed phases` jako jawną listę numerów faktycznie sprawdzonych faz rozdzielonych przecinkami (np. `1, 3`) albo `none`, gdy nie sprawdzono żadnej. Nigdy nie wywnioskuj zakresu z nazwy pliku raportu, werdyktu ani etykiety „Full plan”. Pełny przegląd wymienia każdy sprawdzony numer i może zastąpić kilka raportów faz dla pokrycia archiwum; dodane lub pozostawione bez przeglądu fazy nie są uwzględniane. Wznowienie triage zachowuje oryginalne pokrycie; nie uzupełniaj niepewnego starszego zakresu.

**Każda ścieżka przez tę umiejętność zapisuje raport i oznacza zmianę** — Triage now, Triage later i Done zapisują plik. To zachowuje wynik przeglądu i poprawny roboczy `change.md.status`; publikacja w GitHubie przebiega zgodnie z nadrzędnym skillem. Zrób to *przed* przedstawieniem opcji kontynuowania — nigdy warunkowo i nigdy wyłącznie w gałęziach „save”.

1. **Zapisz plik raportu** do `context/changes/<change-id>/reviews/impl-review.md` (albo `context/changes/<change-id>/reviews/impl-review-phase-N.md` dla przeglądu ograniczonego do fazy), używając poniższego formatu. Utwórz katalog `reviews/`, jeśli nie istnieje.
2. **Oznacz `change.md`**: ustaw `status: impl_reviewed` oraz `updated: <today>`. Raz, tutaj — niezależnie od opcji kontynuowania wybranej przez użytkownika. (Jeśli pole `change.md` ma już `impl_reviewed`, tylko odśwież `updated`.)
3. Jeśli użytkownik później przeprowadzi triage, raport na dysku jest kopią roboczą: jego pola `Decision:` są aktualizowane w miejscu po rozstrzygnięciu każdego ustalenia (Krok 5), a wszelkie działania następcze „fix in plan/code” są kolejkowane do `context/changes/<change-id>/follow-ups/review-fixes.md`.

```markdown
<!-- IMPL-REVIEW-REPORT -->
# Implementation Review: [Plan Title]

- **Plan**: [plan file path]
- **Scope**: Phase [N] of [Total] / Full plan
- **Reviewed phases**: [explicit phase numbers, e.g. 1, 2, 3]
- **Date**: YYYY-MM-DD
- **Verdict**: [APPROVED/NEEDS ATTENTION/REJECTED]
- **Findings**: [N critical] [N warnings] [N observations]

## Verdicts

| Dimension | Verdict |
|-----------|---------|
| Plan Adherence | PASS/WARNING/FAIL |
| Scope Discipline | PASS/WARNING/FAIL |
| Safety & Quality | PASS/WARNING/FAIL |
| Architecture | PASS/WARNING/FAIL |
| Pattern Consistency | PASS/WARNING/FAIL |
| Success Criteria | PASS/WARNING/FAIL |

## Findings

### F1 — SQL injection in auth handler

- **Severity**: ❌ CRITICAL
- **Impact**: 🔎 MEDIUM — real tradeoff; pause to reason through it
- **Dimension**: Safety & Quality
- **Location**: src/auth/handler.ts:42
- **Detail**: SQL query built with string concatenation. Plan specified parameterized queries.
- **Fix**: Replace the template literal with a parameterized query using db.query($1, [value]).
  - Strength: Matches pattern in src/users/query.ts; removes injection class.
  - Tradeoff: Minor — one call site, a few-line change.
  - Confidence: HIGH — identical pattern used elsewhere.
  - Blind spot: None significant.
- **Decision**: PENDING

### F2 — Unplanned /api/status endpoint

- **Severity**: ⚠️ WARNING
- **Impact**: 🔬 HIGH — architectural stakes; think carefully before deciding
- **Dimension**: Scope Discipline
- **Location**: src/api/routes.ts:18
- **Detail**: New GET /api/status endpoint not in plan.
- **Fix A ⭐ Recommended**: Document in the plan as an addendum
  - Strength: Preserves the work; updates source of truth.
  - Tradeoff: Plan becomes a slightly moving target.
  - Confidence: HIGH — addendum pattern used regularly here.
  - Blind spot: Original-scope stakeholders not notified.
- **Fix B**: Remove and add to follow-up work
  - Strength: Keeps scope discipline strict.
  - Tradeoff: Loses implemented work; another PR later.
  - Confidence: MEDIUM — depends on callers.
  - Blind spot: Haven't checked for callers.
- **Decision**: PENDING

### F3 — camelCase vs. snake_case

- **Severity**: ⚠️ WARNING
- **Impact**: 🏃 LOW — quick decision; fix is obvious and narrowly scoped
- **Dimension**: Pattern Consistency
- **Location**: src/utils/format.ts
- **Detail**: Uses camelCase while existing utils use snake_case.
- **Fix**: Rename exports to snake_case to match src/utils/.
- **Decision**: PENDING
```

Znacznik `<!-- IMPL-REVIEW-REPORT -->` oraz pola `Decision: PENDING` umożliwiają tryb wznowienia.

### Opcje kontynuowania

Gdy raport jest już zapisany, a `change.md` już oznaczony, zapytaj użytkownika:

**Przegląd zapisano w `<report-path>`. Jak chcesz kontynuować?**

**Implementation Review — [N] findings**

- **Przeprowadź triage ustaleń teraz**: Przejdź przez każde ustalenie i podejmij decyzję. Decyzje są zapisywane z powrotem w zapisanym raporcie.
- **Przeprowadź triage później**: Wznów za pomocą `/raven-implement-review <report-path>`.
- **Gotowe**: Raport zapisany — sam zajmę się ustaleniami.

- **Przeprowadź triage ustaleń teraz** → przejdź do Kroku 5; zapisany raport jest kopią roboczą.
- **Przeprowadź triage później** → wypisz ścieżkę zapisanego raportu i przypomnij o uruchomieniu `/raven-implement-review <report-path>`.
- **Gotowe** → wypisz ścieżkę zapisanego raportu i ZATRZYMAJ SIĘ.

Niezależnie od wyboru plik raportu i oznaczenie `impl_reviewed` już istnieją na dysku — wybór decyduje wyłącznie o tym, czy triage następuje teraz, później, czy pozostaje po stronie użytkownika.

## Krok 5: Interaktywny triage

Zaktualizuj status zadania na „Triage”.

### Tryb wznowienia

Jeśli wejście nastąpiło przez zapisany plik: przeczytaj go, sparsuj nagłówki `### F`, odfiltruj do `Decision: PENDING`. Jeśli żadnego nie ma: „Wszystkie ustalenia zostały rozstrzygnięte.” Gotowe.

### Pętla triage

Przechodź przez ustalenia w kolejności ważności (CRITICAL → WARNING → OBSERVATION). Dla każdego:

**Z 2 opcjami naprawy:**

Zapytaj użytkownika:

**F[N] — [title]**

Severity: [sev icon] [SEV]  
Impact: [impact icon] [LEVEL] — [meaning]  
Dimension: [dim]  
Location: [loc]

Detail: [detail]

[Fix A block]

[Fix B block]

**Finding [current] of [total remaining]**

- **Zastosuj Fix A ⭐**: [Fix A one-liner]
- **Zastosuj Fix B**: [Fix B one-liner]
- **Pomiń**: Nie warto teraz naprawiać.
- **Zapisz jako lekcję**: Zapisz jako powtarzającą się regułę projektu przez `/raven-lesson`.

**Z 1 opcją naprawy:**

Zapytaj użytkownika:

**F[N] — [title]**

Severity: [sev icon] [SEV]  
Impact: [impact icon] [LEVEL] — [meaning]  
Dimension: [dim]  
Location: [loc]

Detail: [detail]

[Fix block]

**Finding [current] of [total remaining]**

- **Napraw teraz**: [Fix one-liner]
- **Napraw inaczej**: Inne podejście — omówmy to.
- **Pomiń**: Nie warto teraz naprawiać.
- **Zapisz jako lekcję**: Zapisz jako powtarzającą się regułę projektu przez `/raven-lesson`.

**Obsługa odpowiedzi:**
- **Apply Fix A/B / Fix now**: pokaż dokładną zmianę kodu przed/po. Krótkie potwierdzenie („Zastosować to?”), a następnie edytuj. Oznacz FIXED (zapisz wybraną opcję, np. „Fixed via Fix A”).
- **Fix differently**: zapytaj o preferowane podejście, zastosuj je, oznacz FIXED.
- **Record as lesson**: wstępnie wypełnij cztery pola wpisu lekcji bezpośrednio na podstawie ustalenia — `Context` z Location ustalenia, `Problem` z Detail ustalenia, `Rule` i `Applies to` pozostaw jako puste placeholdery do wypełnienia przez użytkownika. Pokaż proponowany wpis jako kompletny blok markdown i poproś użytkownika o edycję lub potwierdzenie: „Zatwierdzić ten wpis?” z opcjami „Zatwierdzić ten wpis?”, „Edytuj przed zapisaniem” lub „Anuluj”. Po potwierdzeniu dodaj wpis jako nową sekcję H2 do `context/foundation/lessons.md` — jeśli plik nie istnieje, najpierw go utwórz z tym kanonicznym 5-wierszowym nagłówkiem (bez osobnego pliku szablonu; nagłówek jest osadzony bezpośrednio tutaj):

  ```
  # Lessons Learned

  > Append-only register of recurring rules and patterns. Re-read at start by /raven-frame, /raven-research, /raven-plan, /raven-plan-review, /raven-implement, /raven-implement-review.

  ```

  Przepływ wstępnego wypełnienia, a następnie potwierdzenia jest kluczowym szczegółem UX; użytkownik musi zobaczyć pełny proponowany wpis z wstępnie wypełnionymi Context/Problem i mieć możliwość edytowania Rule oraz Applies-to przed dodaniem. Po pomyślnym dodaniu **zawsze** zapytaj użytkownika: „Lekcja zapisana. Czy zastosować także poprawkę w bieżącym kodzie?” z opcjami „Tak — napraw teraz” / „Nie — tylko lekcja”. **Nigdy nie pomijaj tego pytania ani nie decyduj w imieniu użytkownika** — niezależnie od tego, czy poprawka jest trywialna, poza zakresem lub obejmuje wiele plików, decyzja należy do użytkownika. Jeśli tak: pokaż zmianę kodu przed/po, zastosuj ją, oznacz `FIXED + ACCEPTED-AS-RULE: <rule title>`. Jeśli nie: oznacz `ACCEPTED-AS-RULE: <rule title>` (ustalenie pozostaje nienaprawione, reguła jest zapisana dla przyszłej pracy).
- **Skip** → SKIPPED. Przejdź dalej, nie dyskutuj.
- **Inne (wolny tekst)**: zinterpretuj intencję użytkownika. Typowe intencje: „fix differently” (szczególnie w kontekście dwóch poprawek) → zapytaj o preferowane podejście, zastosuj je, oznacz FIXED; „accept risk” → oznacz ACCEPTED z uzasadnieniem użytkownika; „dismiss”/„disagree” → oznacz DISMISSED.

Po każdej decyzji zaktualizuj pole `Decision:` zapisanego raportu dla tego ustalenia (raport zawsze istnieje na dysku — zobacz Krok 4).

### Podsumowanie

```
═══════════════════════════════════════════════════════════
  TRIAGE COMPLETE
═══════════════════════════════════════════════════════════

  Fixed:     F1, F2 (Fix A)   (2)
  Rule:      F3 (+ fixed)     (1)
  Skipped:   F4               (1)
  Accepted:  F5               (1)

═══════════════════════════════════════════════════════════
```

Zaktualizuj zapisany raport o końcowe decyzje. Oznacz zadanie przeglądu jako ukończone.

## Uwagi

- To jest umiejętność **przeglądu**. Domyślnie analizuj i raportuj — wprowadzaj zmiany tylko podczas triage, gdy użytkownik wyraźnie wybierze „Apply Fix” lub „Fix differently” dla konkretnego ustalenia.
- Bądź konkretny. „src/auth/handler.ts:42 — SQL query built with string concatenation, vulnerable to injection” — nie „gdzieś może występować problem z bezpieczeństwem”.
- Nie oznaczaj preferencji stylistycznych, chyba że mają znaczenie. Jeśli kod działa i realizuje plan, drobne różnice stylistyczne względem istniejącego kodu są obserwacjami, a nie ostrzeżeniami.
- Jeśli sam plan był błędny (np. zakładał niebezpieczne podejście), oznacz to — ten przegląd wychwytuje również problemy planu.
- Wpływ dotyczy *wysiłku decyzyjnego*, a nie *ważności*. LOW impact przy ustaleniu CRITICAL oznacza, że poprawka jest oczywista; HIGH impact przy WARNING oznacza, że kompromis jest rzeczywisty.
- Dwie opcje naprawy tylko wtedy, gdy istnieje rzeczywisty kompromis. Nie wymyślaj alternatyw dla trywialnych poprawek.
- Przy przeglądzie pojedynczej fazy nadal sprawdź, czy zmiany z tej fazy nie naruszyły założeń poprzednich faz. Fazy mogą wzajemnie oddziaływać.
- Podczas triage utrzymuj tempo. Użytkownik przeczytał już raport.
- Podczas naprawiania wprowadzaj minimalne, ukierunkowane zmiany. Nie refaktoryzuj otaczającego kodu ani nie „ulepszaj” rzeczy, które nie zostały oznaczone.
