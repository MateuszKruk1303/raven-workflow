# Niezależny tester przeglądarkowy

Obowiązkowa część review funkcjonalności dostępnej przez przeglądarkę. Wykonywana automatycznie po implementacji i po zleconych poprawkach, zanim koordynator przedstawi komplet wyników użytkownikowi. Nie zastępuje technicznego review ani późniejszego sprawdzenia użytkownika, test suite i checków przed merge. Nie wymaga tworzenia ani utrzymywania testów E2E w repo — to rzeczywiste sprawdzenie przez narzędzia przeglądarkowe.

## Agent i środowisko

Koordynator uruchamia NOWEGO testera (`fork_turns="none"` lub odpowiednik), innego niż implementator i reviewer kodu, bez ich transkryptów. Przekazuje pełną treść ticketa/change i kryteriów sub-issues, zaakceptowany snapshot planu, decyzje produktowe, repo/worktree, oceniany SHA, URL aplikacji, sposób startu, dostępne dane testowe, tę instrukcję i absolutną ścieżkę `raven-browser/SKILL.md`. Podsumowanie implementatora nie zastępuje wymagań.

Tester czyta raven-browser i stosuje jego wybór trybu: domyślnie Playwright CLI we własnej nazwanej sesji; Brave przez MCP tylko na wyraźne polecenie lub zgodę użytkownika na użycie przeglądarki. Przy potwierdzonym ograniczeniu CLI tester może przekazać koordynatorowi uzasadnioną prośbę o osobistą przeglądarkę zgodnie z raven-browser; przełączenie wymaga zgody użytkownika. Koordynator przekazuje polecenie lub zgodę, jeśli padły; samo zlecenie browser-review nie wybiera MCP. W obu trybach obowiązują snapshoty, dobór interakcji i ochrona sesji użytkownika. **W roli testera nie stosuje polecenia raven-browser „Napraw znalezioną regresję”**: nie edytuje kodu, testów, wymagań, konfiguracji ani danych rzeczywistych. Zgłasza problem i kończy scenariusz. Potwierdzone niespełnienie wymagania uruchamia naprawę przez implementatora zgodnie z poniższą pętlą; tester pozostaje niezależny i sam nie naprawia kodu.

Przed testem zweryfikuj, że serwer obsługuje wskazany worktree/build i oceniany SHA. Sam dostępny localhost nie wystarcza. Zapisz URL, środowisko, sposób ustalenia wersji i stan danych. Nie restartuj obcych serwerów ani prywatnej przeglądarki bez uprawnienia. Brak narzędzi, logowania, poprawnego serwera lub danych to BLOCKED/NOT VERIFIED, nie PASS. Nie zastępuj wizyty w przeglądarce samym HTTP, analizą kodu lub twierdzeniem implementatora.

Koordynator zamraża kod na czas sprawdzenia przez testera. Techniczny reviewer nie jest jeszcze uruchamiany: jego etap zaczyna się dopiero po potwierdzeniu wszystkich wymagań przez testera. Implementator poprawia kod między przebiegami testera, nigdy równolegle z nimi. Jeden agent steruje wspólną przeglądarką w danym czasie. Jeśli wersja kodu/serwera zmieni się podczas testu, oznacz dotknięte wyniki jako nieaktualne i sprawdź je ponownie na ustalonej wersji.

## Izolacja i sprzątanie

Przed scenariuszem ustal fixture/seed, unikalny identyfikator danych bieżącego przebiegu i sposób cleanup. Używaj środowiska oraz kont testowych. W bloku końcowym usuń wyłącznie własne dane i zamknij własną sesję CLI, także po FAIL; nie resetuj cudzej bazy. Zapisz nieudany cleanup jako blokadę powtarzalności. Nie przenoś storageState ani sekretów osobistej przeglądarki do testów, repo lub raportu.

## Pokrycie wymagań

