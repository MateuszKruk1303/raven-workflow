---
name: raven-jira-roadmap
description: "Ustal zakres i kolejność pracy Raven ze wskazanych ticketów, sprintu lub epiki Jira. Jira jest źródłem wymagań, GitHub Issues trackerem wykonania; bez kopiowania treści i zapisów do Jira."
---

# Raven Jira Roadmap

Stosuj [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Jira przechowuje wymagania i biznesowy status. Plan/kod/dowody Raven są wersjonowane w Git, a PR służy współpracy. GitHub Issues jest jedynym trackerem wykonania Raven i roadmapy; nie utrzymuj lokalnego backlogu ani kopii biznesowych statusów Jira.

Ustal instancję i jawny zakres kluczy/URL/sprintu/epiki. Pobierz opisy, AC, istotne decyzje i relacje w tym zakresie z potrzebną paginacją. Nie importuj sąsiednich sprintów lub całej historii komentarzy. Zależności poza zakresem oznacz jako zewnętrzne. Brak dostępu nie jest pustą kolejką.

1. Zidentyfikuj źródła przez instancję + niezmienny issue ID; klucz i URL są dodatkowymi polami. Odczytaj wersję/updated i istotne kryteria. Epika/sprint jest kontenerem, nie automatycznie change. Podzadania nie duplikują zakresu rodzica.
2. Stosuj [granice change](../raven-workflow/references/change-scope.md): jeden ticket może być change, lecz zbyt szeroki wymaga propozycji podziału. Utwórz albo wykorzystaj powiązany issue GH dla każdego uzgodnionego change, z krótkim wynikiem, linkiem i identyfikatorem/wersją źródła Jira. Nie kopiuj ticketu, komentarzy ani jego biznesowego statusu. Plan wskazuje oba issues i wersję wymagań; nie twórz osobnego jira-map.md lub lokalnej roadmapy. Zapis obejmuje tylko ustalone repo i zakres; nie twórz Project przy okazji.
3. Wymagania firmowe przechowuj wyłącznie w zatwierdzonym miejscu. Repo kodu i prywatne repo artefaktów mogą być oddzielne; jawnie zapisz mapowanie, jeśli polityka firmy tego wymaga. Prywatny Project nie ukrywa publicznego repo. Nie kopiuj poufnych treści do osobistego domyślnego remote; publikacja wymaga odpowiedniej autoryzacji.
4. Przy odświeżeniu porównaj źródło i pokaż added/changed/unchanged/out-of-scope/unavailable. Zmiana wymagań trafia do issue; istniejący plan jest jednorazowym kontekstem roboczym i nie wymaga aktualizacji ani ponownego review; nie nadpisuj decyzji ani postępu. Usunięcie ze sprintu nie usuwa lokalnego change.
5. Status Jira jest metadanymi źródła; Jira Done nie dowodzi merge kodu. Nie zmieniaj Jiry ani nie zamykaj issues GH podczas mapowania. Nie uruchamiaj implementacji ani nie ustawiaj In progress przy samym układaniu kolejki.

Oddaj mapowanie, źródła/wersje, kolejność, zależności, różnice i luki. Mapowanie wynika z linków issue GH → Jira i źródeł planu; historyczne mapowania zachowaj. Odczyt istniejącego checkpointu przed edycją wspiera współpracę, ale nie obiecuje transakcyjnej blokady trackera.
