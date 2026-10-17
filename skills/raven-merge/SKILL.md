---
name: raven-merge
description: "Zmerguj wskazany PR/change po aktualnych dowodach, CI, odbiorze i zgodzie użytkownika. Po potwierdzonym merge zamknij powiązany issue; deploy jest osobny."
---

# Raven Merge

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Zlecenie „zmerguj C-03” upoważnia do merge jednoznacznego PR; nie pytaj ponownie o tę zgodę. Odbiór wyniku musi być potwierdzony; jedna wypowiedź „akceptuję, zmerguj” może dostarczyć obu decyzji. Sam status, plan lub PASS nie stanowią zgody merge.

## Preflight

Rozwiąż plan, issue i PR z jednoznacznego repo/branch/URL. Potwierdź powiązanie PR–issue oraz że merge dostarczy cały zakres taska; brak powiązania blokuje finalizację. Sprawdź aktualny kontrakt/fingerprint i jego akceptację, pełny zakres dostarczenia, review kodu+wymagań+testów, odbiór użytkownika i obowiązujące manual gates. Dowody muszą dotyczyć aktualnego drzewa/head oraz istotnej konfiguracji/środowiska. Przy częściowym PR lub kilku kandydatach ustal finalny zakres; nie merguj seryjnie przez domysł.

Jeżeli checkpoint wskazuje `execution_mode: auto` lub `qa_required: true`, sprawdź również aktualny PASS niezależnego wykonawczego QA i raport testera. Zachowaj tę bramkę po ręcznych poprawkach i zmianie sesji; sam brak pola przy dowodach wykonania w auto nie jest zwolnieniem z QA. Nie dodawaj jej historycznym change ani realizacji wyłącznie manualnej.

Odczytaj aktualny head, base, draft, mergeability, wymagane reviews/checki, rulesets/branch protection i merge queue. Sprawdź także kontrole planu niewymuszane przez serwer. Brak dostępu lub UNKNOWN nie oznacza braku wymagań. FAIL, konflikt, brak odbioru lub kontrola NOT VERIFIED blokują merge; pending pozostaje oczekiwaniem. Nie zmieniaj zabezpieczeń, nie zatwierdzaj własnego PR w imieniu reviewera i nie używaj bypassu.

## Merge dokładnej wersji

Wybierz metodę zgodną z polityką repo i jawną decyzją użytkownika; bez preferencji pierwszą dozwoloną squash → merge commit → rebase. Przy wymaganej queue stosuj jej mechanikę. Bezpośrednio przed zapisem odśwież head/base i bramki. Użyj operacji z atomowym warunkiem oczekiwanego SHA, np. `gh pr merge --match-head-commit SHA`. Jeśli narzędzie tego nie obsługuje, wybierz właściwe lub zatrzymaj zapis.

Nie używaj `--admin`, `--delete-branch` ani opcjonalnego auto-merge do obejścia pending. Queue lub przyjęcie polecenia nie dowodzi merge. Po żądaniu, także timeout, odczytaj mergedAt, merge commit, base i dostarczony zakres. Squash/rebase nie muszą mieć SHA równego head. Przy nieznanym wyniku zachowaj checkpoint; nie wysyłaj ślepo ponownego żądania. PR już merged wymaga odczytu dowodów, nie kolejnego merge.

## Finalizacja issue

Po potwierdzeniu udanego merge zamknij dokładny powiązany issue jako completed/Done i usuń etykiety in-progress/blocked oraz zarządzany powód blokady. Zlecenie raven-merge obejmuje tę finalizację. Readback musi potwierdzać właściwy issue i stan. Nie zamykaj go po samym wysłaniu żądania, przyjęciu do queue, review ani publikacji PR. Już poprawnie zamknięty issue oznacza no-op po sprawdzeniu dowodu merge. Nie twórz boarda/pól ani nie zamykaj sąsiednich tasków. Jira pozostaje bez zapisów.

Jeśli finalizacja zawiedzie, raportuj **PR merged; issue nadal wymaga finalizacji**. Nie cofaj ani nie powtarzaj merge. Zachowaj dowód merge i brakującą operację w checkpointcie; przy wznowieniu odczytaj dokładny PR i issue, wykonaj wyłącznie brakujący zapis i readback. Po dwóch nieskutecznych próbach nazwij blokadę. Brak Project lub awaria jego widoku nie blokują poprawnego merge ani finalizacji issue. Aktualizacja dokumentacyjna po merge nie uzasadnia pushu w nieobjęte miejsce. Deploy pozostaje osobnym zleceniem.
