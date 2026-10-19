---
name: raven-plan
description: "Przygotuj plan jednego change: wymagania z issue, decyzje i podejście w kodzie projektu. Opcjonalnie zleć jedno niezależne review planu. Plan jest jednorazowym kontekstem roboczym dla raven-auto-implement."
---

# Raven Plan

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md) i [granice change](../raven-workflow/references/change-scope.md).

Plan zbiera to, czego wykonawca potrzebuje, żeby zrobić robotę dobrze: wynik, rozstrzygnięte decyzje, podejście w realnym kodzie i sposób weryfikacji. Nie jest kontraktem ani trackerem. Drobna zmiana nie potrzebuje planu — wskaż od razu `raven-auto-implement`.

## Wejście

Przyjmij issue, opis, change ID lub istniejący plan. Odczytaj body issue (zakres i AC), wskazane źródła i decyzje. Przy nowym issue przypisz się i ustaw In progress, jeśli projekt używa statusów; przygotuj branch według [pracy na taskach](../raven-workflow/references/git-workflow.md). Zlecenie planu jednego change nie upoważnia do reorganizacji kolejki.

## Kroki

1. **Granice.** Zanim zaczniesz szczegółowy research, oceń, czy to jeden samodzielnie odbieralny wynik. Zbyt szeroki zakres wraca do użytkownika z propozycją podziału i pierwszym change.
2. **Kod.** Zbadaj tylko to, co rozstrzyga wykonalność, kontrakty i odbiór: istniejące wzorce, architekturę, testy. Negatywny wynik wyszukiwania nie dowodzi nieobecności.
3. **Pytania.** Pytaj tylko o rzeczywiste nierozstrzygnięte decyzje produktowe lub architektoniczne, z rekomendacją i kompromisem — [przykłady](references/questions.md). Detale techniczne w ustalonych granicach rozstrzygnij sam.
4. **Zapis.** Zapisz `context/changes/<id>/plan.md` według [szablonu](references/plan-template.md), proporcjonalnie do zmiany. Testy są częścią kroków implementacji.

## Review planu (opcjonalne)

Uruchom, gdy użytkownik o nie prosi albo plan dotyka zmiany kosztownej lub trudnej do odwrócenia. Jeden świeży agent bez transkryptu autora dostaje plan, issue i dostęp do kodu. Ocenia read-only: jeden rezultat i pokrycie wymagań, wykonalność względem rzeczywistych plików i API, spójność z architekturą, obsługę błędów i migracji, obserwowalne AC i testy. Każda uwaga ma ważność (critical/warning/suggestion), miejsce, skutek i rekomendację.

Potwierdzone uwagi w ustalonych granicach popraw sam w jednej rundzie; zmiana wymagań lub zakresu wraca do użytkownika. Wynik review podaj w czacie, bez osobnego pliku. Bez możliwości uruchomienia świeżego agenta zgłoś brak review; samoocena nie jest review.

## Finał

W czacie: ścieżka planu, kluczowe decyzje, otwarte kwestie (jeśli są), wynik review (jeśli był) i następny krok `raven-auto-implement <id>`. Zapis planu nie uruchamia implementacji. Gdy host nie pozwala zapisać pliku, oddaj plan w czacie.
