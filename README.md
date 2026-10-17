# Raven Workflow

[Greenfield](#greenfield) · [Brownfield](#brownfield) · [Realizacja taska — manual](#realizacja-taska--manual) · [Skróty auto](#skróty-auto)

Diagramy czytaj od góry. `JEŚLI` oznacza krok warunkowy, `LUB` — wybór jednego skilla. Zaczęty task wznawiaj od zapisanego etapu.

## Greenfield

```text
raven-workflow
Ustal punkt startowy i brakujące przygotowanie
│
▼
raven-shape
Uzgodnij problem, odbiorców i zakres produktu
│  zapis: context/foundation/shape-notes.md
▼
raven-prd
Zapisz wymagania i kryteria odbioru
│  zapis: context/foundation/prd.md
▼
raven-architecture
Ustal decyzje przekrojowe i ograniczenia
│  zapis: context/foundation/architecture.md
▼
raven-init-stack
LUB raven-medusa-ecommerce-init
Uruchom wybrany szkielet, bazę i środowisko
│
▼
raven-agents-md LUB raven-md
Zapisz instrukcje pracy agentów w AGENTS.md
│
▼
raven-test-plan
Ustal ryzyka, warstwy testów i sposób weryfikacji
│  zapis: context/foundation/test-plan.md
▼
raven-github-setup
Przygotuj repo GH, tracking i politykę publikacji
│  Issues: taski i stan projektu
│  Project: opcjonalny widok
▼
raven-hooks
Skonfiguruj CI: lint, typy i właściwe testy
│
▼
raven-roadmap
Utwórz issues: wyniki, AC, zależności i kolejność
│  bez planowania implementacji całego backlogu
▼
WYBIERZ ISSUE
Przejdź do diagramu „Realizacja taska — manual”
```

## Brownfield

```text
raven-workflow
Odczytaj wskazany issue, repo, branch i checkpoint
│
├─ Task już rozpoczęty?
│  Wróć do brakującego etapu realizacji taska.
│  Nie powtarzaj przygotowania projektu.
│
▼
JEŚLI obszar kodu jest nieznany
raven-repo-map
Rozpoznaj moduły, zależności i istniejące testy
│
▼
JEŚLI warsztat ma braki — uzupełnij tylko brakujące
├─ raven-agents-md LUB raven-md
│  Instrukcje agentów w AGENTS.md
├─ raven-test-plan
│  Strategia testowania i ryzyka
├─ raven-github-setup
│  Repo GH, tracking issues i polityka publikacji
└─ raven-hooks
   CI dla istniejącego stacku
│
▼
JEŚLI wymagania lub rozwiązanie są niejasne
├─ raven-frame
│  Oddziel objaw, przyczynę i proponowane rozwiązanie
├─ raven-research
│  Zbierz dowody z kodu dla konkretnych pytań
├─ raven-domain-distillation
│  Wyjaśnij rozbieżności modelu domeny
└─ raven-architecture
   Ustal potrzebne decyzje przekrojowe
│  Dobierz potrzebne narzędzia, nie wszystkie.
▼
JEŚLI zlecono utworzenie lub zmianę kolejki
raven-roadmap
LUB raven-jira-roadmap — dla wymagań z Jira
Ustal taski GH, ich zakres, zależności i kolejność
│  Jira: źródło wymagań; GH: tracking wykonania
▼
WYBIERZ ISSUE
Przejdź do diagramu „Realizacja taska — manual”
```

Dla znanego taska w przygotowanym repo przejdź bezpośrednio od `raven-workflow` do realizacji. Rozpoznanie będące częścią zleconego planowania odbywa się już po oznaczeniu issue jako In progress.

## Realizacja taska — manual

Wspólna ścieżka dla greenfield i brownfield. Jeden issue = jeden change. Plan, plan testów i checkpoint są w `context/changes/<id>/plan.md` na branchu; domyślnie bez dodatkowego worktree.

```text
raven-plan
Najpierw: issue → In progress + wykonawca
Potem: wymagania, plan implementacji i plan testów
│  zapis: plan.md; bez implementacji
│
├─ raven-pr — JEŚLI publikacja jest autoryzowana
│  Utwórz wczesny draft: link do issue i planu.
│  Aktualizuj ten sam PR w trakcie pracy.
│
▼
raven-plan-review
Niezależnie sprawdź zakres, wykonalność i testy
│
├─ Uwagi blokujące → raven-plan → ponowne review
│  Zmiany zakresu wymagają decyzji użytkownika.
│
▼
UŻYTKOWNIK: zaakceptuj konkretną wersję planu
│  review agenta nie zastępuje tej decyzji
▼
raven-implement
Wykonaj zatwierdzony plan wraz z testami
│  zapis: kod, testy, postęp i dowody w planie
│
├─ Zmiana kontraktu → plan → review → akceptacja
│  Zwykłe poprawki w zakresie nie restartują planu.
│
▼
raven-implement-review
Niezależnie oceń wymagania, kod i skuteczność testów
│
├─ Defekty → raven-implement → ponowne review
│  Naprawy i ponowna ocena dotyczą zmienionego zakresu.
│
▼
raven-pr
Zaktualizuj istniejący PR lub opublikuj nowy
│  publikacja w zakresie zgody; CI sprawdza wersję PR
▼
JEŚLI potrzebne dodatkowe QA
raven-manual-qa
Sprawdź działającą funkcję i zapisz defekty
│  bez automatycznego poprawiania produktu
│  defekty wracają do implementacji i review
▼
UŻYTKOWNIK: odbierz wynik i zleć merge
CI: wszystkie wymagane kontrole muszą przejść
│  issue nadal In progress
▼
raven-merge
Zweryfikuj bramki i zmerguj sprawdzony PR
│
├─ Merge niepotwierdzony → nie zamykaj issue
├─ Merge OK, zapis issue zawiódł
│  Wznów tylko finalizację issue, bez ponownego merge.
│
▼
ISSUE → DONE
Dopiero po potwierdzonym merge
│
▼
Następny issue → raven-plan
Deploy wymaga osobnego zlecenia.
```

Blokada na dowolnym etapie: issue pozostaje otwarte, otrzymuje `blocked` i krótki powód. Po rozwiązaniu blokady kontynuuj od checkpointu. Dwie nieskuteczne próby naprawy tego samego problemu zatrzymują pętlę.

## Skróty auto

Auto zastępuje wybrane wywołania manualne; nie usuwa decyzji użytkownika ani bramek merge.

```text
raven-auto-plan
└─ raven-plan → raven-plan-review → poprawki
   ↓
   Akceptacja użytkownika

raven-auto-implement
└─ raven-implement → raven-implement-review → poprawki
   ↓
   Odbiór użytkownika + CI → raven-merge
```

## Osobne zadanie testowe

Zwykły task tworzy testy podczas `raven-implement`. Poniższa ścieżka dotyczy osobno zleconych testów lub ochrony przed zmianą.

```text
Issue testowe → In progress + wykonawca
│
▼
raven-test
Dodaj testy, reprodukcję błędu lub ochronę refaktoru
│
▼
raven-test-review
Niezależnie oceń skuteczność ochrony
│  uwagi → raven-test → ponowne review
▼
raven-pr → odbiór + CI → raven-merge → issue Done

Skrót: raven-auto-test
Zawiera wykonanie, review i poprawki w zakresie.
```

---

<details>
<summary>Katalog skilli i odnośniki</summary>

## Katalog skilli

| Skill | Zastosowanie |
| --- | --- |
| [raven-agents-md](skills/raven-agents-md/SKILL.md) | Onboarding AGENTS.md z rzeczywistego repo. |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Przekrojowe decyzje architektoniczne. |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Implementacja, testy, jedno review i naprawy w zakresie. |
| [raven-auto-plan](skills/raven-auto-plan/SKILL.md) | Plan i niezależne review do decyzji użytkownika. |
| [raven-auto-test](skills/raven-auto-test/SKILL.md) | Osobne zlecenie testów z niezależnym review i naprawami. |
| [raven-browser](skills/raven-browser/SKILL.md) | Osobna sesja Playwright CLI, zasady dostępu do przeglądarki. |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Projektowanie i spójna aktualizacja rodziny Raven. |
| [raven-domain-distillation](skills/raven-domain-distillation/SKILL.md) | Niezależne porównanie języka dokumentów i kodu. |
| [raven-frame](skills/raven-frame/SKILL.md) | Oddzielenie obserwacji od założonej przyczyny. |
| [raven-github-setup](skills/raven-github-setup/SKILL.md) | Remote, wymagany tracking issues i polityka publikacji; Project opcjonalny. |
| [raven-hooks](skills/raven-hooks/SKILL.md) | GitHub Actions dla rzeczywistych kontroli projektu. |
| [raven-implement](skills/raven-implement/SKILL.md) | Realizacja planu wraz z testami. |
| [raven-implement-review](skills/raven-implement-review/SKILL.md) | Jedno review wymagań, kodu i testów. |
| [raven-init-stack](skills/raven-init-stack/SKILL.md) | Better T Stack i lokalna baza. |
| [raven-jira-roadmap](skills/raven-jira-roadmap/SKILL.md) | Jira jako źródło wymagań, issue GH jako tracking wykonania bez kopiowania treści. |
| [raven-lesson](skills/raven-lesson/SKILL.md) | Zapis jednej uzgodnionej powtarzalnej reguły. |
| [raven-manual-qa](skills/raven-manual-qa/SKILL.md) | Dodatkowa eksploracja UI i potwierdzone reprodukcje. |
| [raven-md](skills/raven-md/SKILL.md) | Tworzenie lub aktualizacja wskazanych instrukcji. |
| [raven-medusa-ecommerce-init](skills/raven-medusa-ecommerce-init/SKILL.md) | Medusa + Next.js: lokalne monorepo i środowisko. |
| [raven-merge](skills/raven-merge/SKILL.md) | Merge sprawdzonego PR, potem zweryfikowane zamknięcie jego issue. |
| [raven-plan](skills/raven-plan/SKILL.md) | Manualne przygotowanie lokalnego planu. |
| [raven-plan-review](skills/raven-plan-review/SKILL.md) | Niezależna ocena wykonalności i granic planu. |
| [raven-pr](skills/raven-pr/SKILL.md) | Wczesny draft lub aktualizacja PR, logiczne commity i zwykły push. |
| [raven-prd](skills/raven-prd/SKILL.md) | Wymagania produktu z notatek i decyzji. |
| [raven-repo-map](skills/raven-repo-map/SKILL.md) | Mapa nieznanego repo, zależności i ryzyk. |
| [raven-research](skills/raven-research/SKILL.md) | Ograniczone badanie kodu i lokalny raport dowodów. |
| [raven-roadmap](skills/raven-roadmap/SKILL.md) | Kolejność samodzielnych changes i zależności w GitHub Issues. |
| [raven-rule-review](skills/raven-rule-review/SKILL.md) | Ocena jakości instrukcji AI. |
| [raven-shape](skills/raven-shape/SKILL.md) | Dopracowanie problemu i zakresu produktu. |
| [raven-test](skills/raven-test/SKILL.md) | Osobne testy, before-change lub uzupełnienie ochrony. |
| [raven-test-plan](skills/raven-test-plan/SKILL.md) | Strategia testów, ryzyka i cookbook w repo. |
| [raven-test-review](skills/raven-test-review/SKILL.md) | Ocena konkretnych testów na zlecenie lub według ryzyka. |
| [raven-workflow](skills/raven-workflow/SKILL.md) | Router, status i wznowienie z repo. |


</details>

<details>
<summary>Instalacja i utrzymanie</summary>

## Instalacja, doctor i rozwój

Repo jest źródłem dystrybucji. Python 3.10+ i środowisko lokalne:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/raven.py doctor
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/raven.py sync --to "$HOME/.codex/skills"
# Po przejrzeniu pełnego diffu i w zakresie zgody na instalację:
.venv/bin/python tools/raven.py sync --to "$HOME/.codex/skills" --apply
.venv/bin/python tools/raven.py doctor --installed "$HOME/.codex/skills"
```

Sync obejmuje zarejestrowaną rodzinę Raven, nie inne skille. Tworzy backup dotkniętych katalogów, usuwa nieaktualne pliki tych skilli i wycofane raven-pilot-* / raven-seed. Nie zmienia globalnego AGENTS.md. Przejrzyj różnice i nie nadpisuj niezwiązanych lokalnych modyfikacji; sync nie jest automatycznym scaleniem. Symlinki i kolizje plik/katalog wymagają uporządkowania przed zapisem. Instalacja nie potwierdza odświeżenia katalogu aktywnego UI.

W globalnych instrukcjach wskaż: przy pracy Raven najpierw czytaj raven-workflow, następnie tylko skille potrzebne do zadania. Rozwijając skille, użyj raven-create-skill i dostępnego hostowi skill-creator; nie instaluj ani nie publikuj zmian bez objęcia tego zleceniem.

Doctor sprawdza frontmatter, nazwy, lokalne odsyłacze, katalog, politykę ról i [kontrakt](workflow-contract.json), a `--installed` również zgodność instalacji. `doctor --json` daje raport maszynowy. Kontrakt deklaruje zależności, nie wykonuje workflow: `initial_artifacts` to wymagane zewnętrzne dowody/decyzje, nie fikcyjne zgody. PR jest operacją boczną i nie blokuje lokalnej implementacji. Opcjonalne dodatkowe QA/testy są poza standardowym cyklem; tracking issues jest wymagany, Project pozostaje widokiem.

Statyczny PASS nie dowodzi zachowania agenta ani prawdziwych uprawnień, CI i gotowości aplikacji. Zmiany instrukcji wymagają właściwych testów i niezależnych prób na rzeczywistych wejściach. Workflow [Raven integrity](.github/workflows/integrity.yml) uruchamia kontrole repo; sam YAML nie ustanawia required checks w GitHubie.

</details>
