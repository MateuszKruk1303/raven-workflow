# Kontrakt pracy Git-first

## Zakres kontraktu i wyjątek auto-implement

Poniższe reguły etapów, trackingu, fingerprintu/review, checkpointów i przekazania obowiązują standardowy workflow. Samodzielny [raven-auto-implement](../../raven-auto-implement/SKILL.md) jest wyjątkiem: wykonuje wskazany plan oraz aktualne polecenie, bez tych obowiązków i bez uruchamiania kolejnych etapów. Nie wymaga aktualizacji ani review planu po zmianie wymagania w poleceniu. Kończy na potrzebnych zmianach, adekwatnej samoweryfikacji i krótkim finale w czacie. W JSON opisuje go osobne `auto_implementation`, poza `stages`; nie jest dodatkowym etapem workflow. Wyjątek nie zmienia wymagań innych skilli, w tym osobno zleconego PR i merge, ani rzeczywistych ograniczeń projektu/narzędzi i bezpieczeństwa.

## Źródła prawdy i mały kontekst

GitHub Issues jest obowiązkowym trackerem tasków, ich właścicieli, stanu projektu i roadmapy. Jeden issue odpowiada jednemu samodzielnie planowalnemu, weryfikowalnemu i mergeowalnemu change, jak zadanie Jira; fazy planu nie są issues. Project jest opcjonalnym widokiem tych samych issues, bez drugiego stanu do synchronizacji. Nie twórz lokalnej roadmapy ani drugiego backlogu.

`context/changes/<id>/plan.md` jest jednym dokumentem wykonawczym na branchu/PR: linki i wersje wymagań, kontrakt implementacji, plan testów, postęp oraz checkpoint. Instrukcja ręcznej weryfikacji występuje wyłącznie w końcowej wiadomości czatu; nie twórz ani nie aktualizuj acceptance.md i nie kopiuj kroków odbioru do planu, issue, PR ani QA. Historyczne artefakty pozostają bez zmian. Git przechowuje wersje dokumentów, kodu i testów. Oddzielny raport dodawaj tylko jako potrzebny dowód, np. niezależne review; zwykły wynik testu lub postęp mieści się w planie. Nie twórz dodatkowego change.md, raportu implementacji ani kopii planu/raportów w GH. Dokumenty przekrojowe pozostają w `context/foundation/`; nie są trackerem tasków. PR linkuje issue i wersjonowany plan.

Przy wznowieniu: instrukcje repo → konkretny issue/change/branch/PR → plan i checkpoint → wskazane dowody → potrzebny diff. Nie skanuj boarda ani historii wszystkich issues. Jira może być źródłem wymagań; issue GH zawiera link i krótki zakres wykonania, nie kopię ticketu. Historyczne artefakty pozostają nienaruszone; kontynuacja wymaga jawnego mapowania do issue GH, bez automatycznej migracji historii.

## Podjęcie taska i stan widoczny zespołowi

Na początku **zleconego planowania lub implementacji**, przed badaniem szczegółów i edycją, rozwiąż dokładny issue i wykonawcę GH, odczytaj jego stan i ustaw In progress oraz assignee. Zlecenie tego etapu Raven obejmuje tę aktualizację jego issue; nie obejmuje push/PR/merge. Dla nowego jednoznacznego taska bez issue utwórz jeden issue z krótkim wynikiem, kryteriami i linkami do źródeł w ustalonym repo. Przy nieustalonym repo, wykonawcy lub kolizji z cudzym assignee wyjaśnij brak przed podjęciem; nie przejmuj pracy po samym timestampie. Nie twórz issue dla każdej fazy ani przy samym pytaniu o status.

Domyślnie otwarty issue z etykietą `in-progress` oznacza In progress, dodatkowe `blocked` oznacza blokadę, a `closed` oznacza Done. Nazwy etykiet mogą pochodzić z konfiguracji projektu. Przy blokadzie zachowaj wykonawcę i In progress, dodaj blocked oraz krótki powód i potrzebną decyzję w zarządzanym fragmencie issue. Usuń blokadę dopiero po potwierdzeniu rozwiązania. Review, gotowy PR, PASS i odbiór użytkownika pozostawiają issue In progress. Done/closed następuje wyłącznie po potwierdzonym udanym raven-merge dostarczającym cały zakres issue.

