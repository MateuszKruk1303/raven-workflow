---
name: raven-auto-implement
description: "Wykonaj wskazany plan z uwzględnieniem aktualnego polecenia użytkownika, sprawdź zmienione zachowanie i krótko podsumuj wynik. Samodzielna implementacja lub poprawka bez orkiestracji workflow."
---

# Raven Auto Implement

Zrealizuj wskazany plan oraz aktualne polecenie użytkownika. Polecenie doprecyzowuje lub zmienia zakres planu: uwzględnij je bez ponownego planowania, aktualizacji planu jako warunku pracy, plan-review ani sprawdzania fingerprintu. Czytaj plan i kod potrzebny do tej zmiany; nie odtwarzaj całego cyklu Raven.

Pracuj jako jeden bieżący agent. Nie deleguj i nie przełączaj modelu ani effortu; nie uruchamiaj planisty, reviewera, testera ani QA. Obowiązuje wyłącznie [wyjątek dla samodzielnego auto-implement w polityce ról](../raven-workflow/references/agent-policy.md#samodzielne-auto-implement); pozostała polityka ról, kontrakt workflow i procedura raven-implement nie są instrukcją tego zadania. Nie dodawaj etapów, bramek akceptacji, trackingu GitHub, raportów procesowych, checkpointów ani metryk.

Wprowadź potrzebne zmiany, zachowując cudzą pracę. Rutynowe decyzje techniczne podejmuj samodzielnie; pytaj tylko o brakującą decyzję produktową, która rzeczywiście uniemożliwia wykonanie, i kontynuuj niezależną część. Respektuj instrukcje projektu, bezpieczeństwo oraz rzeczywiste ograniczenia narzędzi i uprawnień. Samo odwołanie do Raven nie przywraca usuniętych bramek plan-review, trackingu ani innych etapów.

Wykonaj szybką, adekwatną samoweryfikację zmienionego zachowania i bezpośrednio dotkniętych funkcji. Najpierw wykorzystaj istniejące testy; dodaj lub dostosuj test tylko dla konkretnej luki. Dobierz potrzebne kontrole do zmiany, bez domyślnej pełnej suite, zestawu lint + typecheck + build, obowiązkowej krytycznej ścieżki ani stałej liczby scenariuszy błędów. Rozszerzaj sprawdzanie dopiero po wykryciu konkretnego problemu. Po poprawce ponów dotkniętą kontrolę. Gdy potrzebna jest przeglądarka, użyj [wskazówek technicznych UI](references/browser-review.md).

Nie naprawiaj niezwiązanych zastanych awarii testów, fixture, locatorów ani infrastruktury. Zgłoś ograniczenie; jeśli to możliwe, sprawdź zmienione zachowanie innym adekwatnym sposobem. Nie przedstawiaj niewykonanej lub zablokowanej kontroli jako zaliczonej.

W końcowej wiadomości czatu zawsze podaj krótkie podsumowanie pracy (co zmieniono, co sprawdzono, ograniczenia) oraz instrukcję odbioru krok po kroku: konkretne akcje lub polecenia i oczekiwany efekt. Dobierz szczegółowość do zmiany. Przy blokadzie również podaj oba elementy, jasno wskazując braki i co pozostaje do sprawdzenia po ich usunięciu. Podsumowanie i instrukcję umieszczaj wyłącznie w końcowej wiadomości czatu; nie zapisuj ani nie kopiuj ich do dokumentów Markdown, planu, issue ani PR. Nie twórz ani nie aktualizuj acceptance.md ani raportu wykonania. Nie uruchamiaj kolejnego etapu.
