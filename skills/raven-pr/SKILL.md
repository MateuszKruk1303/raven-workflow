---
name: raven-pr
description: "Opublikuj change Raven: podziel jego niezacommitowane zmiany na logiczne commity, wykonaj zwykły push i utwórz lub zaktualizuj PR z aktualnym opisem oraz historią poprawek. Wywołanie jest decyzją publikacji; bez audytu gotowości, implementacji ani merge."
---

# Raven PR

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

Zlecenie publikacji przez raven-pr jest ostateczną decyzją użytkownika: obejmuje przygotowanie logicznych commitów z istniejących zmian ticketa, commit, zwykły push oraz utworzenie lub aktualizację PR. Wykonaj te kroki bez ponownego pytania o zgodę. Samo pytanie o skill lub status nie jest zleceniem publikacji. Nie implementuj nowych poprawek, nie wykonuj merge, deploya ani zmian statusów Project.

To krok publikacji. Nie wymagaj raportu testera, akceptacji review, zielonego CI ani ponownego potwierdzenia wcześniejszych etapów. Nie uruchamiaj samodzielnie testów, CI ani audytu gotowości. Zachowaj działające hooki commit/push i wymagane przez repo mechanizmy Git; nie omijaj ich ani nie uruchamiaj całego etapu implementacji w celu utworzenia commitu. Błąd hooka jest konkretną przeszkodą publikacji, nie zgodą na zmianę kodu lub wyłączenie kontroli.

Przeczytaj [wspólny kontrakt GitHub](../raven-auto-plan/references/github-contract.md) w zakresie tożsamości, zapisu i powiązań. Etapy testów i review pozostają częścią workflow; wywołanie PR nie uruchamia ich ani nie audytuje ich ukończenia.

## Ustal zakres i docelowy PR

Odczytaj instrukcje repo, github.json, change issue, istotne decyzje oraz rzeczywisty stan Git: branch, HEAD, base, remotes, śledzoną gałąź, commity do publikacji, staged, unstaged i untracked. Diff kodu i treść issue służą ustaleniu zakresu oraz opisu, nie ponownemu review. Pytaj tylko o rzeczywistą niejednoznaczność, której nie rozstrzygają źródła.

Przed commitami i pushem wyszukaj PR dla tego ticketa po powiązaniach oraz markerze `<!-- raven:pr change=C-03 -->` z rzeczywistym ID; sprawdź też head/base, repo źródłowe gałęzi i stany open/closed/merged. Raven ID nie jest globalnie unikalny: potwierdź pełny URL issue i repo artefaktów. Sama zbieżność nazwy brancha lub tytułu nie wystarcza.

- Jeden właściwy otwarty PR: aktualizuj go. Lokalna gałąź i docelowy remote muszą odpowiadać jego head repo/branch, a base uzgodnionemu celowi. Przy rozbieżności zatrzymaj publikację i wskaż właściwy PR; nie twórz alternatywnego PR ani nie pushuj innej gałęzi pod jego opis.
- Brak PR: utwórz go dla jednoznacznie ustalonego head/base. Nie publikuj bezpośrednio na base/default branch; jeśli zmiany są tam lokalnie, wydziel gałąź zmiany bez utraty pracy. Detached HEAD lub nierozstrzygnięta tożsamość wymagają ustalenia docelowej gałęzi przed zapisami.
- Wiele pasujących PR albo wyłącznie closed/merged: zgłoś stan i ustal dalszy cel. Nie otwieraj ponownie ani nie duplikuj zamkniętego PR bez osobnego zlecenia.

Przed zmianą zdalnej gałęzi zachowaj odczytany PR body, jego wersję/updatedAt i head SHA. Dla aktualizacji oraz każdego wznowienia przeczytaj [historię publikacji i ponowienia](references/publication-history.md). Nie utożsamiaj obecnego zdalnego HEAD z ostatnią wersją opisaną w PR.

## Przygotuj logiczne commity

Zachowaj istniejące commity implementacji. Grupuj tylko niezacommitowane zmiany należące do ticketa według spójnego celu, np. zachowanie z jego testami albo niezależna aktualizacja dokumentacji. Jeden mały spójny diff może być jednym commitem; nie narzucaj liczby commitów ani podziału na pliki. Opisy commitów dopasuj do konwencji repo i rzeczywistego zakresu.

Rozdziel staged, unstaged oraz untracked należące do ticketa od cudzych zmian. Nie używaj zbiorczego `git add .`/`git add -A` ani commitu całego zastanego indeksu. Przy mieszanych plikach wybierz konkretne hunki; samo filtrowanie ścieżek nie wystarcza. Gdy zmian nie da się bezpiecznie rozdzielić albo przypisać do ticketa, pozostaw je i ustal zakres przed zależnym commitem/pushem.

