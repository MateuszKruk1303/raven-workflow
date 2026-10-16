---
name: raven-manual-qa
description: Przeprowadź eksploracyjne QA działającej funkcji w przeglądarce na podstawie issue GitHub. Opublikuj plan scenariuszy z ticketa i implementacji. Sprawdź wymagania, przypadki brzegowe i nietypowe zachowania użytkownika; zgłoś wyłącznie potwierdzone problemy z Expected, Actual i reprodukcją. Użyj do dodatkowego sprawdzenia funkcji lub retestu, bez poprawiania kodu i tworzenia suite testów.
---

# Raven Manual QA

Przy wykonywaniu QA stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md): niezależny tester Astra/high.

Działaj jak dociekliwy tester manualny: korzystaj z rzeczywistego UI, rozumiej cel użytkownika i próbuj znaleźć sposób, w jaki pozornie działająca funkcja zawiedzie. Testuj wymagania oraz sensowne warianty, których autor mógł nie przewidzieć. Nie obiecuj absolutnej pewności ani braku wszystkich możliwych błędów.

To osobno zlecane QA, dostępne także dla zwykłego issue GitHub bez planu Raven. Nie wymaga wcześniejszego review, formalnego odbioru, osobnego briefu programisty ani nowej fazy planowania. Nie zastępuje osobistej akceptacji użytkownika, technicznego review ani trwałych testów. Nie uruchamiaj automatycznej pętli napraw.

## 1. Ustal ticket i kontekst

Przyjmij pełny URL issue, numer z jednoznacznym repo lub Raven ID. Przeczytaj AGENTS.md i istniejące powiązanie `context/foundation/github.json`, pełne issue, komentarze, kryteria odbioru oraz związane taski, PR i decyzje w zakresie testowanej funkcji. Przy niejednoznacznym tickecie ustal cel. Nie twórz issue ani konfiguracji Raven tylko po to, aby wykonać QA.

Rozdziel wymagania od sugestii implementatora. Kryteria i zaakceptowane decyzje są podstawą Expected. Happy path programisty to punkt startowy, nie granica testowania. Sprzeczne źródła albo niejasna reguła biznesowa wymagają ustalenia; nie zgłaszaj własnej preferencji jako błędu.

**Wskazówki programisty i dataset są opcjonalne.** Najpierw samodzielnie znajdź potrzebne informacje:

- URL środowiska, sposób uruchomienia, konta/role testowe i wersję builda: issue, komentarze/PR, README, instrukcje projektu, konfiguracja i działające usługi;
- dane: wskazane załączniki i pliki, katalogi fixtures, datasets, seeds, przykładowe CSV/JSON, istniejące scenariusze testowe oraz odpowiednie skrypty projektu;
- warunki scenariusza: format danych, powiązania rekordów, puste i wypełnione stany, daty oraz uprawnienia.

Szukaj celowo po nazwach i odniesieniach związanych z funkcją; nie czytaj całego dysku ani wszystkich datasetów. Przy dużym pliku sprawdź schemat i reprezentatywne rekordy. Nie wypisuj sekretów ani danych osobowych. Ustal przeznaczenie seed/import przed uruchomieniem: dataset może być do odczytu, a seed może kasować bazę. Nie uruchamiaj destrukcyjnego resetu lub migracji jako domyślnego przygotowania QA.

Wykorzystaj istniejące pasujące dane. W uzgodnionym środowisku testowym możesz utworzyć niewielkie, rozpoznawalne dane przez UI lub udokumentowany helper. Dobierz wartości samodzielnie, jeśli nie wymagają decyzji produktowej. Pytaj tylko o rzeczywisty brak: np. niedostępne konto, nieznany URL lub reset danych wymagający zgody. Brak wskazówek programisty nie blokuje QA.

## 2. Przygotuj rzeczywistą sesję

Przeczytaj [raven-browser](../raven-browser/SKILL.md) i zastosuj jego zasady połączenia, własnej karty, snapshotów, ochrony prywatnej sesji i artefaktów. Jeśli użytkownik wskazał inną przeglądarkę lub dostępne środowisko, respektuj ten wybór. Brak połączenia oznacza blokadę, nie zaliczenie testu.

**W tym skillu nie wykonuj instrukcji raven-browser „Napraw znalezioną regresję”.** Nie edytuj kodu produktu, testów, wymagań ani konfiguracji. Odczyt kodu/logów pomaga znaleźć dane lub zawęzić reprodukcję, ale nie zastępuje próby w UI. Nie generuj suite E2E. Narzędzia automatyzacji przeglądarki służą do wykonywania manualnych scenariuszy.

Ustal URL, środowisko, rolę i stan początkowy danych oraz faktycznie obsługiwaną wersję aplikacji. Lokalny HEAD nie dowodzi wersji zdalnego wdrożenia. Jeśli SHA jest niedostępny, zanotuj identyfikator builda lub brak możliwości ustalenia wersji i czas przebiegu. Gdy wersja zmieni się podczas QA, ponów zależne scenariusze albo oznacz je jako niesprawdzone.

