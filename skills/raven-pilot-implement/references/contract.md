# Kontrakt Raven Pilot

## Cel i granice

Najkrótsza wiarygodna droga od wizji do pilota z rzeczywistymi użytkownikami i feedbackiem. Akceptuj świadome uproszczenia i ręczne operacje; nie dodawaj rozwiązań na skalę produkcji bez potrzeby. Poprawne uprawnienia i ochrona realnych danych są częścią działającego produktu. Workflow `raven-prod-*` jest osobnym przyszłym zakresem; nie twórz go i nie przełączaj na niego tylko dlatego, że pilot ma pierwszych użytkowników.

Użytkownik pracuje z AI przy wizji/przygotowaniu oraz ocenie działającego produktu. Decyzje architektoniczne uzgadnia z użytkownikiem podczas prepare. W środku agent samodzielnie planuje szczegóły wykonawcze w uzgodnionej architekturze, implementuje, weryfikuje i poprawia. Nie wprowadzaj bramek zatwierdzania planu zadania ani wyników review agenta.

## Ścieżki i zastany projekt

- Notatki: `context/pilot/shape-notes.md`; PRD: `context/pilot/prd.md`; roadmapa: `context/pilot/roadmap.md`.
- Konfiguracja opcjonalna: `context/pilot/workflow.md` (nadpisania modeli, budżetów, jawne granice). Brak pliku oznacza domyślne wartości z tego kontraktu; nie twórz go bez potrzeby.
- Setup: `context/pilot/setup.md`, tylko gdy wykonano init lub wykryto braki środowiska.
- Aktywne chunki: `context/pilot/chunks/C-01-slug/`.
- Zamknięte chunki: `archive/raven-pilot/C-01-slug/`, pod katalogiem projektu.
- Wcześniejsze dokumenty produktu spoza workflow Raven są źródłami do odczytu. Nie migruj ich ani nie zmieniaj automatycznie. Przy pierwszym użyciu Raven zapisz pochodzenie przejętych wymagań; przy późniejszych sprzecznościach nie udawaj, że obie wersje są aktualne — ujawnij konflikt.

Twórz tylko katalogi potrzebne do bieżącego etapu. Nie kasuj pracy użytkownika. Czytaj obowiązujące AGENTS.md i lokalne instrukcje; preferuj stack i package manager projektu. Nie wybieraj ponownie technologii. Nie uruchamiaj publikacji, płatnych usług ani kontaktowania użytkowników bez autoryzacji obejmującej konkretną operację. W pilocie migracje wymagane przez implementowany zakres wykonuj autonomicznie na ustalonej bazie dev, także zdalnej, bez osobnych zgód na migracje. Przed wykonaniem sprawdź cel połączenia, zakres SQL i rejestr zastosowanych migracji; stosuj brakujące migracje bez resetowania bazy ani kasowania niezwiązanych danych. Produkcja jest poza zakresem tego workflow. Nieznany lub sprzeczny cel połączenia wymaga wyjaśnienia środowiska, nie rutynowej zgody na migrację dev.

Przed zapisem/przeniesieniem rozwiąż ścieżki i symlinki; odrzuć ID zawierające separator ścieżki lub `..`. Każde archiwum jest niezmienne, także gdy użytkownik poda je jako wejście do prepare/review/test. Respektuj lokalne zakazy zapisu i wymagane komunikaty. Jeśli praca dotyczy archiwalnego chunka, skieruj do nowego chunka przez `$raven-pilot-prepare`. Domyślny nowy katalog archiwum nie upoważnia do omijania ogólnego repozytoryjnego zakazu archiwizacji.

## Obowiązkowa synchronizacja dokumentacji

Każdy skill przed wyborem pracy oraz przy zmianie stanu czyta i stosuje [synchronizację roadmapy i kolejkę](synchronization.md). Roadmapa musi odzwierciedlać aktualny stan pracy po każdym checkpointcie, także przy blokadzie lub przerwaniu; nie czekaj na osobne wywołanie roadmap. Zapis dokumentacji jest częścią wykonania zadania, a nie opcjonalnym podsumowaniem. Nie zgłaszaj zakończenia etapu, gdy aktualizacja dokumentacji się nie udała.

## Polityka pytań i autonomii

