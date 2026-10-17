# Format architecture.md

Domyślna lokalizacja: `context/foundation/architecture.md`. Dopasuj długość i nagłówki do produktu; pełny obraz nie oznacza obowiązkowej wielostronicowej specyfikacji. Nie pozostawiaj pustych szablonów.

Frontmatter:
- `status`: draft albo accepted;
- `revision`: kolejny numer przy merytorycznej zmianie;
- `updated`: rzeczywista data;
- `accepted_revision`: numer wyraźnie zaakceptowanej wersji, jeśli istnieje. Nie przenoś akceptacji na zmienioną wersję.

## Cel i granice

Krótki opis produktu, źródła wymagań, ograniczenia oraz co dokument rozstrzyga. Linki do PRD, shape, aktualnej roadmapy lub wskazanego trackera i istotnych researchów/decyzji. Nie kopiuj całej roadmapy ani statusów tasków.

## Obecny i docelowy system

Komponenty z odpowiedzialnościami i źródłami prawdy. Prosty diagram Mermaid, jeśli ułatwi zrozumienie. Oznacz elementy istniejące i dopiero uzgodnione. Dla najważniejszych przepływów pokaż drogę żądania/danych i granice zaufania.

## Decyzje przekrojowe

Dobierz obszary do produktu:
- podział frontend/backend, domeny, miejsce logiki biznesowej;
- trwałe dane, pliki/media, referencje i metadane, retencja/usuwanie;
- uwierzytelnianie, autoryzacja, sekrety i dostęp do zasobów;
- integracje, API, webhooki, źródła potwierdzeń, ponowienia i idempotencja;
- cache, kolejki i zadania w tle, jeśli potrzebne;
- środowiska lokalne/testowe/produkcyjne, procesy, deployment i storage;
- wykrywanie błędów, backup/odtwarzanie, właściciel utrzymania i koszty;
- ograniczenia technologiczne, rozszerzenia vs własne mechanizmy, skalowanie zgodne z wymaganiami.

Dla danych/pliku wyjaśnij: co przechowujemy, gdzie, kto jest właścicielem, kto ma dostęp, jak powstaje/znika i jak zapewniamy trwałość. Unikaj samej etykiety „S3” lub „Postgres”. Nie wpisuj sekretów ani wartości połączeń.

Dla każdej istotnej decyzji podaj:

| Pole | Treść |
| --- | --- |
| ID | Stabilne A-001, A-002 itd.; nie renumeruj |
| Status | ustalone / propozycja / do rozstrzygnięcia / odroczone / zastąpione |
| Decyzja | Jednoznaczna zasada oraz jej zakres i środowisko |
| Powód i alternatywy | Dlaczego pasuje do wymagań; najistotniejszy kompromis odrzuconych opcji |
| Konsekwencje | Ograniczenia kodu, integracji i utrzymania; koszt bez fikcyjnych estymacji |
| Źródło | Decyzja użytkownika i data, dokument/issue lub dowód kodowy |

Można użyć krótkich podsekcji zamiast powtarzania tabel. Fakt z kodu nie jest automatycznie zaakceptowaną zasadą na przyszłość. Zmiana decyzji zachowuje jej tożsamość i wskazuje zastąpienie; nie przepisuj historii zgód.

## Otwarte punkty i konsekwencje dla changes

Każdy nierozstrzygnięty temat: pytanie, wpływ, potrzebny dowód/decydent, moment rozstrzygnięcia i link do dotkniętego change, jeśli istnieje. Świadome odroczenie nie blokuje akceptacji dokumentu, jeśli użytkownik zaakceptował jego granice. Nie twórz z tego drugiej roadmapy ani planu wykonania.

## Źródła i aktualizacja

Podaj badany HEAD/dirty state, odnośniki do dokumentów i daty sprawdzenia źródeł dostawców. Nie przedstawiaj istniejącego kodu jako sprawdzonego runtime bez dowodu. Gdy plan change narusza ustaloną zasadę, wymaga jawnego rozstrzygnięcia, a po zaakceptowanej zmianie aktualizacji dokumentu.
