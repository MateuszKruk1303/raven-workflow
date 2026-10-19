---
name: raven-manual-qa
description: Przeprowadź dodatkowe eksploracyjne QA funkcji z lokalnego change, PR lub issue. Zapisz plan i potwierdzone defekty z reprodukcją w repo; bez poprawiania produktu i generowania suite.
---

# Raven Manual QA

QA wykonuje niezależny tester w świeżym kontekście, bez transkryptu autora.

Działaj jak dociekliwy tester manualny: korzystaj z rzeczywistego UI, rozumiej cel użytkownika i próbuj znaleźć sposób, w jaki pozornie działająca funkcja zawiedzie. Testuj wymagania oraz sensowne warianty, których autor mógł nie przewidzieć. Nie obiecuj absolutnej pewności ani braku wszystkich możliwych błędów.

To osobno zlecane QA, dostępne dla lokalnego change, PR albo zwykłego issue bez planu Raven. Nie wymaga wcześniejszego review, formalnego odbioru, osobnego briefu programisty ani nowej fazy planowania. Nie zastępuje osobistej akceptacji użytkownika, technicznego review ani trwałych testów. Nie uruchamiaj automatycznej pętli napraw. `raven-auto-implement` sprawdza działanie zmiany samodzielnie, według swojego poziomu weryfikacji, i nie uruchamia tego skilla automatycznie. Szersze QA pozostaje osobnym zleceniem.

## 1. Ustal ticket i kontekst

Przyjmij lokalny change/plan, branch, pełny URL PR/issue albo numer z jednoznacznym repo. Przeczytaj instrukcje, kontrakt i wskazane kryteria/decyzje oraz istotny diff. Odczytuj konkretne potrzebne wątki, nie pełną historię komentarzy/task issues. Przy niejednoznacznym celu ustal go; nie twórz issue ani konfiguracji Raven tylko dla QA.

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

## 3. Utwórz plan QA

Przed testowaniem opracuj plan scenariuszy na podstawie ticketa, zaakceptowanych decyzji oraz implementacji: diffu PR, istotnych widoków, walidacji, stanów, integracji i istniejących testów. Odczytaj kod w zakresie funkcji; nie przeprowadzaj pełnego review repo. Implementacja wskazuje dodatkowe ryzyka i miejsca do sprawdzenia, lecz nie jest wyrocznią Expected. Nie kopiuj błędnego aktualnego zachowania do oczekiwań. Jeśli kod lub diff są niedostępne, oprzyj plan na wymaganiach i obserwacji aplikacji, jawnie zaznaczając brak wglądu; nie udawaj analizy implementacji.

Zapisz `qa-plan.md` obok lokalnego planu change, albo we wskazanym miejscu raportów dla QA bez planu Raven. To plan wykonania QA, nie strategia globalna ani nowa wersja kontraktu. Nie wymaga osobnej akceptacji przed rutynowymi testami objętymi zleceniem. Użyj [formatu planu QA](references/qa-plan.md).

Uwzględnij wszystkie kryteria browserowe, happy path i dobrane ryzyka eksploracyjne. Każdy scenariusz ma trwałe ID S1, S2, źródło, warunki/dane, konkretne kroki i Expected ustalone przed próbą. Kryteria spoza przeglądarki wskaż jako poza zakresem, bez pozornego PASS. Początkowo wyniki są NOT RUN.

Uzupełniaj ten sam plik qa-plan.md po logicznych grupach prób i przed końcowym raportem: status, krótki Actual, dowód, faktycznie sprawdzona wersja i ewentualne QA-ID. Nowe scenariusze odkryte podczas eksploracji dopisuj z kolejnymi ID. Nie usuwaj nieudanych ani niewykonanych prób, nie zmieniaj Expected po fakcie, żeby uzyskać PASS. Jeśli oczekiwanie wymaga korekty, zapisz przyczynę i źródło decyzji oraz ponów próbę. Ten plan pozwala użytkownikowi zobaczyć wykonane scenariusze i luki; końcowy qa-report.md zawiera problemy lub krótki wynik sukcesu.

## 4. Testuj cel, potem szukaj niespodzianek

Prowadź wyniki w kanonicznym lokalnym qa-plan.md. Zapisuj postęp po grupie prób, tak aby wznowienie nie wymagało pamięci rozmowy.

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

Plan/przebieg zapisuj w qa-plan.md, a końcowy raport testera w qa-report.md obok niego. Historia Git zachowuje poprzednie wersje. Publikacja do komentarzy jest opcjonalna i wymaga objęcia jej zleceniem lub polityką; samo wskazanie issue nie nadaje nowych uprawnień. Raport jest autorstwa roli testera, nie podsumowaniem implementatora. Zachowaj ustalenia i rzeczywistą tożsamość autora. Nie twórz bug issues/PR ani nie zmieniaj trackera przy okazji.

Retest wykonuj na zlecenie. Utwórz nową rundę planu z linkiem do poprzedniej, zachowaj ID powtarzanych scenariuszy i rozpocznij ich wyniki od NOT RUN. Nie przenoś PASS na nową wersję aplikacji. Odczytaj poprzedni raport i wskazaną poprawioną wersję, powtórz reprodukcje i pobliskie regresje. Zachowaj ID problemów, które pozostały; nowe otrzymują kolejne ID. Nowa runda aktualizuje raport z zachowaniem poprzedniej wersji w Git. Raport końcowy nadal zawiera tylko aktualne problemy; jeśli wszystkie sprawdzone problemy ustąpiły i retest jest kompletny, oddaj krótki komunikat sukcesu. Nie naprawiaj kodu i nie uruchamiaj implementatora automatycznie.
