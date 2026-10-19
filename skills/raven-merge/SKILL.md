---
name: raven-merge
description: "Zmerguj wskazany PR po zielonym CI i zgodzie użytkownika, potem potwierdź zamknięcie issue. Deploy jest osobny."
---

# Raven Merge

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md).

Polecenie „zmerguj <PR/change>” jest zgodą na merge jednoznacznie wskazanego PR. Nie pytaj o nią ponownie; przy kilku kandydatach ustal, który.

## Przed merge

Odczytaj aktualny head, base, draft, mergeability, wymagane checki i reviews, branch protection i merge queue. FAIL, konflikt lub brak wymaganej kontroli blokują merge; pending oznacza czekanie. Brak dostępu do danych o ochronie nie oznacza jej braku. Nie używaj `--admin`, bypassu ani nie zatwierdzaj własnego PR.

## Merge

Metoda zgodna z polityką repo; bez preferencji pierwsza dozwolona z: squash, merge commit, rebase. Merguj dokładnie sprawdzony head (`gh pr merge --match-head-commit <SHA>`); przy queue stosuj jej mechanikę. Po żądaniu, także po timeout, odczytaj `mergedAt` i merge commit; nie wysyłaj ślepo drugiego żądania.

## Po merge

Sprawdź, że powiązany issue jest zamknięty; jeśli nie, zamknij go i usuń etykiety in-progress/blocked. Gdy to się nie uda, zgłoś „PR zmergowany; issue wymaga zamknięcia”, bez cofania merge. W czacie podaj PR, merge commit, stan issue i stan lokalnego checkoutu. Merge nie rozpoczyna kolejnego taska ani deploya.
