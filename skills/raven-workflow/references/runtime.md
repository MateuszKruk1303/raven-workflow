# Ograniczony helper runtime

`python3 <raven-workflow>/scripts/raven_runtime.py --repo PATH <command>` obsługuje poniższe operacje. Nie jest silnikiem etapów: nie ocenia wymagań, zgód, jakości review, CI ani gotowości merge. Nie commituje, nie pushuje ani nie merguje. Jawna komenda issue aktualizuje tylko wskazany task; lokalne komendy nie łączą się z GH. Sprawdź `--help` dla rzeczywistego interfejsu.

| Polecenie | Działanie |
| --- | --- |
| `fingerprint ID` | SHA-256 treści jedynego bloku contract z LF |
| `status ID` / `resume ID` | Read-only stan lokalny; bez sieci i bez odtwarzania historii GH |
| `start ID --session S --worktree PATH [--base HEAD]` | Opcjonalne utworzenie izolowanego worktree i brancha `raven/ID`; może zacząć przed powstaniem planu |
| `checkpoint ID --session S --stage STAGE --next NEXT [--evidence TEXT] [--repair-attempts N]` | Zapis kanonicznego checkpointu JSON w planie poza kontraktem |
| `publish-pr ID --session S --title TITLE --body-file PATH --dry-run` | Podgląd ograniczonej publikacji draftu |
| `publish-pr ID --session S --title TITLE --body-file PATH --apply` | Draft PR dla **już wypchniętego** aktualnego HEAD i autoryzowanej konfiguracji |
| `read-pr ID --number N` | Ograniczony odczyt wskazanego PR, bez historii komentarzy |
| `issue ID --number N --event read` | Read-only odczyt konkretnego issue, bez skanu boarda |
| `issue ID --number N --event start --assignee LOGIN --session S --dry-run/--apply` | Potwierdzenie In progress i wykonawcy; działa także przed utworzeniem planu |
| `issue ID --number N --event block --reason TEXT --session S --dry-run/--apply` | Blokada i krótki powód w zarządzanym fragmencie issue |
| `issue ID --number N --event merge --pr N --session S --dry-run/--apply` | Po weryfikacji merge i powiązania PR zamknięcie issue jako Done |

Przykład: `python3 <raven-workflow>/scripts/raven_runtime.py --repo /path/project status C-03`. Ścieżka skilla pochodzi z rzeczywistej instalacji, nie zgaduj katalogu. Jeśli helper jest niedostępny, nazwij brak; zwykłe operacje Git/plików są możliwe według tego samego kontraktu, bez udawania wyniku helpera.

`start` służy wybranemu wariantowi z izolacją; zwykła praca na branchu w aktualnym checkout nie wymaga tej komendy. `start` wymaga jawnej ścieżki worktree poza repo źródłowym. Jeśli plan już istnieje, jego pełne bajty muszą odpowiadać wybranemu commitowi bazowemu; helper nie commituje niezatwierdzonych plików. Nie przełącza ukradkiem głównej sesji. Brak planu jest raportowany jako `plan_missing: true`, `fingerprint: null` — nie jako gotowość pracy.

`start` nie wybiera taska, nie pyta o branch i nie pobiera aktualnej bazy. Dla nowego change wykonaj wcześniej [przygotowanie brancha](change-branch.md) i podaj `--base <zweryfikowany-SHA-bazy>`; domyślne HEAD może nadal wskazywać poprzedni feature branch. Przy wznowieniu zachowaj pierwotną bazę z checkpointu/journalu zamiast wyznaczać nową.

Checkpoint ma dokładnie jeden blok `<!-- raven:checkpoint:start -->` … `<!-- raven:checkpoint:end -->` poza kontraktem; zawiera JSON. Helper zapisuje stage/next/evidence, session, fingerprint, branch/head, base/PR/issue (URL) jeśli znane, code_tree, checkpoint_sequence i opcjonalne repair_attempts. Przy ręcznym zapisie zachowaj ten sam blok, nie twórz równoległego checkpointu w prozie. `checkpoint_sequence` liczy zapisy, nie próby napraw. `--repair-attempts` zapisuje rzeczywistą podaną liczbę; nie zeruj jej przy wznowieniu.

Bez `start` ustal bazowy commit przed zmianami i wpisz jego pełny SHA jako `base` do checkpointu w planie przed pierwszym wywołaniem `checkpoint`. Helper zachowuje tę wartość; sam nie wyznacza bazy bez zapisu w planie lub journalu. Przy wznowieniu nie zastępuj bazy bieżącym HEAD.

Parametr API `acceptance_ref` i flaga `--acceptance-ref` zostały usunięte. Runtime nie tworzy akceptacji planu. Historyczne `acceptance` i inne nieznane pola checkpointu zachowuje bez zmian jako ignorowane dane, bez migracji lub bramki wykonania. `contract_current`, `code_head_current` i `code_tree_current` są oddzielnymi porównaniami; zgodność kontraktu nie dowodzi aktualności testów. `dirty` obejmuje pliki nieśledzone. Checklista Progress pozostaje poza kontraktem; zapis checkpointu jej nie odhacza.

Lokalny journal w wspólnym katalogu Git wspiera wznowienie przerwanych operacji. Kanoniczny checkpoint jest w wersjonowanym planie. Mutex chroni czas pojedynczego polecenia, nie rezerwuje change dla sesji ani nie zapewnia blokady między hostami.

