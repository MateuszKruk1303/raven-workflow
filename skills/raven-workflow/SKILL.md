---
name: raven-workflow
description: "Ręcznie wywoływany tutorial Raven: objaśnij model pracy na taskach GitHub, mapę skilli i pasujący następny krok dla wskazanej pracy. Nie jest routerem ani obowiązkowym etapem."
---

# Raven Workflow

Wywołuj tylko na wyraźne polecenie, jako tutorial i podpowiedź. Tutorial jest read-only: nie podejmuj issue i nie uruchamiaj innych skilli.

## Model pracy

Pracujemy na taskach w GitHub Issues — szczegóły w [pracy na taskach](references/git-workflow.md). Issue niesie wymagania biznesowe, plan jest opcjonalnym jednorazowym kontekstem agenta, a stan pracy to issue, branch, commity i PR. Granice jednego change opisują [granice change](references/change-scope.md).

Przy pytaniu o stan wskazanej pracy odczytaj issue (stan, assignee), branch, commity i PR, objaśnij, gdzie praca jest, i zaproponuj pasujący skill.

## Typowa ścieżka

- **Drobna zmiana:** [raven-auto-implement](../raven-auto-implement/SKILL.md) z samym poleceniem.
- **Task:** issue → opcjonalnie [raven-plan](../raven-plan/SKILL.md) → [raven-auto-implement](../raven-auto-implement/SKILL.md) → ręczny odbiór według instrukcji z czatu i ewentualne poprawki → [raven-pr](../raven-pr/SKILL.md) → [raven-merge](../raven-merge/SKILL.md).
- **Na żądanie lub przy ryzyku:** [raven-implement-review](../raven-implement-review/SKILL.md) (wymagania, kod, testy), [raven-test](../raven-test/SKILL.md) (trwałe testy, before-change), [raven-manual-qa](../raven-manual-qa/SKILL.md) (eksploracyjne QA).

`raven-auto-implement` dobiera weryfikację do ryzyka (`quick`/`standard`/`thorough`) i nie uruchamia kolejnych skilli.

## Przygotowanie projektu

**Greenfield:** [shape](../raven-shape/SKILL.md) → [PRD](../raven-prd/SKILL.md) → [architektura](../raven-architecture/SKILL.md) → [stack](../raven-init-stack/SKILL.md) lub [Medusa](../raven-medusa-ecommerce-init/SKILL.md) → [AGENTS.md](../raven-md/SKILL.md), [CI](../raven-hooks/SKILL.md), [GitHub](../raven-github-setup/SKILL.md) → [roadmapa](../raven-roadmap/SKILL.md).

**Brownfield:** w razie potrzeby [mapa repo](../raven-repo-map/SKILL.md), [research](../raven-research/SKILL.md), [domena](../raven-domain-distillation/SKILL.md) lub [architektura](../raven-architecture/SKILL.md). Mały znany task nie wymaga żadnego z nich. Jira jako źródło wymagań: [raven-roadmap](../raven-roadmap/SKILL.md).

## Narzędzia

[raven-issue-update](../raven-issue-update/SKILL.md) dopisuje wymaganie do istniejącego issue. [raven-browser](../raven-browser/SKILL.md) steruje przeglądarką dla innych skilli. [raven-lesson](../raven-lesson/SKILL.md) utrwala powtarzalną regułę na zlecenie. [raven-create-skill](../raven-create-skill/SKILL.md) rozwija Raven.

Wycofane skille (raven-pilot-*, raven-seed, raven-implement, raven-auto-plan, raven-plan-review, raven-auto-test, raven-test-review, raven-test-plan, raven-frame, raven-agents-md, raven-rule-review, raven-jira-roadmap) nie wracają. Historyczne artefakty zostają bez zmian.