Odczyt/status jest read-only. Zapis wykonuj zdarzeniowo przy starcie/przejęciu, blokadzie/odblokowaniu i merge; zgodny stan oznacza no-op. Czytaj dokładny issue, zapisuj wyłącznie potrzebne pola z zachowaniem cudzych treści i sprawdzaj rezultat. Po timeout najpierw odczytaj stan; nie powtarzaj ślepo mutacji. Szczegóły [runtime](runtime.md) nie zastępują autoryzacji ani oceny wykonawcy.

Brak GH lub nieudany zapis statusu nie oznacza podjęcia taska. Oznacz `tracking-unconfirmed` i nazwij brak; wolno kontynuować niezależne rozpoznanie read-only, ale nie zaczynaj ani nie wznawiaj zależnego planowania/implementacji jako aktywnego taska bez potwierdzonego claimu. Jeśli dostęp zniknie w trakcie już podjętej pracy, zachowaj checkpoint; nie deklaruj aktualizacji blokady lub ukończenia bez readback i rozstrzygnij brak przed dalszą zależną pracą. Nie zastępuj GH lokalną roadmapą.

## Plan i postęp

Użyj [szablonu planu](../../raven-plan/references/procedures/plan/references/plan-templates.md). Jedyny blok `<!-- raven:contract:start -->` … `<!-- raven:contract:end -->` zawiera ID, wynik, źródła i wersje wymagań, kryteria odbioru, zakres/wyłączenia, istotne decyzje techniczne, kroki ze stabilnymi ID, ryzyka, zobowiązania testowe i bramki. Checklista wykonania oraz checkpoint leżą poza blokiem.

Fingerprint to SHA-256 zawartości bloku z końcami linii LF. Nie usuwa treści ani whitespace wewnątrz bloku. Użyj runtime `fingerprint`, zamiast ręcznie wymyślać hash. Review wskazuje oceniony fingerprint. Plan nie ma pola ani etapu formalnej akceptacji. Zlecenie implementacji jednoznacznego planu, przez raven-implement, uruchamia wykonanie w jego zakresie po sprawdzeniu aktualnego niezależnego review i rozstrzygnięciu blokujących findings. Nie zapisuj zastępczego rejestru zgody wykonania. Sam gotowy plan, review lub PASS nie uruchamia implementacji.

Zmiana kontraktu wymaga aktualizacji planu i odświeżenia review w dotkniętym zakresie przed zależnym wykonaniem. Jawne nowe wymaganie użytkownika w zleceniu poprawki jest już decyzją: uwzględnij je bez ponownego pytania o akceptację planu. Pytaj wyłącznie o nierozstrzygnięty wybór, sprzeczność lub rozszerzenie poza zlecenie. Checkboxy, wyniki testów, checkpoint, lokalizacja raportu i pozostały opis wykonania nie zmieniają fingerprintu kontraktu. Rutynowe szczegóły realizacji w istniejących granicach nie wymagają nowego planu.

Przed zapisami nowego planu lub implementacji zastosuj [przygotowanie brancha change](change-branch.md): rozwiąż konkretny task, odróżnij go od zamkniętego/merged poprzednika i ustal nowy branch przed utworzeniem folderu planu. Przy nowym change zapytaj o branch, chyba że zgoda już obejmuje ten task; po zgodzie przygotuj go z potwierdzonej aktualnej bazy projektu. Domyślnie użyj aktualnego checkoutu. Wznowienie aktywnego change zachowuje branch, katalog i bazowy SHA. Dirty tree, kolizje i izolację obsłuż według tej samej procedury, bez przenoszenia cudzych zmian, resetu, stasha czy porządkowego commitu. Worktree pozostaje wariantem izolacji, tworzonym poza repo; odczyt/status nie tworzą brancha ani worktree.

## Współpraca i przekazanie sesji

