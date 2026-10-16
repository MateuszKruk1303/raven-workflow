---
name: raven-implement
description: Implementuj zatwierdzony plan change z GitHuba interaktywnie. Manualny etap z bramkami i decyzjami między fazami, bez automatycznej pętli testera i końcowego review.
---

# Raven Implement

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [implement](references/procedures/implement/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Wykonaj lokalną procedurę implementacji z [manualnym adapterem GitHub](../raven-plan/references/manual-github.md). Zachowaj źródłową dyscyplinę implementacji, wybór trybu wykonania, rozróżnienie Minor/Structural, fazy, bramki i ich limity napraw, manual verification, staging własnych zmian, rytuał commitów i decyzje o następnej fazie. Nie stosuj orkiestracji raven-auto-implement.

## Przed edycją

Odczytaj cały change, plan/taski, zatwierdzony snapshot, review i decyzje oraz lessons i instrukcje repo. Sprawdź, czy akceptacja dotyczy bieżącego fingerprintu. Bez zatwierdzonego planu nazwij brak; nie twórz planu podczas implementacji. Odtwórz adapter i ustal repo_root/worktree, branch, HEAD, staging i cudze zmiany.

Zapisz bazowy SHA przed pierwszą edycją w checkpointcie raven:execution. Przy wznowieniu zachowaj istniejącą bazę; nie ustawiaj bieżącego HEAD jako początku już rozpoczętej zmiany. Ustaw In progress zgodnie z rzeczywistym stanem.

## Realizacja

Prowadź użytkownika przez proces Raven. Zlecenie jednej fazy nie oznacza wszystkich faz. Jeśli użytkownik już zlecił kilka faz lub określił tryb, zachowaj tę decyzję według zasad źródłowych. Nie zamieniaj manual gates w automatyczne odhaczenia. Wykonuj wymagane kontrole projektu, w tym sprawdzenie przeglądarkowe, jeśli wynika z zakresu/instrukcji; nie dodawaj automatycznie niezależnego testera i pętli napraw wariantu auto.

Na granicach faz publikuj Progress, SHA i dowody w taskach oraz checkpoint w rodzicu. Lokalne commity obejmują kod; kopie artefaktów i lokalna roadmapa nie trafiają do stagingu ani epilogu. Zachowaj źródłowy wybór „review tej fazy”; gdy użytkownik go wybierze, wykonaj raven-implement-review dla tej fazy, a następnie wróć do decyzji kontynuacji.

## Zakończenie lub poprawki

Zakończ na wykonanym zakresie i jego weryfikacji. Podaj commity, link change, wyniki bramek, oczekujące ręczne sprawdzenia i pozostałe fazy. Nie uruchamiaj końcowego review, PR ani następnego change automatycznie. Status Review oznacza oczekiwanie na odbiór/review, nigdy Done.

Poprawki wyraźnie zlecone przez użytkownika wykonuj w zakresie wskazanych ustaleń/feedbacku, zachowując bramki i dowody. Nie odtwarzaj ukończonych faz ani nie uznawaj starych raportów za pokrycie nowego kodu. Po poprawce oddaj wynik użytkownikowi; nowe review jest osobnym zleceniem.

## Osobny obowiązkowy etap trwałych testów

Po oddaniu implementacji i sprawdzeniu użytkownika, przed PR, workflow wymaga raven-test. Plan wydziela odpowiednie fazy unit/integration/E2E dla tego etapu. Implementacja wykonuje swoje bieżące bramki, lecz nie realizuje odroczonych faz trwałych testów i nie uruchamia raven-test automatycznie. W handoffie wskaż go jako wymagany następny etap przed publikacją PR.

Etap trwałych testów ma dwa warianty: raven-test → osobno raven-test-review (manual) albo raven-auto-test (pisanie, uruchomienie, niezależne review i poprawki wad testów w jednym cyklu). Oba używają tego samego change i źródeł; wybór należy do użytkownika. Samo ukończenie manualnego raven-test nie oznacza ukończenia review testów.
