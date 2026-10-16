---
name: raven-init-stack
description: Zainicjalizuj stack Raven przez Better T Stack w bieżącym folderze, po krótkim wywiadzie architektonicznym opartym na PRD. Przygotuj lokalny PostgreSQL w Docker Compose i zapisz decyzje, konfigurację oraz weryfikację w context/foundation/tech-stack.md. Użyj przy raven-init-stack lub przygotowaniu tego stacku projektu.
---

# Raven Init Stack

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

Wywołanie: `$raven-init-stack <nazwa-aplikacji>`, np. `$raven-init-stack equi-sell`.

Przyjmij nazwę jako nazwę aplikacji i prefiks pakietów workspace, nie jako ścieżkę. Jeśli użytkownik jej nie podał i nie wskazał jednoznacznie w bieżącym poleceniu, dołącz pytanie o nazwę do wywiadu poniżej. Użyj formatu kebab-case, np. `equi-sell`; nie traktuj argumentu jako kodu powłoki. Nie zmieniaj nazwy folderu użytkownika.

## PRD i decyzje architektoniczne — przed generowaniem

Przeczytaj `context/foundation/prd.md`, istniejący `tech-stack.md`, instrukcje repozytorium i dostępne ustalenia z rozmowy. Najpierw przeanalizuj wymagania, dopiero potem zadawaj pytania. Jeśli PRD nie istnieje, poproś o jego lokalizację albo krótki opis produktu; nie wymyślaj wymagań. Użytkownik może świadomie zlecić sam bazowy szkielet bez PRD.

Użytkownik pełni rolę architekta. Przeprowadź krótki wywiad: kilka istotnych pytań wynikających z produktu, po 1–3 na turę. Nie stosuj uniwersalnej ankiety i nie pytaj ponownie o ustalone decyzje. Przy każdym pytaniu wskaż wymaganie z PRD, rekomendację oraz krótki powód lub kompromis. Przykładowe tematy, tylko gdy mają zastosowanie:

- Obrazki i pliki: gdzie przechowujemy pliki — np. storage zgodny z S3/R2 lub lokalny dysk — i czy w bazie zapisujemy tylko metadane? Jak ma działać development?
- Dostęp: czy produkt potrzebuje logowania, czy jest osobistym narzędziem localhost? Nie dodawaj kont tylko dlatego, że starter je wspiera.
- Długie operacje, procesy agentów i realtime: co działa poza żądaniem HTTP, jak przeżywa zamknięcie strony i restart aplikacji?
- Integracje oraz dane: co jest źródłem prawdy, które usługi są potrzebne od początku, co można odłożyć?

Dopuszczaj odpowiedzi „nie wiem”, „zaproponuj” i „odłóżmy”. Przy niewiedzy przedstaw rekomendację i pozwól ją przyjąć lub zmienić; samo milczenie nie jest zgodą. Jeśli użytkownik jawnie deleguje konkretny wybór, wybierz i zapisz uzasadnienie. Nie blokuj szkieletu na integracjach, które można dodać później. Decyzje wpływające na generowanie muszą być rozstrzygnięte przed nim; przy odłożonej decyzji uzgodnij minimalny wariant umożliwiający start.

Zbierz wynik w krótkim podsumowaniu w chacie i w `tech-stack.md`: decyzja, status (zatwierdzona / propozycja / odłożona), uzasadnienie oraz konsekwencja dla inicjalizacji. Nie dodawaj osobnego rytuału akceptacji, jeśli odpowiedzi już rozstrzygnęły wybory. Decyzje dotyczą tego projektu; zapis do globalnych preferencji wymaga osobnej zgody użytkownika. Nie przerabiaj PRD ani nie implementuj funkcji produktu w ramach tego wywiadu.

## Generowanie szkieletu

Bazą jest Next.js, Hono, Bun, tRPC, PostgreSQL, Drizzle i Turborepo. Better Auth stosuj, gdy ustalenia obejmują logowanie; dla uzgodnionego braku logowania wybierz wariant bez auth. Inne odstępstwa od bazy uzgodnij, zamiast samodzielnie zmieniać stack. Sprawdź opcje aktualnego CLI przed użyciem zmienionych flag.

