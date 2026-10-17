---
name: raven-jira-roadmap
description: "Ustal zakres i kolejność pracy Raven ze wskazanych ticketów, sprintu lub epiki Jira. Jira pozostaje źródłem wymagań; bez duplikowania backlogu w GitHub Issues i bez zapisów do Jira."
---

# Raven Jira Roadmap

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Jira przechowuje wymagania i biznesowy status. Plan/kod/dowody Raven są wersjonowane w Git, a PR służy współpracy. Korzystaj z jednego istniejącego trackera; lokalne mapowanie do change nie jest nowym edytowalnym backlogiem.

Ustal instancję i jawny zakres kluczy/URL/sprintu/epiki. Pobierz opisy, AC, istotne decyzje i relacje w tym zakresie z potrzebną paginacją. Nie importuj sąsiednich sprintów lub całej historii komentarzy. Zależności poza zakresem oznacz jako zewnętrzne. Brak dostępu nie jest pustą kolejką.

1. Zidentyfikuj źródła przez instancję + niezmienny issue ID; klucz i URL są dodatkowymi polami. Odczytaj wersję/updated i istotne kryteria. Epika/sprint jest kontenerem, nie automatycznie change. Podzadania nie duplikują zakresu rodzica.
2. Stosuj [granice change](../raven-workflow/references/change-scope.md): jeden ticket może być change, lecz zbyt szeroki wymaga propozycji podziału. Zapisz lokalne mapowanie i odsyłacze w `context/foundation/jira-map.md` lub istniejącej roadmapie; wybierz jedno miejsce. Nie twórz lustrzanych issues GH, Project ani snapshotów komentarzy. Plan wskazuje źródłowy ticket i wersję oraz kontrakt niezbędny do realizacji.
3. Wymagania firmowe przechowuj wyłącznie w zatwierdzonym miejscu. Repo kodu i prywatne repo artefaktów mogą być oddzielne; jawnie zapisz mapowanie, jeśli polityka firmy tego wymaga. Prywatny Project nie ukrywa publicznego repo. Nie kopiuj poufnych treści do osobistego domyślnego remote; publikacja wymaga odpowiedniej autoryzacji.
4. Przy odświeżeniu porównaj źródło i pokaż added/changed/unchanged/out-of-scope/unavailable. Zmiana wymagań jest propozycją aktualizacji kontraktu, z nowym fingerprintem i akceptacją; nie nadpisuj decyzji ani postępu. Usunięcie ze sprintu nie usuwa lokalnego change.
5. Status Jira jest metadanymi źródła; Jira Done nie dowodzi merge kodu. Nie zmieniaj Jiry, nie zamykaj issues, nie twórz zewnętrznych komentarzy ani nie uruchamiaj implementacji po mapowaniu.

Oddaj mapowanie, źródła/wersje, kolejność, zależności, różnice i luki. Historia Git zachowuje wcześniejsze mapowanie. Odczyt istniejącego checkpointu przed edycją wspiera współpracę, ale nie obiecuje transakcyjnej blokady trackera.
