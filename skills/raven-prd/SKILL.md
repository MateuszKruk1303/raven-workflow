---
name: raven-prd
description: >
  Generate context/foundation/prd.md from shape-notes.md (or raw notes) against
  the locked PRD schema. Auto-routes to greenfield (10 sections) or brownfield
  (11 sections) template based on context_type in shape-notes.md or cwd
  auto-detection. Use when the user has shaping notes ready and wants a
  schema-conformant PRD written to disk. Trigger phrases: "write the PRD",
  "generate PRD", "create the PRD from notes", "stwórz PRD", "turn notes into a
  PRD", "PRD from shape-notes". Use AFTER /raven-shape, not in place of it.
---
# PRD: Generowanie context/foundation/prd.md z shape-notes

Ta umiejętność jest drugim ogniwem w łańcuchu bootstrapowania. Kolejność dalszych etapów określa raven-workflow. Jej jedyne zadanie: wziąć plik ukształtowanych notatek i wygenerować `context/foundation/prd.md`, który jest zgodny z zablokowanym schematem PRD, kierując każdą lukę do `## Open Questions` zamiast wymyślać treść.

Umiejętność automatycznie kieruje do poprawnego szablonu na podstawie `context_type` w danych wejściowych:
- **greenfield** → 10-sekcyjny szablon PRD (produkt budowany od podstaw)
- **brownfield** → 11-sekcyjny szablon PRD (zmiana różnicowa w istniejącym systemie)

Ta umiejętność jest **generatorem dokumentów**, a nie moderatorem procesu odkrywania. NIGDY nie wymyśla decyzji domenowych, reguł logiki biznesowej, kryteriów sukcesu ani historyjek użytkownika. Wszystko, czego brakuje w danych wejściowych, trafia dosłownie do `## Open Questions`, aby człowiek mógł to rozstrzygnąć.

Zablokowany schemat, z którym zgodna jest ta umiejętność, znajduje się w `references/prd-schema.md` (względem tego SKILL.md). Przeczytaj go przed wygenerowaniem jakiegokolwiek artefaktu i ponownie sprawdź względem niego utworzony plik przed zapisaniem na dysk.

## Kiedy używać, kiedy pomijać

**Używaj, gdy**: użytkownik uruchomił `/raven-shape` (a `context/foundation/shape-notes.md` istnieje z blokiem checkpoint), LUB użytkownik ma plik surowych notatek, który chce przekształcić w szkic PRD, LUB użytkownik wyraźnie prosi o (ponowne) wygenerowanie `context/foundation/prd.md`.

**Pomiń, gdy**: użytkownik nadal tworzy pomysły i nie ma notatek — najpierw wskaż `/raven-shape`. Pomiń także, gdy użytkownik chce ręcznie *edytować* istniejący PRD — ta umiejętność zapisuje całe pliki; precyzyjne edycje są poza zakresem.

## Relacja z innymi umiejętnościami

- `/raven-shape` — tworzy `shape-notes.md`, kanoniczne dane wejściowe. Zawsze preferowany etap poprzedzający tę umiejętność.
- Dalszy routing: [raven-workflow](../raven-workflow/SKILL.md), w tym architektura, potrzebny setup i roadmapa. Zachowaj istniejący stack w brownfield.

## Początkowa odpowiedź

Gdy ta umiejętność jest wywoływana:

1. **Jeśli podano argument ścieżki** (np. `/raven-prd @notes/raw.md` lub `/raven-prd context/foundation/shape-notes.md`), przechwyć go jako ścieżkę wejściową. Przejdź do Kroku 1.
2. **Jeśli nie podano argumentu**, ustaw domyślną ścieżkę wejściową na `context/foundation/shape-notes.md` i przejdź do Kroku 1. Nie pytaj jeszcze — Krok 1 obsługuje przypadek braku danych wejściowych.

## Proces

### Krok 1: Zlokalizuj dane wejściowe

Rozwiąż ścieżkę wejściową:

- Jeśli przekazano argument, użyj go dosłownie (usuń początkowy `@`, jeśli występuje).
- W przeciwnym razie użyj domyślnie `context/foundation/shape-notes.md`.

Przetestuj rozwiązaną ścieżkę:

```bash
test -f "<resolved-path>"
```

Jeśli plik istnieje, przeczytaj go W CAŁOŚCI (bez `limit`/`offset`) i przejdź do Kroku 1.5.

Jeśli plik nie istnieje, zapytaj użytkownika:

**Dane wejściowe?** Nie znaleziono pliku wejściowego w `<resolved-path>`. Jak chcesz kontynuować?

- **Najpierw uruchom /raven-shape (Zalecane)**: Zatrzymaj się tutaj. Uruchom `/raven-shape`, aby utworzyć shape-notes.md, a następnie ponownie wywołaj `/raven-prd`.
- **Wklej surowe notatki**: Poczekaj, aż użytkownik wklei dowolne posiadane notatki. Kontrola ubogich danych wejściowych ostrzeże o brakujących sygnałach.
- **Anuluj**: Zakończ bez zmian.

Po wybraniu „Najpierw uruchom /raven-shape”: wypisz „Stopping. Run `/raven-shape` to produce shape-notes.md, then re-invoke `/raven-prd`.” i ZATRZYMAJ SIĘ.

Po wybraniu „Wklej surowe notatki”: wyświetl komunikat „Paste your notes below. End with an empty line.” i przechwyć tekst użytkownika jako dane wejściowe w pamięci. Przejdź do Kroku 1.5 z tą treścią.

Po wybraniu „Anuluj”: ZATRZYMAJ SIĘ bez zmian.

### Krok 1.5: Określ typ kontekstu

Określ, czy wygenerować PRD greenfield, czy brownfield:

1. **Jeśli dane wejściowe mają `context_type:` w frontmatter** — użyj tej wartości bezpośrednio. Potwierdzenie nie jest potrzebne.
2. **Jeśli w frontmatter nie ma `context_type:`** (surowe notatki, wklejone dane wejściowe) — automatycznie wykryj na podstawie cwd:

   Oceń intencję i rzeczywisty stan produktu na podstawie README, kodu i historii. Sam starter, lockfile lub manifest nie oznacza brownfield. Przy niejednoznaczności zapytaj o nowy produkt albo zmianę istniejącego.

   Zapytaj użytkownika:

   **Kontekst** Nie znaleziono context_type w danych wejściowych. Na podstawie markerów cwd wygląda to na [greenfield|brownfield]. Zgadza się?

   - **[Wykryty tryb] — poprawny (Zalecane)**: Wygeneruj PRD [greenfield|brownfield].
   - **[Inny tryb] — zastąp**: Wygeneruj zamiast tego PRD [other].

Zapisz rozstrzygnięty `context_type` do użycia w Krokach 2 i 3. Przejdź do Kroku 2.

### Krok 2: Oceń dane wejściowe

Oceń znaczenie treści, nie zgodność nagłówków lub formatowanie Markdown. Akceptuj polskie i angielskie sekcje, wymagania FR w tabelach lub listach oraz obserwowalne scenariusze bez pogrubionego Given/When/Then. Zachowaj istniejące ID i źródła wymagań.

Sprawdź problem/odbiorcę, zakres, wymagania i kryteria, reguły biznesowe (albo uzasadnione nie dotyczy), ograniczenia oraz w brownfield obecny system i zachowania do zachowania. Checkpoint pomaga wznowić pracę, lecz nie dowodzi kompletności. Każdą rzeczywistą lukę wraz z konsekwencją przenieś do Open Questions. Gdy użytkownik zlecił szkic z niepełnych notatek, wykonaj go bez ponownego pytania o tę samą zgodę. Pytaj tylko o decyzje konieczne do ustalenia zakresu; nie wymyślaj treści.

### Krok 3: Wygeneruj PRD