Pytaj, jeśli brak odpowiedzi może istotnie zmienić hipotezę, zakres, doświadczenie, regułę biznesową lub konsekwencje operacji i nie da się jej wiarygodnie wyprowadzić ze źródeł. Nie pytaj tylko dlatego, że można zaproponować kilka opcji. Użytkownik pełni rolę solutions architect: decyzje o usługach/dostawcach, przechowywaniu danych i plików, granicach usług, komunikacji, zadaniach w tle, hostingu i istotnych kompromisach operacyjnych wymagają uzgodnienia podczas prepare, także gdy są odwracalne. Korzystaj z wcześniejszych uzgodnień bez powtarzania pytań; sam kod ani rekomendacja agenta nie oznaczają akceptacji. Szczegóły wykonawcze i konwencje w uzgodnionej architekturze agent podejmuje sam. Plan zapisuje decyzje wraz ze źródłem akceptacji i granicami swobody implementatora; nierozstrzygnięty wybór architektoniczny pozostawia draft. Nowy wybór lub konieczność zmiany uzgodnionej architektury podczas implementacji wymaga checkpointu i konkretnego pytania do użytkownika, bez cichego zamiennika. Rekomendacja nie zastępuje brakującej intencji użytkownika. Nie pytaj o liczbę pytań, nie przeprowadzaj obowiązkowych rund, nie traktuj milczenia jako zgody.

Przy implementacji samodzielnie rozstrzygaj zwykłe decyzje techniczne i naprawialne błędy. Rzeczywisty blocker to brak niezbędnego dostępu, konfiguracji, uprawnienia lub decyzji użytkownika, którego agent nie może sam usunąć w autoryzowanym zakresie. Gdy go potwierdzisz, zatrzymaj realizację, zapisz bezpieczny checkpoint blocked z resume_status i zadaj użytkownikowi jedno konkretne pytanie lub wskaż wymagane działanie. Nie ukrywaj takiej blokady w follow-up do późniejszego review i nie zajmuj sesji pracą zastępczą. Nie ponawiaj bez końca operacji czekającej na ten sam dostęp. Wymagane zgody narzędzi uzyskuj przez ich mechanizm, bez obchodzenia zabezpieczeń. Po odpowiedzi lub zleceniu wznowienia kontynuuj w tej samej rozmowie od checkpointu; najpierw sprawdź usunięcie blokady, nie uruchamiaj całego procesu od nowa. Uwagi nieblokujące mogą pozostać w follow-up.

## Testy i dowody

`raven-pilot-implement` wykonuje tylko proste istniejące kontrole i jedno reprezentatywne sprawdzenie krytycznego przepływu przez niezależnego reviewera. Szczegółowe granice i warunek zakończenia określa [orkiestracja](orchestration.md). Nie wymaga dowodów dla wszystkich AC; pozostały odbiór należy do użytkownika. W implement nie twórz ani nie edytuj testów, fixtures i infrastruktury testowej. `raven-pilot-test` po akceptacji wykorzystuje istniejące scenariusze, także historyczne scenariusze z implementacji, i uzupełnia testy dobrane do ryzyk. Pozostałe etapy mogą uruchamiać adekwatne istniejące kontrole oraz bezpośrednio sprawdzać UI/API. Istniejącego testu nie zmieniaj, by ukryć regresję; wynik niezgodny z nowym wymaganiem jawnie odrocz do etapu testów, nie nazywaj go zaliczonym.

Każdy raport rozróżnia: sprawdzone, nieuruchomione, zablokowane i błędy zastane. Sukces wymaga wyników, nie deklaracji. Kompleksowy etap testów zaczyna się po akceptacji człowieka i wykorzystuje także historyczne testy Playwright powstałe podczas wcześniejszych implementacji. To oddzielne wywołanie lub wcześniej jawnie zlecony etap po akceptacji; wynik automatycznej weryfikacji nie zastępuje tej akceptacji.

## Artefakty chunka

- `plan.md`: kontrakt produktu, ID PRD, `spec_revision`, AC, zadania z zależnościami, runbook, ograniczenia, decyzje/założenia, potrzeby uprawnień i budżet.
- `state.json`: jedyne źródło stanu wykonania; roadmapa jest jego widokiem. Aktualizuj atomowo przez plik tymczasowy i rename. Jeden właściciel zapisu: koordynator podczas implementacji, prowadzący agent podczas innych etapów.
- `tasks/T-01/plan.md`: opcjonalny zwięzły plan wykonawczy implementatora; wykorzystuj istniejący plan chunka, jeśli wystarcza. `implementation.md`: wynik i kontrole; `review-01.md`, kolejne numery: niezmieniane wyniki niezależnego review. Powiązane zadania mogą wskazywać wspólny raport z wynikami według ID. Twórz tylko potrzebne artefakty w toku pracy.
- `tasks/T-01/verification.md`: opcjonalny istniejący indeks scenariuszy i dowodów. Implement nie musi go tworzyć ani rozszerzać; krótki wynik głównego przepływu w raporcie review wystarcza.
- `decisions.md`: istotne decyzje i zmiany po feedbacku. Krótkie decyzje można początkowo utrzymywać w plan.md; przenosząc je, zachowaj odnośnik.
- `handoff.md`: techniczne dowody całego flow i kontekst przekazania dla agentów. Instrukcję ludzkiego odbioru przekazuj wyłącznie w końcowej odpowiedzi w czacie, bez zapisywania jej jako artefaktu Markdown.
- `sessions/<session_id>/{notes.json,metrics.json,report.md}`: opcjonalna telemetria na żądanie, według [telemetrii](telemetry.md). Domyślna implementacja jej nie zbiera; wcześniejsze raporty pozostają bez zmian.
- `test-report.md`: dopiero w etapie testów, z pokryciem ryzyk i rzeczywistymi wynikami.

