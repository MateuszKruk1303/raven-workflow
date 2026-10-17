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
3. Odczytaj dokładny powiązany issue (stan i assignee), bez skanowania boarda. Sprawdź fingerprint i akceptację, następny krok oraz aktualność wskazanych dowodów. Dla PR pobierz tylko jego bieżące dane, wymagane checki i konkretne nierozwiązane wątki. Pełna historia komentarzy/task issues nie jest wymagana.
4. Objaśnij stan, istotną lukę i pasujący następny skill. Tutorial i status są read-only; nie podejmuj issue i nie uruchamiaj z nich kolejnych etapów. Jeśli użytkownik osobno zleca wykonanie, stosuj bezpośrednio instrukcje wybranego skilla i zachowane decyzje.

Ograniczone deterministyczne operacje opisuje [runtime](references/runtime.md); helper nie interpretuje wymagań ani nie zatwierdza planów.

## Przygotowanie projektu

**Greenfield:** [shape](../raven-shape/SKILL.md) → [PRD](../raven-prd/SKILL.md) → [architektura](../raven-architecture/SKILL.md) → [stack](../raven-init-stack/SKILL.md) lub [Medusa](../raven-medusa-ecommerce-init/SKILL.md) → [instrukcje repo](../raven-agents-md/SKILL.md) / [wskazany AGENTS.md](../raven-md/SKILL.md), [strategia testów](../raven-test-plan/SKILL.md), [CI](../raven-hooks/SKILL.md) → [roadmapa](../raven-roadmap/SKILL.md) → change. Nie odtwarzaj gotowego setupu. [GitHub setup](../raven-github-setup/SKILL.md) uzupełnia potrzebny remote, tracking issues i politykę publikacji; Project nie jest warunkiem.

**Brownfield:** zakres/wznowienie → opcjonalna [mapa](../raven-repo-map/SKILL.md) przy nieznanym obszarze → realne braki instrukcji/test strategy/CI → opcjonalne [frame](../raven-frame/SKILL.md), [research](../raven-research/SKILL.md), [domena](../raven-domain-distillation/SKILL.md) lub [architektura](../raven-architecture/SKILL.md) → plan. Mały znany task nie wymaga mapy ani setupu boarda. [Jira](../raven-jira-roadmap/SKILL.md) pozostaje źródłem wymagań, a issue GH śledzi wykonanie przez link, bez kopiowania treści ticketu.

## Cykl change

| Etap | Manual | Auto |
| --- | --- | --- |
| Plan | [raven-plan](../raven-plan/SKILL.md), potem [raven-plan-review](../raven-plan-review/SKILL.md) | [raven-auto-plan](../raven-auto-plan/SKILL.md) obejmuje review |
| Akceptacja | Użytkownik akceptuje konkretny fingerprint | Ta sama decyzja |
| Implementacja + testy | [raven-implement](../raven-implement/SKILL.md) | [raven-auto-implement](../raven-auto-implement/SKILL.md) |
| Niezależne review wymagań + kodu + testów | [raven-implement-review](../raven-implement-review/SKILL.md) | Wbudowane jedno świeże review i naprawy w zakresie |
| Wykonawcze QA | Dodatkowe na zlecenie lub według ryzyka | Obowiązkowy osobny świeży tester; scenariusze → poprawki → retest do PASS albo blokady |
| Odbiór i aktualne CI | Użytkownik odbiera wynik; CI dla PR | To samo |
| Merge | Jawnie zlecony [raven-merge](../raven-merge/SKILL.md) | Ta sama zgoda |

[raven-pr](../raven-pr/SKILL.md) publikuje i aktualizuje PR **w trakcie** cyklu, wcześnie jako draft, gdy istnieje autoryzowana polityka. Praca lokalna może trwać bez PR przy potwierdzonym issue GH. Issue pozostaje In progress przez review i PR; Done następuje po udanym raven-merge. Odbiór nie wymusza osobnego etapu pisania testów: testy są częścią implementacji.

[raven-test](../raven-test/SKILL.md), [raven-auto-test](../raven-auto-test/SKILL.md) i [raven-test-review](../raven-test-review/SKILL.md) służą osobnym zleceniom ochrony testowej, before-change, lukom lub ryzyku. [raven-manual-qa](../raven-manual-qa/SKILL.md) to dodatkowe QA, [raven-browser](../raven-browser/SKILL.md) — narzędzie przeglądarkowe. Nie są obowiązkowymi dodatkowymi etapami każdego change. Auto-implement ma własną obowiązkową procedurę wykonawczego QA, z tymczasowymi scenariuszami do ponawiania; samodzielne manual-qa nadal nie naprawia produktu.

## Pozostałe narzędzia i historia

[Granice change](references/change-scope.md) obowiązują roadmapę, plan i review. [Rule review](../raven-rule-review/SKILL.md) ocenia instrukcje; [lesson](../raven-lesson/SKILL.md) utrwala powtarzalną regułę na zlecenie; [create-skill](../raven-create-skill/SKILL.md) rozwija Raven. Skille domenowe stosuj do odpowiedniej pracy, bez dodawania etapów procesu.

Wycofane raven-pilot-* i raven-seed nie wracają. Zachowaj historyczne artefakty i decyzje. Kontynuacja starej pracy wymaga jawnego mapowania do lokalnego change; nie kasuj ani nie migruj historii podczas aktualizacji skilli.