Użyj przeczytanego schematu `references/prd-schema.md`; ponów odczyt tylko gdy zmienił się plik lub nie masz jego treści.

Najpierw zbuduj zawartość PRD **w pamięci** (jeszcze nie na dysku):

#### 3a. Frontmatter

Wypełnij każde wymagane pole frontmatter zgodnie ze schematem:

- `project` — wyodrębnij z input frontmatter `project:`, jeśli występuje; w przeciwnym razie z nagłówka Title (`# <Project>`); w przeciwnym razie `# TODO: project — see Open Questions`.
- `version` — `1` dla pierwszego PRD zapisywanego przez tę umiejętność. Krok kolizji (Krok 4) zwiększa tę wartość, jeśli użytkownik wybierze zapis wersjonowany.
- `status` — `draft`. Nigdy nie promuj do `reviewed`/`locked`; to decyzja dalszego etapu.
- `created` — dzisiejsza data w formacie `YYYY-MM-DD` (użyj `date +%Y-%m-%d`).
- `context_type` — `greenfield` lub `brownfield` (z Kroku 1.5).
- `product_type` — pobierz z danych wejściowych, jeśli dostępne; w przeciwnym razie `# TODO: product_type — see Open Questions` (i dodaj wpis Open Question).
- `target_scale`, `timeline_budget` — ta sama zasada. Jeśli dane wejściowe zawierają pole, skopiuj je dosłownie; jeśli nie, wygeneruj `# TODO: <field> — see Open Questions` i dodaj pasujące Open Question. Dla brownfield `timeline_budget` używa `delivery_weeks` zamiast `mvp_weeks`.

**NIE wypełniaj** `team_profile`, `tech_preferences` ani `deployment_constraint` we frontmatter PRD, nawet gdy notatki wejściowe je zawierają. Pola te są zbierane przez dalszy etap wyboru tech-stack (greenfield) lub oceny stacku (brownfield), a nie przez PRD. Jeśli dane wejściowe je zawierają, podsumuj je w komunikacie przekazania Kroku 5 pod „kontekst do architektury i planowania Raven”, aby użytkownik wiedział, że treść jest kierowana dalej, a nie po cichu odrzucana — ale NIE umieszczaj ich we frontmatter PRD.

Nazwy kluczy pól są zgodnie ze schematem nośne. Wartości pól nie są.

#### 3b. Wymagane sekcje (w kolejności schematu)

Lista sekcji zależy od `context_type`:

**Greenfield (10 sekcji):**

Wygeneruj dokładnie te 10 nagłówków na poziomie `##`, w dokładnie tej kolejności (kontrakt nazw sekcji schematu określa, według czego parsery dalszych etapów dzielą dokument):

1. `## Vision & Problem Statement`
2. `## User & Persona`
3. `## Success Criteria` (z `### Primary` / `### Secondary` / `### Guardrails`)
4. `## User Stories`
5. `## Functional Requirements`
6. `## Non-Functional Requirements`
7. `## Business Logic`
8. `## Access Control`
9. `## Non-Goals`
10. `## Open Questions`

**Brownfield (11 sekcji):**

Wygeneruj dokładnie te 11 nagłówków na poziomie `##`, w dokładnie tej kolejności:

