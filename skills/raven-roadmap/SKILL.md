---
name: raven-roadmap
description: "Utwórz lub odśwież kolejność samodzielnych changes na podstawie PRD. GitHub Issues przechowuje taski, zależności i stan roadmapy; Project jest opcjonalnym widokiem."
---

# Raven Roadmap

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Do wplecenia dodatkowego wymagania w zakres i AC jednego wskazanego istniejącego issue użyj [raven-issue-update](../raven-issue-update/SKILL.md). Roadmapa potrafi aktualizować istniejące issues w ramach zleconej zmiany kolejki; pojedynczy dodatek nie wymaga jej reorganizacji ani ponownego podziału PRD.

Przeczytaj [granice change](../raven-workflow/references/change-scope.md). Wejście to PRD/zaakceptowane wymagania, istniejąca architektura i stan produktu. Roadmapa ustala rezultaty oraz zależności, nie zatwierdza planu implementacji.

Roadmapę utrzymuj wyłącznie w GitHub Issues ustalonego repo. Zlecenie utworzenia lub aktualizacji roadmapy obejmuje zapis jej issues w uzgodnionym zakresie. Project jest opcjonalnym widokiem; nie twórz lokalnej roadmapy, drugiego backlogu ani boarda przy okazji. Brak dostępu oznacza niewykonaną publikację: przedstaw propozycję w rozmowie i nazwij brak, bez udawania gotowej roadmapy. Sam odczyt/status nie mutuje.

Podziel uzgodnione wymagania na osobno planowalne, weryfikowalne i mergeowalne wyniki. Zachowaj pionowy zakres oraz wymagane gwarancje; nie twórz zmian „cały backend”/„cały frontend”, issues dla faz implementacji. Jeden issue to jeden task/change. Każdy ma numer/URL, krótki wynik, zakres/wyłączenia, źródła, AC, zależności i kolejność. Większy nierozdzielny zakres krótko uzasadnij. Dalsze changes pozostają na poziomie rezultatu, bez szczegółowego projektowania przyszłych integracji.

Pokryj całe uzgodnione PRD: wymaganie przypisane do change, już dostarczone z dowodem albo jawnie odłożone decyzją. Nie zamieniaj wyłączeń w nowy backlog. Graf zależności musi być acykliczny; relacja rodzic–dziecko nie jest zależnością wykonania. Milestones są opcjonalne. Zwykłą sekwencję i techniczny podział wynikający z PRD wykonaj autonomicznie; zmiana wymagań/priorytetów lub odroczenie koniecznej gwarancji wymaga decyzji.

Przy aktualizacji zachowaj ID, decyzje, postęp i historię. Nie reorganizuj istniejącej kolejki przy samym pytaniu o status albo plan jednego change. Nie migruj historycznej roadmapy bez zlecenia. [Zapis i weryfikacja](references/github-publication.md) określają oszczędne operacje na issues GH.

Oddaj linki do roadmapy w GH, pierwszy gotowy do planowania rezultat, zależności i rzeczywiste luki. Nie twórz pełnych planów wszystkich changes ani nie uruchamiaj implementacji.