Po wywiadzie uruchom w bieżącym katalogu poniższą komendę, dostosowując auth do ustaleń. `--db-setup none` pozostawia konfigurację lokalnej bazy krokowi Docker Compose poniżej:

```sh
bun create better-t-stack@latest . --frontend next --backend hono --runtime bun --api trpc --auth better-auth --payments none --database postgres --orm drizzle --db-setup none --package-manager bun --no-git --web-deploy none --server-deploy none --install --addons turborepo --examples none
```

- Argument `.` oznacza bieżący katalog jako katalog główny projektu. Nie twórz dodatkowego katalogu nadrzędnego ani tymczasowego podkatalogu na szkielet. Generator początkowo wyprowadza nazwę pakietu z nazwy bieżącego folderu; po generowaniu dostosuj ją do argumentu skilla zgodnie z instrukcją poniżej. Standardowe katalogi monorepo `apps/` i `packages/` powstają bezpośrednio w nim.
- Sprawdź dostępność Bun i zawartość bieżącego folderu. Jeśli Bun nie jest dostępny, zgłoś brak. Pusty folder inicjalizuj od razu. Jeśli zawiera wcześniejsze pliki, sprawdź kolizje: zachowaj `.git/`, `context/` i instrukcje projektu. Dla niekolidujących plików wybierz scalanie (`merge` / `--directory-conflict merge`); nie wybieraj czyszczenia (`overwrite`) ani nowej nazwy katalogu (`increment`). Scalanie nie gwarantuje ochrony kolidujących plików: jeśli istnieje już aplikacja lub pliki docelowe generatora, wskaż konkretne kolizje i ustal ich obsługę przed uruchomieniem.
- Nie dodawaj `--yes`: Better T Stack odrzuca połączenie tej flagi z własnymi opcjami stosu. Jeśli generator pyta o otwarcie edytora, wybierz `Not now`, chyba że użytkownik zażądał otwarcia.
- Poczekaj na zakończenie instalacji. Błędy uprawnień lub dostępu do sieci obsłuż zgodnie z regułami środowiska. Przy innym błędzie zachowaj częściowe pliki i zgłoś przyczynę; nie uruchamiaj kolejnych prób nadpisujących katalog ani nie zmieniaj samodzielnie stosu.
- Projekt pozostaje w folderze wywołania. Nie zmieniaj katalogu roboczego na rodzica i nie stosuj obejścia z generowaniem do podkatalogu. Po inicjalizacji utwórz lub celowo uaktualnij `context/foundation/tech-stack.md` według zasad poniżej. Pozostałej dokumentacji istniejącego projektu nie zmieniaj bez dodatkowego polecenia.
- Po generowaniu nadaj aplikacji nazwę z argumentu. Jeśli różni się od nazwy wyprowadzonej przez CLI, zmień główne `package.json.name`, scope wygenerowanych pakietów (np. `@horse-market/db` → `@equi-sell/db`), zależności workspace, importy, eksporty oraz odwołania w wygenerowanych konfiguracjach, skryptach i metadanych UI. Zachowaj nazwy zadań/aplikacji `web` i `server`. Ogranicz zmiany do plików utworzonych przez generator: nie wykonuj globalnego zastępowania w istniejącej dokumentacji, sekretach, node_modules ani artefaktach builda. W `bts.jsonc` komenda odtwarzająca ma nadal wskazywać `.` jako katalog; nie zmieniaj jej na nazwę aplikacji.
- Po zmianie nazw uruchom `bun install`, aby zsynchronizować lockfile i powiązania workspace, a potem `bun run check-types`, jeśli skrypt istnieje. Nie uznawaj samej zmiany głównego package.json za ukończone nadanie nazwy.
- Po sukcesie sprawdź nazwę głównego pakietu, spójność scope/importów oraz obecność `package.json` i `bts.jsonc` w katalogu wywołania. Następnie przygotuj lokalną bazę i zapisz dokument stacku według zasad poniżej. Sam sukces generatora nie potwierdza działania auth ani połączenia z bazą.

Ta umiejętność tworzy szkielet i instaluje wybrane zależności. Nie tworzy usług chmurowych, nie wdraża aplikacji ani nie wykonuje migracji na istniejącej bazie.


## Lokalny PostgreSQL w Docker Compose

