# Wspólny kontrakt GitHub dla workflow Raven

Czytaj przy wejściu do raven-auto-plan, raven-auto-implement, raven-plan, raven-plan-review, raven-implement, raven-implement-review, raven-research, raven-pr i raven-merge. Ten kontrakt zmienia transport i orkiestrację skilli źródłowych, nie ich merytoryczne kryteria. GitHub jest jedynym trwałym źródłem kontekstu change. Dokumentacja produktu, AGENTS.md i lessons pozostają wersjonowane w repo.

## Tożsamość i zakres uprawnień

Odczytaj instrukcje projektu, `context/foundation/github.json`, rzeczywiste repo i prywatny Project. Zweryfikuj konto, dostęp, pola i ich opcje; manifest nie zastępuje odczytu. Nie zmieniaj widoczności ani nie wybieraj innego repo przy błędzie. Numer issue, node ID, Raven ID i Project item ID to różne identyfikatory. Change ma etykietę `raven:change`, task ma `raven:task` i natywną relację sub-issue z change. Wykorzystaj istniejące ID, etykiety i kontrakt raven-roadmap, nie twórz drugiego systemu numeracji. Nowy task używa kolejnego nieużytego ID rodzica, np. `C-03/T-02`.

Przyjmuj URL issue, numer z jednoznacznym repo lub Raven ID. Pobierz pełny opis, sub-issues, relacje i stan Project. Przy pierwszym odczycie pobierz komentarze z pełną paginacją. Przy wznowieniu można użyć lokalnego cache pełnych źródeł tylko po sprawdzeniu kompletnej listy ID/updatedAt i pobraniu nowych/edytowanych treści oraz usunięciu skasowanych wpisów. Sam indeks lub ostatni komentarz nie wystarcza; przy braku weryfikowalnego cache odczytaj pełną historię. Do kontekstu roli wczytaj aktualne kontrakty oraz wszystkie istotne raporty i decyzje; starsze źródła zachowaj dostępne do weryfikacji. Sam tytuł nie identyfikuje pracy. Jeśli użytkownik prosi o następny change, odczytaj kolejkę, zależności i Raven Order; uzasadnij wybór. Przy rzeczywistej niejednoznaczności pytaj. Zamknięta/ukończona zmiana pozostaje historyczna; nie otwieraj jej ponownie bez zlecenia.

Wywołania skilli upoważniają do następujących zapisów w wybranej zmianie:
- auto-plan: kontekst issue, plan, potrzebne sub-issues/relacje, wersje, review i decyzje;
- manual plan: kontekst issue, plan, taski/relacje i snapshoty; manual plan-review: raport, decyzje i wyraźnie zlecone poprawki planu;
- research: zapewnienie tożsamości jawnie zleconej nowej zmiany (albo użycie istniejącej), membership/pola i Backlog → Preparing, wersjonowany raport badawczy w komentarzu i odsyłacz do niego; bez planu i tasków implementacyjnych;
- auto-implement: postęp, dowody, review kodu i raport niezależnego testera przeglądarkowego, decyzje i statusy wykonania;
- manual implement: postęp, dowody, checkpointy i statusy wykonania; manual implement-review: raport, decyzje, wyraźnie zlecone poprawki oraz ich dowody;
- pr: podział istniejących niezacommitowanych zmian ticketa na logiczne commity, commit, zwykły push gałęzi zmiany oraz utworzenie/aktualizacja PR z aktualnym opisem, historią poprawek i powiązaniami; wywołanie jest decyzją publikacji. Bez osobnego uruchamiania kontroli, audytu gotowości, zmian statusów Project i bezpośredniego zamykania issues; hooki commit/push pozostają aktywne.
- merge: merge jednoznacznego PR obejmującego wskazany change, następnie jawne ustawienie i odczyt Done w kanonicznym polu wskazanym przez `fields.status.id` dla jego itemu na powiązanym Project; wywołanie upoważnia do obu zapisów bez ponownej zgody, także do samej finalizacji już zmergowanego PR. Bez zbiorczego zamykania tasków, zapisów do Jira, usuwania gałęzi i deploya.
Nie wysyłaj innych komentarzy, wiadomości, powiadomień ani zmian poza zakresem. Prośba o status/dyskusję pozostaje tylko do odczytu. Skille nie uruchamiają automatycznie researchu, lesson, następnego etapu, merge ani deploya.

