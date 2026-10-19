---
name: raven-auto-plan
description: "Przygotuj lokalny plan change i przeprowadź jedno niezależne review z ograniczoną pętlą poprawek, po czym oddaj gotowy plan do wykonania przez raven-auto-implement."
---

# Raven Auto Plan

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Koordynuj planistę i świeżego reviewera według polityki ról. Nie deleguj ponownie całego skilla. Wykorzystuj [procedurę planu](../raven-plan/references/procedures/plan/procedure.md) oraz [procedurę review](../raven-plan-review/references/procedures/plan-review/procedure.md). Obie role dostają aktualne wymagania, lokalny plan i wskazane źródła, bez transkryptu drugiej roli.

1. Rozwiąż konkretny issue i change; stary branch po merged/closed tasku nie wybiera kolejnego issue. Przed zapisami folderu/planu i delegowaniem zastosuj [przygotowanie brancha](../raven-workflow/references/change-branch.md): dla nowego change zapytaj o nowy branch (bez ponowienia istniejącej zgody), po zgodzie przygotuj aktualną bazę i branch, a przy wznowieniu odzyskaj dotychczasowy. Potwierdź In progress oraz assignee według wspólnego kontraktu przed szczegółowym researchem i planowaniem. Dopiero w potwierdzonym katalogu change utwórz folder planu dla nowego rezultatu. Stosuj [granice change](../raven-workflow/references/change-scope.md) przed szczegółowym researchem. Przy podziale istniejącej kolejki uzyskaj brakującą zgodę; auto nie rozszerza zakresu.
2. Planista przygotowuje kompletny kontrakt i proporcjonalne kroki z testami, rozdzielając kontrole implementacji od audytu/domknięcia regresji raven-test po ręcznej weryfikacji. Wykorzystuje istniejące decyzje, pyta tylko o rzeczywiste luki. Wymaga potwierdzonego issue; Project pozostaje opcjonalny.
3. Świeży reviewer sam czyta plan, wymagania i niezbędny kod; zapisuje `plan-review.md` z fingerprintem. Reviewer nie edytuje planu.
4. Potwierdzone błędy w uzgodnionych granicach wracają do planisty automatycznie. Po dwóch nieskutecznych próbach tego samego problemu zapisz checkpoint, potrzebną decyzję i blokadę w issue. Zmiana wymagań/podejścia wykraczająca poza ustalenia wymaga użytkownika; reviewer nie zatwierdza jej za niego.
5. Po odświeżeniu dotkniętego review oddaj gotowy plan, wynik i dokładny fingerprint oraz wskaż `raven-auto-implement <id>` jako następny krok. Nie dodawaj oczekiwania na akceptację planu. Samo zlecenie planowania ani PASS nie uruchamia implementacji.

Wczesny draft jest dopuszczalny według wcześniej autoryzowanej polityki, bez nowych praw z samego taska. Git przechowuje historię; review nie publikuje kopii całego planu do komentarzy.