Ten krok jest częścią inicjalizacji. Utwórz `compose.yaml` w roocie albo uzupełnij istniejącą konfigurację Compose, zachowując jej usługi i dane. Przy ponownym uruchomieniu wykorzystaj istniejący serwis PostgreSQL, jeśli spełnia ustalenia; nie twórz drugiego kontenera ani nowego wolumenu zamiast dotychczasowego.

- Użyj oficjalnego obrazu PostgreSQL z jawną, kompatybilną wersją główną, nie `latest`. Sprawdź aktualną dokumentację obrazu dla wybranej wersji, w szczególności ścieżkę montowania danych. Dodaj nazwany wolumen oraz healthcheck z `pg_isready`.
- Udostępnij port wyłącznie na `127.0.0.1`. Sprawdź zajętość portu hosta i w razie kolizji wybierz wolny, aktualizując połączenie aplikacji. Nie ustawiaj globalnego `container_name` ani globalnej nazwy wolumenu; wykorzystaj izolację projektu Compose, uwzględniając równoległe projekty i worktree.
- Przygotuj lokalne dane dostępowe i spójną konfigurację połączenia w plikach env rzeczywiście odczytywanych przez wygenerowaną aplikację. Dla Bun uruchamianego na hoście użyj adresu localhost i portu hosta. Rozróżnij plik env odczytywany przez Compose od pliku env aplikacji; sprawdź, że oba korzystają z tych samych danych. Nie nadpisuj istniejących sekretów ani zdalnego `DATABASE_URL`; w razie konfliktu ustal konfigurację lokalną.
- Dodaj bezpieczne `.env.example` i odpowiednie wpisy `.gitignore`. Nie zapisuj haseł ani connection stringów z poświadczeniami w dokumentacji, chacie lub logach narzędzi. Nie wyświetlaj rozwiniętej konfiguracji Compose; do walidacji użyj wariantu bez wypisywania wartości.
- Sprawdź dostępność Docker Compose i działającego demona. Zweryfikuj konfigurację i uruchom tylko serwis bazy (`docker compose up -d <serwis>` z odpowiednim plikiem/projektem, jeśli potrzebne). Poczekaj na healthcheck z ograniczonym czasem, a następnie sprawdź połączenie z procesu na hoście przez konfigurację aplikacji i proste `SELECT 1`. Zdrowy kontener sam w sobie nie dowodzi poprawnego połączenia aplikacji.
- Jeśli Docker jest niedostępny, przygotuj pliki i oznacz uruchomienie oraz kontrolę połączenia jako niewykonane. Podaj konkretną akcję użytkownika i komendę wznowienia; nie deklaruj pełnego sukcesu ani nie instaluj Dockera w ramach tego skilla.
- Na potwierdzonej nowej, pustej bazie deweloperskiej zastosuj wygenerowany schemat przez istniejący skrypt projektu, jeżeli jest wymagany do startu. Na istniejącej bazie nie uruchamiaj migracji ani operacji resetujących w ramach tego skilla. Nie używaj `down -v`, nie usuwaj wolumenów i nie zmieniaj wersji obrazu istniejącej bazy bez uzgodnienia migracji. Zmiana zmiennych inicjalizacyjnych obrazu nie zmienia hasła w istniejącym wolumenie.

W końcowym handoffie w chacie podaj rzeczywiste polecenia uruchomienia i zatrzymania lokalnej bazy bez kasowania danych oraz uruchomienia aplikacji, wynik kontroli połączenia i ewentualny brakujący krok. Nie odsyłaj użytkownika wyłącznie do dokumentacji. Nie dodawaj E2E w ramach inicjalizacji.


## Automatyczny zapis tech-stack.md

Zapis `context/foundation/tech-stack.md` jest częścią tego skilla, nie osobnym opcjonalnym krokiem. Wywołanie inicjalizacji upoważnia również do tego zapisu — nie pytaj ponownie o zgodę na dokumentację wyniku.

### Przed inicjalizacją

Jeśli dokument istnieje, przeczytaj go wraz z obowiązującymi instrukcjami projektu i sprawdź ręczne/niezacommitowane zmiany. Zachowaj decyzje, uzasadnienia i informacje o integracjach. Istotną sprzeczność między wybranym zestawem a zatwierdzonym stackiem lub wymaganiami projektu rozstrzygnij przed uruchomieniem generatora; nie nadpisuj decyzji konfiguracją domyślną. Dokument nie jest dowodem, że zależności są już zainstalowane.

