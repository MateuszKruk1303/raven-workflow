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

## Ryzyka i bramki
[Ochrona zachowania, migracja/rollback, konkretne ryzyka i testy. Manual gates tylko gdy rzeczywiście potrzebne. Dodatkowy tester/audyt tylko z uzasadnieniem.]
<!-- raven:contract:end -->

## Akceptacja kontraktu
- Fingerprint: [wartość z runtime fingerprint]
- Decyzja i źródło: [rzeczywista wypowiedź/link; brak zgody oznacz wprost]

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

Nie kopiuj wymaganej treści kroków do drugiego edytowalnego kontraktu w Progress. Checklista wskazuje ich ID. Review i akceptacja odnoszą się do całego bloku kontraktu; zmianę technicznego podejścia lub test obligations traktuj jak zmianę kontraktu. Historia Git przechowuje poprzednie wersje bez snapshotów GH.

## Mała zmiana

Dla jednozdaniowej poprawki dokumentacji wystarczy krótki kontrakt w jednym akapicie/listach: ID/cel i źródło, jedno AC, zakres/wyłączenia, potrzebna decyzja, P1 i adekwatna kontrola (np. diff). Zachowaj markery, fingerprint/źródło akceptacji, jeden checkbox P1 i jeden checkpoint JSON z rzeczywistym base/branch/head/next. Nie wypełniaj pustych wielkich sekcji ani nie wymyślaj test suite. Liczy się komplet informacji, nie liczba nagłówków.