Zachowaj obce pliki i ich stan staged/unstaged. Użyj selektywnego stagingu, a przy zajętym indeksie izolowanego indeksu lub równoważnej metody, która nie wciągnie obcych zmian do commitu. Zachowaj stan początkowy do porównania; po commitach uzgodnij indeks z nowym HEAD wyłącznie dla opublikowanych hunków, pozostawiając cudzy staged diff i working tree. Nie stosuj globalnego resetu ani stashowania cudzej pracy. Jeśli nie potrafisz zachować tego stanu, zatrzymaj się przed commitem.

Przed każdym commitem sprawdź dokładny staged diff, po nim jego SHA i rzeczywistą zawartość oraz pozostały diff. Hook może zmienić pliki lub odrzucić commit: odczytaj wynik i nie traktuj samych komunikatów jako dowodu utworzenia commitu. Nie dodawaj automatycznie nowych zmian hooka o nieustalonym zakresie. Nie wykonuj amend, reset, rebase ani squash istniejących commitów dla uporządkowania historii. Brak niezacommitowanych zmian jest prawidłowy — przejdź do publikacji istniejących commitów bez pustego commitu.

## Przygotuj aktualny opis

Tytuł i opis dopasuj do szablonu repo oraz całego aktualnego diffu PR względem base. Prowadź opis od problemu i wynikowego zachowania. Zawrzyj krótko cel, rzeczywiste zmiany, link do change i istotne kompromisy, odstępstwa lub ograniczenia niewyjaśnione w artefaktach issue. Podaj przykład przed/po, gdy pomaga. Nie kopiuj planu ani historii rozmowy i nie wymyślaj uzasadnień.

Aktualizacja PR po poprawkach ma dwa rezultaty w jego body: opis całego aktualnego rozwiązania oraz zachowaną, uzupełnioną historię opublikowanych poprawek. Sam komentarz, lista commitów lub dopisanie najnowszej poprawki do nieaktualnego opisu nie wystarcza. Używaj bloków i granic SHA z [referencji historii](references/publication-history.md), zachowując ręczne dopiski. Przy pierwszym PR zapisz punkt początkowy historii; nie przedstawiaj pierwszej publikacji jako poprawki wcześniejszej wersji.

Przytocz dostępne wyniki weryfikacji, jeśli pomagają lub wymaga ich szablon, z ich rzeczywistym zakresem/SHA i ograniczeniami. Nowy commit nie dziedziczy automatycznie PASS starszego drzewa. Nie deklaruj niepotwierdzonej gotowości do merge ani nie uruchamiaj dodatkowych kontroli dla wypełnienia opisu.

## Push i zapis PR

Sprawdź dokładny zakres wysyłanych commitów, remote i docelowy ref. Obce commity w zakresie push także wymagają rozstrzygnięcia; izolacja stagingu nie usuwa ich z historii. Wykonaj zwykły push do ustalonego head brancha, nigdy force-push. Odrzucony push lub rozbieżną historię zgłoś bez automatycznego pull/rebase/merge i bez przepisywania historii. Jeśli właściwy SHA już jest zdalnie, nie powtarzaj pushu.

Po potwierdzeniu zdalnego SHA ponownie odczytaj PR i jego body/updatedAt, także po niepewnym wyniku wcześniejszego tworzenia. Zachowaj cudze edycje i wcześniejszą historię, aktualizując własne bloki. Przy kolizji treści ustal rozstrzygnięcie zamiast nadpisywać. Przekaż body strukturalnie lub przez `--body-file`, bez interpolowania tekstu do shella. W nowym PR domyślnie użyj zwykłego PR, draft na życzenie; w istniejącym zachowaj stan draft, chyba że użytkownik zlecił jego zmianę.

Powiąż pełny zakres issue przez `Closes #...`, częściowy przez `Refs #...`; uwzględnij tylko rzeczywiście objęte taski. Przy oddzielnym `code_repository` commit/push/PR dotyczą repo kodu, a issue repo artefaktów linkuj pełnym URL jako Refs. Closes dla innego repo wymaga jawnie ustalonego powiązania i potwierdzonego zakresu. Nie ujawniaj linków prywatnych artefaktów w szerszym/publicznym PR bez ustalonej zgody. Nie zamykaj issues bezpośrednio, nie ustawiaj Done i nie konfiguruj finalizacji Project.

Odczytaj zapisany PR: URL, head/base i SHA, tytuł, aktualny opis, historię oraz powiązania. Dopiero potwierdzony odczyt oznacza zakończenie publikacji. Przy częściowym sukcesie podaj utworzone SHA, stan push/PR i dokładny brakujący krok, zachowując payload do wznowienia według referencji. Nie odwracaj wykonanych commitów/pushu ani nie zaczynaj implementacji od nowa. Zakończ linkiem do PR, krótkim zakresem publikacji oraz informacją o pozostawionych obcych zmianach, jeśli występują. Nie przejmuj monitorowania CI ani napraw kodu. Następny osobno zlecany etap to [raven-merge](../raven-merge/SKILL.md) dla tego samego C-ID: merge po spełnieniu bramek, następnie jawne Done na właściwym Project. Samo zlecenie raven-pr nie upoważnia do tego etapu.
