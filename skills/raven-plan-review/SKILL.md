---
name: raven-plan-review
description: Oceń plan change z GitHuba pod kątem wykonalności i zgodności z wymaganiami, zapisz raport i przeprowadź wybrany przez użytkownika triage. Osobny manualny etap bez automatycznej implementacji.
---

# Raven Plan Review

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [plan-review](references/procedures/plan-review/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Wykonaj lokalną procedurę review planu z [manualnym adapterem GitHub](../raven-plan/references/manual-github.md). Zachowaj tryby źródłowe, analizę i delegowanie, pięć wymiarów oceny, format raportu, werdykty SOUND/REVISE/RETHINK oraz interaktywny triage. Nie stosuj zakończenia report-only narzuconego reviewerowi w raven-auto-plan.

## Oceniana wersja

Odczytaj change, wszystkie kontrakty faz, zależności, research, lessons i decyzje. Zweryfikuj kompletny snapshot i fingerprint bieżącego planu. Jeśli snapshotu brak dla kompletnego opublikowanego planu, utrwal go przed oceną; częściowa publikacja blokuje review. Odtwórz pełny plan w adapterze, nie oceniaj tylko skrótu rodzica.

Zachowaj źródłowe kryteria i kontrolę Progress. Lokalizacje planu w raporcie mapuj na issue + sekcję/fazę; dowody kodowe zachowują path:line. Nie traktuj zaplanowanego nowego pliku jak błędnie założonej istniejącej zależności.

## Raport, triage i koniec

Publikuj raport z markerem raven:plan-review, wersją i fingerprintem. Zachowaj format Raven, ID ustaleń i dowody. Przedstaw raport w czacie i zachowaj źródłowy wybór triage teraz/później. URL zapisanego raportu wznawia triage zamiast wykonywać nowy audyt.

Wybrane przez użytkownika poprawki wykonuj zgodnie z triage Raven, publikując zmienione kontrakty i nowy snapshot. Nie zmieniaj historycznego werdyktu. Nie uruchamiaj automatycznie nowej rundy review ani implementacji; wskaż potrzebę oceny zmienionej wersji. Przy akceptacji sprawdź zgodność fingerprintu, zapisz rzeczywistą decyzję i ustaw Ready wyłącznie przy spełnionych warunkach wspólnego kontraktu. Nie uznawaj samego SOUND lub zakończenia triage za akceptację użytkownika.