## Bieżące treści

Zachowaj ludzkie opisy, istniejące kryteria i sekcje roadmapy. Dodawaj lub edytuj własne oznaczone bloki, nie zastępuj całego issue szablonem.

W change issue:
- istniejący Rezultat, Zakres, Poza zakresem, Kryteria odbioru, Źródła i decyzje produktowe;
- blok `<!-- raven:plan:start -->` … `<!-- raven:plan:end -->`: skrót (rola plan-brief), stan końcowy, podejście, kontrakty przekrojowe, ryzyka, wyłączenia techniczne, referencje i wymagane testy/checki przed merge;
- blok `<!-- raven:tasks:start -->` … `<!-- raven:tasks:end -->`: uporządkowane linki do faz/sub-issues, Raven ID i zależności;
- blok `<!-- raven:context:start -->` … `<!-- raven:context:end -->`: linki do researchu, bieżącej opublikowanej wersji/snapshotu, review i decyzji. To indeks, nie druga kopia treści ani postępu.

W sub-issue fazy:
- marker `<!-- raven:task id=C-03/T-02 -->` z prawdziwym ID;
- blok `<!-- raven:phase:start -->` … `<!-- raven:phase:end -->`: numer i nazwa fazy, Overview, Changes Required, Intent + Contract per file, Automated Verification, Manual Verification i zależności. Zachowaj merytoryczną zawartość fazy Raven; nie zamieniaj planu w listę ogólnych tytułów;
- blok `<!-- raven:progress:start -->` … `<!-- raven:progress:end -->`: sekcje Automated/Manual, trwałe identyfikatory `N.M`, checkboxy zgodne z kontraktem Progress Raven, SHA oraz linki do dowodów. Brak dowodu nie oznacza PASS. Nie odhaczaj sprawdzenia ręcznego zamiast użytkownika.

Jedna faza wykonania = jeden task, nie jeden task na plik. Przy aktualizacji zachowaj ID tasków i punktów Progress. Nie kasuj/nie zamykaj taska z rozpoczętą pracą tylko dlatego, że nowy plan go nie zawiera; uzgodnij zmianę zakresu. Dla nowych pustych tasków stan początkowy to Backlog. Zależności wykonania są natywne, relacja rodzic–dziecko ich nie zastępuje. Wewnątrz jednego change kolejną fazę odblokowują zweryfikowany Progress i kontrakt wyniku poprzedniej fazy, nie zamknięcie jej issue ani status Done. Zależności między changes wymagają dostarczonej/zmergowanej pracy zgodnie z ich kontraktem. Nie twórz deadlocku wymagającego merge taska przed implementacją następnej fazy tego samego PR.

## Wersje, raporty i decyzje

Bieżące opisy są edytowalne. Przed review publikuj niezmienny snapshot planu: wersja `vN`, wymagania rodzica, pełna część techniczna/brief, uporządkowane pełne kontrakty faz, kryteria weryfikacji, ID/URL tasków i zależności. Nie zapisuj samej listy linków do edytowalnych opisów.

Dla kontroli wersji zbuduj obiekt JSON `requirements`, `plan`, `phases` (uporządkowana tablica z ID, URL, kontraktem i zależnościami). Przechowuj dokładne teksty, koduj jako UTF-8 z sortowaniem kluczy, bez zbędnych odstępów, i policz SHA-256. Nie włączaj do fingerprintu pól postępu, statusu Project, indeksu komentarzy ani samych dowodów wykonania. Zmiana wymagań, kontraktów lub kryteriów zmienia wersję. Sam postęp jej nie zmienia.

Do obliczenia i porównania użyj [snapshot_fingerprint.py](../scripts/snapshot_fingerprint.py): `python3 <skill-dir>/scripts/snapshot_fingerprint.py <contract.json> [--expect <sha256>]`. Helper wymaga dokładnych tekstów requirements/plan i uporządkowanej tablicy obiektów phases; sortuje klucze, zachowuje Unicode bez ASCII escaping i koduje UTF-8. Weryfikuje strukturę zewnętrzną, duplikaty kluczy i hash, lecz nie zastępuje kontroli kompletności wymagań, ID/URL/zależności ani odczytu GH po zapisie. Przed wywołaniem oddziel Progress i inne zmienne pola od tekstów kontraktu; helper nie usuwa sekcji heurystycznie. Nie drukuje treści wymagań ani nie zapisuje do GH. Dla historycznego snapshotu o innym sposobie kodowania zachowaj jego oryginalny payload i fingerprint; nie przeliczaj po cichu zaakceptowanej wersji ani nie przenoś zgody po rozbieżności.

