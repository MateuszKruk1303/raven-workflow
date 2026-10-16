# Historia PR i wznowienie publikacji

Czytaj przy aktualizacji istniejącego PR lub wznowieniu przerwanego zapisu. Przy pierwszym PR użyj poniższych markerów, zapisując tylko publikację początkową. Historia dotyczy kolejnych wersji opublikowanych w opisie PR, a nie wszystkich lokalnych prób ani samej listy commitów.

## Body i granice wersji

Zachowaj marker tożsamości `<!-- raven:pr change=C-03 -->` i pełny link do change issue. Bieżący opis utrzymuj w `<!-- raven:pr-current:start -->` … `<!-- raven:pr-current:end -->`; historię w `<!-- raven:pr-history:start -->` … `<!-- raven:pr-history:end -->`. Są częścią tego samego body i jednego zapisu. Ręczne dopiski poza blokami zachowaj, a edycje użytkownika wewnątrz bloków uwzględnij przy scalaniu; oznaczenie bloku nie upoważnia do kasowania jego treści.

Każdy wpis historii zawiera datę, krótki rzeczowy zakres, pełne SHA początku/końca i marker `<!-- raven:pr-publication change=C-03 kind=initial|update|baseline from=FULL_SHA to=FULL_SHA -->` z jedną rzeczywistą wartością kind. Markery identyfikują wpisy, a nie wynik testów:

- `initial`: pierwszy PR, od zapisanego merge-base do opublikowanego head; nazwij wpis „Pierwsza publikacja”.
- `update`: poprawki od ostatniego potwierdzonego `to` do nowego head; opisz efekt poprawki i, gdy źródła to potwierdzają, jej powód lub powiązaną uwagę review. Zachowaj starsze wpisy.
- `baseline`: przyjęcie istniejącego PR bez wiarygodnej granicy wcześniejszej publikacji; `from=to` wskazuje pierwszy potwierdzony punkt odniesienia, nie odtworzoną historię.

Aktualny opis powstaje z całego diffu PR. Wpis poprawki powstaje z zakresu ostatnio opisanego SHA → nowy head, jego diffu i istotnych decyzji; obejmuje także commity utworzone wcześniej lub już pushnięte. Nie używaj do tego wyłącznie `origin/branch..HEAD` ani aktualnego head PR: po pushu oba mogą nie zawierać poprawki wciąż nieopisanej w body. Potwierdź, że poprzedni SHA należy do historii nowego head; rozbieżność wymaga wyjaśnienia, nie fikcyjnej ciągłości ani automatycznego rebase.

Gdy head nie zmienił się od ostatniej potwierdzonej publikacji, nie dopisuj fikcyjnej poprawki ani duplikatu wpisu. Możesz poprawić aktualny opis/powiązania bez nowego wpisu kodowego. Zachowaj istniejącą historię i marker. Dla tego samego zakresu `kind/from/to` istnieje jeden wpis; doprecyzowanie jego treści nie tworzy kolejnej rundy.

## Istniejący PR bez markerów

Nie zakładaj, że całe dotychczasowe body jest generowane. Odczytaj je przed pushem i zachowaj ręczne notatki, checklisty, linki oraz istniejącą historię. Jednoznacznie rozpoznany stary opis rozwiązania zastąp aktualnym, zachowując potrzebny kontekst historyczny. Gdy autorstwo fragmentów jest niejasne, zachowaj je poza nowym blokiem i oznacz stary opis jako wcześniejszy; nie usuwaj ani nie przerabiaj niepewnych dopisków na własną historię.

Ustal SHA ostatniej opisanej publikacji z wiarygodnego źródła: wcześniejszego wpisu/body, zachowanego checkpointu powiązanego z odczytanym PR lub historii GitHub jednoznacznie wiążącej opis z SHA. Zdalny head odczytany teraz nie dowodzi, że body już go opisuje. Jeśli granicy nie da się odzyskać, nie zgaduj: zapisz `baseline` dla aktualnie publikowanego head i jawnie podaj, że zakres wcześniejszych poprawek jest nieustalony. Zachowaj istniejącą historię słowną, nie dopisuj wymyślonych dat, przyczyn ani wersji. Kolejne publikacje korzystają już z potwierdzonej granicy.

## Częściowy sukces i retry

Przed pierwszą mutacją zachowaj poza śledzonym drzewem repo roboczy checkpoint: repo kodu i issue URL, PR/head/base, początkowy HEAD i odczytany zdalny SHA, poprzednią granicę publikacji, wersję/body PR, planowane grupy commitów oraz przygotowany payload opisu/historii. Po każdym kroku uzupełnij rzeczywiste SHA i wynik. To pomoc odzyskania niezapisanego wyniku; aktualny Git i odczyt GH rozstrzygają, co wykonano. Nie commituj checkpointu ani nie nadpisuj oczekującego payloadu przy wznowieniu.

| Punkt przerwania | Wznowienie |
| --- | --- |
| Commit odrzucony lub wynik niepewny | Sprawdź HEAD/log i zawartość commitu, indeks oraz working tree. Zachowaj udane grupy i commituj tylko pozostałe hunki. Nie powielaj commitów, nie amenduj udanych i nie obchodź hooka. |
| Commit gotowy, push nieudany/niepewny | Porównaj dokładny remote/ref i SHA. Jeśli zmiana jest już zdalnie, przejdź do body; inaczej ponów tylko zwykły push, o ile jest bezpieczny. Divergence wymaga decyzji. |
| Push gotowy, create/edit PR nieudane/timeout | Wyszukaj właściwy PR we wszystkich stanach i odczytaj body. Nie twórz duplikatu. Użyj poprzedniej granicy z body lub checkpointu, nie nowego zdalnego head; uzupełnij brakujący opis i wpis historii. |
| Zapis body niepewny lub odczyt końcowy nieudany | Odczytaj PR i porównaj zapisany opis, zakres wpisu, powiązania i head SHA z payloadem. Jeśli zapis już się udał, nie dopisuj wpisu ponownie. Jeśli jest częściowy lub równolegle zmieniony, scal brakujący fragment z aktualnym body. |

Jeśli nowe lokalne lub zdalne zmiany pojawiły się po przerwaniu, najpierw ustal ich zakres; nie wysyłaj ich automatycznie jako części starego payloadu. Jeżeli obecne body potwierdza publikację, użyj jej jako nowej granicy; jeśli nie, zachowaj starą i opisz pełny nadal nieopublikowany zakres. Przy utracie checkpointu odtwórz stan z Git/GH, a nie z pamięci rozmowy; brak wiarygodnej granicy obsłuż jawnym baseline.

Po niepewnym wyniku najpierw odczyt, dopiero potem ponowienie brakującego zapisu. Nie powtarzaj bez końca tego samego błędu: przy trwałym braku dostępu, ponownym niepowodzeniu tego samego kroku albo wymaganej decyzji zakończ z częściowym wynikiem i zachowanym payloadem. Brak dostępu do GH nie oznacza braku PR.
