---
name: raven-pilot-implement
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Implementuj lub wznów chunk Raven Pilot: implementator wykonuje całość A–Z, reviewer sprawdza wymaganie na krytycznym przepływie i zwraca konkretne błędy albo przekazuje wynik do odbioru użytkownika. Proste kontrole, bez rozbudowanego testowania."
---

# Raven Pilot Implement

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


Przeczytaj raz [kontrakt](references/contract.md), [orkiestrację](references/orchestration.md) i [synchronizację](references/synchronization.md); nie czytaj ponownie niezmienionych instrukcji. Brak referencji oznacza niepełną instalację.

Celem jest działające wymaganie gotowe do sprawdzenia przez użytkownika. Preferuj szybkie przekazanie użytecznego rezultatu; dopracowanie wariantów, przypadków brzegowych i pełne testy pozostają poza implementacją. Nie zmniejszaj uzgodnionego zakresu produktu, zmniejsz zakres jego automatycznej weryfikacji.

1. Agent główny koordynuje i zapisuje wspólny stan. Jeden implementator wykonuje cały chunk A–Z; osobny reviewer sprawdza rezultat. Używaj tych samych dwóch wątków także przy poprawkach. Bez dodatkowego planisty, audytora ani agenta od testów. Nie symuluj niezależnego review, gdy delegacja jest niedostępna.
2. Odczytaj plan, stan i bieżący kod. Przy wznowieniu kontynuuj od zapisanego kroku, wykorzystując istniejące wyniki. Przed edycją ustaw `implementing`. Wymagane migracje ustalonej bazy dev wykonuj zgodnie z kontraktem; nie powtarzaj setupu ani zastosowanych migracji.
3. Implementator realizuje wszystkie zadania potrzebne do wymagania i integruje całość. Uruchamia tylko proste istniejące kontrole potrzebne do wychwycenia błędów, np. typecheck zmienionego pakietu i build potrzebny do uruchomienia. Nie tworzy testów, fixtures ani infrastruktury testowej. Przekazuje reviewerowi adres aplikacji, niesekretne dane demo, zakres zmiany i krótkie wyniki kontroli.
4. Reviewer sprawdza wymaganie na jednym reprezentatywnym krytycznym przepływie A–Z. Czyta tylko kod potrzebny do oceny konkretnej wątpliwości. Jeżeli działa, kończy `PASS` i przekazuje wynik do odbioru użytkownika. Nie rozpoczyna dodatkowego audytu, pełnej macierzy AC ani budowy scenariuszy Playwright.
5. Jeżeli wymaganie nie działa, reviewer zwraca `CHANGES_REQUIRED`: co nie działa, jak odtworzyć i oczekiwany wynik. Implementator naprawia; reviewer sprawdza wyłącznie poprawkę i jej bezpośredni wpływ. Nie uruchamiaj ponownie całej weryfikacji. Zasady zakończenia i ograniczenia pętli są w orkiestracji.
6. Po `PASS` zapisz `awaiting_review`, krótki techniczny `handoff.md` i zsynchronizuj roadmapę. Resztę weryfikuje użytkownik. Brak pełnego pokrycia AC lub niewykonane warianty nie blokują przekazania; zapisuj je jako niesprawdzone. Nie deklaruj pełnej weryfikacji ani akceptacji użytkownika.

## Przekazanie użytkownikowi

Końcowa odpowiedź ma zawierać: co działa, bezpośredni adres aplikacji i ewentualnie uruchomienie, kilka kroków odbioru z oczekiwanym wynikiem, potrzebne niesekretne dane demo, wykonane kontrole oraz znane braki i niesprawdzony zakres. Następny krok: `$raven-pilot-review <id>`.

Instrukcja odbioru jest wyłącznie w czacie; `handoff.md` zachowuje zwięzły kontekst techniczny i wyniki. Nie kopiuj logów i historii do kilku raportów. [Telemetria](references/telemetry.md) jest opcjonalna, tylko na żądanie; jej zbieranie nie jest częścią domyślnej implementacji. Pełne testy i archiwizacja są osobnymi etapami po akceptacji.