Zwykłe operacje na danych testowych są częścią zlecenia. Zakupy, wysyłka wiadomości, publikacja i usuwanie rzeczywistych danych nie wynikają z samego dostępu do zalogowanej przeglądarki. Próby nadużycia wykonuj na własnych rekordach i kontach testowych, bez obciążania usługi, obchodzenia zabezpieczeń ani naruszania cudzych danych. Zatrzymaj konkretny scenariusz, jeśli nie można go wykonać w dozwolonym zakresie; kontynuuj niezależne testy.

## 3. Utwórz i opublikuj plan QA

Przed testowaniem opracuj plan scenariuszy na podstawie ticketa, zaakceptowanych decyzji oraz implementacji: diffu PR, istotnych widoków, walidacji, stanów, integracji i istniejących testów. Odczytaj kod w zakresie funkcji; nie przeprowadzaj pełnego review repo. Implementacja wskazuje dodatkowe ryzyka i miejsca do sprawdzenia, lecz nie jest wyrocznią Expected. Nie kopiuj błędnego aktualnego zachowania do oczekiwań. Jeśli kod lub diff są niedostępne, oprzyj plan na wymaganiach i obserwacji aplikacji, jawnie zaznaczając brak wglądu; nie udawaj analizy implementacji.

Opublikuj osobny komentarz **„Raven Manual QA — plan i przebieg”** z markerem `<!-- raven:manual-qa-plan issue=OWNER/REPO#NUMBER round=N -->`. To plan wykonania QA tego ticketa, nie globalna strategia raven-test-plan ani nowa wersja planu implementacji. Nie wymaga osobnego zatwierdzania przed rutynowymi testami objętymi zleceniem. Użyj [formatu planu QA](references/qa-plan.md).

Uwzględnij wszystkie kryteria browserowe, happy path i dobrane ryzyka eksploracyjne. Każdy scenariusz ma trwałe ID S1, S2, źródło, warunki/dane, konkretne kroki i Expected ustalone przed próbą. Kryteria spoza przeglądarki wskaż jako poza zakresem, bez pozornego PASS. Początkowo wyniki są NOT RUN.

Uzupełniaj ten sam komentarz po logicznych grupach prób i przed końcowym raportem: status, krótki Actual, dowód, faktycznie sprawdzona wersja i ewentualne QA-ID. Nowe scenariusze odkryte podczas eksploracji dopisuj z kolejnymi ID. Nie usuwaj nieudanych ani niewykonanych prób, nie zmieniaj Expected po fakcie, żeby uzyskać PASS. Jeśli oczekiwanie wymaga korekty, zapisz przyczynę i źródło decyzji oraz ponów próbę. Ten komentarz pozwala użytkownikowi zobaczyć zarówno wykonane scenariusze, jak i luki; końcowy raport pozostaje osobnym komentarzem tylko z problemami.

## 4. Testuj cel, potem szukaj niespodzianek

Prowadź wyniki zgodnie z opublikowanym planem. Lokalna kopia robocza pomaga przy utracie połączenia, ale nie zastępuje aktualizacji komentarza.

1. Przejdź pełną podstawową ścieżkę użytkownika. Sprawdź rezultat i utrwalenie po odświeżeniu lub ponownym otwarciu, nie tylko komunikat sukcesu.
2. Sprawdź wszystkie kryteria ticketa możliwe do zweryfikowania w przeglądarce. Pozostałe nazwij jako poza zakresem browser QA; nie zaliczaj ich na podstawie kodu lub deklaracji autora.
3. Dobierz eksplorację z [heurystyk QA](references/exploration.md) do ryzyka i zachowania aplikacji. Łącz działania, zmieniaj kolejność, przerywaj przepływ i wracaj. Nie wykonuj mechanicznie całej listy dla każdego ticketa.
4. Obserwuj UI i związane błędy konsoli/sieci. Dowodem defektu jest zaobserwowany skutek lub naruszenie kontraktu; ostrzeżenie z zewnętrznego skryptu samo nie jest błędem produktu.
5. Przy problemie zawęź warunki i wykonaj możliwie krótką reprodukcję. Jeśli bezpiecznie możliwe, powtórz z czystego stanu. Dla błędu sporadycznego podaj rzeczywistą częstość, np. 2/5, i zachowaj dowód; nie wymagaj deterministyczności ani nie wymyślaj jej.
6. Po znalezieniu błędu testuj dalej niezależne obszary. Nie kończ na pierwszym defekcie i nie produkuj wielu zgłoszeń tego samego problemu. Zakończ, gdy kryteria browserowe i dobrane istotne ryzyka zostały sprawdzone, a kolejna eksploracja nie daje nowego sygnału. Przy limicie czasu pokaż niewykonany zakres zamiast deklarować pełny sukces.

Po testach usuń wyłącznie własne dane tymczasowe, jeśli jest to bezpieczne; zachowaj minimalne dane potrzebne do reprodukcji i podaj ich identyfikatory. Przywróć zmienione ustawienia sesji/rozmiar okna. Nie resetuj środowiska współdzielonego. Jeśli cleanup się nie uda, wskaż pozostawione rekordy jako ograniczenie operacyjne.

