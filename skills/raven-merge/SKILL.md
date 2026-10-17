---
name: raven-merge
description: "Zmerguj wskazany PR/change po aktualnych dowodach, CI, odbiorze i zgodzie użytkownika. Opcjonalny tracker finalizuj niezależnie, jeśli objęty zleceniem; deploy jest osobny."
---

# Raven Merge

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Zlecenie „zmerguj C-03” upoważnia do merge jednoznacznego PR; nie pytaj ponownie o tę zgodę. Odbiór wyniku musi być potwierdzony; jedna wypowiedź „akceptuję, zmerguj” może dostarczyć obu decyzji. Sam status, plan lub PASS nie stanowią zgody merge.

## Preflight

Rozwiąż plan i PR z jednoznacznego repo/branch/URL. Sprawdź aktualny kontrakt/fingerprint i jego akceptację, pełny zakres dostarczenia, review kodu+wymagań+testów, odbiór użytkownika i obowiązujące manual gates. Dowody muszą dotyczyć aktualnego drzewa/head oraz istotnej konfiguracji/środowiska. Przy częściowym PR lub kilku kandydatach ustal finalny zakres; nie merguj seryjnie przez domysł.

Odczytaj aktualny head, base, draft, mergeability, wymagane reviews/checki, rulesets/branch protection i merge queue. Sprawdź także kontrole planu niewymuszane przez serwer. Brak dostępu lub UNKNOWN nie oznacza braku wymagań. FAIL, konflikt, brak odbioru lub kontrola NOT VERIFIED blokują merge; pending pozostaje oczekiwaniem. Nie zmieniaj zabezpieczeń, nie zatwierdzaj własnego PR w imieniu reviewera i nie używaj bypassu.

## Merge dokładnej wersji

Wybierz metodę zgodną z polityką repo i jawną decyzją użytkownika; bez preferencji pierwszą dozwoloną squash → merge commit → rebase. Przy wymaganej queue stosuj jej mechanikę. Bezpośrednio przed zapisem odśwież head/base i bramki. Użyj operacji z atomowym warunkiem oczekiwanego SHA, np. `gh pr merge --match-head-commit SHA`. Jeśli narzędzie tego nie obsługuje, wybierz właściwe lub zatrzymaj zapis.

Nie używaj `--admin`, `--delete-branch` ani opcjonalnego auto-merge do obejścia pending. Queue lub przyjęcie polecenia nie dowodzi merge. Po żądaniu, także timeout, odczytaj mergedAt, merge commit, base i dostarczony zakres. Squash/rebase nie muszą mieć SHA równego head. Przy nieznanym wyniku zachowaj checkpoint; nie wysyłaj ślepo ponownego żądania. PR już merged wymaga odczytu dowodów, nie kolejnego merge.

## Opcjonalny tracker

Brak Project/issue nie blokuje merge. Aktualizacja istniejącego trackera jest osobną opcjonalną operacją tylko w zakresie zgody. Dla GH potwierdź właściwy Project, item/content, pole statusu po ID oraz opcję Done; odczytaj rezultat zapisu. Nie twórz boarda/pól/zastępczego itemu przy okazji i nie zamykaj zbiorowo tasków. Nie zapisuj do Jira bez odrębnego zlecenia.

Jeśli tracker zawiedzie, raportuj **PR merged; opcjonalna aktualizacja trackera niewykonana**. Nie cofaj merge, nie przedstawiaj go jako nieudanego i nie blokuj wcześniejszego merge dostępem do boarda. Przy wznowieniu ponów tylko autoryzowany brakujący zapis po readback, z limitem dwóch nieskutecznych prób. Zapisz dowód merge i next w lokalnym checkpointcie; aktualizacja dokumentacyjna po merge nie uzasadnia pushu w nieobjęte miejsce. Nie uruchamiaj deploya.
