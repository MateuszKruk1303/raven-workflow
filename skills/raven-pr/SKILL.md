---
name: raven-pr
description: "Wypchnij branch i utwórz lub zaktualizuj PR wskazanego change, powiązany z issue. Tylko na wyraźne polecenie; bez merge."
---

# Raven PR

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md).

Wywołanie `raven-pr` jest zgodą na zwykły push bieżącego brancha i utworzenie lub aktualizację jego PR. Nie pytaj o nią ponownie.

1. Ustal repo, branch, bazę i issue. Sprawdź working tree: do commitu trafia tylko własna praca, cudze zmiany zostają nietknięte. Niezacommitowaną własną pracę zacommituj w logicznych krokach.
2. Znajdź istniejący PR dla tego brancha; aktualizuj go zamiast tworzyć duplikat. Po timeout najpierw odczytaj stan, potem ewentualnie ponów.
3. Zwykły push, bez force-push. Opis PR: problem i wynik, `Closes #N`, zakres, sekcja `## Weryfikacja` według [zasad](../raven-workflow/references/git-workflow.md#weryfikacja-i-raportowanie), znane braki. Weryfikację bierz z finału `raven-auto-implement`, `raven-test` lub review w bieżącym kontekście; nie dopisuj kontroli, których nie widzisz. Przy aktualizacji PR odśwież sekcję o nowe kontrole. Wielowierszowy body przekazuj przez plik (`--body-file`). Draft, gdy użytkownik o niego prosi albo praca jest niekompletna.
4. Odczytaj PR po zapisie (URL, head, base, stan) i podaj go w czacie wraz z brakami, jeśli są.

Nie merguj, nie zmieniaj ochrony brancha i nie zamykaj issue. Lokalny wynik testów to nie CI.
