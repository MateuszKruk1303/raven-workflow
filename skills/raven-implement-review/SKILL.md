---
name: raven-implement-review
description: Przeprowadź techniczne review implementacji change z GitHuba względem planu i wymagań, opublikuj raport i prowadź ręczny triage. Bez automatycznej pętli tester–implementator.
---

# Raven Implement Review

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [impl-review](references/procedures/impl-review/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Wykonaj lokalną procedurę review implementacji z [manualnym adapterem GitHub](../raven-plan/references/manual-github.md). Zachowaj źródłowe sześć wymiarów, wybór dostarczonych faz, analizy dobrane do ryzyka, kontrolę kryteriów, ważność ustaleń, format raportu i interaktywny triage. Nie stosuj automatycznej bramki testera ani trybu report-only z raven-auto-implement.

## Wejście i zakres

Przyjmij change, wskazane fazy lub URL raportu do wznowienia triage. Odczytaj plan, snapshot, Progress tasków, checkpointy wykonania, decyzje i lessons. Odtwórz adapter. Ustal jawne base/head SHA na podstawie checkpointów i Git zamiast heurystyki daty lokalnego planu. Brak jednoznacznej bazy wymaga ustalenia zakresu, nie pominięcia wcześniejszych zmian.

Oceń wszystkie dostarczone fazy i cały ustalony diff base_sha..reviewed_sha, również przy oczekujących manual checks lub późniejszych testach. Jawne zlecenie węższego review ogranicza zakres. Wymień ocenione fazy; brakujące kontrole i odbiór raportuj oddzielnie, bez deklarowania ich PASS ani pełnego ukończenia planu.

Review może zostać zlecone niezależnie od raportu browser-review. Wykonaj weryfikację przewidzianą przez Raven i projekt; nie uruchamiaj z tego powodu automatycznego cyklu napraw testera. Oceniaj ustalony stan kodu, nie ruchomy diff.

## Raport i decyzje

Zapisz raport w komentarzu raven:impl-review z wersją planu, SHA, Reviewed phases, stabilnymi ID i dowodami path:line. Zachowaj marker IMPL-REVIEW-REPORT oraz treść źródłowego formatu. Przedstaw raport i źródłowy wybór triage teraz/później. Zapisuj decyzje osobno bez zmieniania historycznego raportu; URL raportu pozwala wznowić nierozstrzygnięte ustalenia.

Zachowaj opcje triage i wykonuj wyłącznie wybrane działania w planie/kodzie. Zlecone poprawki muszą przejść właściwe bramki; zapisz nowe SHA lub wersję planu oraz faktyczny wynik. Zmiana kontraktu wymaga uzgodnienia. Osobna lekcja wymaga zlecenia raven-lesson. Nie uruchamiaj automatycznej kolejnej rundy review/testera ani PR; poinformuj, które dowody wymagają odświeżenia po poprawkach.

Zakończ raportem, decyzjami, wykonanymi działaniami i pozostałymi kontrolami. Akceptacja ryzyka nie zmienia werdyktu technicznego, nie oznacza naprawy ani Done. Osobisty odbiór, dodatkowe testy i raven-pr pozostają oddzielnymi etapami.
