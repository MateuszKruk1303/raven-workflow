---
name: raven-merge
description: "Zmerguj wskazany PR/change po aktualnych dowodach, CI, odbiorze i zgodzie użytkownika. Po potwierdzonym merge zamknij powiązany issue; deploy jest osobny."
---

# Raven Merge

Stosuj [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Zlecenie „zmerguj C-03” upoważnia do merge jednoznacznego PR; nie pytaj ponownie o tę zgodę. Odbiór wyniku musi być potwierdzony; honoruj zapis `user_acceptance` z jawnego raven-pr dla aktualnego zakresu i wersji bez ponownego pytania; jedna wypowiedź „akceptuję, zmerguj” może dostarczyć obu decyzji. Sam status, plan lub PASS nie stanowią zgody merge.

## Preflight

Rozwiąż plan, issue i PR z jednoznacznego repo/branch/URL. Potwierdź powiązanie PR–issue oraz że merge dostarczy cały zakres taska; brak powiązania blokuje finalizację. Sprawdź aktualny kontrakt/fingerprint, pełny zakres dostarczenia, review kodu+wymagań+testów, odbiór użytkownika i obowiązujące manual gates. Dowody muszą być aktualne dla dostarczanego zakresu i istotnej konfiguracji/środowiska. Oceń wynik `test_stage` i rzeczywistą wystarczalność ochrony; zgoda publikacji z brakami nie omija bramek merge. Functional delta po odbiorze wymaga ponownego odbioru. Zmiana wyłącznie dokumentacji/testów wymaga oceny wpływu na zachowanie i dowody, a nie automatycznego unieważnienia odbioru przez nowe SHA. Zachowaj źródło/zakres/wersję poprzedniej decyzji i zapisz podstawę jej ważności. Atomowy head guard przy samym merge nadal dotyczy dokładnie bieżącego sprawdzonego SHA. Przy częściowym PR lub kilku kandydatach ustal finalny zakres; nie merguj seryjnie przez domysł.

Sprawdź QA, jeśli wynika z odrębnego jawnego zlecenia lub bramki projektu/kontraktu, z zapisanym źródłem obowiązku. Historyczne `execution_mode: auto` ani `qa_required: true` same nie wymagają QA; zachowaj te pola i raporty bez przywracania starej automatycznej pętli. Brak obowiązku QA nie znosi aktualnego code review, testów, CI ani odbioru.

Odczytaj aktualny head, base, draft, mergeability, wymagane reviews/checki, rulesets/branch protection i merge queue. Sprawdź także kontrole planu niewymuszane przez serwer. Brak dostępu lub UNKNOWN nie oznacza braku wymagań. FAIL, konflikt, brak odbioru lub kontrola NOT VERIFIED blokują merge; pending pozostaje oczekiwaniem. Nie zmieniaj zabezpieczeń, nie zatwierdzaj własnego PR w imieniu reviewera i nie używaj bypassu.

## Merge dokładnej wersji

Wybierz metodę zgodną z polityką repo i jawną decyzją użytkownika; bez preferencji pierwszą dozwoloną squash → merge commit → rebase. Przy wymaganej queue stosuj jej mechanikę. Bezpośrednio przed zapisem odśwież head/base i bramki. Użyj operacji z atomowym warunkiem oczekiwanego SHA, np. `gh pr merge --match-head-commit SHA`. Jeśli narzędzie tego nie obsługuje, wybierz właściwe lub zatrzymaj zapis.

Nie używaj `--admin`, `--delete-branch` ani opcjonalnego auto-merge do obejścia pending. Queue lub przyjęcie polecenia nie dowodzi merge. Po żądaniu, także timeout, odczytaj mergedAt, merge commit, base i dostarczony zakres. Squash/rebase nie muszą mieć SHA równego head. Przy nieznanym wyniku zachowaj checkpoint; nie wysyłaj ślepo ponownego żądania. PR już merged wymaga odczytu dowodów, nie kolejnego merge.

## Finalizacja issue

Po potwierdzeniu udanego merge zamknij dokładny powiązany issue jako completed/Done i usuń etykiety in-progress/blocked oraz zarządzany powód blokady. Zlecenie raven-merge obejmuje tę finalizację. Readback musi potwierdzać właściwy issue i stan. Nie zamykaj go po samym wysłaniu żądania, przyjęciu do queue, review ani publikacji PR. Już poprawnie zamknięty issue oznacza no-op po sprawdzeniu dowodu merge. Nie twórz boarda/pól ani nie zamykaj sąsiednich tasków. Jira pozostaje bez zapisów.

Jeśli finalizacja zawiedzie, raportuj **PR merged; issue nadal wymaga finalizacji**. Nie cofaj ani nie powtarzaj merge. Zachowaj dowód merge i brakującą operację w checkpointcie; przy wznowieniu odczytaj dokładny PR i issue, wykonaj wyłącznie brakujący zapis i readback. Po dwóch nieskutecznych próbach nazwij blokadę. Brak Project lub awaria jego widoku nie blokują poprawnego merge ani finalizacji issue. Aktualizacja dokumentacyjna po merge nie uzasadnia pushu w nieobjęte miejsce. Deploy pozostaje osobnym zleceniem.

W handoffie podaj stan lokalnego checkoutu. Pozostawiony branch zmergowanego change jest historyczny i nie wybiera następnego taska. Sam merge nie rozpoczyna nowego change ani nie przygotowuje dla niego brancha. Przy kolejnym zleceniu planowania obowiązuje [przygotowanie brancha](../raven-workflow/references/change-branch.md): konkretny nowy issue i decyzja o branchu przed zapisami planu.

Instrukcja ręczna jest wyłącznie w końcowej wiadomości czatu implementatora. Nie wymagaj acceptance.md ani nie twórz/aktualizuj go; nie kopiuj kroków odbioru do artefaktów. Historyczne pliki i pola zachowaj. Oceniaj rzeczywiste dowody i feedback, bez domniemanego odbioru.