Snapshot jest komentarzem z markerem `<!-- raven:plan-snapshot change=C-03 version=1 -->`, fingerprintem i kompletnym obiektem w bloku JSON. To historyczny zapis ocenianej wersji; bieżący plan nadal pochodzi z opisów. Przy limicie długości podziel payload na ponumerowane części z jednoznacznymi markerami; opublikuj manifest z linkami, kolejnością i hashem dopiero po potwierdzeniu wszystkich części. Nie ucinaj treści ani nie przenoś kanonicznego planu do lokalnego pliku. Niepełny snapshot nie jest gotowy do review.

Raporty mają własne komentarze i stabilne markery:
- `raven:research change=C-03 research=1`;
- `raven:plan-review change=C-03 version=1 round=1`;
- `raven:impl-review change=C-03 round=1` wraz z base/head SHA i wersją planu;
- `raven:browser-review change=C-03 round=1` z SHA aplikacji, środowiskiem, pełną macierzą kryteriów ticketa, dowodami i uwagami B1/B2;
- `raven:decision change=C-03 stage=plan|implementation round=1` z referencją raportu/wersji/SHA, treścią decyzji użytkownika, wybranymi ID oraz rozstrzygnięciami;
- `raven:execution change=C-03 run=1` dla checkpointu (branch, base/head SHA, wersja planu, mapowanie faz/tasków, komendy i wyniki weryfikacji, blokady, następny krok).

Wszystkie markery umieszczaj w komentarzach HTML; wartości przykładowe zastąp rzeczywistymi. Kolejne rundy nie nadpisują raportów wcześniejszych rund. Uwagi mają stabilne ID w ramach etapu; przy odwołaniu zawsze podaj etap/raport, żeby plan F1 nie pomylił się z implementacją F1. Akceptacja użytkownika nie zmienia werdyktu technicznego. ACCEPTED/DISMISSED/SKIPPED nie oznacza FIXED. Nie wymyślaj uzasadnień użytkownika. Nowa wersja kontraktu wymaga nowego review i akceptacji; nie przenoś zgody automatycznie.

## Adapter do skilli źródłowych Raven

Skille Raven korzystają z własnych procedur, szablonów i helperów w katalogach references/procedures, wskazanych bezpośrednio w ich SKILL.md. Podagentom przekaż absolutne ścieżki tych lokalnych plików. Nie wymagają żadnej innej rodziny skilli ani instalacji pakietu workflow.

Dla konkretnego przebiegu utwórz poza śledzonym drzewem repo katalog roboczy hosta. Odtwórz z GH `change.md`, pełny `plan.md`, `plan-brief.md`, opcjonalny `research.md` i raporty. Podaj `artifact_dir` oraz osobno `repo_root`/worktree. Wszystkie ścieżki kodu rozwiązuje się względem repo_root. Nazwy źródłowe `context/changes/<id>/...` oznaczają w tym adapterze pliki wewnątrz artifact_dir. Nie twórz symlinków, nie podmieniaj istniejących plików context i nie commituj kopii roboczych.

Pełny plan renderuj z wymagań i części przekrojowej rodzica oraz faz w kolejności tasków. Zachowaj strukturę `raven-plan/references/procedures/plan/references/plan-templates.md`; jedną sekcję `## Progress` buduj z bloków progress sub-issues zgodnie z `progress-format.md`. Brief pochodzi ze skrótu rodzica, a change.md z jego tożsamości i decyzji. Historyczne snapshoty służą review; implementacja wymaga zgodności bieżącego fingerprintu z zatwierdzonym snapshotem. Referencje do wcześniejszych changes/archive rozwiązuj do GH, nie do nieistniejących lokalnych folderów.

