---
name: raven-implement
description: "Wykonaj lub wznów wskazany lokalny plan change wraz z potrzebnymi testami. Manualny etap realizacji ze wspólnym checkpointem i dowodami."
---

# Raven Implement

Na początku zleconej implementacji potwierdź In progress i assignee konkretnego issue GH według wspólnego kontraktu; nie mutuj issue podczas samego statusu. Przed zależną implementacją sprawdź również aktualne niezależne `plan-review.md` dla bieżącego fingerprintu i rozstrzygnięcie blokujących findings. Brak lub nieaktualne review kieruje do raven-plan-review/auto-plan; plan nie wymaga formalnej akceptacji. Nie wymagaj nowego review dla samych checkboxów lub checkpointu.

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [procedurę implementacji](references/procedures/implement/procedure.md). Rozwiąż change/branch/PR. Wywołanie z jednoznacznym planem zleca jego realizację; nie twórz zapisu akceptacji planu. Sam plan lub PASS review nie rozpoczyna implementacji. Sprawdź instrukcje, bazę, HEAD, staging i cudze zmiany; zachowaj je.

Wykonaj zlecony zakres oraz jego testy. Nie wymagaj osobnej zgody na rutynowe fazy, naprawy i lokalne commity własnego zakresu, jeśli obejmuje je bieżące zlecenie. Manual oznacza oddanie wyniku tego etapu, nie pytanie po każdej komendzie. Respektuj realne bramki człowieka i zmianę kontraktu.

Postęp i checkpoint zapisuj w planie poza blokiem kontraktu. Wczesny draft/aktualizacja PR wykorzystują wcześniej autoryzowaną politykę; brak dostępu do trackera obsłuż według wspólnego kontraktu, a brak uprawnienia publikacji nie blokuje pracy lokalnej. Oddaj działający rezultat, testy, ograniczenia, aktualny diff i handoff do jednego niezależnego raven-implement-review. Nie uruchamiaj samodzielnie dodatkowego testera ani merge.

Manual implement pozostaje prostą alternatywą realizacji z potrzebnymi testami i kontrolami projektu. Nie deklaruje końcowego domknięcia regresji raven-test. Po review wynik można ręcznie zweryfikować, następnie wywołać raven-test i raven-pr; instrukcję ręczną podaj wyłącznie w końcowej wiadomości czatu, jeśli jest częścią zlecenia, bez narzucania manualnemu trybowi osobnego testera auto.