Jeden change ma jednego aktywnego zapisującego wykonawcę. W kanonicznym checkpointcie zapisuj identyfikator sesji oraz właściciela pracy (`session`, `owner`), stan i następny krok. Przed edycją sprawdź aktualnego właściciela oraz katalog pracy; reviewer pracuje read-only wobec ocenianego kodu, planu i testów. Równoległe rozpoznanie read-only jest możliwe, ale dwóch autorów nie edytuje jednocześnie tego samego change.

Przekazanie jest jawne: dotychczasowy wykonawca zatrzymuje zapisy i procesy modyfikujące pliki, utrwala checkpoint z bazą/drzewem, dowodami i licznikami, a koordynator lub użytkownik przekazuje zakres następnej sesji. Nowy wykonawca potwierdza przejęcie w tym samym checkpointcie i kontynuuje od zapisanej granicy. Upływ czasu, stary timestamp albo brak odpowiedzi nie upoważniają do automatycznego przejęcia; przy nieznanym stanie ustal właściciela przed zależnymi zapisami.

Mutex runtime chroni wyłącznie czas pojedynczej komendy na danym wspólnym katalogu Git. Nie jest rezerwacją sesji ani rozproszoną blokadą między hostami. Checkpoint i jawny handoff są protokołem współpracy, nie gwarancją transakcyjną. Nie zeruj liczników prób ani nie nadpisuj cudzych pól podczas przekazania.

## Wykonanie i niezależna kontrola

Etapy standardowego workflow używają tych samych plików, fingerprintu i dowodów. Manual oddaje wynik zleconego etapu. Samodzielny auto-implement podlega wyjątkowi na początku tego dokumentu. Auto-plan zachowuje własną pętlę planowania i review. Nie pytaj o każdą komendę, commit, fazę ani oczywistą poprawkę w zleconym zakresie. Respektuj rzeczywiste manual gates. Nierozstrzygnięta zmiana wymagań lub istotnego podejścia, rozszerzenie poza zlecenie albo nieobjęte uprawnienie wraca do użytkownika; nie pytaj ponownie o decyzję podaną w zleceniu.

Testy powstają wraz z implementacją. Dobierz unit/integration/E2E do ryzyka i istniejącej ochrony, bez obowiązku każdej warstwy. Przed niechronionym refaktorem zapewnij testy charakteryzacyjne; przed bugfixem reprodukcję, gdy ma sens. Brak nowych testów uzasadnij obserwowalnym charakterem zmiany lub istniejącym pokryciem. Sam browser smoke nie zastępuje wymaganych trwałych testów.

Normalny change otrzymuje jedno świeże niezależne review kodu, wymagań i testów przez osobno wywołane raven-implement-review przed standardowym PR. Review planu jest wcześniejszą bramką raven-implement. Samodzielny `raven-auto-implement` podlega wyjątkowi na początku tego dokumentu. Jawne bramki i konieczne testy bezpieczeństwa/kontraktu mają pierwszeństwo. Szerokie QA jest opcjonalnym osobnym zleceniem; reviewer/tester nie uruchamia się automatycznie. Zlecony reviewer nie poprawia ocenianej pracy, a osobny tester nie zmienia produktu ani trwałych testów.

Potwierdzone defekty w zakresie zleconego wykonania naprawiaj bez nowej zgody. Dwie nieskuteczne próby tego samego problemu zatrzymują zależną pętlę: zapisz reprodukcję, próby i potrzebną decyzję. Nowy agent lub sesja nie zerują licznika. Awaria środowiska nie jest defektem produktu. Nie naprawiaj automatycznie zastanych niezwiązanych testów, fixture, locatorów ani infrastruktury; zapisz ograniczenie i sprawdź krytyczną ścieżkę dostępnym adekwatnym kanałem. Rzeczywista blokada ścieżki lub wymaganej bramki pozostaje BLOCKED/NOT VERIFIED. Po poprawce ponów reprodukcję i zależną regresję; oznacz dotknięte review do odświeżenia w osobno zleconym etapie. Nie powtarzaj całej suite bez przyczyny.

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