1. `## Current System Overview` — co istnieje teraz: kluczowa architektura, tech stack, baza użytkowników. Ta sekcja nie ma odpowiednika greenfield; ustanawia linię bazową, względem której wszystkie kolejne sekcje opisują zmiany.
2. `## Problem Statement & Motivation` — co jest niepoprawne/brakuje, dlaczego teraz. Ujęte różnicowo: skupia się na luce między stanem obecnym a pożądanym.
3. `## User & Persona` — kogo dotyczy (istniejący użytkownicy + nowi, jeśli są). Dla brownfield podkreśl istniejących użytkowników, których doświadczenie się zmienia.
4. `## Success Criteria` (z `### Primary` / `### Secondary` / `### Guardrails`) — po czym wiemy, że zmiana zadziałała. Guardrails powinny jawnie obejmować istniejące zachowanie, które nie może ulec regresji.
5. `## User Stories` — co zmienia się dla użytkownika. Ujęte różnicowo: Given/When/Then opisuje nowe zachowanie, z jawnymi uwagami o tym, co wcześniej było inne.
6. `## Scope of Change` — co jest modyfikowane/dodawane/usuwane. Jawna różnica: sklasyfikuj każdy element jako `new`, `modified` lub `removed`. Zastępuje to domyślne założenie „wszystko jest nowe” z greenfield `## Functional Requirements`.
7. `## Constraints & Compatibility` — kompatybilność wsteczna, migracja danych, istniejące integracje, zachowane zachowanie. Sekcja specyficzna dla brownfield, która czyni zachowanie jawnym.
8. `## Business Logic Changes` — dodania/modyfikacje reguł domenowych (nie pełny model domenowy). Jeśli zmiana dotyczy wyłącznie infrastruktury (bez zmiany logiki domenowej), zaznacz to jawnie.
9. `## Access Control Changes` — zmiany uprawnień, jeśli występują. Jeśli nie ma zmian, podaj: „No access control changes.”
10. `## Non-Goals` — czego NIE zmieniamy. Kluczowe dla brownfield: jawnie wskazuje aspekty istniejącego systemu, które są poza zakresem.
11. `## Open Questions`

**NIE generuj** sekcji `## Data Model`, `## Data Model Changes`, `## Implementation Decisions`, `## Testing Strategy` ani `## Deployment & CI/CD` w żadnym trybie — te kwestie nie są częścią schematu PRD. Encje i ich cykle życia wynikają z FRs oraz User Stories i są ustalane podczas wyboru stacku / planowania implementacji, a nie w PRD. Jeśli notatki wejściowe zawierają treść modelu danych lub implementacji, podsumuj ją w komunikacie przekazania Kroku 5 pod „forward to technical-roadmap”, aby użytkownik wiedział, że jest kierowana dalej, a nie po cichu odrzucana — ale NIE generuj tych sekcji w PRD.

#### Zasady zawartości sekcji (oba tryby)

Dla każdej sekcji:

- **Jeśli dane wejściowe mają pasującą treść** — przepisz ją wiernie do sekcji. Zachowaj sformułowania użytkownika. Konwertuj formatowanie tylko wtedy, gdy schemat wymaga określonego kształtu (np. format FR-NNN, Given/When/Then dla historyjek użytkownika, trzy podsekcje Success Criteria). Nie parafrazuj, nie podsumowuj ani nie „ulepszaj” słów użytkownika.
- **Jeśli dane wejściowe mają częściową treść** — przepisz to, co jest, następnie zakończ `# TODO: <what's missing> — see Open Questions` wewnątrz sekcji i dodaj pasujący numerowany wpis w `## Open Questions`.
- **Jeśli dane wejściowe nie mają pasującej treści** — wygeneruj tylko nagłówek oraz `# TODO: <section name> — see Open Questions`, a następnie dodaj pasujący numerowany wpis w `## Open Questions`.

Jeśli `/raven-shape` zapisał cytaty blokowe Socrates pod FRs, zachowaj je dosłownie — są nośne dla dalszego przeglądu.

Jeśli shape-notes.md zawierał blok `## Quality cross-check` (z Kroku 7 `/raven-shape`), odzwierciedl każdą lukę w `## Open Questions` jako numerowany wpis wskazujący brakujący element i jego konsekwencję.

**Zasady treści specyficzne dla brownfield:**

- FRs z `Change: preserved` stają się jawnymi elementami zachowania w `## Scope of Change`, a nie `## Non-Goals`.
- `## Current System Overview` jest mapowane z sekcji `## Current System` w shape-notes.
- `## Constraints & Compatibility` jest mapowane z sekcji `## Constraints & Preserved Behavior` w shape-notes.
- Konwencja ujęcia różnicowego: sekcje opisują to, co się zmienia, a nie cały system. „The auth model adds Google OAuth alongside existing email login” — a nie „The system supports email login and Google OAuth.”

