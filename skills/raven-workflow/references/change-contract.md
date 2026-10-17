# Kontrakt pracy Git-first

## Źródła prawdy i mały kontekst

GitHub Issues jest obowiązkowym trackerem tasków, ich właścicieli, stanu projektu i roadmapy. Jeden issue odpowiada jednemu samodzielnie planowalnemu, weryfikowalnemu i mergeowalnemu change, jak zadanie Jira; fazy planu nie są issues. Project jest opcjonalnym widokiem tych samych issues, bez drugiego stanu do synchronizacji. Nie twórz lokalnej roadmapy ani drugiego backlogu.

`context/changes/<id>/plan.md` jest jednym dokumentem wykonawczym na branchu/PR: linki i wersje wymagań, kontrakt implementacji, plan testów, akceptacja, postęp oraz checkpoint. Git przechowuje wersje dokumentów, kodu i testów. Oddzielny raport dodawaj tylko jako potrzebny dowód, np. niezależne review; zwykły wynik testu lub postęp mieści się w planie. Nie twórz dodatkowego change.md, raportu implementacji ani kopii planu/raportów w GH. Dokumenty przekrojowe pozostają w `context/foundation/`; nie są trackerem tasków. PR linkuje issue i wersjonowany plan.

Przy wznowieniu: instrukcje repo → konkretny issue/change/branch/PR → plan i checkpoint → wskazane dowody → potrzebny diff. Nie skanuj boarda ani historii wszystkich issues. Jira może być źródłem wymagań; issue GH zawiera link i krótki zakres wykonania, nie kopię ticketu. Historyczne artefakty pozostają nienaruszone; kontynuacja wymaga jawnego mapowania do issue GH, bez automatycznej migracji historii.

## Podjęcie taska i stan widoczny zespołowi

Na początku **zleconego planowania lub implementacji**, przed badaniem szczegółów i edycją, rozwiąż dokładny issue i wykonawcę GH, odczytaj jego stan i ustaw In progress oraz assignee. Zlecenie tego etapu Raven obejmuje tę aktualizację jego issue; nie obejmuje push/PR/merge. Dla nowego jednoznacznego taska bez issue utwórz jeden issue z krótkim wynikiem, kryteriami i linkami do źródeł w ustalonym repo. Przy nieustalonym repo, wykonawcy lub kolizji z cudzym assignee wyjaśnij brak przed podjęciem; nie przejmuj pracy po samym timestampie. Nie twórz issue dla każdej fazy ani przy samym pytaniu o status.

Domyślnie otwarty issue z etykietą `in-progress` oznacza In progress, dodatkowe `blocked` oznacza blokadę, a `closed` oznacza Done. Nazwy etykiet mogą pochodzić z konfiguracji projektu. Przy blokadzie zachowaj wykonawcę i In progress, dodaj blocked oraz krótki powód i potrzebną decyzję w zarządzanym fragmencie issue. Usuń blokadę dopiero po potwierdzeniu rozwiązania. Review, gotowy PR, PASS i odbiór użytkownika pozostawiają issue In progress. Done/closed następuje wyłącznie po potwierdzonym udanym raven-merge dostarczającym cały zakres issue.

Odczyt/status jest read-only. Zapis wykonuj zdarzeniowo przy starcie/przejęciu, blokadzie/odblokowaniu i merge; zgodny stan oznacza no-op. Czytaj dokładny issue, zapisuj wyłącznie potrzebne pola z zachowaniem cudzych treści i sprawdzaj rezultat. Po timeout najpierw odczytaj stan; nie powtarzaj ślepo mutacji. Szczegóły [runtime](runtime.md) nie zastępują autoryzacji ani oceny wykonawcy.

Brak GH lub nieudany zapis statusu nie oznacza podjęcia taska. Oznacz `tracking-unconfirmed` i nazwij brak; wolno kontynuować niezależne rozpoznanie read-only, ale nie zaczynaj ani nie wznawiaj zależnego planowania/implementacji jako aktywnego taska bez potwierdzonego claimu. Jeśli dostęp zniknie w trakcie już podjętej pracy, zachowaj checkpoint; nie deklaruj aktualizacji blokady lub ukończenia bez readback i rozstrzygnij brak przed dalszą zależną pracą. Nie zastępuj GH lokalną roadmapą.

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

