---
name: raven-frame
description: Zweryfikuj założenia problemu przed planowaniem. Oddziel obserwację od przyczyny i rozwiązania; Frame Brief i dowody zapisz w change GitHub.
---

# Raven Frame

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Przed wykonaniem przeczytaj lokalne procedury Raven: [frame](references/procedures/frame/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż te pliki oraz kontrakt GH. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Przeczytaj pełny lokalny [frame](references/procedures/frame/procedure.md) i jego wymagane referencje, a następnie [kontrakt raportów brownfield](../raven-repo-map/references/github-brownfield.md). 

Wykonaj pełny proces: rozdzielenie obserwacji/przyczyny/kierunku, zawężenie zakresu, mapa wymiarów oparta na dowodach, niezależne badania hipotez, pytania rozstrzygające, próba podważenia wiodącej hipotezy i Frame Brief. Zachowaj początkowe sformułowanie użytkownika, poziom pewności oraz kompletne sekcje źródłowego briefu. Nie wymuszaj przeformułowania, gdy dowody potwierdzają pierwotne założenie. To analiza CO wymaga rozwiązania, przed planem JAK.

## Adapter Raven

- Input: change issue/URL, raport researchu w GH lub opis inline. Odczytaj pełne wymagania, komentarze, lessons i dostępne dowody. Rozwiąż repo kodu oddzielnie od repo artefaktów.
- Istniejący change jest miejscem publikacji. Przy opisie inline bez change przygotuj tożsamość zmiany według kontraktu Raven i utwórz issue dopiero w jednoznacznie wskazanym repo/Project; nie twórz lokalnego change.md jako źródła prawdy. Nie otwieraj ponownie zakończonego change.
- `context/changes/.../frame.md` oznacza wyłącznie kopię roboczą poza śledzonym repo. Historyczne research/changes/archive rozwiązuj przez GH. Nie wykonuj lokalnych aktualizacji statusu ani archiwizacji ze źródła.
- Wywołanie upoważnia do publikacji briefu `raven:frame` i odsyłacza w indeksie kontekstu change. Kolejna runda jest nową wersją; zapisuj wersje wejść i HEAD.
- Podagenci pracują tylko odczytowo; koordynator zapisuje GH. Nie zmieniaj kodu, wymagań Jira, zaakceptowanego planu ani statusu Ready/Done. Proponowane nowe rozumienie problemu wymaga decyzji użytkownika przed zmianą zakresu planu.

Oddaj link, potwierdzone/przeformułowane pytanie i pewność. Przy LOW wskaż brakujący dowód. Planowanie pozostaje osobno zlecanym etapem.
