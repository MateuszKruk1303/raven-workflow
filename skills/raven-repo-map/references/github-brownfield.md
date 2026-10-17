# Raporty brownfield w Git

Raport konkretnego change zapisz w `context/changes/<id>/`: `research.md`, `frame.md`, `domain.md`, `glossary.md`, `qa-plan.md`, `qa-report.md` lub `rule-review.md`, zależnie od zadania. Raport przekrojowy ma jedno miejsce w `context/foundation/`, np. `repo-map.md`, `domain.md`, `glossary.md` albo `rule-review.md`. Nie twórz issues artefaktów, snapshotów komentarzy ani drugiej kopii raportu.

Raport zawiera cel/zakres, źródła i wersje, HEAD/branch/dirty state, czas badania, dowody path:line, metodę, niepewności i następny krok. Używaj rzeczywistych metadanych; nieznane oznacz. Odróżniaj fakty, interpretacje i decyzje. Aktualizuj plik z czytelnym diffem; historię przechowuje Git. PR może linkować raport w zakresie polityki publikacji.

Poufne materiały należą do zatwierdzonego repo artefaktów, które może być inne niż repo kodu. Jawnie zapisz mapowanie; nie kopiuj do osobistego remote. Prywatny Project nie zapewnia prywatności publicznego repo. Brak dostępu do źródła oznacza lukę, nie pozwolenie na zastępczą publikację.

Przy wznowieniu czytaj bieżący raport/checkpoint i tylko wskazane źródła potrzebne do luki. Nie pobieraj całej historii issues. Historyczne artefakty GH pozostają na miejscu; migracja wymaga osobnego zlecenia.
