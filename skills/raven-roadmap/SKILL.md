---
name: raven-roadmap
description: "Utwórz lub odśwież kolejność samodzielnych changes na podstawie PRD. Roadmapa żyje w repo albo jednym istniejącym trackerze; bez obowiązkowych task issues i Project."
---

# Raven Roadmap

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [granice change](../raven-workflow/references/change-scope.md). Wejście to PRD/zaakceptowane wymagania, istniejąca architektura i stan produktu. Roadmapa ustala rezultaty oraz zależności, nie zatwierdza planu implementacji.

Wykorzystaj jedno miejsce kolejki: `context/roadmap.md` domyślnie albo wskazany istniejący tracker. Nie utrzymuj dwóch edytowalnych roadmap. Zlecenie roadmapy upoważnia do lokalnego opracowania; zapis zewnętrzny wymaga odpowiedniej wcześniejszej polityki lub jawnego zakresu zlecenia. Brak GH nie blokuje lokalnej roadmapy i nie upoważnia do tworzenia boarda.

Podziel uzgodnione wymagania na osobno planowalne, weryfikowalne i mergeowalne wyniki. Zachowaj pionowy zakres oraz wymagane gwarancje; nie twórz zmian „cały backend”/„cały frontend”, epik ani obowiązkowej warstwy tasków. Każdy wiersz ma ID, wynik, zakres/wyłączenia, źródła, AC, zależności i kolejność. Większy nierozdzielny zakres krótko uzasadnij. Dalsze changes pozostają na poziomie rezultatu, bez szczegółowego projektowania przyszłych integracji.

Pokryj całe uzgodnione PRD: wymaganie przypisane do change, już dostarczone z dowodem albo jawnie odłożone decyzją. Nie zamieniaj wyłączeń w nowy backlog. Graf zależności musi być acykliczny; relacja rodzic–dziecko nie jest zależnością wykonania. Milestones są opcjonalne. Zwykłą sekwencję i techniczny podział wynikający z PRD wykonaj autonomicznie; zmiana wymagań/priorytetów lub odroczenie koniecznej gwarancji wymaga decyzji.

Przy aktualizacji zachowaj ID, decyzje, postęp i historię. Nie reorganizuj istniejącej kolejki przy samym pytaniu o status albo plan jednego change. Nie migruj historycznej roadmapy bez zlecenia. [Zapis i weryfikacja](references/github-publication.md) określają operacje lokalne i opcjonalny tracker.

Oddaj roadmapę, pierwszy gotowy do planowania rezultat, zależności i rzeczywiste luki. Nie twórz pełnych planów wszystkich changes ani nie uruchamiaj implementacji.
