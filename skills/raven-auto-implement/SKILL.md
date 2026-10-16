---
name: raven-auto-implement
description: Realizuj lub wznów zatwierdzony plan change z GitHuba przez raven-implement, następnie prowadź pętlę implementator–niezależny tester do potwierdzenia wszystkich wymagań ticketa. Dopiero wtedy uruchom świeżego reviewera technicznego z raportem i instrukcją manualnego odbioru. Potwierdzone błędy wymagań tester kieruje automatycznie do poprawki i ponownego testu; uwagi reviewera kodu rozstrzyga użytkownik. Nie służy do przygotowania planu ani tworzenia roadmapy.
---

# Raven Auto Implement

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Procedury do odczytu przez wykonawcę właściwej roli (E2E tylko gdy wybrano tę warstwę): [implement](../raven-implement/references/procedures/implement/procedure.md); [impl-review](../raven-implement-review/references/procedures/impl-review/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż ścieżki procedur jego roli oraz kontrakt GH; koordynator nie musi ładować instrukcji wykonawczych innych ról. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Jesteś koordynatorem cyklu: **implementator → niezależny tester → automatyczne poprawki niespełnionych wymagań i ponowne testy → review finalnego kodu → odbiór użytkownika**. Zachowaj mechanikę Raven; dodaj orkiestrację i trwałe przekazanie pracy, zamiast projektować drugi proces implementacji. Nie implementuj ani nie oceniaj własnego kodu w roli koordynatora.

## Źródłowe skille i granice adaptacji

Najpierw przeczytaj [wspólny kontrakt GitHub](../raven-auto-plan/references/github-contract.md). GitHub przechowuje plan, postęp, raporty i decyzje; lokalne pliki Raven są wyłącznie kopiami roboczymi w artifact_dir. Kontrakt ten ma pierwszeństwo w kwestiach transportu i przechowywania.

Implementator czyta procedurę implementacji, implementation-discipline.md i progress-format.md; reviewer procedurę review. Agentom przekaż rzeczywiste absolutne ścieżki tych plików.

Zachowaj z Raven: plan i `change.md`, fazy, `## Progress` jako format postępu (kanoniczne dane w taskach GH), klasyfikację Minor/Structural, preflight bramek, dyscyplinę implementacji, weryfikację i limit prób naprawienia bramki, celowy staging, commity kodu faz (bez epilogu lokalnych artefaktów), sześć wymiarów review, dowody, ważność uwag i zapis raportu. Respektuj instrukcje projektu oraz uzgodniony zakres testów; nie dodawaj E2E ani infrastruktury dlatego, że skill jest używany.

Poniższe adaptacje realizują uzgodniony workflow Raven i mają pierwszeństwo w miejscach kolizji ze źródłowymi skillami:

- Wybór trybu jest już dokonany: świeży implementator realizuje plan we własnym kontekście. Nie pyta o delegowanie każdej fazy ani o kontynuowanie następnej. Domyślnie wykonuje wszystkie pozostałe fazy implementacyjne, chyba że użytkownik ograniczył zakres. Jeśli plan jawnie wydziela późniejszą fazę testów/checków przed merge, pozostaw ją do tego etapu i nazwij w handoffie; nie pomijaj jednak bramek przypisanych do implementacji.
- Lokalne commity własnych zmian i standardowe komunikaty Raven są częścią zlecenia; nie pytaj o zatwierdzenie każdego komunikatu. Nie dołączaj cudzych zmian ani istniejącego stagingu. Przy nakładających się zmianach wymagających rozstrzygnięcia wróć do użytkownika. Nie pushuj, nie otwieraj PR i nie merge'uj bez odpowiedniego zlecenia.
- Zachowaj rzeczywiste manual gates zapisane w planie i pytania o rozbieżności Structural. Nie twórz pustego pytania o manual verification, gdy plan nie wymaga żadnej. Nie odhaczaj odbioru użytkownika na podstawie testów agenta.
- Dopiero po potwierdzeniu wszystkich wymagań przez testera końcowe review techniczne uruchamia się automatycznie jako NOWY agent. Nie pytaj, czy uruchomić review.
- Reviewer kończy na zapisaniu raportu. Interaktywny triage i edycje z kroku 5 `raven-implement-review` należą do koordynatora oraz nowego implementatora, nigdy do reviewera.
- Zakres diffu pochodzi z jawnie zapisanych SHA, nie z heurystyki daty planu opisanej w Raven.
- W Ravenie GitHub jest źródłem kolejki i statusów. Nie twórz ani nie synchronizuj lokalnego `roadmap.md`.

## 1. Rozpoznaj zlecenie i stan

Przyjmij Raven ID, issue lub kontynuację wcześniejszej rozmowy. Lokalna ścieżka może wskazać jedynie kopię roboczą; rozwiąż jej źródło w GH. Stary plan istniejący wyłącznie lokalnie wymaga jawnej migracji przez raven-auto-plan, nie cichej zmiany źródła prawdy. Rozróżnij: realizacja planu, wznowienie, zlecenie poprawek, akceptacja wyniku, prośba tylko o status. Status jest tylko do odczytu. Nie wybieraj arbitralnie najnowszej zmiany, gdy kontekst wskazuje kilka możliwości.

Odczytaj instrukcje repo, cały plan rodzica i tasków, dostępne lessons, snapshot, wcześniejsze raporty oraz decyzje z GH. Potwierdź zgodność aktualnego fingerprintu z zaakceptowaną wersją, a potem odtwórz adapter Raven. Nie modyfikuj archiwów. Brak planu lub istotne nierozstrzygnięte decyzje oznaczają powrót do przygotowania, nie generowanie planu podczas implementacji. Jawne „zrealizuj ten plan” stanowi zgodę na realizację; nie pytaj drugi raz o tę samą zgodę.

Sprawdź Git: repo, branch/worktree, HEAD, staging i istniejące niezacommitowane zmiany. Zapewnij izolację pracy bez resetowania lub przenoszenia cudzych edycji. Bez repo Git i ustalonego zakresu nie da się zapewnić cyklu commitów oraz niezależnego review: zgłoś brak, nie inicjalizuj ani nie łącz repo po cichu.

W komentarzu checkpointu `raven:execution` utrzymuj branch, bazowy SHA zmiany, oceniany SHA, wersję planu, rundę i linki do raportów/decyzji. Zapisz bazowy SHA PRZED pierwszą edycją. Przy wznowieniu zachowaj bazę; przy przejmowaniu rozpoczętej zmiany ustal ją z istniejących commitów i zakresu, nie przyjmuj bieżącego HEAD jako początku wcześniejszej pracy. Postęp faz zapisuj w blokach Progress właściwych tasków. Nie twórz drugiego kanonicznego stanu w change.md/JSON.

## 2. Uruchom implementatora

Ten skill jawnie wymaga delegowania. Utwórz nowego agenta bez historii rozmowy (`fork_turns="none"` lub odpowiednik hosta). Nie przekazuj mu pełnego transkryptu. Pakiet wejścia obejmuje:

- ścieżkę repo/worktree, change-id, plan, instrukcje projektu i wymagane źródła oraz repo_root i artifact_dir;
- ścieżkę [implement](../raven-implement/references/procedures/implement/procedure.md) oraz niniejszego skilla z adaptacjami;
- zatwierdzony zakres, decyzje użytkownika, początkowy stan Git i bazowy SHA;
- w rundzie poprawkowej: raport, jawnie zlecone ID uwag, decyzje dotyczące pozostałych uwag i ewentualny wybrany sposób naprawy.

Agent wykonuje `raven-implement` we własnym kontekście, z bramkami, stagingiem kodu i roboczym Progress. Nie zapisuje do GH. Na granicy każdej fazy przekazuje koordynatorowi checkpoint; koordynator publikuje postęp i dowody, potwierdza zapis i pozwala kontynuować. Nie prosi użytkownika o rutynowe przejście do następnej fazy. Nie stage’uje kopii artefaktów ani nie wykonuje ich commitu epilogu. Dla poprawek nie wykonuje ponownie odhaczonych faz: stosuje dyscyplinę i bramki Raven do zleconego diffu, zachowuje historię planu i zwraca dowody napraw do osobnego checkpointu, bez nadpisywania historycznego raportu review. Zmiana kontraktu wymaga decyzji użytkownika.

Wymagaj zwrotu: wykonany zakres, zmienione pliki, commity/HEAD, wyniki kontroli, oczekujące manual gates, rozbieżności i blokady. Agent zapisuje roboczy stan przed zakończeniem; koordynator utrwala go w GH. Pytania kieruje do koordynatora, który przekazuje je użytkownikowi. Przy konieczności wznowienia uruchom świeżego agenta z zapisaną decyzją.

Nie przerywaj siłą prawidłowo kończącego się procesu. Poczekaj na zakończenie implementatora, sprawdź stan Git i brak działających procesów modyfikujących kod. Nie używaj tego agenta jako reviewera/testera. W automatycznej pętli błędów wymagań możesz wznowić go jako implementatora zgodnie z kontraktem browser-review; poprawki z ręcznego triage nadal mogą trafić do świeżego implementatora. Jeśli host nie wspiera świeżych agentów, zgłoś brak i przygotuj przekazanie do nowej sesji; nie udawaj niezależności przez zmianę roli w tej samej rozmowie.

## 3. Implementator i niezależny tester — do spełnienia wymagań

Po zakończonej implementacji zapisz oceniany HEAD. Ustal pełny diff `base_sha..reviewed_sha`; przy poprawkach zapisz także poprzedni oceniony SHA jako bazę diffu poprawkowego. Review nie startuje na ruchomym stanie kodu. Nie chowaj niezatwierdzonych zmian produktu: dokończ przekazanie lub zgłoś blokadę. Raporty i checkpointy znajdują się w GH i nie należą do diffu kodu.

Uruchom świeżego niezależnego testera bez historii implementatora. Przeczytaj i przekaż mu [kontrakt testów przeglądarkowych](references/browser-review.md), a dla funkcji webowej także raven-browser. Tester rzeczywiście wykonuje scenariusze w przeglądarce i utrzymuje macierz wszystkich kryteriów ticketa. Kryteria poza UI sprawdza odpowiednimi kontrolami; brak scenariusza UI nie zwalnia z weryfikacji wymagań.

Koordynator publikuje raport z dowodami i uwagami B1, B2. Potwierdzony FAIL w zakresie ticketa automatycznie wznawia implementatora, a po poprawkach niezależnego testera. Stosuj pętlę, limity prób i checkpointy z kontraktu. Tester nigdy sam nie poprawia kodu.

**Nie spawnuj, nie wznawiaj ani nie uruchamiaj technicznego reviewera, dopóki tester nie potwierdzi PASS wszystkich kryteriów funkcjonalnych ticketa na finalnym SHA.** Nie wykonuj review technicznego równolegle ani wstępnie. FAIL, BLOCKED, NOT VERIFIED lub brak dowodu zatrzymują przejście. Samo pokrycie scenariuszy nie wystarcza: każdy musi zakończyć się oczekiwanym rezultatem. Utrwal raport i przejście bramki w GH wraz z SHA i wersją wymagań.

Osobisty odbiór użytkownika oraz jawnie wydzielone późniejsze testy/checki przed merge pozostają oczekujące. Nie są zastępstwem dowodów spełnienia wymagań funkcjonalnych i nie wolno odkładać pod ich nazwą niezweryfikowanego kryterium ticketa. „100%” oznacza wszystkie uzgodnione kryteria z dowodami w opisanych scenariuszach, nie gwarancję braku dowolnego błędu.

## 4. Świeży reviewer techniczny — po bramce testera

Sprawdź, że HEAD i wymagania nadal odpowiadają zielonemu raportowi testera. Zmiana kodu lub wymagań cofa proces do weryfikacji przez testera; wcześniejszy PASS nie otwiera bramki dla nowej wersji.

Uruchom NOWEGO reviewera bez dziedziczenia rozmowy implementatora. Przekaż mu surowe źródła: wymagania, plan, instrukcje repo, base/reviewed SHA, wcześniejszy raport i decyzje użytkownika. Podsumowanie implementatora jest twierdzeniem do sprawdzenia, nie dowodem poprawności.

Reviewer czyta i wykonuje `raven-implement-review`: analizuje zgodność, zakres, bezpieczeństwo i jakość, architekturę, wzorce oraz kryteria sukcesu. Zgodnie ze wspólną procedurą review obejmuje WSZYSTKIE dostarczone fazy i cały wskazany diff kodu, także gdy manual checks lub późniejsze testy są oczekujące. Wymień ocenione fazy, a brakujące kontrole/odbiór raportuj oddzielnie bez deklarowania PASS lub pełnego ukończenia planu. Może delegować przewidziane przez Raven odczyty w dostępnych slotach. Nie zmienia kodu, planu, testów ani statusów GitHuba; zapisuje tylko własny raport i wykonuje niezbędną weryfikację bez destrukcyjnych skutków.

Reviewer zwraca raport w artifact_dir, zachowując format i marker raportu Raven. Koordynator publikuje oddzielny komentarz każdej rundy w głównym change issue zgodnie z kontraktem GH. Dodaj ocenione SHA i zakres. Zachowuj ID `F1`, `F2` itd. między rundami; nowe uwagi otrzymują kolejne nieużyte ID. Dla każdej uwagi zachowaj dowód `path:line`, skutek, ważność i konkretną propozycję rozwiązania. Nie wymuszaj liczby uwag.

W rundzie poprawkowej reviewer sprawdza zlecone naprawy i regresje w ich obszarze, uwzględniając pełny kontekst zmiany. Nie powtarza całego audytu bez powodu. Uwagi zaakceptowane lub odrzucone przez użytkownika nie stają się ponownie żądaniem naprawy bez nowego dowodu lub zmiany ryzyka; taką różnicę trzeba jawnie opisać. Sam raport technicznego reviewera nie uruchamia automatycznej poprawki. Wyjątkiem jest niezależnie potwierdzone przez testera niespełnienie kryterium ticketa, obsługiwane przez pętlę browser-review.

Raport reviewera musi zawierać także **instrukcję manualnych checków użytkownika**: sposób uruchomienia i URL, potrzebną rolę/konto oraz dane testowe (bez sekretów), numerowane kroki i oczekiwany wynik dla głównych przepływów ticketa oraz istotnych wariantów błędów. Powiąż scenariusze z kryteriami, wskaż co tester już potwierdził, co użytkownik ma ocenić osobiście i jakie późniejsze checki pozostają. Instrukcja ma pozwalać wykonać odbiór bez rekonstruowania planu. Koordynator publikuje ją razem z raportem technicznym w GH i przekazuje w czacie.

## 5. Decyzja użytkownika i poprawki

Przedstaw wynik w czacie: co zrealizowano, co sprawdzono i czego nie sprawdzono, zwięzłe uwagi F z review kodu i B z przeglądarki, pokrycie kryteriów ticketa oraz sposób ręcznego odbioru. Nie każ użytkownikowi otwierać raportu, aby zrozumiał problem. Werdykt techniczny reviewera nie jest decyzją odbioru.

Po zakończeniu automatycznej pętli testera i review finalnej wersji czekaj na decyzję użytkownika. Dotyczy to również review bez uwag. Po zablokowaniu pętli pokaż problem, nie gotowość do odbioru. Użytkownik może zaakceptować wynik mimo uwag, zlecić wszystkie poprawki, wybrać ID, wskazać inne rozwiązanie lub zatrzymać pracę. Brak odpowiedzi nie oznacza akceptacji ani zlecenia naprawy uwag F; naprawy potwierdzonych błędów B w zakresie wymagań są już autoryzowane przez ten workflow.

Przykład: „Popraw F1 i F3, F2 akceptuję”. Zapisz w komentarzu decyzji F1/F3 jako zlecone, F2 jako ACCEPTED z rzeczywistym uzasadnieniem użytkownika, jeśli je podał; nie wymyślaj uzasadnień. Uwagi niewymienione pozostają nierozstrzygnięte. Zachowaj słownik decyzji Raven; odróżnij zlecenie poprawki od potwierdzonego FIXED. Własny feedback użytkownika zapisz jako identyfikowalny punkt z zakresem i oczekiwanym zachowaniem.

Jednoznaczne „popraw wszystkie” lub „popraw F1” wystarcza — nie pytaj ponownie o zgodę na każdą edycję. Przy niejasnym „do poprawy” zapytaj tylko o nieustalony zakres. Zmiany produktu wykraczające poza plan wymagają uzgodnienia.

Po zleceniu zapisz decyzję i wróć do kroku 2 ze ŚWIEŻYM implementatorem, następnie niezależnym testerem i jego pętlą napraw; dopiero po ponownym PASS wszystkich kryteriów uruchom świeżego reviewera technicznego. Każda runda obejmuje wyłącznie aktualne zlecenie; nie traktuj wcześniejszego „napraw wszystkie” jako pozwolenia na naprawianie przyszłych zgłoszeń. Powracający problem lub spór pokaż użytkownikowi. Automatyczne naprawy ograniczają się do pętli testera z zapisanym limitem prób; pozostałe uwagi nie uruchamiają pętli.

Akceptację przypisz do konkretnej ocenionej wersji. Nie przedstawiaj zaakceptowanego ryzyka jako naprawionego ani nie przerabiaj negatywnego werdyktu reviewera na pozytywny. Akceptacja nie oznacza automatycznej zgody na push, merge, deploy lub archiwizację. Nie zastępuje również późniejszej fazy testów i wymaganych checków przed merge. W handoffie wskaż wykonane kontrole oraz pozostałą weryfikację; nie przedstawiaj implementacji jako gotowej do merge wyłącznie na podstawie akceptacji review. Zachowaj bramki implementacyjne Raven — późniejsza faza testów nie jest powodem ich pomijania. Zachowaj oczekujące manual checks, chyba że użytkownik jawnie potwierdził wykonanie albo świadomie odstąpił od nich; odstąpienie nie jest wynikiem PASS.

## Sprawdzenie użytkownika po implementacji

Po review kodu i niezależnych checkach przeglądarkowych oddaj działającą zmianę użytkownikowi do jego własnego sprawdzenia. Podaj sposób uruchomienia, scenariusze i znane ograniczenia; nie kieruj go automatycznie do raven-pr. Użytkownik może sam testować, zgłaszać problemy, zlecać poprawki i osobne etapy testów/checków, zanim uzna zmianę za gotową do PR. To normalna część cyklu, nie wyjątek ani blokada.

Feedback użytkownika jest pełnoprawnym wejściem niezależnym od uwag reviewera. Zapisz problem, oczekiwane zachowanie i dostępne kroki odtworzenia w change. Wyraźne zlecenie poprawki uruchamia świeżego implementatora, pętlę niezależnego testera i dopiero po jej powodzeniu świeże review techniczne w ramach tego samego change; nie wymagaj ponownego wpisywania nazwy skilla. Samo pytanie lub obserwacja bez jasnej intencji naprawy nie upoważnia do rozszerzenia zakresu. Jeśli zmieniają się wymagania produktu, uzgodnij zmianę planu. Po poprawkach ponownie oddaj wynik użytkownikowi do sprawdzenia.

Akceptacja technicznego review, akceptacja konkretnej poprawki i zakończenie własnych testów użytkownika są odrębnymi decyzjami. Zapisuj je zgodnie z rzeczywistą wypowiedzią, bez dopowiadania zgody na PR. raven-pr jest dopiero końcowym etapem na osobne zlecenie.

## GitHub i wznowienie

Stosuj wspólny kontrakt GH. Wymagane powiązanie wynika z github.json i rzeczywistego change; brak dostępu zgłoś, nie twórz lokalnej roadmapy jako zastępstwa. Ustawiaj In progress przy wykonaniu, Review przy przekazaniu do decyzji/testów/checków/merge, Blocked tylko przy konkretnej przeszkodzie. **Nigdy nie ustawiaj Done i nie zamykaj change ani tasków**, również po akceptacji review. Późniejsze testy i checki muszą przejść, a osobno zlecony raven-merge potwierdza merge i zapisuje Done na boardzie. Nie uruchamiaj raven-pr ani raven-lesson automatycznie.

Po przerwie odtwórz stan z GH i aktualnego Git. Gdy raport już istnieje i czeka na użytkownika, pokaż go zamiast ponownie implementować lub robić review. Odróżnij ten stan od checkpointu aktywnej automatycznej pętli błędów B: ją wznawiaj od zapisanego kroku i licznika prób, nie wymagając nowego zlecenia. Po zmianie HEAD/wymagań nie przenoś akceptacji na nową wersję. Błąd publikacji checkpointu lub raportu oznacza etap niezsynchronizowany; zachowaj roboczy payload i wznów zapis, nie powtarzaj implementacji. Zakończ każdy handoff opisem wyniku, uwag, pozostałych testów/checków, oczekiwanej decyzji i ewentualnych blokad.

## Osobny obowiązkowy etap trwałych testów

Po oddaniu implementacji i sprawdzeniu użytkownika, przed PR, workflow wymaga raven-test. Plan wydziela odpowiednie fazy unit/integration/E2E dla tego etapu. Implementacja wykonuje swoje bieżące bramki, lecz nie realizuje odroczonych faz trwałych testów i nie uruchamia raven-test automatycznie. W handoffie wskaż go jako wymagany następny etap przed publikacją PR.

Ten skill nie generuje ani nie rozbudowuje suite E2E, nawet gdy plan zawiera późniejsze fazy E2E. Tester sprawdza krytyczny przepływ i uzgodnione kryteria na bieżącej wersji aplikacji; trwałe testy pisze raven-test.

Etap trwałych testów ma dwa warianty: raven-test → osobno raven-test-review (manual) albo raven-auto-test (pisanie, uruchomienie, niezależne review i poprawki wad testów w jednym cyklu). Oba używają tego samego change i źródeł; wybór należy do użytkownika. Samo ukończenie manualnego raven-test nie oznacza ukończenia review testów.
