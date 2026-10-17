# Ograniczony helper runtime

`python3 <raven-workflow>/scripts/raven_runtime.py --repo PATH <command>` obsługuje poniższe operacje. Nie jest silnikiem etapów: nie ocenia wymagań, zgód, jakości review, CI ani gotowości merge. Nie commituję, nie pushuje, nie merguje i nie aktualizuje trackera. Sprawdź `--help` dla rzeczywistego interfejsu.

| Polecenie | Działanie |
| --- | --- |
| `fingerprint ID` | SHA-256 treści jedynego bloku contract z LF |
| `status ID` / `resume ID` | Read-only stan lokalny; bez sieci i bez odtwarzania historii GH |
| `start ID --session S --worktree PATH [--base HEAD]` | Jawny izolowany worktree i branch `raven/ID`; może zacząć przed powstaniem planu |
| `checkpoint ID --session S --stage STAGE --next NEXT [--evidence TEXT] [--acceptance-ref REF] [--repair-attempts N]` | Zapis kanonicznego checkpointu JSON w planie poza kontraktem |
| `publish-pr ID --session S --title TITLE --body-file PATH --dry-run` | Podgląd ograniczonej publikacji draftu |
| `publish-pr ID --session S --title TITLE --body-file PATH --apply` | Draft PR dla **już wypchniętego** aktualnego HEAD i autoryzowanej konfiguracji |
| `read-pr ID --number N` | Ograniczony odczyt wskazanego PR, bez historii komentarzy |

Przykład: `python3 <raven-workflow>/scripts/raven_runtime.py --repo /path/project status C-03`. Ścieżka skilla pochodzi z rzeczywistej instalacji, nie zgaduj katalogu. Jeśli helper jest niedostępny, nazwij brak; zwykłe operacje Git/plików są możliwe według tego samego kontraktu, bez udawania wyniku helpera.

`start` wymaga jawnej ścieżki worktree poza repo źródłowym. Jeśli plan już istnieje, jego pełne bajty muszą odpowiadać wybranemu commitowi bazowemu; helper nie commituje niezatwierdzonych plików. Nie przełącza ukradkiem głównej sesji. Brak planu jest raportowany jako `plan_missing: true`, `fingerprint: null` — nie jako gotowość pracy.

Checkpoint ma dokładnie jeden blok `<!-- raven:checkpoint:start -->` … `<!-- raven:checkpoint:end -->` poza kontraktem; zawiera JSON. Helper zapisuje stage/next/evidence, session, fingerprint, branch/head, base/PR jeśli znane, code_tree, checkpoint_sequence i opcjonalne repair_attempts/acceptance. Przy ręcznym zapisie zachowaj ten sam blok, nie twórz równoległego checkpointu w prozie. `checkpoint_sequence` liczy zapisy, nie próby napraw. `--repair-attempts` zapisuje rzeczywistą podaną liczbę; nie zeruj jej przy wznowieniu.

`--acceptance-ref` utrwala wyłącznie istniejący dowód decyzji, z fingerprintem i `verified: false`. Helper nie potwierdza zgody użytkownika; koordynator sprawdza ją w źródle. Bez nowego ref zachowuje dotychczasowy zapis. `contract_current`, `code_head_current` i `code_tree_current` są oddzielnymi porównaniami; zgodność kontraktu nie dowodzi aktualności testów. `dirty` obejmuje pliki nieśledzone. Checklista Progress pozostaje poza kontraktem; zapis checkpointu jej nie odhacza.

Lokalny journal w wspólnym katalogu Git wspiera wznowienie przerwanych operacji. Kanoniczny checkpoint jest w wersjonowanym planie. Mutex chroni czas pojedynczego polecenia, nie rezerwuje change dla sesji ani nie zapewnia blokady między hostami.

Publikacja wymaga `.raven/config.json` z `repository.owner/name/base_branch`, `publication.mode: draft-pr` i rzeczywistym `authorized_by`; te pola dokumentują wcześniejszą zgodę, nie nadają nowych praw. Helper używa `GH_TOKEN` albo `GITHUB_TOKEN`; nie wypisuj sekretów i nie zakładaj fallbacku do `gh auth`. Sprawdza tożsamość zdalnej gałęzi/HEAD oraz istniejący PR, odmawia niejednoznacznego powiązania i weryfikuje zapis. Tylko stan `published` potwierdza otwarty PR zgodny z SHA; `stale-remote`, `closed` i `merged` wymagają odrębnej interpretacji, nie są sukcesem nowej publikacji. Push i bogatszą aktualizację PR wykonuje raven-pr w zakresie zgody.

`read-pr` zwraca number/url/title/body/state/draft/merged/mergeable i tożsamość base/head. Nie pobiera CI ani reviews; te bramki odczytuje właściwy skill osobnym ograniczonym zapytaniem. `resume` nie rozwiązuje automatycznie PR do worktree: skill najpierw ustala mapowanie i potrzebny Git fetch w autoryzowanym zakresie.
