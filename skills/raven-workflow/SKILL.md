---
name: raven-workflow
description: "Ręcznie wywoływany tutorial i wprowadzenie do Raven. Objaśnij etapy, stan wskazanej pracy i możliwy następny skill; nie jest automatycznym routerem ani obowiązkowym krokiem."
---

# Raven Workflow

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Wywołuj wyłącznie na wyraźne ręczne polecenie użytkownika jako tutorial, wprowadzenie i podpowiedzi. Samo użycie innego raven-*, pytanie o gotowość lub wznowienie nie uruchamia tego skilla. Instrukcje potrzebnego etapu i wspólne referencje czytaj bezpośrednio; nie uruchamiaj etapów podczas tutorialu. Stan taska i roadmapy pochodzi z GitHub Issues, szczegóły wykonania z planu i bieżących dowodów, nie z pamięci rozmowy.

## Start i wznowienie

1. Przeczytaj instrukcje repo. Rozwiąż jawny issue/change ID, ścieżkę `plan.md`, branch albo PR; nie wybieraj najnowszego z kilku kandydatów.
2. Odczytaj plan/checkpoint, aktualny branch/HEAD i dirty state. Konfiguracja `.raven/config.json` jest opcjonalna. `context/foundation/github.json` może wskazywać historyczne źródło; nie migruj go automatycznie.
3. Odczytaj dokładny powiązany issue (stan i assignee), bez skanowania boarda. Sprawdź fingerprint i aktualne review planu, następny krok oraz aktualność wskazanych dowodów. Dla PR pobierz tylko jego bieżące dane, wymagane checki i konkretne nierozwiązane wątki. Pełna historia komentarzy/task issues nie jest wymagana.
4. Objaśnij stan, istotną lukę i pasujący następny skill. Tutorial i status są read-only; nie podejmuj issue i nie uruchamiaj z nich kolejnych etapów. Jeśli użytkownik osobno zleca wykonanie, stosuj bezpośrednio instrukcje wybranego skilla i zachowane decyzje.

Ograniczone deterministyczne operacje opisuje [runtime](references/runtime.md); helper nie interpretuje wymagań ani nie zleca wykonania.

## Przygotowanie projektu

**Greenfield:** [shape](../raven-shape/SKILL.md) → [PRD](../raven-prd/SKILL.md) → [architektura](../raven-architecture/SKILL.md) → [stack](../raven-init-stack/SKILL.md) lub [Medusa](../raven-medusa-ecommerce-init/SKILL.md) → [instrukcje repo](../raven-agents-md/SKILL.md) / [wskazany AGENTS.md](../raven-md/SKILL.md), [strategia testów](../raven-test-plan/SKILL.md), [CI](../raven-hooks/SKILL.md) → [roadmapa](../raven-roadmap/SKILL.md) → change. Nie odtwarzaj gotowego setupu. [GitHub setup](../raven-github-setup/SKILL.md) uzupełnia potrzebny remote, tracking issues i politykę publikacji; Project nie jest warunkiem.

**Brownfield:** zakres/wznowienie → opcjonalna [mapa](../raven-repo-map/SKILL.md) przy nieznanym obszarze → realne braki instrukcji/test strategy/CI → opcjonalne [frame](../raven-frame/SKILL.md), [research](../raven-research/SKILL.md), [domena](../raven-domain-distillation/SKILL.md) lub [architektura](../raven-architecture/SKILL.md) → plan. Mały znany task nie wymaga mapy ani setupu boarda. [Jira](../raven-jira-roadmap/SKILL.md) pozostaje źródłem wymagań, a issue GH śledzi wykonanie przez link, bez kopiowania treści ticketu.

## Cykl change

Poniżej możliwa kolejność osobnych zleceń. Samodzielne `raven-auto-implement` wymaga tylko wskazanego planu i aktualnego polecenia; nie uzależnia wykonania od review planu, fingerprintu, GitHuba ani checkpointów i nie uruchamia kolejnych etapów.

