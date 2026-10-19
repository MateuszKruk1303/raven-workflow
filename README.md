# Raven Workflow

[Model pracy](#model-pracy) · [Greenfield](#greenfield) · [Brownfield](#brownfield) · [Wzorce pracy](#wzorce-pracy) · [Po który skill sięgnąć](#skille-raven--po-który-sięgnąć-i-kiedy) · [Katalog](#katalog-skilli)

Skille Raven wywołujesz bezpośrednio. `raven-workflow` to opcjonalny tutorial uruchamiany wyłącznie ręcznie.

## Model pracy

Pracujemy na taskach w GitHub Issues, bez dodatkowej maszynerii procesu.

- **Issue** niesie wymagania biznesowe i kryteria odbioru. Jira, jeśli jest, zostaje źródłem wymagań; issue tylko ją linkuje.
- **Plan** (`context/changes/<id>/plan.md`) jest opcjonalnym, jednorazowym kontekstem roboczym agenta. Nie jest kontraktem: nie ma fingerprintu, checkpointów ani statusów. Nowe wymaganie trafia do issue albo polecenia.
- **Stan pracy** to issue, branch, commity i PR.
- **Drobna zmiana** (usunięcie przycisku, zmiana numeru telefonu) nie potrzebuje issue ani planu: `raven-auto-implement` z samym poleceniem.
- **Push, PR i merge** tylko na wyraźne polecenie.
- **Wyniki i instrukcja odbioru** trafiają do czatu, nie do raportów. PR dostaje krótką sekcję „Weryfikacja”: co faktycznie sprawdzono i czego nie.

Zasady: [praca na taskach GitHub](skills/raven-workflow/references/git-workflow.md), [granice change](skills/raven-workflow/references/change-scope.md).

## Greenfield

Nowy produkt od pomysłu do pierwszego taska. Każdy krok zapisuje jeden dokument, z którego korzysta następny.

```text
raven-shape          chaotyczny pomysł, notatki, rozmowy → uporządkowany problem, odbiorcy, MVP, reguły
│                    context/foundation/shape-notes.md
▼
raven-prd            wymagania i kryteria odbioru
│                    context/foundation/prd.md
▼
raven-architecture   decyzje przekrojowe: dane, integracje, auth, granice modułów
│                    context/foundation/architecture.md
▼
raven-init-stack     szkielet Better T Stack + lokalny Postgres
LUB raven-medusa-ecommerce-init   sklep Medusa + Next.js
▼
raven-md             AGENTS.md z faktycznych komend i konwencji
raven-github-setup   repo, Issues, etykiety in-progress/blocked
raven-hooks          CI: lint, typecheck, testy po PR
▼
raven-roadmap        PRD → issues: wyniki, AC, zależności, kolejność
▼
pierwszy issue → wzorzec „Task z issue”
```

## Brownfield

Istniejący projekt. Dobierz tylko to, czego brakuje; mały znany task nie wymaga niczego z poniższych.

```text
Nieznany kod?                    raven-repo-map            mapa obszarów, zależności, historii, ryzyk
Konkretne pytanie do kodu?       raven-research            odpowiedź z dowodami path:line
Decyzja przekrojowa?             raven-architecture        architecture.md
Brak AGENTS.md / CI / etykiet?   raven-md · raven-hooks · raven-github-setup
Słabe AGENTS.md?                 raven-md (tryb review)    karta wyników, bez przepisywania
Kolejka z PRD lub Jiry?          raven-roadmap             issues linkujące źródło
Refaktor bez testów?             raven-test (before-change) przed zmianą
▼
wzorzec pracy poniżej
```

## Wzorce pracy

### Zmiana z doskoku

Drobna rzecz bez issue i planu: copy, styl, usunięcie elementu, config.

```text
raven-auto-implement — usuń numer telefonu ze stopki
```

Agent zwykle wybiera `quick`, robi commit na krótkim branchu (nigdy na domyślnym) i podaje w czacie, jak sprawdzić efekt. Push, PR i merge zlecasz osobno, jeśli chcesz.

### Task z issue

Typowa funkcja lub poprawka.

```text
raven-plan #42              (opcjonalnie) plan w realnym kodzie; review planu na żądanie
raven-auto-implement #42    implementacja + weryfikacja (domyślnie standard)
  ↳ ręczny odbiór według instrukcji z czatu
  ↳ problem? raven-auto-implement #42 — <co nie działa>
raven-pr #42                push + PR z Closes #42
raven-merge #42             zielone CI → merge → issue zamknięty
```

Plan pomijasz, gdy issue i polecenie wystarczą. Nowe wymaganie w trakcie pracy dopisujesz do polecenia albo przez `raven-issue-update`; planu nie aktualizujesz.

### Ryzykowna zmiana

Gdy błąd byłby kosztowny, trudny do odwrócenia lub trudny do zauważenia przed użytkownikiem.

```text
raven-plan #57 — z review         świeży agent ocenia plan, jedna runda poprawek
raven-auto-implement #57          agent sam wybierze thorough albo powiesz: „thorough”
raven-implement-review #57        (opcjonalnie) niezależne review całego change przed PR
raven-pr → raven-merge
```

`thorough` dokłada baseline testów, testy całego obszaru, ścieżkę end-to-end ze scenariuszem błędu i jedno niezależne review.

### Bugfix

```text
raven-test — reprodukcja: <opis błędu>     (opcjonalnie) test EXPECTED_RED na obecnym kodzie
raven-auto-implement — napraw <błąd>       poprawka; test przechodzi na zielono
```

Przy prostym błędzie wystarczy samo `raven-auto-implement`: jeśli brakuje testu na naprawione zachowanie, dopisze go sam.

### Refaktor

```text
raven-test — before-change <moduł>         testy charakteryzacyjne obecnego zachowania
raven-auto-implement — refaktor <moduł>    zmiana przy zielonych testach
```

### Kontrola jakości na żądanie

```text
raven-implement-review <branch/PR>   wymagania, poprawność, bezpieczeństwo, skuteczność testów
raven-test <change>                  mapa AC → test, tylko brakujące testy
raven-manual-qa <issue/PR>           eksploracja w przeglądarce, defekty z reprodukcją
```

Żaden z nich nie uruchamia się automatycznie i żaden nie jest warunkiem PR.

### Jira w zespole

```text
raven-roadmap — PROJ-120..PROJ-128   issues GH linkujące tickety, bez kopiowania i zapisów do Jiry
```

Dalej wzorzec „Task z issue”. Wymagania zostają w Jirze, wykonanie śledzisz w GitHub.

## Skille Raven — po który sięgnąć i kiedy

Instalacja w projekcie: `npx skills add MateuszKruk1303/raven-workflow`, aktualizacja: `npx skills update -p -y`.

Skille są ułożone w kolejności, w jakiej zwykle pojawiają się w pracy. Żaden etap nie jest obowiązkowy — drobną zmianę zrobisz samym `raven-auto-implement`.

| Etap | Kiedy sięgasz | Skill | Co dostajesz |
| --- | --- | --- | --- |
| **0. Zgubiłem się** | _„Nie wiem, gdzie jestem i co dalej.”_ | [`raven-workflow`](skills/raven-workflow/SKILL.md) | Etap pracy z issue, brancha, commitów i PR oraz następny skill. Niczego nie zmienia. |
| **1. Mam pomysł** | _„Mam pomysł, ale jest jeszcze mglisty.”_ | [`raven-shape`](skills/raven-shape/SKILL.md) | Problem, odbiorcy, MVP i reguły w `shape-notes.md`. Rozmowę można wznowić. |
| | _„Wiem, czego chcę — niech to będzie porządny dokument.”_ | [`raven-prd`](skills/raven-prd/SKILL.md) | `context/foundation/prd.md`: wymagania, zakres, wyłączenia. |
| **2. Stawiam fundamenty** | _„Chcę podjąć duże decyzje świadomie.”_ | [`raven-architecture`](skills/raven-architecture/SKILL.md) | Opcje z kompromisami i rekomendacją w `context/foundation/architecture.md`. |
| | _„Chcę działający szkielet bez ręcznego klejenia.”_ | [`raven-init-stack`](skills/raven-init-stack/SKILL.md) | Better T Stack + lokalny Postgres; decyzje w `tech-stack.md`. |
| | _„Robię sklep na Medusie i ma ruszyć lokalnie.”_ | [`raven-medusa-ecommerce-init`](skills/raven-medusa-ecommerce-init/SKILL.md) | Monorepo Medusa + Next.js: migracje, seed, admin, storefront. |
| | _„Agent gubi się w repo albo łamie konwencje.”_ | [`raven-md`](skills/raven-md/SKILL.md) | `AGENTS.md` z faktów repo albo karta wyników (tryb review). |
| | _„Nie chcę pamiętać o lincie i testach przed merge.”_ | [`raven-hooks`](skills/raven-hooks/SKILL.md) | GitHub Actions: lint, typecheck, testy po PR. |
| | _„Chcę pracować na taskach w GitHubie.”_ | [`raven-github-setup`](skills/raven-github-setup/SKILL.md) | Remote, Issues, etykiety `in-progress`/`blocked`; Project na zlecenie. |
| **3. Układam kolejkę** | _„Mam PRD i nie wiem, od czego zacząć.”_ | [`raven-roadmap`](skills/raven-roadmap/SKILL.md) | Małe changes jako GitHub Issues w kolejności; źródło: PRD lub Jira. |
| | _„Przypomniało mi się jeszcze jedno wymaganie.”_ | [`raven-issue-update`](skills/raven-issue-update/SKILL.md) | Wymaganie wplecione w treść i AC istniejącego issue. |
| **4. Wchodzę w nieznany kod** | _„Dostałem cudze repo i nie wiem, co gdzie jest.”_ | [`raven-repo-map`](skills/raven-repo-map/SKILL.md) | Obszary, zależności, historia, ryzyka — raport z dowodami. |
| | _„Muszę wiedzieć, jak to naprawdę działa.”_ | [`raven-research`](skills/raven-research/SKILL.md) | Odpowiedź z dowodami, opcje i luki w `context/changes/<id>/research.md`. |
| **5. Robię change** | _„Task jest ryzykowny, agent nie może strzelać.”_ | [`raven-plan`](skills/raven-plan/SKILL.md) | Plan jednego change w realnym kodzie; review planu na żądanie. |
| | _„Po prostu to zrób — i udowodnij, że działa.”_ | [`raven-auto-implement`](skills/raven-auto-implement/SKILL.md) | Commity, weryfikacja `quick`/`standard`/`thorough`, instrukcja odbioru w czacie. |
| | _„Chcę zobaczyć to w przeglądarce.”_ | [`raven-browser`](skills/raven-browser/SKILL.md) | Izolowana sesja Playwright dla innych skilli; Brave tylko na polecenie. |
| | _„Niech ktoś spróbuje to zepsuć.”_ | [`raven-manual-qa`](skills/raven-manual-qa/SKILL.md) | Eksploracja w UI, defekty z reprodukcją w czacie. Niczego nie naprawia. |
| | _„Chcę drugiej pary oczu na ten kod.”_ | [`raven-implement-review`](skills/raven-implement-review/SKILL.md) | Read-only review: wymagania, poprawność, skuteczność testów. |
| | _„Nie chcę, żeby to się po cichu zepsuło.”_ | [`raven-test`](skills/raven-test/SKILL.md) | Tylko brakujące testy; before-change przed refaktorem. |
| **6. Oddaję pracę** | _„Jestem zadowolony — wystawiam to.”_ | [`raven-pr`](skills/raven-pr/SKILL.md) | Push i PR powiązany z issue, z sekcją „Weryfikacja”; bez merge. |
| | _„CI zielone, akceptuję — zamykamy.”_ | [`raven-merge`](skills/raven-merge/SKILL.md) | Merge po zielonym CI i Twojej zgodzie, zamknięty issue. |
| **7. Uczę się na błędach** | _„Znowu ten sam błąd.”_ | [`raven-lesson`](skills/raven-lesson/SKILL.md) | Jedna reguła w `context/foundation/lessons.md`, czytana przez kolejne skille. |
| | _„Brakuje mi narzędzia w Raven.”_ | [`raven-create-skill`](skills/raven-create-skill/SKILL.md) | Nowy lub zmieniony skill Raven z walidacją. |

## Katalog skilli

| Skill | Co robi | Testy | Wynik |
| --- | --- | --- | --- |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Przekrojowe decyzje architektoniczne na podstawie PRD i kodu. | Nie pisze; uwzględnia testowalność. | `context/foundation/architecture.md` |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Realizuje polecenie, opcjonalnie z issue lub planem; jeden agent. | **Tak:** wykorzystuje istniejące, dopisuje dla luk; `quick`/`standard`/`thorough`. | Commity (bez push/PR) i finał w czacie |
| [raven-browser](skills/raven-browser/SKILL.md) | Steruje przeglądarką (domyślnie osobna sesja Playwright CLI) dla innych skilli. | Scenariusze ad hoc; nie zastępuje trwałych E2E. | Obserwacje, screenshoty, logi |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Projektuje i zmienia skille Raven z niezależnym review. | Doctor, testy repo, forward-test zachowania. | Pakiet skilla w tym repo |
| [raven-github-setup](skills/raven-github-setup/SKILL.md) | Repo, włączone Issues, etykiety in-progress/blocked; Project na zlecenie. | Nie dotyczy. | Konfiguracja GitHub |
| [raven-hooks](skills/raven-hooks/SKILL.md) | GitHub Actions: lint, typecheck i właściwe testy po PR. | Uruchamia w CI; nie pisze testów produktu. | Pliki workflow CI |
| [raven-implement-review](skills/raven-implement-review/SKILL.md) | Świeży reviewer: wymagania, poprawność, architektura, bezpieczeństwo, skuteczność testów. | Ocenia; nie poprawia. | Uwagi i werdykt w czacie |
| [raven-init-stack](skills/raven-init-stack/SKILL.md) | Better T Stack, lokalny Postgres, env. | Sprawdza setup i typy. | Szkielet aplikacji, `tech-stack.md` |
| [raven-issue-update](skills/raven-issue-update/SKILL.md) | Wplata wymaganie w zakres i AC istniejącego issue. | Nie dotyczy; readback zapisu. | Zaktualizowany body issue |
| [raven-lesson](skills/raven-lesson/SKILL.md) | Utrwala powtarzalną regułę projektu na zlecenie. | Nie pisze. | `context/foundation/lessons.md` |
| [raven-manual-qa](skills/raven-manual-qa/SKILL.md) | Eksploracyjne QA działającej funkcji w przeglądarce. | Nie pisze i nie naprawia. | Defekty z reprodukcją w czacie |
| [raven-md](skills/raven-md/SKILL.md) | Tworzy, aktualizuje lub ocenia AGENTS.md na podstawie faktów z repo. | Nie pisze. | `AGENTS.md` albo karta wyników |
| [raven-medusa-ecommerce-init](skills/raven-medusa-ecommerce-init/SKILL.md) | Lokalny starter Medusa + Next.js: baza, Redis, migracje, seed, admin, storefront. | Sprawdza start i podstawowy przepływ zakupu. | Działające lokalne monorepo |
| [raven-merge](skills/raven-merge/SKILL.md) | Merge po zielonym CI dokładnego head, potem zamknięcie issue. | Czyta wynik CI. | Zmergowany PR, zamknięty issue |
| [raven-plan](skills/raven-plan/SKILL.md) | Plan jednego wyniku w realnym kodzie; opcjonalne review planu przez świeżego agenta. | Planuje; nie pisze. | `context/changes/<id>/plan.md` |
| [raven-pr](skills/raven-pr/SKILL.md) | Push i utworzenie lub aktualizacja PR powiązanego z issue, z sekcją „Weryfikacja”. | Nie uruchamia; opisuje faktycznie wykonane kontrole. | PR |
| [raven-prd](skills/raven-prd/SKILL.md) | PRD z notatek shape lub surowych ustaleń. | Nie pisze; definiuje zachowania do weryfikacji. | `context/foundation/prd.md` |
| [raven-repo-map](skills/raven-repo-map/SKILL.md) | Mapa istniejącego repo: obszary, zależności, historia, ryzyka. | Nie pisze. | `context/foundation/repo-map.md` |
| [raven-research](skills/raven-research/SKILL.md) | Odpowiedzi na konkretne pytania o kod lub wykonalność, z dowodami. | Uruchamia tylko, gdy odpowiada to na pytanie. | `research.md` |
| [raven-roadmap](skills/raven-roadmap/SKILL.md) | Kolejka changes jako GitHub Issues, z PRD albo Jira. | Nie pisze. | Issues z AC i zależnościami |
| [raven-shape](skills/raven-shape/SKILL.md) | Rozmowa porządkująca chaotyczny pomysł: problem, odbiorcy, MVP, reguły. | Nie pisze. | `context/foundation/shape-notes.md` |
| [raven-test](skills/raven-test/SKILL.md) | Trwała ochrona testami: mapa AC → test, tylko brakujące testy, before-change. | **Tak:** tylko dla nazwanych luk. | Testy w repo, mapa w czacie |
| [raven-workflow](skills/raven-workflow/SKILL.md) | Ręczny tutorial: model pracy i mapa skilli. | Nie dotyczy. | Objaśnienie w rozmowie |

<details>
<summary>Instalacja i utrzymanie</summary>

Repo jest źródłem dystrybucji. Python 3.10+:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/raven.py doctor
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/raven.py sync --to <katalog-skilli>          # podgląd
.venv/bin/python tools/raven.py sync --to <katalog-skilli> --apply  # zapis z backupem
.venv/bin/python tools/raven.py doctor --installed <katalog-skilli>
```

Sync obejmuje tylko rodzinę Raven. Robi backup dotkniętych katalogów, usuwa nieaktualne pliki i wycofane skille. Przejrzyj podgląd, bo sync nadpisuje lokalne modyfikacje skilli Raven.

Doctor sprawdza frontmatter, nazwy, lokalne linki i [katalog](workflow-contract.json): każdy skill zarejestrowany i opisany w README, a wycofany nie wraca — ani jako katalog, ani jako wzmianka lub artefakt w treści skilli (lista w `tools/raven.py`). Katalog nie zawiera etapów, bramek, ról ani modeli. Statyczny PASS nie dowodzi zachowania agenta; zmiany instrukcji sprawdzaj próbami na rzeczywistych wejściach. [Raven integrity](.github/workflows/integrity.yml) uruchamia te kontrole w CI.

</details>