Minimalny kształt state.json (null oznacza brak danych, nigdy zgodę):

```json
{
  "schema_version": 1,
  "chunk_id": "C-01",
  "status": "draft",
  "spec_revision": 1,
  "state_revision": 1,
  "tasks": [],
  "blockers": [],
  "acceptance": null,
  "verification": null,
  "run": null,
  "updated_at": null
}
```

Każde zadanie: `id`, `depends_on`, `status` (pending/planning/implementing/reviewing/done/blocked), `attempts`, `artifacts`. `run` przechowuje ID sesji/agentów gdy dostępne, `session_started_at`, `session_elapsed_minutes`, `cumulative_elapsed_minutes`, liczniki prób i następny krok; numery agentów mogą być nieważne po restarcie, więc artefakty są podstawą wznowienia. Czas służy wyłącznie informacji; nie stosuj limitu czasu workflow. Historyczne session_limit_minutes usuń z aktywnego stanu przy aktualizacji, zachowując historię zakończonych sesji. `blockers` zawiera zakres, przyczynę, dowody i potrzebne działanie oraz `resume_status`, gdy całość zatrzymano.

`acceptance`: wypowiedź użytkownika/odniesienie do wiadomości, data, spec_revision i manifest zaakceptowanego kodu. Manifest obejmuje istotne pliki produktu/konfiguracji z SHA-256, także nowe pliki bez commita i usunięcia (oznaczone jako deleted); sam HEAD nie wystarczy. Przy wznowieniu obejrzyj też nowe istotne pliki, nie tylko wcześniej wpisane. `verification` zawiera końcowy manifest, wyniki/polecenia kontroli i datę; bez sekretów. Zmiana kontraktu unieważnia acceptance i verification. Zmiana kodu zgodna z zaakceptowanym zachowaniem wymaga aktualnej weryfikacji i zapisu różnicy, nie fikcyjnego nowego zatwierdzenia człowieka.

## Stany i bramki

`draft → ready → implementing → awaiting_review → accepted → testing → ready_to_archive → archived`

- ready: paczka kompletna do autonomicznej realizacji; wywołanie implement autoryzuje pracę w zakresie.
- awaiting_review: zakres chunka zaimplementowany i zintegrowany; reviewer sprawdził główny przepływ. Pozostałe AC i warianty mogą czekać na odbiór użytkownika, jawnie jako niesprawdzone.
- accepted: człowiek zaakceptował konkretny aktualny rezultat.
- ready_to_archive: zaakceptowane zachowanie zabezpieczone i wymagane kontrole zaliczone.
- blocked: rzeczywista przeszkoda wymagająca inputu/działania użytkownika albo wyczerpany limit nieudanych poprawek implementacji opisany w orkiestracji; zapisz powód, potrzebną decyzję i resume_status. Nie udawaj braku dostępu, gdy powodem jest limit poprawek.
- paused: prośba użytkownika lub przerwanie wykonania przez platformę; zapisz następny krok. Sam upływ czasu nie powoduje pauzy. To stan pliku workflow, nie automatyczna zmiana statusu narzędzia goal.

Review z poprawkami pozostawia awaiting_review do ponownej akceptacji; po zaakceptowaniu nowa zmiana zachowania wraca do awaiting_review. Niedokończone testy pozostają testing albo blocked. Resume odczytuje dowody i stan kodu, nie powtarza bezmyślnie wykonanych operacji. Nie uruchamiaj równocześnie dwóch koordynatorów tego samego chunka; sprawdź znane aktywne sesje. Brak pewności co do aktywnego zapisu jest blokadą współbieżności, nie zgodą na przejęcie.

## Modele i budżety

### Autorzy artefaktów produktowych

`raven-pilot-prd`, `raven-pilot-prepare` i `raven-pilot-roadmap` wymagają autora na `gpt-6-astra` z `reasoning_effort="high"`. To jawny wybór użytkownika dla jakości artefaktów; nie stosuj do tych ról fallbacku implementacyjnego na Sol. Zmiana wymaga późniejszego jawnego polecenia użytkownika, nie samej ogólnej konfiguracji modeli implementacyjnych w workflow.md.

