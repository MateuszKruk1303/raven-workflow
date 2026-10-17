# Kontrakt pracy Git-first

## Źródła prawdy i mały kontekst

Plan i stan change są w `context/changes/<id>/plan.md`. Wersje dokumentów, kodu i testów przechowuje historia Git. Raporty powstają obok planu; dokumenty przekrojowe w `context/foundation/`. Pliki są zwykłą częścią repo, podlegają review i celowemu stagingowi. Nie twórz issue dla każdej fazy, snapshotów planu w komentarzach ani drugiej edytowalnej kopii stanu. GitHub PR służy współpracy, review i CI. Issues i Project są opcjonalnym trackerem.

Przy wznowieniu: instrukcje repo → jednoznaczny change/branch/PR → aktualny plan i checkpoint → wskazane raporty → potrzebny diff. Czytaj pełny obowiązujący kontrakt, ale nie całą historię komentarzy ani wszystkich changes. Sięgaj do konkretnego commitu lub wątku tylko przy luce, sprzeczności albo potrzebie zweryfikowania decyzji. Brak dostępu do GH nie blokuje lokalnej analizy/implementacji; uniemożliwia potwierdzenie zdalnych review, CI i merge. Nie zgaduj statusu.

Roadmapa ma jedno miejsce: `context/roadmap.md` albo jeden już używany tracker. Lokalny plan może wskazywać wymagania z Jira/GH; link jest źródłem wymagań, nie obowiązkiem ich duplikowania w issues. Historyczne artefakty Raven pozostają nienaruszone. Ich kontynuacja wymaga jawnego ustalenia mapowania do aktualnego change, bez automatycznej migracji.

## Plan, zgoda i postęp

Użyj [szablonu planu](../../raven-plan/references/procedures/plan/references/plan-templates.md). Jedyny blok `<!-- raven:contract:start -->` … `<!-- raven:contract:end -->` zawiera ID, wynik, źródła i wersje wymagań, kryteria odbioru, zakres/wyłączenia, istotne decyzje techniczne, kroki ze stabilnymi ID, ryzyka, zobowiązania testowe i bramki. Checklista wykonania oraz checkpoint leżą poza blokiem.

Fingerprint to SHA-256 zawartości bloku z końcami linii LF. Nie usuwa treści ani whitespace wewnątrz bloku. Użyj runtime `fingerprint`, zamiast ręcznie wymyślać hash. Akceptacja wskazuje ten fingerprint, rzeczywistą decyzję użytkownika i jej źródło. Zlecenie „zrealizuj ten plan” może być akceptacją jednoznacznie pokazanej wersji. Status, upływ czasu, review agenta ani wpis helpera nie są zgodą człowieka. Nie wymyślaj decyzji podczas zapisu.

Zmiana kontraktu wymaga odświeżenia review w dotkniętym zakresie i nowej akceptacji przed zależnym wykonaniem. Checkboxy, wyniki testów, checkpoint, lokalizacja raportu i pozostały opis wykonania nie unieważniają akceptacji. Nie przenoś decyzji na zmienione wymagania ani zatwierdzone podejście techniczne. Rutynowe szczegóły realizacji w istniejących granicach nie wymagają nowego planu.

Przed nowym planowaniem lub implementacją utwórz albo odzyskaj branch change. Domyślnie pracuj w aktualnym checkout; osobny worktree wybierz przy równoległej pracy, potrzebie izolacji lub wyraźnym życzeniu użytkownika. Przy wznowieniu zachowaj istniejący branch i katalog pracy. Przed przełączeniem sprawdź kolizje, staging i dirty state; nie przenoś cudzych zmian na nową gałąź ani nie resetuj, stashuj czy commituj ich dla porządku. Gdy utrudniają bezpieczną pracę, użyj izolowanego worktree lub ustal sposób zachowania zmian. Worktree twórz poza repo, przez opcjonalny runtime `start` lub bezpieczne Git. Odczyt/status nie tworzą brancha ani worktree.

## Współpraca i przekazanie sesji

Jeden change ma jednego aktywnego zapisującego wykonawcę. W kanonicznym checkpointcie zapisuj identyfikator sesji oraz właściciela pracy (`session`, `owner`), stan i następny krok. Przed edycją sprawdź aktualnego właściciela oraz katalog pracy; reviewer pracuje read-only wobec ocenianego kodu, planu i testów. Równoległe rozpoznanie read-only jest możliwe, ale dwóch autorów nie edytuje jednocześnie tego samego change.

Przekazanie jest jawne: dotychczasowy wykonawca zatrzymuje zapisy i procesy modyfikujące pliki, utrwala checkpoint z bazą/drzewem, dowodami i licznikami, a koordynator lub użytkownik przekazuje zakres następnej sesji. Nowy wykonawca potwierdza przejęcie w tym samym checkpointcie i kontynuuje od zapisanej granicy. Upływ czasu, stary timestamp albo brak odpowiedzi nie upoważniają do automatycznego przejęcia; przy nieznanym stanie ustal właściciela przed zależnymi zapisami.

Mutex runtime chroni wyłącznie czas pojedynczej komendy na danym wspólnym katalogu Git. Nie jest rezerwacją sesji ani rozproszoną blokadą między hostami. Checkpoint i jawny handoff są protokołem współpracy, nie gwarancją transakcyjną. Nie zeruj liczników prób ani nie nadpisuj cudzych pól podczas przekazania.