Nadpisania transportu są jawne: helpery metadanych i lokalny Progress operują wyłącznie na kopiach roboczych; zapisy planu/briefu/researchu/raportu są propozycją do publikacji w GH. Nie stosuj lokalnej synchronizacji roadmapy, bootstrap stagingu plików kontekstu ani commitu epilogu dokumentacji z Raven. Commity kodu, bramki i dyscyplina wcześniejszych etapów pozostają. raven-pr zachowuje istniejące commity i może commitować pozostałe zmiany ticketa według własnej procedury publikacji, bez ponownego uruchamiania bramek implementacji ani omijania hooków Git. Po fazie publikuj Progress/dowody do odpowiednich tasków i checkpoint wykonania do rodzica. Po planowaniu publikuj kontrakty i snapshot. Po review publikuj raport. Odczytaj wynik; dopiero wtedy zgłoś zakończenie etapu.

Tylko koordynator zapisuje GH. Podagenci zwracają artefakty/proponowane zmiany i nie wykonują mutacji zdalnych. Po błędzie publikacji zachowaj lokalny payload jako niezapisany wynik, zgłoś częściowy stan i wznów synchronizację po odczycie GH. Nie implementuj kolejnej zależnej fazy na podstawie nieopublikowanego checkpointu. Kopia lokalna nie staje się źródłem prawdy i nie wolno jej nadpisać regeneracją przed odzyskaniem niezapisanego wyniku.

Przy wznowieniu najpierw czytaj GH, aktualny Git i nowe decyzje użytkownika. Nie restartuj badań ani implementacji, które mają dowody zakończenia. Po zmianie lub utracie kopii roboczej można ją odtworzyć z GH. Nie ma lokalnej roadmapy ani kanonicznego plan.md dla tej zmiany.

## Zapis odporny na powtórzenia

Używaj connectora lub `gh`. Przed pierwszą mutacją poznaj aktualny schemat narzędzia/`--help` lub dokumentację API. Przed zapisem ponownie odczytaj body i updatedAt; porównaj wersję z pobraną. Przy edycji równoległej zachowaj cudze fragmenty, uzgodnij kolizję kontraktu. GitHub nie zapewnia transakcji całego workflow — nie obiecuj atomowości.

Przed tworzeniem obiektu/komentarza wyszukaj marker również po timeout. Ponowienie uzupełnia brakujący krok zamiast dublować task lub raport. Po zapisie odczytaj treść, relacje, pola i hash. Zestaw mutacji wieloobiektowych jest ukończony dopiero po spójnym odczycie wszystkich części; nie publikuj akceptacji dla częściowego planu. Przy trwałym błędzie dostępu zakończ zależne zapisy i zgłoś co się udało.

Treści wielowierszowe przekazuj strukturalnie lub przez `--body-file`, bez interpolacji tekstu użytkownika do shella. Nie publikuj sekretów, absolutnych ścieżek komputera ani nieweryfikowalnych linków. Permalinki do kodu tylko dla bajtów obecnych na wskazanym zdalnym commicie; inne dowody oznacz jako lokalne `path:line` z HEAD i opisem dirty state.

## Tryby manualny i automatyczny

Tryb wybiera jawnie wywołany skill; zapisuj go w checkpointcie jako workflow_mode: manual lub auto. Starsze checkpointy bez pola interpretuj według raportów i bieżącego zlecenia, nie według samej dawnej nazwy skilla. Oba tryby dzielą ten sam change i formaty. Wywołanie manualnego skilla po etapie auto nie wznawia samo automatycznej pętli; jawne wywołanie auto może wykorzystać aktualne dowody manualne, ale nadal musi spełnić własne bramki. Przed zapisem upewnij się, że poprzedni wykonawca nie modyfikuje równolegle tej samej zmiany.

Dla manualnych skilli stosuj [manualny adapter](../../raven-plan/references/manual-github.md). Ich oddzielne wywołania nie dziedziczą orkiestracji auto. Wspólne zasady publikacji, wersji i Done pozostają identyczne.

## Statusy i merge

W raven-auto-implement potwierdzone przez niezależnego testera niespełnienie uzgodnionego kryterium przeglądarkowego uruchamia automatyczne poprawki i retesty w granicach browser-review. Checkpoint zapisuje uwagi B, przypisane kryteria, SHA, próby i wynik, bez fikcyjnej decyzji użytkownika. Technicznego reviewera wolno uruchomić dopiero po zapisanym PASS wszystkich kryteriów funkcjonalnych ticketa na finalnym SHA; brak dowodów, FAIL lub BLOCKED zatrzymuje ten etap. Reviewer publikuje raport F i instrukcję manualnych checków użytkownika. Techniczne uwagi F nadal podlegają ręcznemu triage. Dopiero powodzenie pętli i raport techniczny oznaczają gotowość do osobistego odbioru, nigdy Done.

