---
name: raven-test-plan
description: "Twórz, wznawiaj i odświeżaj strategię testowania w context/foundation/test-plan.md. Ryzyka, cookbook i rollout w Git; bez implementacji testów i obowiązkowego Project."
---

# Raven Test Plan

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [procedurę strategii](references/procedures/test-plan/procedure.md) i jej [schemat](references/procedures/test-plan/references/test-plan-schema.md). Zachowaj discovery, profil none/sparse/meaningful, rzeczywiste obawy użytkownika, koszt × sygnał, challenger, Risk Response Guidance, cookbook, negative space i handoff. Sygnał z historii nie jest wiedzą o zachowaniu.

Kanoniczna strategia to `context/foundation/test-plan.md`; historię zachowuje Git. Nie twórz issue strategii, snapshotów komentarzy ani kopii poza repo jako źródła prawdy. Test-stack, fixtures i konfiguracja również są plikami repo. W brownfield wykorzystaj istniejące testy i narzędzia; w greenfield PRD i decyzje zastępują nieistniejącą historię. Brak strategii nie blokuje dobrze opisanego małego change.

`--status` odczytuje dokument, powiązane lokalne plany/checkpointy i dokładne issues GH potrzebne do ustalenia stanu tasków, bez zapisów ani skanu kolejki. `--refresh` przygotowuje zmianę strategii w lokalnym change, zachowując wcześniejsze źródła i decyzje; nie zmienia automatycznie ochrony zaakceptowanych wymagań. Rollout w strategii opisuje ryzyka i sposób wdrożenia ochrony; konkretne taski, zależności i ich stan należą do issues GH, bez drugiego lokalnego backlogu. Nie oznaczaj delivered na podstawie samej checklisty; sprawdź dowody i dostarczenie.

Zapisz ustalone §1–§8 zgodnie ze schematem, proporcjonalnie do projektu. Pytaj o rzeczywiste nierozstrzygnięte decyzje i potwierdzaj istotny zakres; nie powtarzaj zaakceptowanego briefu. Nie wdrażaj testów ani CI przy okazji. Zwykły change tworzy testy wraz z implementacją; osobny rollout ochrony może używać raven-test/auto-test. CI konfiguruje raven-hooks. Handoff zawiera ścieżkę, wersję Git, bieżący krok, dowody i jedno konkretne następne działanie.