1. Wyprowadź listę WSZYSTKICH kryteriów z ticketa i tasków, nie tylko happy path lub elementów wspomnianych przez implementatora. Zachowaj istniejące ID; jeśli ich brak, nadaj lokalne ID AC1, AC2 z cytatem i linkiem do sekcji źródłowej. Nie modyfikuj wymagań w GH.
2. Dla każdego kryterium ustal warunki wstępne, kroki w UI i oczekiwany rezultat. Uwzględnij istotne warianty, walidacje, błędy, trwałość po odświeżeniu, nawigację i role, jeżeli wynikają z wymagania. Przy wymaganiach wizualnych sprawdź screenshot oraz wymagane rozmiary ekranu. Nie wymyślaj nowego zakresu produktu.
3. Wykonaj interakcje i sprawdź rezultat: zapis i ponowny odczyt, zmianę stanu, komunikat błędu czy wynik nawigacji. Widoczny przycisk lub screenshot samej strony nie dowodzi całego przepływu. Sprawdź związane błędy konsoli i sieci. Korzystaj z danych testowych; zakup, wysłanie wiadomości, publikacja lub usunięcie rzeczywistych danych wymagają osobnego upoważnienia.
4. Kryterium nienadające się do sprawdzenia w UI oznacz NOT APPLICABLE TO BROWSER i wykonaj odpowiednią inną weryfikację (np. test integracyjny/API), zapisując osobny wynik i dowód. NOT APPLICABLE TO BROWSER nie oznacza PASS wymagania; niewykonalna kontrola pozostaje BLOCKED/NOT VERIFIED i blokuje review techniczne. Nie uznawaj go za spełnione na podstawie kodu. Niejasne kryterium lub brak warunków oznacz jako lukę do decyzji, nie interpretuj na korzyść implementacji.

Celem jest pokrycie 100% jawnych kryteriów przeglądarkowych. Raport rozróżnia pokrycie (wykonane / wszystkie właściwe kryteria) oraz zgodność (PASS / wszystkie właściwe kryteria). FAIL jest sprawdzonym kryterium, lecz nie spełnionym. BLOCKED/NOT VERIFIED nie wypadają z mianownika. Wskaż osobno kryteria spoza przeglądarki. Nie pisz „funkcja w 100% poprawna”: możliwe jest „wszystkie N kryteriów przeglądarkowych spełnione na SHA X w opisanych scenariuszach”, jeśli każdy wiersz ma dowód PASS. To nie gwarancja wszystkich możliwych zachowań ani akceptacja użytkownika.

## Raport i poprawki

Tester zwraca raport do artifact_dir; nie zapisuje GH. Raport zawiera wersję planu i SHA aplikacji, środowisko oraz tabelę:

`Kryterium + źródło | Scenariusz/kroki | Oczekiwane | Zaobserwowane | PASS/FAIL/BLOCKED/NOT VERIFIED/NOT APPLICABLE TO BROWSER | Dowód`

Dowody: rzeczywiste obserwacje narzędzi, zwięzłe logi i screenshoty bez sekretów/danych prywatnych. Koordynator publikuje raport jako komentarz `<!-- raven:browser-review change=C-03 round=1 -->`, z wynikiem pokrycia, lukami i stabilnymi uwagami `B1`, `B2` (oddzielnie od F1 review kodu). Gdy artefaktu nie można bezpiecznie opublikować w GH, opisz obserwację w raporcie, oznacz screenshot jako lokalny; nie twórz fałszywego linku ani nie wysyłaj go do zewnętrznego hostingu. Kolejna runda zachowuje poprzedni raport.

## Automatyczna pętla napraw wymagań

Potwierdzony FAIL powiązany z jednoznacznym kryterium zaakceptowanego ticketa jest wystarczającym upoważnieniem do poprawki w jego zakresie. Nie pytaj użytkownika, czy naprawić niedziałający wymagany przepływ. To wyjątek od ręcznego triage uwag technicznego reviewera, nie zgoda na dowolne sugestie usprawnień.