`mode: draft-pr` wymaga rzeczywistego `authorized_by` i zakresu zgody obejmującego wskazane repo, branch, push i draft PR. Konfiguracja dokumentuje zgodę; samo wpisanie wartości jej nie tworzy. Zlecenie taska obejmuje opisany wyżej tracking, ale nie nadaje praw publikacji kodu ani merge. Jeżeli wcześniejsza polityka obejmuje bieżący change, publikuj draft wcześnie, po utworzeniu planu/brancha, i aktualizuj go podczas pracy bez kolejnych pytań. Brak zgody na push/PR blokuje wyłącznie publikację kodu; przy potwierdzonym trackingu przygotuj lokalnie gotowy wynik i pytaj dopiero o konkretną operację. Jawne `raven-pr <id>` jest publikacją i odbiorem jednoznacznie wskazanej wersji: zapisuj rzeczywiste źródło, zakres i wersję decyzji. Automatyczna polityka draftu, istnienie PR, PASS, status, auto/test ani jawnie nieodebrany draft nie odbierają wyniku. Brak implementacji dopuszcza tylko jawnie ustalony incomplete draft. Standardowy PR następuje po raven-test; przy konkretnym braku stosuj pytanie i wyjątek z raven-pr, bez obchodzenia merge/CI.

Nie wysyłaj automatycznie raportów do komentarzy issue/PR, chyba że polecenie lub jawnie wywołany skill obejmuje tę publikację. PR może linkować wersjonowane pliki i krótko opisywać stan. Zewnętrzne uprawnienia, ograniczenia hosta i wymagania projektu nadal obowiązują. Nie używaj force push, nie mieszaj cudzych zmian, nie twórz boarda przy okazji.

## Dowody, checkpoint i ukończenie

W planie utrzymuj zwięzły checkpoint: etap wykonania, następny krok, URL/numer issue i potwierdzenie trackingu, branch, bazowy SHA, aktualny HEAD i dirty state, PR jeśli istnieje, fingerprint, odsyłacze do dowodów, nierozwiązane uwagi, liczniki prób. Ustal bazowy commit przed zmianami, zapisz jego pełny SHA w polu `base` pierwszego checkpointu i zachowaj go przy wznowieniu, także bez runtime `start`. Raport review zawiera oceniany zakres/tree, fingerprint, mapę wymagań na dowody, wyniki i konkretne luki. Dowód testu zawiera polecenie, wynik, wersję kodu, konfigurację i istotne środowisko. Nie przedstawiaj BLOCKED/NOT VERIFIED jako PASS.

Samodzielny `raven-auto-implement` nie zapisuje checkpointu ani `execution_mode`; jego wynik trafia do czatu. Nie twórz automatycznie pola `qa_required` ani raportów QA. Historyczne `qa_required: true`, tryb auto i raporty zachowaj, lecz same nie stanowią obecnej bramki ani nie uruchamiają starego cyklu. QA jest wymagane wyłącznie na podstawie odrębnego jawnego zlecenia lub bramki projektu/kontraktu; zapisz źródło takiego obowiązku. Zmiana skilli nie uchyla tego zlecenia ani rzeczywistych bramek.

Runtime zapisuje kanoniczny checkpoint JSON między markerami `raven:checkpoint:start/end` w planie poza kontraktem; użyj tego samego bloku przy ręcznej edycji. Lokalny operacyjny journal w wspólnym katalogu Git wspiera odzyskiwanie operacji, nie zastępuje planu. Historyczne pola akceptacji planu, w tym `acceptance`, pozostają zachowanymi, ignorowanymi danymi: nie są bramką i nie są tworzone ani aktualizowane. Zachowaj je oraz nieznane pola przy checkpoint/resume, bez migracji historii.

