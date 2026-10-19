# Raven Workflow

[Model pracy](#model-pracy) · [Greenfield](#greenfield) · [Brownfield](#brownfield) · [Task](#task) · [Katalog](#katalog-skilli)

Skille Raven wywołujesz bezpośrednio. `raven-workflow` to opcjonalny tutorial uruchamiany wyłącznie ręcznie.

## Model pracy

Pracujemy na taskach w GitHub Issues, bez dodatkowej maszynerii procesu.

- **Issue** niesie wymagania biznesowe i kryteria odbioru. Jira, jeśli jest, zostaje źródłem wymagań; issue tylko ją linkuje.
- **Plan** (`context/changes/<id>/plan.md`) jest opcjonalnym, jednorazowym kontekstem roboczym agenta. Nie jest kontraktem: nie ma fingerprintu, checkpointów ani statusów. Nowe wymaganie trafia do issue albo polecenia.
- **Stan pracy** to issue, branch, commity i PR.
- **Drobna zmiana** (usunięcie przycisku, zmiana numeru telefonu) nie potrzebuje issue ani planu: `raven-auto-implement` z samym poleceniem.
- **Push, PR i merge** tylko na wyraźne polecenie.
- **Wyniki i instrukcja odbioru** trafiają do czatu, nie do raportów.

Zasady: [praca na taskach GitHub](skills/raven-workflow/references/git-workflow.md), [granice change](skills/raven-workflow/references/change-scope.md).

## Greenfield

```text
raven-shape         chaotyczny pomysł → uporządkowane notatki (shape-notes.md)
▼
raven-prd           wymagania i kryteria odbioru (prd.md)
▼
raven-architecture  decyzje przekrojowe (architecture.md)
▼
raven-init-stack LUB raven-medusa-ecommerce-init
▼
raven-md · raven-hooks · raven-github-setup   AGENTS.md, CI, repo i etykiety
▼
raven-roadmap       issues: wyniki, AC, zależności
▼
Task
```

## Brownfield

Mały znany task: od razu [Task](#task). W razie potrzeby wcześniej:

- `raven-repo-map`: nieznany obszar kodu;
- `raven-research`: konkretne pytania do kodu;
- `raven-domain-distillation`: rozbieżności języka domeny;
- `raven-architecture`: decyzje przekrojowe;
- `raven-md`, `raven-hooks`, `raven-github-setup`: tylko brakujący warsztat;
- `raven-roadmap`: kolejka z PRD albo ticketów Jira.

## Task

```text
issue (opcjonalnie)
▼
raven-plan (opcjonalnie)    plan jednego wyniku; review planu tylko na żądanie lub przy ryzyku
▼
raven-auto-implement        poziom weryfikacji wg ryzyka:
│                             quick     typecheck + istniejące testy
│                             standard  + działanie w uruchomionej aplikacji (domyślny)
│                             thorough  + baseline, testy obszaru, scenariusz błędu, 1 niezależne review
│                           finał w czacie: co zmieniono, co sprawdzono, ograniczenia, instrukcja odbioru
▼
ręczny odbiór → poprawki: raven-auto-implement z bieżącym poleceniem
▼
raven-pr                    push + PR z Closes #N
▼
raven-merge                 zielone CI dokładnego head → merge → issue zamknięty
```

Na żądanie lub przy ryzyku: `raven-implement-review` (wymagania, kod i testy), `raven-test` (trwałe testy, before-change), `raven-manual-qa` (eksploracyjne QA). Żaden z nich nie uruchamia się automatycznie.

## Katalog skilli

| Skill | Co robi | Testy | Wynik |
| --- | --- | --- | --- |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Przekrojowe decyzje architektoniczne na podstawie PRD i kodu. | Nie pisze; uwzględnia testowalność. | `context/foundation/architecture.md` |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Realizuje polecenie, opcjonalnie z issue lub planem; jeden agent. | **Tak:** wykorzystuje istniejące, dopisuje dla luk; `quick`/`standard`/`thorough`. | Commity (bez push/PR) i finał w czacie |
| [raven-browser](skills/raven-browser/SKILL.md) | Steruje przeglądarką (domyślnie osobna sesja Playwright CLI) dla innych skilli. | Scenariusze ad hoc; nie zastępuje trwałych E2E. | Obserwacje, screenshoty, logi |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Projektuje i zmienia skille Raven z niezależnym review. | Doctor, testy repo, forward-test zachowania. | Pakiet skilla w tym repo |
| [raven-domain-distillation](skills/raven-domain-distillation/SKILL.md) | Porównuje język dokumentów z modelem kodu. | Nie pisze. | `domain.md`, `glossary.md` |
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
| [raven-pr](skills/raven-pr/SKILL.md) | Push i utworzenie lub aktualizacja PR powiązanego z issue. | Nie uruchamia. | PR |
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

Doctor sprawdza frontmatter, nazwy, lokalne linki i [katalog](workflow-contract.json): każdy skill zarejestrowany i opisany w README, a wycofany nie wraca. Katalog nie zawiera etapów, bramek, ról ani modeli. Statyczny PASS nie dowodzi zachowania agenta; zmiany instrukcji sprawdzaj próbami na rzeczywistych wejściach. [Raven integrity](.github/workflows/integrity.yml) uruchamia te kontrole w CI.

</details>
