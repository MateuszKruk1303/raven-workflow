---
name: raven-pilot-archive
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Zamknij zweryfikowany chunk Raven Pilot i przenieś jego artefakty do archiwum projektu, aktualizując roadmapę. Zachowaj niezmienność archiwów i respektuj lokalne zakazy zapisu."
---

# Raven Pilot Archive

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

Wejście: jednoznaczny chunk `ready_to_archive` oraz zlecenie archiwizacji (także wcześniejsze w tej samej paczce), albo wznowienie operacji z jej istniejącego dziennika. Wynik: katalog pod repozytoryjnym `archive/raven-pilot/` i aktualny wpis roadmapy. `/archive` oznacza katalog w projekcie, nigdy systemowy katalog główny.

0. **Najpierw rozpoznaj wznowienie.** Przed bramką statusu, kontrolą obecnego kodu i wymaganiem nieistniejącego celu odczytaj dziennik dla ID. Jeżeli źródła nie ma, a cel zawiera pasujący chunk z finalnym stanem archived i dziennik potwierdza wcześniejsze kontrole, nie powtarzaj bramek pierwszej archiwizacji: sprawdź spójność tożsamości i napraw wyłącznie roadmapę/dziennik poza archiwum. Późniejsza zmiana kodu nie zmienia poprawnie zamkniętej historii. Ukończoną operację zwróć idempotentnie. Jeżeli źródło wciąż istnieje z chwilowym stanem archived, cel nie istnieje i dziennik potwierdza przerwanie przed rename, przywróć poprzedni aktywny stan z dziennika i ponów zwykłe bramki. Oba katalogi, brak obu albo niespójny dziennik to blokada do diagnozy, bez kasowania. Bez dziennika nie traktuj samego katalogu archiwum jako zgody na jego naprawianie.
1. Sprawdź ścieżki po rozwiązaniu symlinków, instrukcje repozytorium, akceptację użytkownika, raport testów oraz zgodność manifestu końcowej weryfikacji z istotnym aktualnym kodem. Sam status nie zastępuje dowodów. Nie archiwizuj częściowej pracy ani nie obchodź lokalnego zakazu zapisu do archiwum przez alternatywną ścieżkę. Zarchiwizowanego chunka nie modyfikuj.
2. Domyślna ścieżka to `archive/raven-pilot/<id-slug>/`. Jeżeli wybrany cel jest lokalnie zabroniony, zakończ z dokładnym komunikatem wymaganym przez AGENTS.md. Nie zmieniaj AGENTS.md w celu obejścia zakazu.
3. Przed przeniesieniem sprawdź, że cel nie istnieje, zachowaj poprzedni stan i zapisz dziennik operacji `context/pilot/archive-operations/<id>.json` ze źródłem, celem, poprzednim stanem, potwierdzeniem przejścia bramek, tożsamością/manifestem finalnych artefaktów oraz planowaną aktualizacją roadmapy. Manifest finalnych artefaktów zapisz po finalizacji folderu w kroku 4, przed rename; to dowód tożsamości przy wznowieniu. Nie nadpisuj istniejącego archiwum.
4. Jeszcze w aktywnym folderze zapisz finalny stan `archived`, datę zamknięcia, zakres dostarczonej wartości i linki. Wszystkie odwołania między artefaktami chunka powinny być względne względem folderu chunka; odwołania do kodu opisz jako ścieżki repozytorium. Sprawdź je przed przeniesieniem.
5. Przenieś cały folder jednym rename, gdy system plików na to pozwala; nie stosuj delete-and-copy. Po przeniesieniu nie zapisuj już nic wewnątrz archiwum. Jeśli rename nie powiódł się, przywróć poprzedni stan tylko w nadal aktywnym folderze i zapisz błąd w dzienniku.
6. Dopiero po skutecznym przeniesieniu uaktualnij wiersz chunka w roadmapie do `Done` / `archived`, link do archiwum i wyliczoną kolejkę następnych chunków, a następnie dziennik poza archiwum. Tymczasowy stan archived przed rename nie uprawnia do Done. Przy przerwaniu po udanym przeniesieniu wznowienie naprawia wyłącznie roadmapę/dziennik. Rozpoznaj już zakończoną operację jako sukces bez ponownego przenoszenia. Sprzeczny stan obu katalogów wymaga diagnozy, nie kasowania.
7. Podaj ścieżkę archiwum i zarekomenduj następny chunk wynikający z zależności i celu walidacji. Ukończenie wszystkich chunków porównaj z kryteriami pilot ready; nie utożsamiaj archiwizacji z wdrożeniem, zaproszeniem użytkowników lub potwierdzeniem wartości produktu.

Archiwum dokumentuje dostarczony rezultat. Późniejsze poprawki to nowe chunki; aktualny PRD/roadmapa mogą odwoływać się do archiwów, ale ich nie zmieniają.