Użytkownik odbiera wynik; jawne raven-pr dla jednoznacznej wersji zapisuje ten odbiór, a jedna jednoznaczna wypowiedź „akceptuję, zmerguj” może potwierdzić odbiór i upoważnić merge. Merge honoruje wcześniej zapisany odbiór z PR dla aktualnego zakresu i wersji, bez ponownego pytania. Functional delta wymaga ponownego odbioru; docs/test-only delta wymaga udokumentowanej oceny wpływu, nie automatycznego unieważnienia przez zmianę SHA. Nie wymaga to kolejnej sesji QA po aktualnym zaliczonym przebiegu. QA sprawdzaj tylko, gdy wymaga go odrębne jawne zlecenie lub bramka projektu/kontraktu; samo historyczne `qa_required` lub tryb auto nie wystarcza. Merge wymaga aktualnych dowodów wymagań/testów/review oraz wymaganego QA, odbioru i zgody, wszystkich wymaganych CI oraz niezmienionego sprawdzonego head SHA. Draft PR ani gotowy plan nie upoważniają do merge. Po potwierdzonym merge zamknij powiązany issue i zweryfikuj Done. Awaria tego zapisu oznacza „PR merged; issue nadal wymaga finalizacji”; nie cofaj ani nie powtarzaj merge. Board jest opcjonalnym widokiem i nie jest bramką. Deploy pozostaje osobną operacją.

## Etapy, aktualność i przekazanie dowodów

Możliwe wykorzystanie wyniku auto-implement w standardowym cyklu: plan + plan-review (albo auto-plan) → osobno zlecone auto-implement → ręczna weryfikacja → poprawki auto-implement → osobno zlecone raven-implement-review → raven-test → jawne raven-pr → osobno zlecony merge. Ta kolejność nie jest warunkiem ani zadaniem samodzielnego auto-implement. Manual implement + implement-review pozostaje prostą alternatywą bez obowiązkowego auto QA i bez domyślnego końcowego domknięcia regresji. Wywołanie test nie potwierdza wykonania kroków ręcznych ani odbioru/publikacji. Ręczna weryfikacja i odbiór to odrębne zdarzenia.

W kanonicznym checkpointcie oddziel pola:
- `implementation` i `checks`: zakres, stan, mapa AC → test/asercja/polecenie/wynik, wersja/config/deps/env i luki;
- `review` oraz `qa`, gdy etap rzeczywiście wystąpił: raporty, oceniona wersja, scenariusze, wyniki, findings i liczniki; zachowaj historyczne pola, bez przywracania automatycznego QA przez `execution_mode`/`qa_required`;
- `manual_verification`: rzeczywisty feedback, wynik i źródło albo jawny brak; nie zapisuj tu kopii instrukcji ręcznej. Historyczne `acceptance_instructions` i acceptance.md zachowaj bez aktualizacji; nie są wymaganym wejściem ani wyjściem nowych etapów;
- `test_stage`: zakończenie audytu, wystarczalność ochrony, wykorzystane dowody/uzasadnienie reuse, zamknięte i otwarte luki;
- `user_acceptance`: źródło rzeczywistej decyzji, scope, fingerprint i odebrana wersja/tree; dotyczy odbioru produktu, niezależnego od planowania;
- `publication`/`merge`: autoryzacja, wyjątki, potwierdzony wynik i URL/SHA. `repair_attempts_by_problem` zachowuje stabilne ID i liczniki, bez zerowania na nowej sesji.

To pola rozszerzające istniejący checkpoint, nie nowy tracker ani obowiązek zapełniania pustych etapów. Reuse ocenia wpływ delty na konkretny dowód kod/config/deps/env, nie całe drzewo. Zmiana funkcji wymaga ponowienia reprodukcji i zależnej regresji, aktualnej instrukcji ręcznej wyłącznie w końcowej wiadomości czatu oraz oceny aktualności review/QA i domknięcia regresji w osobno zleconych etapach; wcześniejszy PASS pozostaje historyczną obserwacją swojej wersji. Nie oznaczaj go jako aktualnego bez podstawy.

Dla historycznego resume zachowaj artefakty i PASS, odtwórz powiązanie issue/branch/kontraktu i mapuj istniejące wyniki do obecnych obowiązków. Równoważny udokumentowany audyt może pokrywać raven-test bez fikcyjnego wywołania skilla lub pustego ponowienia. Nazwij faktyczne luki, nie dopisuj wstecz nieprzeprowadzonych etapów ani obowiązku auto QA manualnej pracy. Nie zmieniaj dawnego kontraktu tylko dla formatu nowego checkpointu.