### Po inicjalizacji

Utwórz brakujące `context/foundation/` bez inicjalizowania innych folderów workflow. Zbuduj dokument na podstawie rzeczywistych `package.json`, manifestów workspace, lockfile, `bts.jsonc`, wygenerowanych konfiguracji i wyników wykonanych poleceń. Nie kopiuj wyłącznie planowanej komendy generatora jako opisu stanu.

Dokument zawiera:

- **Projekt i stan** — nazwa, data aktualizacji oraz stan inicjalizacji: planowana, częściowa lub zakończona. „Zakończona” wymaga również uruchomionej i zweryfikowanej lokalnej bazy.
- **Stack** — tabela: obszar, technologia, rola w aplikacji, wersja i źródło. Obejmij frontend, backend, runtime/package manager, API, bazę danych, ORM, auth oraz workspace/build tooling. Podawaj wersję z lockfile, jeśli została ustalona; zakres z manifestu oznacz jako deklarowany. Nie wpisuj wymyślonych wersji ani „latest” jako wersji zainstalowanej.
- **Decyzje architektoniczne** — wynik wywiadu, statusy, uzasadnienia i otwarte pytania. Zapisuj odłożone decyzje bez przedstawiania rekomendacji jako zatwierdzonych.
- **Struktura i granice** — rzeczywiste katalogi aplikacji/pakietów, ich odpowiedzialności i odnośniki do konfiguracji. Decyzje architektoniczne z rozmowy uwzględniaj tylko, gdy dotyczą tego projektu; odróżnij docelową architekturę od utworzonego szkieletu.
- **Uruchamianie i konfiguracja lokalna** — istniejące skrypty, katalog uruchomienia, wymagane usługi i nazwy zmiennych z bezpiecznych szablonów. Uwzględnij plik Compose, serwis PostgreSQL, wersję obrazu, port hosta, wolumen, lokalizacje plików env oraz polecenia start/stop bazy. Bez wartości sekretów, tokenów i connection stringów zawierających poświadczenia.
- **Weryfikacja** — faktycznie wykonane polecenia i ich wyniki. Odróżnij zaliczony typecheck od nieprzetestowanego działania bazy czy auth.
- **Pozostałe kroki i ograniczenia** — np. niedostępny Docker, niezastosowany schemat, odłożone decyzje, niewykonane kontrole i ustalone integracje, których initializer nie instaluje. Nie deklaruj ich jako działających.

Nie narzucaj każdej aplikacji architektury harnessu Raven. Pi, GitHub jako kolejka, polityki agentów czy brak logowania pojawiają się tylko, jeśli wynikają z ustaleń danego projektu. Sam zapis dokumentu nie rozszerza zakresu inicjalizacji o te integracje. Nie twórz roadmapy ani tasków w tym pliku.

### Aktualizacja i kontrola

Nowy dokument zapisz w języku użytkownika; przy istniejącym zachowaj jego język i przydatną strukturę. Uaktualniaj fakty dotyczące inicjalizacji, nie przepisuj dokumentu od zera. Zachowaj ręczne ustalenia i nieznane sekcje. Przed zapisem sprawdź, czy plik nie zmienił się od odczytu; jeśli tak, ponownie go wczytaj i uwzględnij zmiany.

Zapisz atomowo przez plik tymczasowy w tym samym katalogu. Po zapisie sprawdź zgodność z wygenerowanym projektem i poprawność względnych linków. Ponowne uruchomienie nie tworzy kolejnego dokumentu ani nie dopisuje duplikatów sekcji; nie jest też zgodą na ponowne generowanie istniejącej aplikacji.

Jeśli inicjalizacja pozostawiła częściowy szkielet, zapisz potwierdzone fakty ze stanem „częściowa” i konkretnym błędem, zachowując wcześniejsze decyzje. Jeżeli generator w ogóle nie ruszył, możesz zapisać uzgodnioną architekturę ze stanem „planowana”, ale nie sugeruj wykonania inicjalizacji. Jeśli zapis dokumentu nie powiedzie się po udanym bootstrapie, zgłoś częściowe zakończenie skilla: szkielet istnieje, dokument wymaga uzupełnienia; nie uruchamiaj z tego powodu generatora ponownie.