## 5. Raportuj tylko problemy

Dla każdego potwierdzonego problemu użyj poniższego formatu. Expected musi mieć podstawę w tickecie, decyzji lub konkretnym niezmienniku, np. brak podwójnego zapisu po pojedynczej operacji. Nie publikuj spekulacji, niepotwierdzonej przyczyny, sugestii nowych funkcji ani pochwał między zgłoszeniami.

```text
QA-1 — Krótki tytuł opisujący skutek
Wpływ: krytyczny / istotny / drobny — konkretny skutek dla użytkownika
Scenariusz: S-ID z planu QA
Kontekst: URL/środowisko, build lub czas przebiegu, rola, dataset/rekord
Warunki wstępne: stan konieczny do odtworzenia
Expected: oczekiwany wynik + źródło wymagania lub niezmiennik
Actual: rzeczywiście zaobserwowany wynik
Reprodukcja:
1. ...
2. ...
3. ...
Powtarzalność: rzeczywisty wynik prób, np. 2/3
Dowód: screenshot/log/obserwacja, jeśli dostępne; bez prywatnych danych
```

Jeden problem = jeden wpis. Uporządkuj od największego wpływu. Wspólny kontekst można podać raz na początku raportu. Nie doklejaj tabeli PASS, pełnego dziennika prób ani checklisty sukcesów. Lokalnego screenshotu nie przedstawiaj jako publicznego linku.

**Brak problemów przy ukończonym sprawdzeniu:** zwróć krótko: „Funkcjonalność działa poprawnie w sprawdzonych scenariuszach — nie znalazłem problemów.” Dodaj identyfikację środowiska/builda i link do planu z wynikami. Nie twórz pustego raportu błędów i nie obiecuj pewności 100%.

**Niepełne sprawdzenie:** zwróć potwierdzone problemy, jeśli są, oraz oddzielną krótką informację „QA nieukończone: [blokada lub niesprawdzony zakres]”. Brak błędów przy zablokowanym logowaniu, niedostępnych danych albo niewykonanych istotnych scenariuszach nie uprawnia do komunikatu o poprawności. Kwestie do wyjaśnienia nie są fikcyjnymi defektami Expected/Actual.

## 6. Publikacja i retest

Domyślnie wywołanie tego skilla dla wskazanego issue obejmuje publikację planu QA, aktualizację jego przebiegu oraz osobny komentarz końcowy testera w tym issue. W czacie zwróć wynik i linki do obu komentarzy. Polecenie „tylko lokalnie”, „bez zapisu” lub ograniczenie dostępu ma pierwszeństwo. Nie twórz osobnych bug issues, PR ani wiadomości do innych osób. Nie zmieniaj statusu Project, wymagań ani checkboxów osobistego odbioru.

Komentarz końcowy zatytułuj **„Raven Manual QA — raport testera”**, oznacz rolę „Tester: raven-manual-qa” i dodaj link do planu tej rundy. Użyj markera `<!-- raven:manual-qa issue=OWNER/REPO#NUMBER round=N -->` z rzeczywistą tożsamością. Raport jest autorstwa roli testera, a nie podsumowaniem implementatora. GitHub wyświetli konto rzeczywiście użyte do publikacji; nie podszywaj się pod osobne konto człowieka lub bota i nie konfiguruj go przy okazji. Jeśli zapis wykonuje koordynator, zachowuje treść i autorstwo roli testera bez zmiany ustaleń. Przy sukcesie komentarz zawiera krótki komunikat, przy problemach tylko raport defektów, przy blokadzie także krótkie ograniczenie. Odczytaj wynik zapisu. Po timeout sprawdź marker i rundę każdego komentarza, zanim ponowisz publikację. Edytuj tylko własny komentarz planu bieżącej rundy; zachowuj dopiski użytkownika. Gdy publikacja planu jest niedostępna, kontynuuj wykonalne testy z lokalnym planem i zgłoś brak synchronizacji; nie deklaruj zapisania wyniku w issue. Błąd publikacji zgłoś oddzielnie od wyniku QA; gotowy raport oddaj w czacie.

Retest wykonuj na zlecenie. Utwórz nową rundę planu z linkiem do poprzedniej, zachowaj ID powtarzanych scenariuszy i rozpocznij ich wyniki od NOT RUN. Nie przenoś PASS na nową wersję aplikacji. Odczytaj poprzedni raport i wskazaną poprawioną wersję, powtórz reprodukcje i pobliskie regresje. Zachowaj ID problemów, które pozostały; nowe otrzymują kolejne ID. Nowa runda jest osobnym komentarzem, nie nadpisuje historii. Raport końcowy nadal zawiera tylko aktualne problemy; jeśli wszystkie sprawdzone problemy ustąpiły i retest jest kompletny, oddaj krótki komunikat sukcesu. Nie naprawiaj kodu i nie uruchamiaj implementatora automatycznie.