Skill jest instrukcją, nie przełącznikiem modelu bieżącej rozmowy. Jeśli środowisko wiarygodnie potwierdza, że prowadzący agent działa na Astra high, wykonuje on ten etap bez dodatkowej delegacji. W przeciwnym razie skill wyraźnie zleca utworzenie osobnego autora przez narzędzie subagentów z `model="gpt-6-astra"`, `reasoning_effort="high"`, `fork_turns="none"` (lub odpowiednikami runtime). Nie zakładaj modelu na podstawie nazwy skilla ani samego żądania użytkownika.

Przekaż autorowi pełny opis celu, istotne wypowiedzi/ustalenia użytkownika, ścieżki źródeł, bieżący stan artefaktów, instrukcje repozytorium, ten kontrakt, reguły synchronizacji i treść odpowiedniego skilla. Oznacz go jako autora już uruchomionego na wymaganym modelu, aby nie delegował rekurencyjnie tej samej roli. Autor odpowiada za analizę, pytania wymagające decyzji i zapis artefaktów; główny agent przekazuje jego pytania użytkownikowi, a odpowiedzi wracają do tego samego autora przez followup/message. Nie odpowiadaj za użytkownika i nie przepisuj samodzielnie merytorycznej treści artefaktów słabszym modelem. Tylko autor zapisuje dokumenty i ich checkpointy w czasie tego etapu; główny agent nie zapisuje ich równolegle.

Po wznowieniu wykorzystaj istniejący wątek autora, jeśli dostępny; w innym razie uruchom nowego autora Astra high z aktualnymi artefaktami i dotychczasowymi decyzjami. Raportuj rzeczywisty użyty model/effort. Brak Astry high lub mechanizmu ustawienia modelu oznacza konkretną blokadę; nie zastępuj go po cichu innym modelem i nie deklaruj, że przełączono model rozmowy. Samo mechaniczne odświeżenie statusu roadmapy w implement/review/test/archive nie jest wywołaniem skilla roadmap i nie wymaga uruchamiania Astry. Zmiana wymagań i budowanie roadmapy w tych trzech skillach podlegają powyższej polityce.

### Role autonomicznej implementacji

Agent główny koordynuje; jeden implementator wykonuje chunk A–Z, a jeden niezależny reviewer sprawdza wymaganie na głównym przepływie. Reużywaj ich wątków do konkretnych poprawek. Nie uruchamiaj dodatkowego planisty, audytora ani automatycznej diagnozy. Modele można nadpisać poleceniem użytkownika lub workflow.md:

| Rola | Model | Effort |
|---|---|---|
| Implementator | gpt-6.1-sol | low |
| Reviewer | gpt-6.1-sol | high |

To konfiguracja startowa, nie obietnica najlepszego kosztu. Sprawdź modele/effort w dostępnych narzędziach. Ustawiaj jawnie przy spawn; w tym środowisku zmiana modelu wymaga `fork_turns="none"` lub ograniczonej liczby tur, a nie pełnego forka. Preferuj none z krótkim pakietem zadania i ścieżkami do potrzebnych źródeł. Powiązane zadania i poprawki kontynuuj w istniejących wątkach, zachowując niezależność review; nie mnoż kontekstów dla samej zmiany etapu. Gdy model jest niedostępny, użyj dostępnego Sol dla danej roli i odnotuj zmianę; bez Sol i bez uzgodnionego zastępstwa oznacz blokadę, nie przechodź po cichu na Astrę dla wszystkich.

Implementacja kończy się po wykonaniu wymagania i PASS krytycznego przepływu, bez dalszego poszukiwania ulepszeń i pokrywania wszystkich wariantów. Nie ustalaj arbitralnego limitu całej pracy ani fikcyjnego budżetu tokenów; oszczędność wynika z małego zakresu kontroli i ograniczonej pętli. Maksymalnie dwie rundy poprawek po pierwszym review całego chunka, bez automatycznej eskalacji. Dalszy tryb i zapis blocked przy nadal niedziałającym wymaganiu określa orkiestracja. Przy wznowieniu zachowaj wyniki i liczniki; nie resetuj limitu bez jawnego zlecenia użytkownika.

## Kolejność wywołań

`shape → prd → roadmap → prepare C-01 → implement C-01 → review C-01 → test C-01 → archive C-01`

`init` przygotowuje stack przed pierwszą implementacją, gdy jest potrzebny. Kolejne chunki zaczynają się od prepare. Nie wymagaj poprzednich skilli, jeśli potrzebne artefakty już istnieją. PRD i roadmapa mogą ewoluować na podstawie feedbacku; szczegółowo przygotowuj najbliższą paczkę. Nie wdrażaj po cichu produkcyjnego procesu ticketów i ciężkich bramek.
