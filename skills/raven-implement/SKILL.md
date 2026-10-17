---
name: raven-implement
description: "Wykonaj lub wznów zatwierdzony lokalny plan change wraz z potrzebnymi testami. Manualny etap realizacji ze wspólnym checkpointem i dowodami."
---

# Raven Implement

Na początku zleconej implementacji potwierdź In progress i assignee konkretnego issue GH według wspólnego kontraktu; nie mutuj issue podczas samego statusu. Przed zależną implementacją sprawdź również aktualne niezależne `plan-review.md` dla bieżącego fingerprintu i rozstrzygnięcie blokujących findings. Sama akceptacja planu nie zastępuje zachowanego etapu review; brak lub nieaktualne review kieruje do raven-plan-review/auto-plan. Nie wymagaj nowego review dla samych checkboxów lub checkpointu.

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [procedurę implementacji](references/procedures/implement/procedure.md). Rozwiąż change/branch/PR i porównaj bieżący fingerprint z rzeczywistą akceptacją. Brak zgody blokuje zależne wykonanie, nie odczyt i przygotowanie. Sprawdź instrukcje, bazę, HEAD, staging i cudze zmiany; zachowaj je.

Wykonaj zlecony zakres oraz jego testy. Nie wymagaj osobnej zgody na rutynowe fazy, naprawy i lokalne commity własnego zakresu, jeśli obejmuje je bieżące zlecenie. Manual oznacza oddanie wyniku tego etapu, nie pytanie po każdej komendzie. Respektuj realne bramki człowieka i zmianę kontraktu.

Postęp i checkpoint zapisuj w planie poza blokiem kontraktu. Wczesny draft/aktualizacja PR wykorzystują wcześniej autoryzowaną politykę; przy pracy lokalnej nie blokuj implementacji brakiem GH. Oddaj działający rezultat, testy, ograniczenia, aktualny diff i handoff do jednego niezależnego raven-implement-review. Nie uruchamiaj samodzielnie dodatkowego testera ani merge.