1. Zapisz raport B i checkpoint w GH. Przekaż implementatorowi ID kryterium, oczekiwany wynik, kroki odtworzenia, dowody i oceniony SHA. Nie zmieniaj wymagań ani asercji, żeby uzyskać PASS.
2. Dla efektywności wznów ostatniego implementatora przez follow-up, jeśli host zachował jego kontekst i dotyczy on tej samej zmiany. Przekaż aktualny HEAD oraz zmiany od poprzedniego wykonania; agent ponownie odczytuje dotknięty kod. Jeśli kontekst jest niedostępny/nieaktualny albo agent powtarza błędne założenie, uruchom świeżego implementatora z trwałego checkpointu. Nigdy nie zamieniaj testera lub reviewera w implementatora.
3. Implementator poprawia zgłoszony defekt, wykonuje bramki Raven, zapisuje commit i przekazuje checkpoint. Podczas edycji tester nie operuje na aplikacji. Koordynator publikuje wynik, ustala nowy SHA i potwierdza wersję serwera.
4. Wznów niezależnego testera (lub uruchom nowego, jeśli jego kontekst jest niedostępny). Zachowana sesja testera jest niezależna, bo nigdy nie pisał kodu i nie dziedziczy transkryptu implementatora. Tester ponownie wykonuje nieudane scenariusze i właściwe regresje; samo zapewnienie implementatora nie wystarcza.
5. Powtarzaj dla potwierdzonych defektów w zakresie ticketa. Po uzyskaniu PASS wykonaj końcowy przebieg całego wymaganego przepływu i wszystkich kryteriów przeglądarkowych na finalnym SHA. Poprzednie wyniki można wykorzystać do kierowania naprawą, ale nie zastępują końcowego pełnego przebiegu. Pełna macierz pozostaje w raporcie każdej rundy.
6. Dopiero gdy wszystkie kryteria funkcjonalne ticketa mają PASS z dowodami na finalnym SHA (włącznie z kontrolami poza UI), przekaż koordynatorowi zielony raport otwierający bramkę. Koordynator dopiero teraz spawnuje świeżego reviewera technicznego finalnego diffu. Reviewer przygotowuje raport F oraz instrukcję ręcznych checków dla użytkownika; F podlegają decyzji użytkownika. Po zleconych poprawkach kolejność pozostaje taka sama: implementator → tester aż do PASS → świeży reviewer. Nie uruchamiaj reviewera wcześniej ani równolegle z testerem.

Nie zapętlaj się bez postępu: po dwóch nieskutecznych poprawkach tego samego scenariusza lub ponownym nawrocie tej samej regresji zakończ automatyczne próby i pokaż blokadę z dowodami oraz dotychczasowymi próbami. Nie nazywaj wyniku gotowym do odbioru. Liczniki prób zapisuj w checkpointach, nie resetuj przy zmianie agenta/wznowieniu. Nowa decyzja produktowa, sprzeczne wymagania, konieczność zmiany kontraktu lub brak bezpiecznego środowiska również wracają do użytkownika. BLOCKED/NOT VERIFIED nie jest defektem do ślepego naprawiania kodem.

Gotowość przepływu do odbioru wymaga wszystkich kryteriów funkcjonalnych ticketa PASS na finalnym SHA, bez FAIL/BLOCKED/NOT VERIFIED, oraz kompletnego technicznego review tej wersji. Przedstaw użytkownikowi oba raporty i pozostałe uwagi F do decyzji. Kryteria poza UI wymagają osobnych dowodów przed uruchomieniem technicznego review. Osobisty odbiór i jawnie wydzielona późniejsza faza testów/checków przed merge pozostają odrębnymi etapami; nie przenoś do nich brakującej weryfikacji wymagań funkcjonalnych. Gotowość do osobistego odbioru nie jest Done, zgodą na PR, merge ani zaliczeniem późniejszych testów.

Użytkownik może jawnie zatrzymać pętlę lub zaakceptować wyjątek; zapisz decyzję, zachowując rzeczywisty FAIL i nie deklarując 100% spełnienia wymagań. Sugestie wykraczające poza wymagania nie uruchamiają automatycznych napraw.

Sprawdzenie przez testera nie odhacza pól wymagających osobistego odbioru użytkownika. Dla zmian wyłącznie dokumentacyjnych/backendowych bez scenariusza UI koordynator zapisuje uzasadnione „nie dotyczy”; nie uruchamia pozornej wizyty w przeglądarce. Niezależny tester weryfikuje wtedy wymagania adekwatnymi kontrolami poza UI przed uruchomieniem technicznego review. Dla funkcji webowej nie wolno pominąć testera z powodu braku narzędzi — zgłoś nieukończony etap.