Cykl nie jest bezpośrednim przejściem implement → PR. Po implementacji i technicznym review następuje osobny etap prowadzony przez użytkownika: własne sprawdzenie aplikacji, raportowanie problemów, zlecanie poprawek oraz dodatkowe testy/checki. Może obejmować wiele rozmów i osobno wywołanych skilli. Akceptacja raportu reviewera nie oznacza zakończenia tego etapu. Nie narzucaj dla niego nowej komendy ani nie sugeruj PR jako domyślnego następnego kroku po implementacji. Użytkownik decyduje, kiedy wywołać raven-pr. Wywołanie jest ostateczną decyzją publikacji: skill przygotowuje logiczne commity pozostałych zmian, wykonuje zwykły push i tworzy/aktualizuje PR z bieżącym opisem oraz historią poprawek, bez ponownego audytu ukończenia tych etapów.

Project jest kanonicznym statusem kolejki. Backlog → Preparing podczas rozpoczęcia zleconego researchu lub planowania. Zakończony research pozostaje Preparing do późniejszego planowania; nie tworzy Ready. Ready dopiero po review, jawnej akceptacji konkretnej wersji i spełnieniu zależności; w przeciwnym razie zapisz akceptację oddzielnie i nazwij przeszkodę. In progress podczas realizacji/poprawek, Review podczas oczekiwania na decyzję, testy/checki lub merge. Blocked tylko dla konkretnej blokady. Nie resetuj późniejszych stanów przy ponownym wywołaniu.

Ani ukończenie fazy, zielone review, akceptacja w czacie, wykonanie testów, ani utworzenie PR nie ustawiają Done i nie zamykają issue/tasków. Progress może wykazać wykonaną fazę, podczas gdy status taska pozostaje Review. Done tylko po potwierdzonym merge pełnego zakresu change do docelowej gałęzi finalizacji (domyślnie default branch), po wymaganych testach i checkach. Nie ustawiaj Done jako skrótu przed merge; closed bez merge, auto-merge i kolejka nie są sukcesem. Osobno zlecony [raven-merge](../../raven-merge/SKILL.md) odpowiada za dwa uporządkowane wyniki: `merged_pr` → `board_done`. Przed merge potwierdza PR/zakres i rzeczywisty item change, kanoniczne pole `fields.status.id` (np. Status lub Raven Status) typu single-select z opcją Done oraz dostęp do właściwego Project z github.json. Po merge jawnie zapisuje Done i wykonuje readback; nie polega na automatyzacji. Błąd boarda to częściowy sukces: wznowienie odzyskuje dowód merge i dokańcza sam status bez powtórnego merge. Nie tworzy brakującej konfiguracji i nie zamyka zbiorczo tasków. raven-pr pozostaje publikacją, bez sprawdzania i konfigurowania finalizacji.

## Testy po implementacji i checki po PR

raven-test-plan przechowuje globalną strategię, ryzyka, cookbook i rollout w issue strategii. raven-test implementuje trwałe testy w repo i publikuje raporty raven:test-report oraz Progress w change. raven-hooks zapisuje konfigurację GitHub Actions i raport raven:ci-setup. Wywołania upoważniają do tych zapisów w ramach wskazanego projektu/change; reguły idempotencji i odczytu zwrotnego obowiązują również tutaj.

Obowiązkowa kolejność: oddanie implementacji → sprawdzenie/feedback użytkownika → raven-test + raven-test-review albo raven-auto-test → osobno zlecony raven-pr → checki GitHub Actions → osobno zlecony raven-merge (merge → Done na boardzie). raven-test jest etapem obowiązkowym, z zakresem adekwatnym do ryzyka; nie wymusza nowych testów każdej warstwy dla każdego change. Implementacyjne bramki pozostają, ale nie zastępują tego etapu. raven-auto-implement nie generuje trwałych E2E; jego tester wykonuje bieżące sprawdzenie przepływu.

