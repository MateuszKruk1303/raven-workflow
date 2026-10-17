---
name: raven-pr
description: "Opublikuj lub aktualizuj PR wskazanego change, wcześnie jako draft albo jako gotowy wynik. Wykorzystaj wcześniejszą politykę publikacji; samo zlecenie taska nie daje nowych praw zewnętrznych."
---

# Raven Pr

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Jawne zlecenie raven-pr obejmuje zwykły push i utworzenie/aktualizację właściwego PR w wskazanym repo. Równoważna wcześniejsza polityka może pozwalać robić to w trakcie implementacji bez nowej zgody. Sam status, akceptacja planu lub istnienie tokena tego nie upoważniają.

1. Ustal change/plan, tożsamość repo, branch, base/head i zakres diffu. Sprawdź cudze zmiany oraz istniejący staging. Znajdź dokładnie właściwy PR po repo/head/base i powiązaniu z planem; nie twórz duplikatu po timeout. Nie wyciągaj repo wyłącznie z C-ID.
2. Przygotuj konkretne logiczne commity własnych kodu/testów/dokumentów, celowy staging i zwykły push do autoryzowanej gałęzi. Nie force-pushuj i nie dołączaj cudzej pracy. Wcześnie po przygotowaniu planu/brancha otwórz draft, jeśli polityka na to pozwala; nie wymagaj wtedy zakończonej implementacji/review/testów.
3. Opis PR prowadź od problemu do zachowania, linkuj dokładny issue GH oraz `context/changes/<id>/plan.md` w tej wersji repo, podaj zakres, walidację i pozostałe luki. Użyj markerów `<!-- raven-change:<id> -->` i `<!-- raven-issue:OWNER/REPO#N -->` z rzeczywistym powiązaniem. Link do issue jest zwykłym linkiem, bez automatycznych closing keywords; zamknięcie wykonuje raven-merge po potwierdzeniu merge. Issue pozostaje In progress przez draft, review i gotowy PR. Git jest historią dokumentów; nie kopiuj pełnego planu/raportów do komentarzy. Dla opisu CLI używaj body-file.
4. Aktualizuj ten sam draft w toku pracy. Gotowość do review/merge wynika z dowodów, nie samego trybu PR. Przed oznaczeniem ready sprawdź wykonanie, testy i niezależne review oraz rzeczywiste wymagane bramki. Nie ustawiaj PASS CI na podstawie wyniku lokalnego.
5. Po zapisie odczytaj repo/head/base/URL/stan. Po timeout najpierw readback. Dwie nieskuteczne próby tego samego zapisu wystarczą; zachowaj checkpoint i payload zamiast dublować PR. Zapisz PR i next w lokalnym planie.

Ograniczony [runtime](../raven-workflow/references/runtime.md) potrafi utworzyć draft dla już wypchniętej gałęzi; nie zastępuje kontroli zakresu i uprawnień. Publikacja PR nie obejmuje merge, zamykania zbioru issues, zmiany Project ani deploya. [Historia publikacji](references/publication-history.md) opisuje wznowienie.
