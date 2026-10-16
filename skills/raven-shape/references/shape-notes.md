# Format shape-notes.md

Plik docelowy: `context/foundation/shape-notes.md`. Przy nowym dokumencie użyj poniższego frontmatter. Daty mają format ISO; nieznane wartości pozostają `null`.

```yaml
---
workflow: raven
project: null
context_type: greenfield
created: YYYY-MM-DD
updated: YYYY-MM-DD
checkpoint:
  status: in_progress
  current_topic: problem
  topics_completed: []
  frs_drafted: 0
  next_question: null
---
```

- `context_type`: `greenfield` lub `brownfield`; przy nierozstrzygniętym kontekście `null`.
- `status`: `in_progress`, `complete` (tematy rozstrzygnięte lub uzasadnione jako nieistotne), `warned` (zakończono z jawnymi lukami na prośbę użytkownika).
- Tematy checkpointu: `problem`, `access`, `flow`, `requirements`, `rules`, `scope`, `cross_check`; przy zakończeniu `current_topic: null`.
- `frs_drafted` liczy aktywne FR, nie wyznacza kolejnego numeru ID.

Treść organizuj w sekcje:

1. Źródła i pierwotny pomysł — opis użytkownika, odnośniki, pochodzenie przejętych ustaleń.
2. Obecny system — tylko brownfield: obecne zachowanie, planowana różnica, stan potwierdzony w źródłach.
3. Wizja, problem i odbiorcy — obejście problemu i wartość produktu.
4. Dostęp i role — granice danych i uprawnień, ewentualnie świadomy brak kont.
5. Hipoteza i walidacja — dotarcie do użytkowników, sygnał wyniku, próg albo niewiadoma.
6. Zakres pilota i przepływy — pełna droga do wartości, scenariusze i wyjątki.
7. Wymagania funkcjonalne — trwałe ID, priorytet, źródło, kryteria i ewentualna kategoria zmiany.
8. Reguły biznesowe i dane — reguły, ograniczenia, wyjątki.
9. Wymagania jakościowe i zachowanie do zachowania — obserwowalne gwarancje.
10. Poza zakresem i akceptowane uproszczenia — także ręczne operacje i wizja na później.
11. Ograniczenia i kontekst techniczny — czas, koszty, skala, zastany stack i preferencje do dalszego etapu.
12. Decyzje, założenia i otwarte pytania — odróżnij decyzję użytkownika, dowód ze źródła i propozycję agenta.
13. Kontrola kompletności — konkretne luki i konsekwencje, następny krok przy wznowieniu.

Nie wypełniaj sekcji wymyślonymi treściami. Nieznane informacje oznacz jako nieustalone. Zachowaj dodatkowe sekcje istniejących notatek Raven i ich ustalenia; format nie wymaga przepisywania dokumentu tylko dla zgodności nagłówków. To notatki wejściowe dla PRD, nie gotowy PRD ani plan implementacji.
