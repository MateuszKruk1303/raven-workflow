---
name: raven-jira-roadmap
description: Przenieś wskazane tickety, sprint lub epikę Jira do GitHub jako roadmapę agenta Raven. Jira pozostaje źródłem wymagań; wersjonowane mapowanie i artefakty pracy w prywatnym GH, bez zapisów do Jira.
---

# Raven Jira Roadmap

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

Przeczytaj [kontrakt GitHub](../raven-auto-plan/references/github-contract.md) i [kontrakt raportów brownfield](../raven-repo-map/references/github-brownfield.md). Ten skill tworzy kolejkę pracy agenta dla jawnie wskazanego zakresu Jira. Nie synchronizuje dwukierunkowo backlogów.

## Źródła i zakres

Jira jest źródłem wymagań, kryteriów i biznesowego statusu. GitHub przechowuje plan, badania, review, dowody i stan pracy Raven. Issue GH zawiera oznaczony snapshot Jira i link do oryginału, nie konkurencyjny edytowalny backlog. Rozdziel repo kodu od repo artefaktów i prywatnego Project; prywatny Project nie ukrywa issues publicznego repo. Korzystaj ze wskazanej organizacji i zatwierdzonego miejsca artefaktów; nie kopiuj firmowych danych do domyślnego osobistego repo.

Input: lista kluczy/URL ticketów, konkretny sprint albo epika. Ustal instancję Jira i jednoznaczny zakres, pobierz pełną paginację, opisy, kryteria, istotne ludzkie komentarze, relacje i metadane wersji. Nie importuj automatycznie sąsiednich sprintów ani wszystkich powiązanych zadań. Oznacz zależności poza zakresem jako zewnętrzne. Brak dostępu lub niepełna paginacja nie oznacza pustego sprintu.

## Import i odświeżenie

1. Zbuduj inwentarz źródeł przed zapisami. Domyślnie jeden wykonywalny ticket Jira = jeden Raven change; epika/sprint to grupa. Nie twórz change dla kontenera bez własnej pracy. Dla podzadań zachowaj relacje i nie duplikuj zakresu rodzica. Nie wymyślaj technicznych faz: powstaną podczas planowania.
2. Znajdź istniejące mapowania po parze instancja Jira + niezmienny issue ID; klucz i URL są dodatkowymi polami. Przeszukaj docelowe repo i Project z paginacją. Marker `<!-- raven:jira-source instance=INSTANCE issue_id=ID -->` pozwala wznowić import po timeout. Nie mapuj po samym tytule.
3. Publikuj w issue blok `raven:jira-source:start/end`: klucz, URL, ID, odczytane updated/version, czas pobrania, zakres kryteriów i źródłowe komentarze z ich ID. Zachowaj dokładne wymagania i rozróżnij autorskie streszczenie. Snapshot JSON i SHA-256 treści semantycznych zapisz w komentarzu `raven:jira-snapshot` z numerem wersji; zmiana samej daty pobrania nie zmienia wersji. Duże payloady podziel i potwierdź kompletność według kontraktu.
4. Utwórz brakujące changes z Raven ID, Project item, kolejnością i jawnymi zależnościami; odczytaj rezultat po każdej mutacji. Wznów częściowo zakończony import zamiast tworzyć duplikaty. Nie zastępuj ludzkich sekcji ani artefaktów planu. Zapisz indeks Jira → GH w dedykowanym issue roadmapy.
5. Przy odświeżeniu porównaj nowe źródło z ostatnim snapshotem i raportuj added/changed/unchanged/out-of-scope/unavailable. Nowy snapshot jest historią źródła. Zmiana zaakceptowanych wymagań jest propozycją aktualizacji kontraktu: zachowaj poprzedni plan, oznacz rozjazd i poproś o rozstrzygnięcie przed zależną implementacją. Nie przenoś akceptacji na nową wersję. Usunięcie ticketa ze sprintu nie zamyka i nie usuwa change.
6. Status Jira zapisuj jako metadane źródła, niezależne od Raven Project. Ani Jira Done, ani import nie dowodzą merge Raven. Nie zamykaj issues i nie ustawiaj Done. Przy rozdzielonych repo nie zakładaj automatycznego zamknięcia/statusu po merge. Osobno zlecony [raven-merge](../raven-merge/SKILL.md) weryfikuje PR w repo kodu i jawnie zapisuje Done dla change na powiązanym Project, również bez integracji automatycznej; nie zmienia Jiry.

## Granice

Tylko koordynator zapisuje GH. Jira pozostaje read-only: bez komentarzy AI, aktualizacji statusu lub pola. Nie kopiuj załączników/logów hurtowo; publikuj tylko dane potrzebne do uzgodnionego zakresu i bez sekretów. Nie twórz repo ani nie zmieniaj uprawnień przy błędzie dostępu; setup jest odrębnym zadaniem. Nie uruchamiaj planowania ani implementacji po imporcie.

Oddaj link do roadmapy, mapowanie ticketów, kolejność i zależności, podsumowanie różnic oraz blokady. Przy współpracy kilku osób zapisuj wykonawcę i checkpoint; odczytaj je przed zapisem, nie obiecuj blokady transakcyjnej GitHuba.
