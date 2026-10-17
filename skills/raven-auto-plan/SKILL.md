---
name: raven-auto-plan
description: "Przygotuj lokalny plan change i przeprowadź jedno niezależne review z ograniczoną pętlą poprawek, po czym oddaj konkretny kontrakt do akceptacji użytkownika."
---

# Raven Auto Plan

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Koordynuj planistę i świeżego reviewera według polityki ról. Nie deleguj ponownie całego skilla. Wykorzystuj [procedurę planu](../raven-plan/references/procedures/plan/procedure.md) oraz [procedurę review](../raven-plan-review/references/procedures/plan-review/procedure.md). Obie role dostają aktualne wymagania, lokalny plan i wskazane źródła, bez transkryptu drugiej roli.

1. Rozwiąż issue i change; na początku zlecenia potwierdź In progress oraz assignee zgodnie ze wspólnym kontraktem, przed delegowaniem researchu lub planowania. Utwórz folder planu dla nowego rezultatu. Stosuj [granice change](../raven-workflow/references/change-scope.md) przed szczegółowym researchem. Przy podziale istniejącej kolejki uzyskaj brakującą zgodę; auto nie rozszerza zakresu.
2. Planista przygotowuje kompletny kontrakt i proporcjonalne kroki z testami. Wykorzystuje istniejące decyzje, pyta tylko o rzeczywiste luki. Wymaga potwierdzonego issue; Project pozostaje opcjonalny.
3. Świeży reviewer sam czyta plan, wymagania i niezbędny kod; zapisuje `plan-review.md` z fingerprintem. Reviewer nie edytuje planu.
4. Potwierdzone błędy w uzgodnionych granicach wracają do planisty automatycznie. Po dwóch nieskutecznych próbach tego samego problemu zapisz checkpoint, potrzebną decyzję i blokadę w issue. Zmiana wymagań/podejścia wykraczająca poza ustalenia wymaga użytkownika; reviewer nie zatwierdza jej za niego.
5. Po odświeżeniu dotkniętego review oddaj plan, wynik i dokładny fingerprint do akceptacji. Nie uruchamiaj implementacji na podstawie samego PASS. Jeśli użytkownik już jednoznacznie zaakceptował identyczny kontrakt, zachowaj tę decyzję.

Wczesny draft jest dopuszczalny według wcześniej autoryzowanej polityki, bez nowych praw z samego taska. Git przechowuje historię; review nie publikuje kopii całego planu do komentarzy.