Konfiguracja `.raven/config.json` może utrwalać **wcześniej udzieloną** politykę publikacji. Brak polityki publikacji oznacza brak automatycznego push/PR; obowiązek trackingu issue pozostaje. Przykład struktury, nie gotowa zgoda:

```json
{
  "schema_version": 1,
  "repository": {"owner": "OWNER", "name": "REPO", "base_branch": "main"},
  "publication": {"mode": "local", "authorized_by": null},
  "tracker": {"type": "github-issues", "labels": {"in_progress": "in-progress", "blocked": "blocked"}}
}
```

`mode: draft-pr` wymaga rzeczywistego `authorized_by` i zakresu zgody obejmującego wskazane repo, branch, push i draft PR. Konfiguracja dokumentuje zgodę; samo wpisanie wartości jej nie tworzy. Zlecenie taska obejmuje opisany wyżej tracking, ale nie nadaje praw publikacji kodu ani merge. Jeżeli wcześniejsza polityka obejmuje bieżący change, publikuj draft wcześnie, po utworzeniu planu/brancha, i aktualizuj go podczas pracy bez kolejnych pytań. Brak zgody na push/PR blokuje wyłącznie publikację kodu; przy potwierdzonym trackingu przygotuj lokalnie gotowy wynik i pytaj dopiero o konkretną operację. `raven-pr` jest jawnie zleconą publikacją wskazanego zakresu.

Nie wysyłaj automatycznie raportów do komentarzy issue/PR, chyba że polecenie lub jawnie wywołany skill obejmuje tę publikację. PR może linkować wersjonowane pliki i krótko opisywać stan. Zewnętrzne uprawnienia, ograniczenia hosta i wymagania projektu nadal obowiązują. Nie używaj force push, nie mieszaj cudzych zmian, nie twórz boarda przy okazji.

## Dowody, checkpoint i ukończenie

W planie utrzymuj zwięzły checkpoint: etap wykonania, następny krok, URL/numer issue i potwierdzenie trackingu, branch, bazowy SHA, aktualny HEAD i dirty state, PR jeśli istnieje, fingerprint/akceptacja, odsyłacze do dowodów, nierozwiązane uwagi, liczniki prób. Ustal bazowy commit przed zmianami, zapisz jego pełny SHA w polu `base` pierwszego checkpointu i zachowaj go przy wznowieniu, także bez runtime `start`. Raport review zawiera oceniany zakres/tree, fingerprint, mapę wymagań na dowody, wyniki i konkretne luki. Dowód testu zawiera polecenie, wynik, wersję kodu, konfigurację i istotne środowisko. Nie przedstawiaj BLOCKED/NOT VERIFIED jako PASS.

Runtime zapisuje kanoniczny checkpoint JSON między markerami `raven:checkpoint:start/end` w planie poza kontraktem; użyj tego samego bloku przy ręcznej edycji. Lokalny operacyjny journal w wspólnym katalogu Git wspiera odzyskiwanie operacji, nie zastępuje planu. Zapis postępu nie stanowi akceptacji kontraktu.

Użytkownik odbiera wynik; jedna jednoznaczna wypowiedź „akceptuję, zmerguj” może potwierdzić odbiór i upoważnić merge. Nie wymaga to dodatkowej sesji QA. Merge wymaga aktualnych dowodów wymagań/testów/review, odbioru i zgody, wszystkich wymaganych CI oraz niezmienionego sprawdzonego head SHA. Draft PR ani akceptacja planu nie upoważniają do merge. Po potwierdzonym merge zamknij powiązany issue i zweryfikuj Done. Awaria tego zapisu oznacza „PR merged; issue nadal wymaga finalizacji”; nie cofaj ani nie powtarzaj merge. Board jest opcjonalnym widokiem i nie jest bramką. Deploy pozostaje osobną operacją.
