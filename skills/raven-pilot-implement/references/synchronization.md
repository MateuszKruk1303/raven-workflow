# Roadmapa, kolejka i zgodność z aplikacją

## Źródła prawdy

PRD i plan określają zamierzone zachowanie. Kod i aktualne wyniki weryfikacji opisują to, co faktycznie działa. `state.json` utrwala stan wykonania i dowody, a roadmapa prezentuje go użytkownikowi. Nie uznawaj pola status za dowód działania i nie dopasowuj wymagań do błędu, żeby ukryć rozjazd. Świadomie zmienione wymaganie aktualizuje PRD, jeśli dotyczy jego treści, plan, AC, decyzje, rewizje i roadmapę; niespełnione wymaganie pozostaje jawnie niespełnione.

Uzgodnij dokumentację przy rozpoczęciu lub wznowieniu pakietu pracy, wyniku review, istotnej decyzji lub zmianie wymagań, pauzie/blokadzie i końcowym przekazaniu. Łącz powiązane aktualizacje w jeden checkpoint. Sam spawn, odczyt, polling czy wiadomość o statusie nie wymagają nowej rewizji; aktywny zakres i następny krok muszą pozwalać wznowić pracę po przerwaniu. Weryfikacja jest proporcjonalna: sprawdź zmieniony zakres, istotny diff i aktualność dowodów; nie uruchamiaj całej aplikacji tylko po to, by zmienić etykietę. Jeśli brakuje dowodów, wpisz „niezweryfikowane” i nie podnoś statusu na podstawie deklaracji.

## Wiersz roadmapy

Roadmapa utrzymuje jedną tabelę kolejki z kolumnami:

`Kolejność | ID | Rezultat | Zależności | Status | Etap | Rewizje (spec/state) | Artefakty | Aktualność / blokada | Aktualizacja`

Kolejność to jawne unikalne liczby; można zmienić priorytet bez zmiany trwałego ID. Przy istniejącej roadmapie bez tej kolumny przypisz liczby zgodnie z obecną kolejnością wierszy, bez pytania i bez zmiany zakresu. Nowym wpisom nadawaj unikalne ID, nie odzyskuj ID archiwów. Linki w tabeli są względne względem roadmap.md. Etap jest dokładnym stanem state.json. Rewizje i czas odpowiadają jego zapisowi. Gdy chunka jeszcze nie przygotowano, wpisz `—` dla rewizji/artefaktów; nie twórz pustych folderów dla całej roadmapy.

| Stan wykonania | Status w roadmapie | Etap |
|---|---|---|
| Nieprzygotowany wpis, brak state | todo | not_started |
| draft | preparing | draft |
| ready | ready | ready |
| implementing | in-progress | implementing |
| awaiting_review | in-progress | awaiting_review |
| accepted | in-progress | accepted |
| testing | in-progress | testing |
| ready_to_archive | in-progress | ready_to_archive |
| blocked | blocked | blocked; poprzedni etap w uwadze |
| paused | paused | paused; poprzedni etap w uwadze |
| archived, po potwierdzonym przeniesieniu | Done | archived |

Rzeczywisty blocker wymagający użytkownika zatrzymuje realizację całego chunka: doprowadź pracowników do bezpiecznego checkpointu, zapisz blocked i resume_status oraz poproś o konkretny input. Zadania niewymagające usunięcia blockera zachowują swój dotychczasowy postęp na wznowienie. Zależność od niedokończonego chunka może pozostawać todo z uwagą „czeka na C-xx”; nie wymaga sztucznego state.json. Done oznacza historycznie dostarczony i zarchiwizowany chunk, nie samo zakończenie implementacji ani wdrożenie.

Poniżej tabeli utrzymuj wyliczony wpis `Następny do przygotowania: ID | powód` albo `brak | powód / kolejna akcja`. To pamięć podręczna wyniku algorytmu, nie ręcznie ustawiona decyzja. Przelicz po każdym checkpointcie mogącym zmienić wybór.

## Automatyczny wybór w prepare

1. Odczytaj roadmapę, aktywne state oraz indeks/linki archiwów. Najpierw rozpoznaj niedokończone operacje archiwizacji i synchronizacji. Sprawdź unikalność ID/kolejności, zależności i cykle. Konflikt tożsamości albo brakujące dowody blokują dotknięty zakres; nie zgaduj statusu.
2. Jawne ID/opis użytkownika ma pierwszeństwo. Brak argumentu oznacza automatyczny wybór, nigdy pytanie „który chunk?”.
3. Domyślnie wznów pierwszy według kolejności istniejący draft ze spełnionymi zależnościami, bez aktywnego właściciela zapisu. W dalszej kolejności wybierz pierwszy `ready` ze spełnionymi zależnościami: paczka już jest gotowa, więc nie przygotowuj jej od nowa; podaj implement jako następną akcję, bez automatycznego uruchamiania go poza autoryzacją. Zapobiega to przypadkowemu przygotowaniu całej roadmapy zamiast realizacji najbliższej paczki.
4. Jeśli takich paczek nie ma, wybierz pierwszy nieprzygotowany wpis todo ze spełnionymi zależnościami. Domyślnie zależność jest spełniona po potwierdzonym Done poprzednika. Przy jawnym zleceniu przygotowania z wyprzedzeniem można tworzyć draft zależnego chunka, lecz nie oznaczać go ready bez spełnionych zależności.
5. Pomijaj Done oraz chunki implementing/awaiting_review/accepted/testing/ready_to_archive, paused i blocked: te etapy wymagają właściwego skilla albo wznowienia, nie ponownego przygotowania. Dopuszczaj przygotowanie niezależnego kolejnego chunka. Jeżeli nie ma kwalifikującego się wpisu, podaj konkretny następny ruch dla najwcześniejszego niedomkniętego chunka (review/test/archive/resume/usunięcie blokady), bez pytania o dowolne ID i bez omijania blokad. Jeśli wszystko jest Done, porównaj z kryteriami pilota zamiast wymyślać nowy chunk.
6. Ogłoś wybór z krótkim powodem i rozpocznij prepare. Nie wymagaj zatwierdzenia samego wyboru. Zmiana priorytetu przez użytkownika aktualizuje kolejność roadmapy; nie podmieniaj ID.