**Twarda zasada — nigdy nie wymyślaj**: odtwórz regułę z treści wejściowej niezależnie od liczby zdań i formatowania. Jeśli źródło jawnie uzasadnia brak reguły lub brak zmiany domenowej, zapisz to zgodnie ze schematem. Rzeczywisty brak potrzebnej decyzji oznacz `# TODO: domain rule — see Open Questions` z konkretnym pytaniem; nie ekstrapoluj reguł z nazw encji.

Ta sama zasada dotyczy: kryteriów sukcesu, historyjek użytkownika, priorytetów FR, celów NFR, kontroli dostępu, non-goals. Jeśli czegoś nie ma w danych wejściowych, trafia to do Open Questions.

#### 3c. Autoprzegląd przed zapisem

Przed jakimkolwiek zapisem na dysk wykonaj przejście autoprzeglądu względem listy wymaganych sekcji schematu ORAZ lint na poziomie treści pod kątem wycieku szczegółów technicznych:

**Kontrole strukturalne:**

1. Sparsuj zawartość PRD w pamięci. Wyodrębnij każdy nagłówek `## `.
2. Porównaj z kanoniczną listą sekcji dla aktywnego `context_type` (10 dla greenfield, 11 dla brownfield). Zweryfikuj, że WSZYSTKIE sekcje są obecne, w kolejności, z dokładną pisownią. PRD NIE może zawierać `## Data Model` ani `## Data Model Changes` — te sekcje zostały wycofane.
3. Zweryfikuj, że frontmatter deklaruje wszystkie wymagane klucze zgodnie ze schematem (`project`, `version`, `status`, `created`, `context_type`, `product_type`, `target_scale`, `timeline_budget`).
4. Zweryfikuj, że `## Success Criteria` zawiera podsekcje `### Primary`, `### Secondary`, `### Guardrails` (lub, jeśli ich brakuje, że są oznaczone jako TODO z odpowiadającymi wpisami Open Questions).

**Lint treści pod kątem wycieku technicznego:**

5. Przeskanuj treści wszystkich sekcji na poziomie `##` (z wyłączeniem brownfield `## Current System Overview`, gdzie nazwanie istniejącego stacku jest dozwolone) pod kątem tokenów wskazujących, że szczegóły implementacyjne przeniknęły do PRD. Każde trafienie oceń według znaczenia. Nazwa jest dozwolona, jeśli użytkownik wskazał produkt jako inspirację lub świadomie wymaganą integrację; oznacz tę rolę i źródło ustalenia. Inspiracja nie oznacza przejęcia całego zakresu, architektury ani wyboru bazy kodu. Nie przenoś zaakceptowanej inspiracji/integracji do Open Questions tylko z powodu nazwy. Pozostałe szczegóły implementacyjne traktuj jako wyciek; dosłowny cytat użytkownika skierowany do Open Questions może dokumentować nierozstrzygnięty wybór:

   - **Nazwy dostawców / usług hostowanych**: `OpenRouter`, `Stripe`, `Auth0`, `Supabase`, `Firebase`, `Vercel`, `Cloudflare`, `AWS`, `GCP`, `Azure`, `OpenAI`, `Anthropic` itd. (dowolny produkt/usługa będąca nazwą własną).
   - **Notacja schematu / ORM**: `(FK)`, `nullable`, przyrostki kolumn `_hash`, `_at` przedstawione jako listy pól, `password_hash`, `cascade`, `soft-delete`, `hard-delete`, `migration`, `backfill`.
   - **Lokalizacja wykonawcza**: `client-side`, `server-side`, `on the edge`, `in the cache`, `in the worker`.
   - **Mechanizm egzekwowania**: `per IP`, `per user-agent`, `token bucket`, `rate-limit per <axis>`.
   - **Element interfejsu** (gdy użyty do określenia NFR, a nie historyjki użytkownika): `spinner`, `progress bar`, `streaming response`, `modal`, `toast`.
   - **Transport / protokół**: `WebSocket`, `gRPC`, `GraphQL`, `REST endpoint`, `webhook`, `SSE`.
   - **Czasowniki implementacyjne w regułach domenowych**: „the LLM does X”, „the SRS library decides Y”, „the database stores Z” (nazwanie komponentu wykonującego regułę zamiast określenia samej reguły).

   Dla każdego trafienia wygeneruj ustrukturyzowane ostrzeżenie. NIE przepisuj po cichu — przerwij zapis, aby użytkownik mógł zobaczyć, co wyciekło.

