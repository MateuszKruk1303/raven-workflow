---
name: raven-plan
description: "Przygotuj lub popraw lokalny plan change w repo. Manualne planowanie; niezależne review osobno albo przez raven-auto-plan."
---

# Raven Plan

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [granice change](../raven-workflow/references/change-scope.md) oraz [procedurę planowania](references/procedures/plan/procedure.md). Planista pracuje na wymaganiach i realnym kodzie; nie implementuje produktu.

Przyjmij opis, change ID, lokalny plan, branch, PR albo wskazane źródło wymagań. Zachowaj istniejące decyzje i postęp. Najpierw oceń jeden osobno planowalny, weryfikowalny i mergeowalny rezultat; zbyt szeroki zakres wraca do propozycji podziału przed szczegółowym researchem. Zlecenie planu jednego change nie upoważnia do reorganizacji całej kolejki.

Zapisz plan według [szablonu](references/procedures/plan/references/plan-templates.md). Obejmij testy wraz z implementacją, nie odkładaj ich do obowiązkowego etapu po odbiorze. Rozstrzygnij wymagania, granice i istotne decyzje; pozostaw wykonawcy detale mieszczące się w kontrakcie.

Oddaj wynik, fingerprint, wymagające decyzji kwestie i handoff do raven-plan-review. Nie przedstawiaj własnej samokontroli jako niezależnego review. Nie twórz task issues ani snapshotów GH. Przy ograniczeniu zapisu zastosuj [utrwalenie](references/procedures/plan/references/plan-persistence.md).