| Etap | Wykonanie i wynik |
| --- | --- |
| Plan | [raven-plan](../raven-plan/SKILL.md) + [raven-plan-review](../raven-plan-review/SKILL.md) albo [raven-auto-plan](../raven-auto-plan/SKILL.md); gotowy plan i aktualne review wskazują raven-auto-implement jako następny krok |
| Implementacja | [raven-auto-implement](../raven-auto-implement/SKILL.md): jeden bieżący agent wykonuje plan i aktualne polecenie, szybko sprawdza zmienione zachowanie i zawsze podaje krótkie podsumowanie oraz instrukcję odbioru krok po kroku wyłącznie w końcowej wiadomości czatu; bez delegowania i przełączania modelu |
| Ręczna weryfikacja | Korzysta z instrukcji odbioru w końcowej wiadomości czatu; feedback może zlecić krótką poprawkę auto-implement, bez ponownego planowania |
| Osobne code review | [raven-implement-review](../raven-implement-review/SKILL.md): niezależna ocena przed standardowym PR; auto-implement nie uruchamia jej samo |
| Domknięcie regresji | [raven-test](../raven-test/SKILL.md) audytuje istniejące testy/review/QA i uzupełnia tylko nazwane luki; może skończyć bez edycji testów |
| Odbiór i PR | Jawne [raven-pr](../raven-pr/SKILL.md) dla jednoznacznej wersji zapisuje odbiór i publikuje/aktualizuje PR po krótkim preflight |
| Merge | Osobno zlecony [raven-merge](../raven-merge/SKILL.md), aktualne dowody i CI; honoruje zapisany odbiór, potwierdza merge i zamyka issue |

Manualna alternatywa: [raven-implement](../raven-implement/SKILL.md) + [raven-implement-review](../raven-implement-review/SKILL.md) realizują kod/testy i ocenę, bez obowiązkowego auto QA ani domyślnego końcowego domknięcia regresji. Następnie ręczna weryfikacja, raven-test i raven-pr. Implementacja nadal zawiera potrzebne testy; późniejszy audyt nie generuje automatycznie nowej suite ani dodatkowego review/QA.

Wcześnie autoryzowany draft pozostaje możliwą operacją boczną, bez odbioru użytkownika. Sama polityka draftu, PASS, test lub istnienie PR nie oznaczają odbioru. Braki standardowego preflight PR wymagają konkretnego pytania z raven-pr; zgoda publikacji z brakami nie omija merge/CI. Issue pozostaje In progress do udanego merge.

[raven-auto-test](../raven-auto-test/SKILL.md) i [raven-test-review](../raven-test-review/SKILL.md) służą osobno zleconemu cyklowi lub nazwanemu ryzyku; raven-test obsługuje też before-change i osobne zadania. [raven-manual-qa](../raven-manual-qa/SKILL.md) to dodatkowe QA bez automatycznych napraw, [raven-browser](../raven-browser/SKILL.md) jest narzędziem przeglądarkowym. Nie uruchamiaj ich wszystkich po zwykłym audycie regresji.

## Pozostałe narzędzia i historia

[raven-issue-update](../raven-issue-update/SKILL.md) wplata wymaganie w zakres i AC jednego wskazanego istniejącego issue. To opcjonalny zapis wymagania, bez zmiany kolejki/statusu i bez uruchamiania planowania. Przy aktywnym change wskazuje potrzebę aktualizacji kontraktu przed zależną implementacją.

[Granice change](references/change-scope.md) obowiązują roadmapę, plan i review. [Rule review](../raven-rule-review/SKILL.md) ocenia instrukcje; [lesson](../raven-lesson/SKILL.md) utrwala powtarzalną regułę na zlecenie; [create-skill](../raven-create-skill/SKILL.md) rozwija Raven. Skille domenowe stosuj do odpowiedniej pracy, bez dodawania etapów procesu.

Wycofane raven-pilot-* i raven-seed nie wracają. Zachowaj historyczne artefakty i decyzje. Kontynuacja starej pracy wymaga jawnego mapowania do lokalnego change; nie kasuj ani nie migruj historii podczas aktualizacji skilli.