## Wykonanie i niezależna kontrola

Manual i auto używają tych samych plików, fingerprintu i dowodów. Manual oddaje wynik zleconego etapu; auto koordynuje wykonanie oraz ograniczoną pętlę napraw i review. Nie pytaj o każdą komendę, commit, fazę ani oczywistą poprawkę w zatwierdzonym zakresie. Respektuj rzeczywiste manual gates. Zmiana wymagań, istotnego podejścia albo nieobjęte uprawnienie wraca do użytkownika.

Testy powstają wraz z implementacją. Dobierz unit/integration/E2E do ryzyka i istniejącej ochrony, bez obowiązku każdej warstwy. Przed niechronionym refaktorem zapewnij testy charakteryzacyjne; przed bugfixem reprodukcję, gdy ma sens. Brak nowych testów uzasadnij obserwowalnym charakterem zmiany lub istniejącym pokryciem. Sam browser smoke nie zastępuje wymaganych trwałych testów.

Normalny change otrzymuje jedno świeże niezależne review kodu, wymagań i testów po implementacji. Review planu jest osobnym wcześniejszym etapem. Dodatkowy tester, QA lub specjalistyczny audyt wynika z konkretnego ryzyka (np. auth, migracja, rozliczenia, współbieżność) lub zlecenia; nie mnożymy ról automatycznie. Reviewer nie poprawia ocenianej pracy.

Potwierdzone defekty w zakresie zleconego wykonania naprawiaj bez nowej zgody. Dwie nieskuteczne próby tego samego problemu zatrzymują zależną pętlę: zapisz reprodukcję, próby i potrzebną decyzję. Nowy agent lub sesja nie zerują licznika. Awaria środowiska nie jest defektem produktu. Po poprawce odśwież dotknięte testy i review; nie powtarzaj całej suite bez przyczyny.

## Publikacja i uprawnienia

Konfiguracja `.raven/config.json` może utrwalać **wcześniej udzieloną** politykę publikacji. Domyślny brak konfiguracji oznacza pracę lokalną. Przykład struktury, nie gotowa zgoda:

```json
{
  "schema_version": 1,
  "repository": {"owner": "OWNER", "name": "REPO", "base_branch": "main"},
  "publication": {"mode": "local", "authorized_by": null},
  "tracker": {"type": "local", "ref": "context/roadmap.md"}
}
```

`mode: draft-pr` wymaga rzeczywistego `authorized_by` i zakresu zgody obejmującego wskazane repo, branch, push i draft PR. Konfiguracja dokumentuje zgodę; samo wpisanie wartości jej nie tworzy. Zlecenie taska nie daje nowych praw zewnętrznych. Jeżeli wcześniejsza polityka obejmuje bieżący change, publikuj draft wcześnie, po utworzeniu planu/brancha, i aktualizuj go podczas pracy bez kolejnych pytań. Brak zgody blokuje wyłącznie publikację; przygotuj lokalnie gotowy wynik i pytaj dopiero o konkretną operację. `raven-pr` jest jawnie zleconą publikacją wskazanego zakresu.

Nie wysyłaj automatycznie raportów do komentarzy issue/PR, chyba że polecenie lub jawnie wywołany skill obejmuje tę publikację. PR może linkować wersjonowane pliki i krótko opisywać stan. Zewnętrzne uprawnienia, ograniczenia hosta i wymagania projektu nadal obowiązują. Nie używaj force push, nie mieszaj cudzych zmian, nie twórz boarda przy okazji.

## Dowody, checkpoint i ukończenie

W planie utrzymuj zwięzły checkpoint: stage/status, następny krok, branch, bazowy SHA, aktualny HEAD i dirty state, PR jeśli istnieje, fingerprint/akceptacja, odsyłacze do dowodów, nierozwiązane uwagi, liczniki prób. Ustal bazowy commit przed zmianami, zapisz jego pełny SHA w polu `base` pierwszego checkpointu i zachowaj go przy wznowieniu, także bez runtime `start`. Raport review zawiera oceniany zakres/tree, fingerprint, mapę wymagań na dowody, wyniki i konkretne luki. Dowód testu zawiera polecenie, wynik, wersję kodu, konfigurację i istotne środowisko. Nie przedstawiaj BLOCKED/NOT VERIFIED jako PASS.

Runtime zapisuje kanoniczny checkpoint JSON między markerami `raven:checkpoint:start/end` w planie poza kontraktem; użyj tego samego bloku przy ręcznej edycji. Lokalny operacyjny journal w wspólnym katalogu Git wspiera odzyskiwanie operacji, nie zastępuje planu. Zapis postępu nie stanowi akceptacji kontraktu.

Użytkownik odbiera wynik; jedna jednoznaczna wypowiedź „akceptuję, zmerguj” może potwierdzić odbiór i upoważnić merge. Nie wymaga to dodatkowej sesji QA. Merge wymaga aktualnych dowodów wymagań/testów/review, odbioru i zgody, wszystkich wymaganych CI oraz niezmienionego sprawdzonego head SHA. Draft PR ani akceptacja planu nie upoważniają do merge. Board jest opcjonalny; awaria jego aktualizacji nie cofa ani nie blokuje poprawnego merge. Zapis trackera wymaga odpowiedniej zgody. Deploy pozostaje osobną operacją.