Planowanie wydziela fazy trwałych testów wykonywane przez raven-test po oddaniu implementacji, z kryteriami i powiązaniem do ryzyk. Zlecenie implementacji nie uruchamia automatycznie raven-test ani PR. Handoff wskazuje pozostały obowiązkowy etap. raven-pr pozostaje publikacją, bez audytu testów, odpytania CI czy blokowania publikacji na podstawie raportów; nie traktuj go jako technicznego egzekutora tej kolejności. CI wykonuje skonfigurowane kontrole po PR, a jego egzekwowanie przy merge zależy od ustawień repo.

Review testów: manualny raven-test-review oraz automatyczny raven-auto-test stosują wspólny kontrakt raven-test/references/test-review.md. Autor utrwala test_sources w checkpointcie, reviewer otrzymuje te same wersje surowych źródeł bez transkryptu autora. Raporty raven:test-report i raven:test-review są wspólne dla obu trybów. W manualu użytkownik zleca poprawki; w auto potwierdzone wady testów w zakresie uruchamiają ograniczoną pętlę napraw. Oba wywołania review upoważniają koordynatora do publikacji raportu i rzeczywistych decyzji w wybranym change.

## Rozszerzenia brownfield i Jira

Skille raven-repo-map, raven-frame, raven-domain-distillation i raven-rule-review publikują swoje raporty oraz indeksy zgodnie z [kontraktem brownfield](../../raven-repo-map/references/github-brownfield.md). raven-jira-roadmap publikuje wskazaną roadmapę i snapshoty Jira w GH, bez zapisów do Jira. Jira pozostaje źródłem wymagań biznesowych; GH źródłem artefaktów wykonania. Przy zmianie źródła wymagania zatwierdzonego planu wymagają jawnego rozstrzygnięcia i nowej wersji przed dalszą implementacją.

Opcjonalne code_repository w github.json rozdziela repo kodu od istniejącego repo artefaktów. Checkout, testy, remote, branch i PR odnoszą się do repo kodu; issues, snapshoty i Project do repo artefaktów. Bez tego pola zachowaj dotychczasowe jedno repo. Wszędzie używaj pełnych URL/kwalifikowanych identyfikatorów. Nie wysyłaj raportów do repo kodu przez przypadek.

Planowanie może wydzielić fazę before-change przed refaktorem/bugfixem zgodnie z [kontraktem testów przed zmianą](../../raven-test/references/before-change.md). Jest to wyjątek od zasady wykonywania wszystkich trwałych testów dopiero po implementacji. Wykonuje ją jawnie zlecony raven-test/auto-test; zależna faza implementacji czeka na wymagane zabezpieczenie. Etap końcowych testów i review pozostaje obowiązujący, wykorzystując już napisane testy.

## Research jako wejście do change i źródło planu

Research oraz planowanie mogą rozpocząć przygotowanie tej samej zmiany. Istniejące issue z roadmapy lub researchu realizuje etap tożsamości (new); kolejne wywołanie nie tworzy nowego change ani nie resetuje postępu. Research jest opcjonalny i osobno zlecany. Nie wymaga wcześniejszego planu.

Raporty researchu są niezmiennymi rundami `raven:research change=ID research=N`. Indeks kontekstu wskazuje aktualne raporty dla odpowiednich pytań, nie tylko ostatni komentarz całego issue. Nowa runda jawnie wskazuje zastąpione ustalenia. Odczytaj wszystkie istotne raporty i decyzje, porównaj wymagania i badany kod z bieżącym stanem. Sama zmiana HEAD nie unieważnia całego researchu; sprawdź wpływ zmian na jego dowody.

Plan i auto-plan muszą wskazać wykorzystane research ID/URL oraz co przejęły, co wymagało ponownej weryfikacji i które rekomendacje użytkownik zaakceptował. Nie powtarzaj aktualnych badań ani wywiadu o rozstrzygniętych decyzjach. Research jest dowodem dla planu, nie planem, zatwierdzeniem architektury ani zgodą na implementację. Przy sprzeczności nazwij źródła i rozstrzygnij ją przed zależnym planowaniem.

`context/foundation/architecture.md`, jeśli istnieje, jest wersjonowaną dokumentacją produktu. Uwzględniaj statusy decyzji i rozróżnienie istniejące/docelowe. Research może wykazać rozbieżność, ale sam nie nadpisuje ustalonych zasad. Planista dostaje architekturę i źródłowe raporty; nie tylko streszczenie koordynatora.
