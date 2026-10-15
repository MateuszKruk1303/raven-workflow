---
name: raven-pilot-roadmap
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Zbuduj lub uaktualnij pełną roadmapę od zera do pilot ready w workflow Raven Pilot. Podziel ją na zależne chunki dostarczające testowalne przepływy biznesowe od A do Z."
---

# Raven Pilot Roadmap

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

## Wymagany model autora

Ten etap prowadzi **`gpt-6-astra` z effortem `high`** zgodnie z sekcją „Autorzy artefaktów produktowych” kontraktu. Jeśli bieżący model/effort nie są wiarygodnie potwierdzone jako zgodne, uruchom osobnego autora Astra high i przekazuj mu odpowiedzi użytkownika. To jawne zlecenie delegacji; nie wykonuj tego etapu na domyślnym modelu implementacyjnym. Autor już uruchomiony z właściwą konfiguracją realizuje skill bez ponownego delegowania tej samej roli.

Wejście: PRD i zastany stan projektu. Wynik: `context/pilot/roadmap.md`. Nie twórz jeszcze szczegółowych planów wszystkich chunków.

1. Przeczytaj PRD, istniejącą roadmapę, aktywne stany chunków i istotny kod. Wcześniejsze dokumenty produktu traktuj jako źródła; nie przemianowuj ich ani nie wznawiaj automatycznie starych planów.
2. Rozpisz całą drogę do pilota, preferując najwcześniejszy kontakt z rzeczywistymi użytkownikami. Oddziel późniejszą wizję od wymaganego zakresu. Nie wymagaj kończenia funkcji nice-to-have przed pilotem.
3. Nadaj trwałe ID `C-01`, `C-02` itd. Dla każdego chunka zapisz: rezultat biznesowy, hipotezę/wartość, ID wymagań PRD, zakres i wyłączenia, scenariusz demonstracji A–Z, kryteria akceptacji, zależności, niewiadome oraz status z linkiem do artefaktów, gdy istnieją.
4. Chunkiem jest np. „sprzedający zakłada konto, publikuje ofertę, a kupujący znajduje ją i otwiera”. „Formularz”, „API” i „baza danych” są zadaniami wewnątrz chunka. Minimalny setup włącz do pierwszego konsumującego chunka; nie planuj całych warstw z wyprzedzeniem.
5. Utrzymuj tabelę kolejki w formacie z referencji synchronizacji: kolejność, ID, zależności, status, etap, rewizje, linki i aktualność. Pokaż zależności w tabeli i, jeśli poprawia czytelność, diagramie. Sprawdź nieistniejące ID, cykle oraz pokrycie wszystkich wymagań pilot. Zbyt duży chunk dziel po samodzielnej wartości dla użytkownika.
6. Uwzględnij doprowadzenie produktu do dostępności dla pilota, zbierania feedbacku i obserwacji wyniku. Przygotowanie wdrożenia i faktyczna publikacja mają oddzielne kryteria; nie zakładaj zgody na płatne zasoby ani publiczne operacje.
7. Aktualizuj w miejscu, zachowując ID, ukończone rezultaty i decyzje. Status wykonania wyprowadzaj z artefaktów, nie z deklaracji modelu. Zapisz wpływ zmian na aktywne chunki, bez edytowania zamkniętych archiwów.

Uaktualnij wyliczony wpis „Następny do przygotowania” według wspólnego algorytmu kolejki i podaj `$raven-pilot-prepare` bez konieczności wpisywania ID. Priorytet wartości walidacji odzwierciedlaj w jawnej kolejności roadmapy, a nie w innej heurystyce przy każdym wywołaniu. Nie twórz dodatkowej bramki potwierdzenia zwykłego zapisu roadmapy ani nie uruchamiaj implementacji bez zlecenia.
