# Modele, niezależność i koszt wykonania

Jakość planu i niezależnego review ma pierwszeństwo przed oszczędnością tokenów.

| Rola | Model | Effort |
| --- | --- | --- |
| Planista, architekt, autor shape/PRD/roadmapy, strategii testów i syntezy researchu | `gpt-6-astra` | `high` |
| Projektant i autor instrukcji raven-create-skill | `gpt-6-astra` | `high` |
| Reviewer planu, kodu, testów i innych artefaktów | `gpt-6-astra` | `high` |
| Niezależny tester wymagań (również browser-review) | `gpt-6-astra` | `high` |
| Implementator produktu, autor testów, wykonawca poprawek i konfiguracji | `gpt-6.1-sol` | `low` |
| Ograniczony odczyt/poszukiwanie faktów bez decyzji architektonicznych | `gpt-6.1-sol` | `low` |

## Faktyczne uruchomienie

Przy delegowaniu ustaw jawnie `model` i `reasoning_effort` z tabeli oraz `fork_turns="none"` (lub rzeczywisty odpowiednik hosta). Nie polegaj na dziedziczeniu modelu koordynatora. Zapisz żądany model i potwierdzoną konfigurację; gdy host nie ujawnia modelu wykonania, oznacz ją jako niepotwierdzoną. Tekst promptu ani agents/openai.yaml nie przełącza modelu.

Dla etapu manualnego wykonuj pracę bezpośrednio, jeśli bieżąca konfiguracja odpowiada roli. W przeciwnym razie deleguj tę rolę do właściwego modelu, a pytania i decyzje użytkownika prowadź jako koordynator. To upoważnienie do delegowania zleconego etapu, nie do uruchamiania kolejnych etapów. Agent już uruchomiony w danej roli nie deleguje ponownie całego własnego zadania. Brak wymaganego modelu lub możliwości konfiguracji zgłoś przed zależną pracą; przedstaw przekazanie do odpowiedniej sesji. Nie zastępuj Astry Solem bez decyzji użytkownika i nie zmieniaj globalnej konfiguracji hosta.

Reviewer/tester jest świeży i nie dziedziczy transkryptu autora. Dostaje pełne wymagania, wersje źródeł, zakres/base/head, publiczne decyzje i dowody, a nie wyłącznie streszczenie autora. Koordynator publikuje artefakty zgodnie z kontraktem GH. Niezależność nie wymaga mnożenia kolejnych reviewerów: pojedynczy reviewer Astra może pokryć wszystkie wymiary małej zmiany. Dodatkowe role dobieraj do niezależnych ryzyk, np. auth, migracji lub współbieżności, a nie liczby plików.

## Eskalacja i dowody

Implementator zaczyna na Sol/low. Gdy potwierdzony problem rozumowania uniemożliwia realizację ustalonego kontraktu, podnieś effort do medium i zapisz przyczynę; nie zeruj liczników prób. Awaria środowiska wymaga naprawy środowiska, nie mocniejszego modelu. Niejasność wymagań lub zmiana architektury wraca do planisty Astra i odpowiedniej decyzji użytkownika. Zachowaj limity napraw danego etapu.

Ładuj pełne wymagania i obowiązujące kontrakty, lecz procedury wykonawcze tylko dla aktualnej roli i warstwy testów. Przekazuj ścieżki do źródeł zamiast kopiować cały transkrypt. Czytaj kod potrzebny do oceny zachowania i zależności, rozszerzając zakres przy niepewności; nie czytaj całego repo na zapas.

Wynik kontroli można wykorzystać ponownie tylko z poleceniem, wynikiem, identycznym drzewem kodu (także zmianami niecommitowanymi), konfiguracją, zależnościami i istotnym stanem środowiska. Reviewer sam ocenia wiarygodność dowodu i wykonuje kontrole rozstrzygające ryzyka; nie musi powtarzać całej kosztownej suite bez powodu. Zmiana kodu/środowiska unieważnia dotknięte dowody. Nigdy nie pomijaj wymaganej nowej kontroli ani powtórnego E2E służącego izolacji tylko dla oszczędności.

W istniejącym checkpointcie etapu zapisuj krótko role/model/effort, czas wykonania, liczbę rund napraw i potwierdzone defekty. Tokeny input/output/cache oraz koszt zapisuj wyłącznie gdy host je udostępnia; w przeciwnym razie `unknown`. Nie twórz dodatkowego raportu tylko dla metryk. Oceniaj koszt na zaakceptowany change wraz z regresjami i poprawkami po odbiorze, nie po samej liczbie agentów. Bez pomiaru nie deklaruj procentowej oszczędności.
