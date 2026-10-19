---
name: raven-roadmap
description: "Utwórz lub odśwież kolejkę samodzielnych changes jako GitHub Issues, ze źródłem w PRD albo wskazanych ticketach, sprincie lub epice Jira. Bez planów implementacji i zapisów do Jira."
---

# Raven Roadmap

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md) i [granice change](../raven-workflow/references/change-scope.md).

Roadmapa to GitHub Issues w ustalonym repo: jeden issue = jeden samodzielnie odbieralny wynik. Zlecenie roadmapy obejmuje zapis tych issues. Project jest opcjonalnym widokiem. Nie twórz lokalnej roadmapy ani drugiego backlogu. Dodatek do jednego istniejącego issue to [raven-issue-update](../raven-issue-update/SKILL.md), nie reorganizacja kolejki.

## Źródło

- **PRD** (`context/foundation/prd.md` lub wskazany dokument): pokryj całe uzgodnione PRD — każde wymaganie ma swój change, dowód wcześniejszego dostarczenia albo jawne odroczenie.
- **Jira** (klucze, URL, sprint, epika): pobierz opisy, AC i relacje tylko z tego zakresu. Epika lub sprint to kontener, nie change; jeden ticket może być change, zbyt szeroki dzielisz. Issue GH linkuje ticket (z ID i datą aktualizacji), bez kopiowania treści ani statusu. Do Jiry nie zapisujesz. Status Jira Done nie dowodzi merge.

## Podział

Dziel na pionowe wyniki (UI, API, dane i walidacja razem), nie na warstwy ani fazy. Każdy issue: wynik, zakres i wyłączenia, link do źródła, obserwowalne AC, zależności. Graf zależności acykliczny. Większy nierozdzielny zakres krótko uzasadnij. Zwykły podział uzgodnionego zakresu wykonaj sam; zmiana wymagań lub priorytetów wymaga decyzji użytkownika.

## Zapis

Przed tworzeniem sprawdź istniejące issues w zakresie, żeby nie duplikować (także po timeout). Przy odświeżeniu aktualizuj tylko różnice, zachowując treści ludzi, assignees i statusy; pokaż added/changed/unchanged/out-of-scope. Nie ustawiaj In progress ani nie zamykaj issues przy układaniu kolejki. Po zapisie odczytaj issues. Bez dostępu do GitHub oddaj propozycję w czacie i nazwij niewykonany zapis.

## Finał

W czacie: linki do issues, kolejność i zależności, pierwszy change gotowy do pracy, luki. Nie twórz planów wszystkich changes ani nie uruchamiaj implementacji.