## Protokół checkpointu

Nie da się zagwarantować atomowej transakcji wielu plików Markdown/JSON samą instrukcją. Użyj jawnego checkpointu z możliwością odzyskania; nie obiecuj odporności na każde przerwanie procesu.

1. Jeden właściciel zapisuje współdzielone state, plan chunka, podsumowania, journal i roadmapę; podczas implementacji jest nim koordynator. Pracownicy zapisują wyłącznie przypisane im artefakty zadania (plan techniczny, verification, scenariusze Playwright, implementation, numerowany raport review) w uzgodnionych ścieżkach. Koordynator włącza ich wyniki do wspólnego checkpointu. Przed zmianą współdzielonej roadmapy uzyskaj wyłączną blokadę przez atomowe utworzenie katalogu `context/pilot/.roadmap-lock/` z tożsamością sesji. Przy zajętej blokadzie ponów po zwolnieniu; nie przejmuj jej, dopóki nie ustalisz, że właściciel zakończył działanie. Nie czekaj bez końca: przy nierozstrzygniętej blokadzie raportuj brak możliwości synchronizacji. Nie rób zmian roadmapy na starej kopii; odczytaj ją ponownie pod blokadą i zachowaj pozostałe wiersze/treść użytkownika.
2. Zapisz `context/pilot/sync/<ID>.json`: ID, poprzednią/nową state_revision, docelowy stan, spec_revision, odnośniki do dowodów i listę aktualizowanych artefaktów, fazę pending. Podnoś state_revision przy każdym checkpointcie stanu/postępu. Starszy aktywny state bez pola ma bazową rewizję 0; dodaj pole bez przepisywania historii. Nie modyfikuj starszych archiwów dla uzupełnienia schematu.
3. Zapisz dowody i aktualne statusy realizacji AC/zadań w planie, zachowując rozróżnienie między wymaganiem a wynikiem. Atomowo zapisz state przez temp + rename. Zmień odpowiadający mu wiersz roadmapy, jej podsumowanie kolejki i ewentualne zmienione opisy zakresu. Nie twórz sprzecznych duplikatów statusów w innych sekcjach roadmapy.
4. Ponownie odczytaj zapisane dane: ID, status według mapowania, etap, rewizje, aktualność linków oraz stan AC muszą się zgadzać. Oznacz journal complete i zwolnij własną blokadę również przy obsłużonym błędzie. Nie wykonuj następnej fazy ani nie raportuj jej ukończenia przy nieudanej synchronizacji; opisz błąd i pozostaw journal do odzyskania.
5. Na wznowieniu porównaj pending journal, faktycznie zapisany state, dowody i roadmapę. Napraw brakującą projekcję wyłącznie na podstawie utrwalonych dowodów. Jeżeli przerwano przed zapisem nowego state, nie awansuj stanu tylko z zamiaru w journal; kontynuuj albo wycofaj niedokończony checkpoint po sprawdzeniu plików. Uważaj na porzuconą blokadę: usuń ją dopiero po potwierdzeniu nieaktywności właściciela i w granicach uprawnień.
6. Archiwizacja jest wyjątkiem dla chwilowego state=archived przed rename: źródłem odzyskania jest archive-operations, a Done wolno zapisać dopiero gdy przeniesienie zostało potwierdzone. Uzgodnij ewentualny journal synchronizacji z dziennikiem archiwizacji; nigdy nie zapisuj do przeniesionego folderu. Końcową state_revision ustal przed przeniesieniem i potem tylko odzwierciedl ją w roadmapie.

## Rozjazd kodu i dokumentacji

Przy wykryciu regresji nie poprawiaj samego opisu na „działa”. Oznacz dotknięte AC i dowody jako nieaktualne, utrwal blokadę lub właściwy etap naprawy, a przy zmianie zachowania cofnij akceptację zgodnie z kontraktem. Popraw kod w zakresie autoryzacji albo zgłoś konkretny brak. Przy świadomej korekcie produktu aktualizuj wszystkie dotknięte dokumenty w tym samym checkpointcie.

Archiwum zachowuje prawdę historyczną. Późniejsza regresja lub zastąpienie funkcji nie zmienia jego zawartości ani historycznego Done: roadmapa pokazuje w kolumnie aktualności „regresja / zastąpione przez C-xx”, dowody i link do nowego chunka naprawczego. Taka regresja blokuje zależności, które potrzebują niedziałającej funkcji, mimo historycznego Done. Opis aktualnego produktu w PRD/roadmapie uwzględnia zmianę. Zapisz zaobserwowaną regresję od razu; nowy chunk twórz zgodnie z zakresem zlecenia, nie udawaj, że już istnieje. Nie deklaruj bieżącej sprawności wyłącznie na podstawie starego archiwum ani nie wymagaj przechodzenia wszystkich historycznych flow przy każdej edycji.