Publikacja wymaga `.raven/config.json` z `repository.owner/name/base_branch`, `publication.mode: draft-pr` i rzeczywistym `authorized_by`; te pola dokumentują wcześniejszą zgodę, nie nadają nowych praw. Helper używa `GH_TOKEN` albo `GITHUB_TOKEN`; nie wypisuj sekretów i nie zakładaj fallbacku do `gh auth`. Sprawdza tożsamość zdalnej gałęzi/HEAD oraz istniejący PR, odmawia niejednoznacznego powiązania i weryfikuje zapis. Tylko stan `published` potwierdza otwarty PR zgodny z SHA; `stale-remote`, `closed` i `merged` wymagają odrębnej interpretacji, nie są sukcesem nowej publikacji. Push i bogatszą aktualizację PR wykonuje raven-pr w zakresie zgody.

`read-pr` zwraca number/url/title/body/state/draft/merged/mergeable i tożsamość base/head. Nie pobiera CI ani reviews; te bramki odczytuje właściwy skill osobnym ograniczonym zapytaniem. `resume` nie rozwiązuje automatycznie PR do worktree: skill najpierw ustala mapowanie i potrzebny Git fetch w autoryzowanym zakresie.

## Zdarzenia issue

Dla komend zapisu wybierz dokładnie jedną flagę `--dry-run` albo `--apply`; dry-run pokazuje zamiar bez sieci. W konfiguracji wymagane są `repository` oraz `tracker.type: github-issues`, z `tracker.labels.in_progress` i `tracker.labels.blocked`. Sam config lub token nie stanowi zlecenia. Polityka publikacji kodu jest odrębna; lokalny `start` tworzący worktree nie podejmuje issue.

`issue --event start` stosuj na początku zleconego planowania (auto-implement nie prowadzi trackingu), po rozstrzygnięciu wykonawcy i session ownership. Wykonawca jest jawnym loginem GH, nie domyślną tożsamością tokena. Helper odmawia przejęcia obcego assignee i zamkniętego issue. Zgodny stan to no-op. Przy blocked najpierw potwierdź rozwiązanie przyczyny; dopiero świadomy start usuwa etykietę i zarządzany powód blokady. Samo wznowienie/status nie odblokowuje taska.

Dla `block`/`merge` wykonawca pochodzi z wcześniejszego journalu start albo jawnego `--assignee LOGIN`; przy nowym checkout podaj potwierdzonego ownera zamiast zgadywać. Checkpoint przechowuje `issue` jako pełny URL (string), a `owner` jako osobne pole.

`block` zachowuje In progress i assignee oraz cudzą treść issue; zapisuje tylko krótki bieżący powód. Nie kopiuj raportu ani planu. `merge` sprawdza dokładny PR w skonfigurowanym repo, jego potwierdzony merge i markery `<!-- raven-change:ID -->` oraz `<!-- raven-issue:OWNER/REPO#N -->`. PR zawiera również zwykły link do issue, bez automatycznych closing keywords. Dopiero po spełnieniu bramek raven-merge helper zamyka issue i usuwa etykiety oraz zarządzany powód blokady; sam helper nie potwierdza odbioru, zgody ani jakości dowodów.

Mutacje mają readback i journal zamiaru. Po nieznanym wyniku odczytaj konkretny zasób przed ponowieniem; nie wysyłaj ślepo żądania. `--reconcile` służy jawnemu odzyskaniu tego samego zamiaru po rozpoznaniu niepewnego wyniku, z limitem dwóch prób zapisu; nie omija ownera ani bramek. Przy błędzie po udanym merge wznawiaj wyłącznie finalizację issue. Journal i mutex nie są rozproszoną rezerwacją taska, a checkpoint nie jest drugim trackerem.

## Rozdzielone dowody cyklu

Instrukcja ręczna pozostaje wyłącznie w końcowej wiadomości czatu; runtime nie jest miejscem jej zapisu ani wymogiem odczytu acceptance.md. Historyczne `acceptance_instructions` zachowuj bez aktualizacji. Runtime zachowuje caller-owned pola checkpointu, w tym `implementation`, `checks`, `review`, `qa`, `acceptance_instructions`, `manual_verification`, `test_stage`, `user_acceptance`, `publication`, `merge` i `repair_attempts_by_problem`, bez nadawania im nowej ważności. Agent zapisuje rzeczywiste źródła, zakresy i wersje według change-contract; helper nie wykonuje ani nie zalicza tych etapów. Jawne raven-pr może rejestrować odbiór z wypowiedzi użytkownika, automatyczne `publish-pr` nigdy go nie tworzy.

`code_head_current`/`code_tree_current` to porównania diagnostyczne całego snapshotu, nie wyrok o ważności wszystkich dowodów. Skill ocenia wpływ zmian kod/config/deps/env na konkretny wynik i odbiór, zachowując wersje historyczne. Zmiana wyłącznie docs/test może nie naruszać odbioru; functional delta wymaga ponownego odbioru. Finalny merge nadal stosuje atomowy warunek aktualnego head SHA. Historyczny checkpoint bez nowych pól jest czytelny: uzupełniaj go rzeczywistym mapowaniem zachowanych dowodów, bez fikcyjnego wywołania etapów.