Jeśli którakolwiek kontrola strukturalna LUB lint nie powiedzie się, **przerwij zapis** i zgłoś:

```
PRD generation self-review FAILED:

  Structural:
    - Missing section: <name>
    - Out-of-order section: <name> (expected position N, found position M)
    - Missing frontmatter key: <key>
    - Retired section present: <name>

  Technical leak (content lint):
    - <section name>: "<offending phrase>" — <category, e.g. vendor name / schema notation / runtime location>
    - ...

The PRD was NOT written. For structural failures: the schema and the generator
have drifted — re-read references/prd-schema.md and reconcile.
For leak failures: the input notes carry implementation detail that PRD does
not own. Either (a) rewrite the offending phrasings as outside-observable
properties / scope decisions and re-run, or (b) move the leaked content into
shape-notes' `## Forward: ...` blocks so a downstream skill consumes it.
```

Następnie ZATRZYMAJ SIĘ. Nie przechodź do Kroku 4.

Jeśli wszystkie kontrole przejdą pomyślnie, przejdź do Kroku 4 ze zweryfikowaną zawartością.

### Krok 4: Sprawdzenie kolizji

```bash
test -f context/foundation/prd.md
```

Jeśli plik nie istnieje, zapisz do `context/foundation/prd.md` i przejdź do Kroku 5.

Jeśli plik istnieje, zapytaj użytkownika:

**Kolizja** context/foundation/prd.md już istnieje. Jak chcesz kontynuować?

- **Zapisz jako prd-vN.md (Zalecane)**: Zachowaj historię. Nowy PRD trafi do następnego dostępnego slotu prd-vN.md. Niewersjonowany prd.md pozostanie bez zmian.
- **Nadpisz prd.md**: Zastąp istniejący prd.md. Poprzednia wersja zostanie utracona (chyba że została zatwierdzona).
- **Przerwij**: Zakończ bez zapisów. Bez rozstrzygnięcia kolizji.

Po wybraniu „Zapisz jako prd-vN.md”: wybierz `N`, skanując `context/foundation/` w poszukiwaniu plików pasujących do `prd-v*.md`. Traktuj niewersjonowany `prd.md` jako v1. Następny slot to `N = (max existing N or 1) + 1`. Zapisz zweryfikowaną zawartość do `context/foundation/prd-v<N>.md` i zwiększ pole frontmatter `version:` w treści do `<N>`. Przejdź do Kroku 5.

Po wybraniu „Nadpisz prd.md”: zapisz zweryfikowaną zawartość do `context/foundation/prd.md`. Zachowaj `version: 1` (nadpisanie jest zastąpieniem, a nie nową wersją). Przejdź do Kroku 5.

Po wybraniu „Przerwij”: ZATRZYMAJ SIĘ bez zapisów.

### Krok 5: Przekazanie dalej

Po zapisaniu podsumuj, co zostało utworzone:

```
═══════════════════════════════════════════════════════════
  PRD GENERATED
