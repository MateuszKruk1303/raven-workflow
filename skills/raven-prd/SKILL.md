---
name: raven-prd
description: "Wygeneruj context/foundation/prd.md z shape-notes.md lub surowych notatek, zgodnie ze schematem PRD (greenfield 10 sekcji, brownfield 11). Generator dokumentu, nie autor: luki trafiają do Open Questions. Użyj po raven-shape, gdy notatki są gotowe („stwórz PRD”, „write the PRD”)."
---

# Raven PRD

Zamień uzgodnione notatki w `context/foundation/prd.md` zgodny ze [schematem PRD](references/prd-schema.md). Schemat jest jedynym źródłem nazw sekcji, ich kolejności i kluczy frontmatter; przeczytaj go przed generowaniem. Format wejścia opisuje [format shape-notes](../raven-shape/references/shape-notes.md).

Skill jest generatorem, nie autorem. Nie wymyśla reguł biznesowych, kryteriów sukcesu, historyjek, priorytetów FR, kontroli dostępu ani non-goals. Czego brakuje w wejściu, to trafia do `## Open Questions`.

Pomiń, gdy użytkownik nie ma jeszcze notatek (wskaż `raven-shape`) albo chce precyzyjnie edytować istniejący PRD — skill zapisuje całe pliki.

## Kroki

1. **Wejście.** Ścieżka z argumentu (bez początkowego `@`) albo domyślnie `context/foundation/shape-notes.md`. Przeczytaj plik w całości. Gdy go nie ma, zaproponuj: najpierw `raven-shape` (zalecane), wklejenie surowych notatek albo anulowanie.
2. **Kontekst.** `context_type` z frontmatter notatek. Gdy go brak, oceń intencję i stan produktu (README, kod, historia; sam starter lub lockfile nie oznacza brownfield) i potwierdź wynik z użytkownikiem.
3. **Ocena wejścia.** Oceniaj znaczenie, nie nagłówki: akceptuj polskie i angielskie sekcje, FR w tabelach lub listach, scenariusze bez formalnego Given/When/Then. Zachowaj istniejące ID i źródła wymagań. Checkpoint shape'a pomaga wznowić pracę, ale nie dowodzi kompletności. Pytaj tylko o decyzje konieczne do ustalenia zakresu; zlecony szkic z niepełnych notatek wykonaj bez ponownego pytania.
4. **Generowanie w pamięci.**
   - Frontmatter według schematu: `status: draft` (nigdy wyżej), `version: 1`, `created` z `date +%Y-%m-%d`. Brakujące pole: `# TODO: <pole> — see Open Questions` i wpis w Open Questions. Bez pól stackowych (`team_profile`, `tech_preferences`, `deployment_constraint`).
   - Sekcje `##` dokładnie według schematu dla danego `context_type`, w jego kolejności. Bez sekcji spoza schematu (model danych, decyzje implementacyjne, testy, CI/CD).
   - Treść: przepisz wiernie słowa użytkownika, zmieniając tylko kształt wymagany schematem. Częściowa treść kończy się TODO; brak treści to nagłówek z TODO. Każde TODO ma numerowany wpis w Open Questions z konsekwencją luki. Jawnie uzasadniony brak reguły lub zmiany zapisz jako taki, nie jako lukę.
   - Brownfield opisuje różnicę, nie cały system: zachowania do utrzymania trafiają do `## Scope of Change` jako zachowane, a nie do Non-Goals.
5. **Kontrola przed zapisem.** Porównaj nagłówki i klucze frontmatter ze schematem oraz sprawdź podsekcje Success Criteria. Przejrzyj treść (poza brownfield `## Current System Overview`) pod kątem wycieku implementacji: dostawcy i usługi, notacja schematu/ORM, miejsce wykonania (client/server/edge), mechanizm egzekwowania (per IP, token bucket), elementy UI w NFR, protokoły, reguły domenowe opisane przez komponent („baza zapisuje…”). Nazwa produktu wskazanego przez użytkownika jako inspiracja lub wymagana integracja jest dozwolona z rolą i źródłem. Przy dryfie struktury lub wycieku **nie zapisuj**: pokaż konkretne trafienia i zaproponuj przeformułowanie na obserwowalną właściwość albo pozostawienie szczegółu w notatkach dla dalszego etapu.
6. **Zapis.** Gdy `prd.md` już istnieje, zapytaj: zapis jako `prd-vN.md` (zalecane; `N` = najwyższy istniejący numer + 1, `prd.md` liczy się jako v1, `version: N`), nadpisanie albo przerwanie.

## Finał

W czacie: ścieżka, `context_type`, sekcje wypełnione i oznaczone TODO, liczba Open Questions oraz szczegóły techniczne z notatek, które zostały poza PRD dla architektury lub stacku. Zaproponuj następny krok według rzeczywistego stanu projektu (zwykle `raven-architecture`; w brownfield to, czego faktycznie brakuje). Przy pliku wersjonowanym podaj dokładną ścieżkę. Nie uruchamiaj kolejnego skilla — PRD najpierw przegląda człowiek.
