# Branch nowego change i wznowienie

Stosuj przed zapisami planu lub implementacji. Sam odczyt/status nie przełącza checkoutu ani nie tworzy brancha. Nie uruchamiaj tutorialu raven-workflow.

## Rozwiąż task przed przygotowaniem brancha

Odczytaj instrukcje repo, jawne issue/change/PR, bieżący branch i powiązany plan/checkpoint oraz aktualny stan konkretnego issue i PR. Rozróżnij nowy rezultat od wznowienia aktywnego change. Branch po merged PR lub zamkniętym issue nie wskazuje bieżącego taska tylko dlatego, że nadal jest checkoutem. Nie otwieraj ponownie starego issue ani nie poprawiaj jego planu jako „kolejnego taska”. Brak finalizacji issue po merged PR należy do wznowienia raven-merge, nie do nowego planowania.

Jeżeli użytkownik nie wskazał konkretnego kolejnego issue, ustal go przed claimem i zależnymi zapisami. Wykorzystaj jawnie ustaloną kolejność i zależności; przy niejednoznaczności pytaj o wybór, zamiast brać ostatni plan lub dowolny otwarty issue. Można połączyć wybór taska z pytaniem o branch. Sama odpowiedź „tak, nowy branch” bez jednoznacznego taska nie rozwiązuje wyboru issue.

Przy wznowieniu tego samego otwartego change odzyskaj jego branch i katalog pracy, zachowaj bazowy SHA, checkpoint i postęp. Nie twórz nowego brancha ani nie aktualizuj bazy przez main. Jeśli nowy branch dla wskazanego taska został już przygotowany, sprawdź jego powiązanie i wykorzystaj go; nie twórz kolejnego po przerwie.

## Decyzja przed nowym planem

Dla nowego change bez przygotowanego brancha zapytaj przed tworzeniem folderu/plan.md i delegowaniem planisty: „Czy dla issue #N utworzyć nowy branch z aktualnego main? Przełączę się na main, pobiorę aktualizacje i utworzę raven/<id>”. Podstaw rzeczywisty branch bazowy i nazwę zgodną z projektem. Przy brakującym issue połącz pytanie, np. „Który issue planujemy i czy mam przygotować dla niego nowy branch z aktualnego main?”.

Honoruj wcześniejszą jednoznaczną zgodę obejmującą ten task, również podaną w wywołaniu; nie pytaj ponownie o tę samą decyzję. Zgoda na branch nie oznacza push/PR/merge. Brak odpowiedzi pozostawia zależne zapisy wstrzymane. Odmowa utworzenia brancha nie upoważnia do pisania nowego planu na starym zmergowanym branchu ani na bazie: ustal wskazany istniejący branch dla tego taska lub inny bezpieczny sposób pracy. Możesz kontynuować niezależny odczyt.

## Przygotuj po zgodzie i sprawdź wynik

1. Ustal rzeczywistą bazę i remote z instrukcji projektu, konfiguracji repo oraz Git/GH. Zwykle jest to main; projekt może używać master lub develop. Zweryfikuj repo wskazywane przez remote i branch bazowy, nie zakładaj bez sprawdzenia `origin/main`. Przy sprzecznych źródłach ustal właściwą bazę.
2. Sprawdź aktualny branch, staging, zmiany tracked/untracked, trwającą operację Git, istniejące branche/worktree i kolizję nazwy nowego brancha. Nie przenoś zmian ze starego change do nowego. Nie stosuj reset, stash, clean, wymuszonego checkoutu ani porządkowego commitu. Przy dirty tree pozostaw je nienaruszone; ustal zachowanie zmian lub zastosuj izolowany worktree zgodnie z autoryzowanym sposobem pracy. Błędu aktualizacji bazy nie obchodź innym punktem startu.
3. Dla czystego checkoutu przełącz się na ustalony branch bazowy, np. `git switch main`, a następnie pobierz aktualizację wyłącznie fast-forward, np. `git pull --ff-only origin main`. Jeżeli lokalnej bazy brak, najpierw pobierz właściwą zdalną gałąź i utwórz jej lokalny tracking branch. Nie używaj zwykłego pull dopuszczającego merge/rebase ani starego feature HEAD jako bazy. Gdy baza jest zajęta w innym worktree, sprawdź jego stan i właściciela; nie przełączaj cudzej sesji.
4. Potwierdź sukces pobrania i równość lokalnej bazy ze świeżo pobraną zdalną bazą. Sam udany `pull --ff-only` nie wystarcza: lokalna baza może być ahead. Diverged/ahead, konflikt, brak dostępu lub nieznany wynik zatrzymują tworzenie brancha do rozstrzygnięcia; nie resetuj lokalnych commitów i nie startuj ze starej bazy.
5. Dopiero z potwierdzonej aktualnej bazy utwórz i wybierz nowy branch, np. `git switch -c raven/<id>`. Nie używaj `-C` ani nie nadpisuj istniejącego brancha. Przy wybranej izolacji przygotuj worktree z jawnego, świeżo zweryfikowanego SHA zdalnej bazy; oryginalny checkout pozostaje nienaruszony. Opcjonalny runtime `start` wymaga tu `--base <SHA>` — jego domyślne HEAD nie gwarantuje właściwej bazy.
6. Sprawdź branch, HEAD, katalog i stan drzewa. Zapisz pełny startowy SHA jako `base` w pierwszym checkpointcie nowego planu wraz z issue, branchem i źródłem decyzji o przygotowaniu brancha. Po przerwaniu najpierw odczytaj faktyczny wynik ostatniej operacji i kontynuuj od niego; nie ponawiaj tworzenia w ciemno. Plan i delegowana praca powstają dopiero w potwierdzonym katalogu tego change, po potwierdzeniu claimu issue według wspólnego kontraktu.