═══════════════════════════════════════════════════════════

  Project:          [project from frontmatter]
  Context type:     [greenfield | brownfield]
  Path:             [context/foundation/prd.md | context/foundation/prd-vN.md]
  Schema sections:  [10 / 10 | 11 / 11] present
  Frontmatter:      <K populated, M as TODO>  (8 keys total)
  Open Questions:   <count> entries

  Sections fully populated from input:
    - <list of section names with non-trivial content>

  Sections marked TODO (see Open Questions):
    - <list of section names with TODO placeholders>

═══════════════════════════════════════════════════════════
```

Wskaż następny etap zgodnie z raven-workflow i rzeczywistym stanem projektu: dla nowego produktu architektura → stack → instrukcje repo, strategia testów i CI → roadmapa → cykl change; dla brownfield zakres/wznowienie i rzeczywiste braki setupu przed planem. Nie uruchamiaj kolejnego etapu ani nie nadpisuj schowka. Przy pliku wersjonowanym przekaż jego dokładną ścieżkę; nie zakładaj, że konsumenci wybiorą go zamiast prd.md.

Jeśli notatki wejściowe zawierały przyszłościowe kwestie (preferencje tech-stack, notatki implementacyjne, wskazówki wdrożeniowe), wymień je krótko, aby użytkownik wiedział, że są kierowane do następnego kroku, a nie odrzucane:

```
  Forward to next step (not in PRD):
    • [one-line summary per detected item]
```

Pomiń cały blok, jeśli dane wejściowe nie zawierały żadnych z tych elementów.

ZATRZYMAJ SIĘ. Nie łącz automatycznie z inną umiejętnością.

## Krytyczne zabezpieczenia

1. **Generator, nie autor.** Ta umiejętność zapisuje całe pliki z danych wejściowych już zatwierdzonych przez użytkownika. Nie wymyśla logiki biznesowej, kryteriów sukcesu, historyjek użytkownika ani priorytetów FR. Brakująca treść trafia dosłownie do `## Open Questions`. Sekcja `## Business Logic` PRD jest obszarem najbardziej rygorystycznie kontrolowanym: odtwórz znaczenie reguł ze źródła albo udokumentowany brak ich zastosowania; rzeczywistą lukę oznacz TODO i Open Questions.

2. **Schemat jest kontraktem.** `references/prd-schema.md` definiuje klucze frontmatter, nazwy sekcji i kolejność sekcji. Czytaj go ponownie przy każdym wywołaniu. Ponownie waliduj PRD w pamięci względem niego w Kroku 3c przed zapisem. Dryf między tą umiejętnością a schematem jest trybem awarii, któremu ta umiejętność ma zapobiegać.

