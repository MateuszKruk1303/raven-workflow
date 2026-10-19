# Szablon lokalnego planu

Dostosuj rozmiar do jednego rezultatu. Nie dodawaj faz tylko dla wypełnienia szablonu. Wstaw rzeczywiste dane; usuń instrukcje w nawiasach. Wymagania, podejście, kroki i zobowiązania testowe są wewnątrz **jednego** bloku kontraktu. Checklista oraz checkpoint poza nim.

````markdown
# C-03 — [rezultat]

<!-- raven:contract:start -->
## Tożsamość i źródła
- ID: C-03
- Issue: [dokładny URL issue GH tego taska]
- Cel: [obserwowalny wynik]
- Źródła: [PRD/issue/Jira/ustalenie; wersja lub data istotnej decyzji]
- Punkt startowy: [istniejące zachowanie, kod, ograniczenia]

## Wymagania i kryteria odbioru
- AC1: [warunek → zachowanie → obserwowalny dowód]
- AC2: [istotny błąd lub granica]

## Zakres i wyłączenia
[Co change dostarcza; co pozostaje poza nim. Dla większego nierozdzielnego zakresu rzeczowe uzasadnienie.]

## Podejście i decyzje
[Granice modułów, kontrakty API/danych, istotna kolejność i decyzje. Detale wykonawcze pozostają wykonawcy.]

## Kroki i weryfikacja
- P1: [jeden potrzebny krok, dotknięte obszary, wymagane testy/dowód; powiązane AC]
- P2: [tylko jeśli potrzebny do tego samego rezultatu]

## Strategia weryfikacji
- Implementacja: [testy potrzebne przy kodzie, właściwe lint/typecheck/build i istniejące testy, krytyczna ścieżka dla auto; code review osobno, szerokie QA opcjonalnie; instrukcja ręczna wyłącznie w końcowej wiadomości czatu implementatora]
- Domknięcie regresji: [po ręcznej weryfikacji raven-test audytuje istniejącą ochronę i dowody; uzupełnia tylko nazwane luki, może zakończyć bez nowych testów]

## Ryzyka i bramki
[Ochrona zachowania, migracja/rollback, konkretne ryzyka i testy. Manual gates tylko gdy rzeczywiście potrzebne. Auto-implement ma jednego wykonawcę; osobno wywołane code review i opcjonalne szerokie QA nie uruchamiają się automatycznie.]
<!-- raven:contract:end -->

## Progress
- [ ] P1 — [krótki wynik; dowód po wykonaniu]
- [ ] P2 — [krótki wynik]

## Checkpoint
<!-- raven:checkpoint:start -->
{
  "stage": "planning",
  "issue": "[dokładny URL issue GH]",
  "owner": "[login wykonawcy GH]",
  "next": "plan review",
  "evidence": [],
  "repair_attempts": 0
}
<!-- raven:checkpoint:end -->
````

W checkpointcie wpisz rzeczywisty URL issue i potwierdzony stan trackingu; nie kopiuj placeholderów. Zwięzłe wyniki testów dopisuj w tym planie poza kontraktem, bez obowiązkowego osobnego test-report.md. Oddzielne plan-review.md i review.md zachowują dowody dwóch niezależnych ocen; nie są kolejnymi planami ani trackerami.

Nie kopiuj wymaganej treści kroków do drugiego edytowalnego kontraktu w Progress. Checklista wskazuje ich ID. Review odnosi się do całego bloku kontraktu; zmianę technicznego podejścia lub test obligations traktuj jak zmianę kontraktu. Historia Git przechowuje poprzednie wersje bez snapshotów GH.

## Mała zmiana

Dla jednozdaniowej poprawki dokumentacji wystarczy krótki kontrakt w jednym akapicie/listach: ID/cel i źródło, jedno AC, zakres/wyłączenia, potrzebna decyzja, P1 i adekwatna kontrola (np. diff). Zachowaj markery, fingerprint, jeden checkbox P1 i jeden checkpoint JSON z rzeczywistym base/branch/head/next. Nie wypełniaj pustych wielkich sekcji ani nie wymyślaj test suite. Liczy się komplet informacji, nie liczba nagłówków.

Checkpoint rozszerzaj dopiero rzeczywistymi wynikami: `implementation`, `checks`, `review`, `qa`, `manual_verification`, `test_stage`, `user_acceptance`, `publication`, `merge`. Ich znaczenie określa wspólny kontrakt. Nie dodawaj pól ani statusu akceptacji planu; `user_acceptance` opisuje późniejszy odbiór produktu. Historyczne pola zachowuj zgodnie ze wspólnym kontraktem. Zachowaj wymagania → test/asercja/QA → polecenia/wyniki/wersje i luki, aby raven-test mógł je wykorzystać bez przepisywania raportów.