3. **Oddziel inspiracje i wymagane integracje od wyborów implementacyjnych.** Nazwy produktów wskazanych przez użytkownika jako inspiracje lub wymagane integracje są dozwolone w odpowiedniej istniejącej sekcji PRD, wraz z rolą i źródłem. Nie dodawaj nowej sekcji do schematu. Samo wskazanie inspiracji nie zatwierdza jej funkcji ani stacku. Poza tymi wyjątkami zabronione słownictwo w wygenerowanym PRD obejmuje siedem kategorii, nie tylko frameworki:

   - **Frameworki, bazy danych, platformy hostingowe, konkretne biblioteki** — pierwotna zasada.
   - **Nazwy dostawców / usług hostowanych** — OpenRouter, Stripe, Auth0, Supabase, Firebase, Vercel, Cloudflare, AWS/GCP/Azure, OpenAI, Anthropic i każdy inny produkt lub usługa będąca nazwą własną.
   - **Notacja schematu / ORM** — listy na poziomie pól, `(FK)`, `nullable`, kolumny `_hash`, `password_hash`, `cascade-delete`, `soft-delete`, `hard-delete`, `migration`, `backfill`. (Encje pojawiają się naturalnie w FRs i User Stories; schemat na poziomie kolumn jest kwestią dalszego etapu.)
   - **Lokalizacja wykonawcza** — `client-side`, `server-side`, `on the edge`, `in the cache`, `in the worker`. PRD opisuje, co musi być prawdą na zewnętrznej granicy produktu, a nie gdzie w stacku jest to egzekwowane.
   - **Mechanizm egzekwowania** — `per IP`, `per user-agent`, `token bucket`, `rate-limit per <axis>`. NFR jest właściwością; mechanizm to decyzja projektowa dalszego etapu.
   - **Element interfejsu w NFRs** — `spinner`, `progress bar`, `streaming response`, `modal`, `toast`. NFRs określają jakość obserwowalną dla użytkownika (np. „continuous feedback during long operations”); element interfejsu jest kwestią dalszego etapu.
   - **Transport / protokół** — `WebSocket`, `gRPC`, `GraphQL`, `REST endpoint`, `webhook`, `SSE`. PRD opisuje przepływ informacji tak, jak doświadcza go użytkownik, a nie format transmisji.

   Frontmatter PRD dotyczy wyłącznie poziomu produktu (`product_type`, `target_scale`, `timeline_budget` + metadane); rodzina języków, frameworki, wdrożenie, profil zespołu i wszelkie listy technologii do uniknięcia należą do dalszego kroku (zgodnie z raven-workflow), a NIE do PRD. Jeśli dane wejściowe zawierają szczegóły implementacyjne nieobjęte powyższym wyjątkiem inspiracji lub wymaganej integracji, pozostaw je w blokach `## Forward: ...` shape-notes do wykorzystania przez dalszy etap — NIE przenoś go do frontmatter ani sekcji PRD. Wyjątek: brownfield `## Current System Overview` może wymieniać istniejący stack i dostawców, ponieważ opisuje stan obecny, a nie wybór stacku. Kontrola treści Kroku 3c uwzględnia znaczenie nazwy i źródło decyzji, zamiast blokować zapis wyłącznie na podstawie słowa.

4. **Kolizje sprzyjają historii.** Monit o kolizji zaleca zapis wersjonowany (`prd-vN.md`) zamiast nadpisania. Utracone wcześniejsze wersje są nieodwracalnym trybem awarii; zduplikowany plik w `context/foundation/` nie jest.

5. **Autoprzegląd przerywa przy dryfie.** Jeśli PRD w pamięci nie ma sekcji, ma sekcję w złej kolejności lub brakuje w nim klucza frontmatter, zapis jest PRZERYWANY — a nie po cichu naprawiany. Błąd wskazuje konkretny dryf, aby opiekun mógł uzgodnić schemat i umiejętność.

6. **Wyłącznie uniwersalny język.** Bez brandingu autorów, kursów, społeczności i programów certyfikacyjnych w danych wyjściowych ani artefaktach zapisywanych na dysk. Ta umiejętność jest ogólnym generatorem PRD.

7. **Nigdy nie łącz automatycznie.** Przekazanie jest ogłoszeniem, a nie wywołaniem. Użytkownik wybiera, kiedy (i czy) uruchomić następny krok (zgodnie z raven-workflow). Automatyczne łączenie pominęłoby przegląd wygenerowanego PRD przez człowieka.

## Uwagi

- To jest umiejętność **generatora dokumentów**. Wynikiem jest `context/foundation/prd.md` (lub `prd-vN.md`), kropka.
- Referencja schematu (`references/prd-schema.md`) jest jedynym źródłem prawdy. Każda nazwa pola, nazwa sekcji lub klucz frontmatter wspomniany w tym tekście MUSI istnieć w dokumencie schematu — jeśli nie istnieje, najpierw popraw dokument schematu.
- Oceniaj kompletność treści semantycznie; zgłaszaj konkretne luki, nie brak wybranego formatowania.
- Wzorzec `# TODO: <field-name> — see Open Questions` jest nośny. Narzędzia dalszych etapów (umiejętności przeglądu, architektury i planowania Raven) mogą użyć grep dla `^# TODO: `, aby policzyć nierozstrzygnięte luki i zdecydować, czy PRD jest gotowy do przeglądu.