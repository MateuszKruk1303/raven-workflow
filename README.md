# Raven Workflow

[Greenfield](#greenfield) · [Brownfield](#brownfield) · [Cykl change](#cykl-change) · [Skróty auto](#skróty-auto)

`raven-workflow` to opcjonalny tutorial uruchamiany wyłącznie ręcznie. Pozostałe skille wywołuj bezpośrednio.

Diagramy czytaj od góry. `JEŚLI` oznacza krok warunkowy, `LUB` — wybór jednego skilla. Zaczęty task wznawiaj od zapisanego etapu.

## Greenfield

```text
raven-shape
Uzgodnij problem, odbiorców i zakres produktu
│  zapis: context/foundation/shape-notes.md
▼
raven-prd
Zapisz wymagania i kryteria odbioru
│  zapis: context/foundation/prd.md
▼
raven-architecture
Ustal decyzje przekrojowe i ograniczenia
│  zapis: context/foundation/architecture.md
▼
raven-init-stack
LUB raven-medusa-ecommerce-init
Uruchom wybrany szkielet, bazę i środowisko
│
▼
raven-agents-md LUB raven-md
Zapisz instrukcje pracy agentów w AGENTS.md
│
▼
raven-test-plan
Ustal ryzyka, warstwy testów i sposób weryfikacji
│  zapis: context/foundation/test-plan.md
▼
raven-github-setup
Przygotuj repo GH, tracking i politykę publikacji
│  Issues: taski i stan projektu
│  Project: opcjonalny widok
▼
raven-hooks
Skonfiguruj CI: lint, typy i właściwe testy
│
▼
raven-roadmap
Utwórz issues: wyniki, AC, zależności i kolejność
│  bez planowania implementacji całego backlogu
▼
WYBIERZ ISSUE
Przejdź do diagramu „Cykl change”
```

## Brownfield

```text
Odczytaj wskazany issue, repo, branch i checkpoint
│
├─ Task już rozpoczęty?
│  Wróć do brakującego etapu realizacji taska.
│  Nie powtarzaj przygotowania projektu.
│
▼
JEŚLI obszar kodu jest nieznany
raven-repo-map
Rozpoznaj moduły, zależności i istniejące testy
│
▼
JEŚLI warsztat ma braki — uzupełnij tylko brakujące
├─ raven-agents-md LUB raven-md
│  Instrukcje agentów w AGENTS.md
├─ raven-test-plan
│  Strategia testowania i ryzyka
├─ raven-github-setup
│  Repo GH, tracking issues i polityka publikacji
└─ raven-hooks
   CI dla istniejącego stacku
│
▼
JEŚLI wymagania lub rozwiązanie są niejasne
├─ raven-frame
│  Oddziel objaw, przyczynę i proponowane rozwiązanie
├─ raven-research
│  Zbierz dowody z kodu dla konkretnych pytań
├─ raven-domain-distillation
│  Wyjaśnij rozbieżności modelu domeny
└─ raven-architecture
   Ustal potrzebne decyzje przekrojowe
│  Dobierz potrzebne narzędzia, nie wszystkie.
▼
JEŚLI zlecono utworzenie lub zmianę kolejki
raven-roadmap
LUB raven-jira-roadmap — dla wymagań z Jira
Ustal taski GH, ich zakres, zależności i kolejność
│  Jira: źródło wymagań; GH: tracking wykonania
▼
WYBIERZ ISSUE
Przejdź do diagramu „Cykl change”
```

Dla znanego taska w przygotowanym repo przejdź bezpośrednio do skilla realizacji. Rozpoznanie będące częścią zleconego planowania odbywa się już po oznaczeniu issue jako In progress.

Dodatkowy mechanizm do zapamiętania w istniejącym tasku: `raven-issue-update <URL/numer issue lub change ID> — <wymaganie>`. Skill wplata go w zakres i AC wskazanego issue, zachowuje postęp i potwierdza zapis. Nie reorganizuje kolejki i nie rusza planu. Issue opisuje wymagania biznesowe; plan jest jednorazowym kontekstem roboczym agenta, nie trwałym kontraktem. Nowe wymaganie wystarczy przekazać w issue lub poleceniu dla `raven-auto-implement`, bez aktualizacji planu i ponownego review.

## Cykl change

`raven-auto-implement` można zlecić ze wskazanym planem lub samym poleceniem, bez review planu, fingerprintu, trackingu i checkpointów. Poniższy cykl pokazuje możliwe osobno zlecane prace; nie jest warunkiem wykonania auto-implement.

Jeden issue = jeden change. Plan i checkpoint są w `context/changes/<id>/plan.md`, instrukcja ręczna wyłącznie w końcowej wiadomości czatu. Nie zapisuj jej kopii w planie, issue, PR ani QA; nie twórz ani nie aktualizuj acceptance.md. Domyślnie pracuj na branchu w aktualnym checkout.

Przy nowym issue `raven-auto-plan` ustala task i pyta o nowy branch przed zapisaniem planu, chyba że zgoda już padła. Po zgodzie przełącza się na main (lub bazę projektu), aktualizuje ją przez `pull --ff-only` i tworzy branch change. Sprawdza aktualność bazy i chroni lokalne zmiany. Pozostawiony branch po merge nie wybiera kolejnego taska; wznowienie aktywnego change zachowuje jego branch. Szczegóły: [przygotowanie brancha](skills/raven-workflow/references/change-branch.md).

```text
raven-plan → raven-plan-review LUB raven-auto-plan
│  Najpierw issue In progress + wykonawca, potem plan.
│  Uwagi wracają do planisty; review wskazuje konkretny fingerprint.
│  Gotowy plan wskazuje auto-implement; wykonanie wymaga jego zlecenia.
▼
raven-auto-implement
│  Wskazany plan + aktualne polecenie → potrzebne zmiany
│  Poziom weryfikacji wg ryzyka: quick / standard / thorough
│  standard: działanie sprawdzone w uruchomionej aplikacji
│  thorough: baseline, testy obszaru, scenariusz błędu, 1 review
│  Wynik: co zmieniono/sprawdzono/ograniczenia + odbiór, tylko w czacie
▼
RĘCZNA WERYFIKACJA według końcowej wiadomości czatu
│  Problem: krok, Expected, Actual → raven-auto-implement <id>
│  Poprawka uwzględnia bieżące polecenie bez ponownego planowania.
▼
raven-implement-review <id> — osobno zlecone review wymagań/kodu/testów
▼
raven-test <id>
│  Audyt istniejącej ochrony i review/QA; tylko nazwane luki
│  Może zakończyć bez edycji testów, z konkretnym uzasadnieniem.
▼
raven-pr <id>
│  Jawne wywołanie = odbiór wskazanej jednoznacznej wersji + publikacja
│  Krótki preflight implementacji, domknięcia regresji i aktualności
│  Przy brakach: konkretna zgoda na publikację z jawnymi lukami
▼
ODRĘBNE ZLECENIE MERGE + aktualne dowody i wymagane CI
│  Odbiór z PR jest zachowany; functional delta wymaga ponownego odbioru.
▼
raven-merge → potwierdzony merge → issue Done
│  Gdy finalizacja issue zawiedzie, ponów tylko ten zapis.
▼
Następny issue; deploy pozostaje osobnym zleceniem.
```

Wcześniej autoryzowany draft może powstać w toku pracy, ale nie odbiera wyniku. Sam PASS, automatyczny draft, wywołanie test ani istnienie PR nie stanowią odbioru. Publikacja z jawnymi brakami nie omija bramek merge/CI.

## Skróty auto

`raven-auto-plan` łączy plan, niezależne review i poprawki; oddaje gotowy plan ze wskazaniem raven-auto-implement. `raven-auto-implement` samodzielnie wykonuje wskazany plan oraz aktualne polecenie, które może zmienić wymaganie bez ponownego planowania i review. Pracuje jeden bieżący agent. Przed zmianą wybiera poziom weryfikacji: `quick` (kompilacja i istniejące testy), `standard` (domyślny; dodatkowo działanie w uruchomionej aplikacji) lub `thorough` (sygnały ryzyka: pieniądze, checkout, auth, DB, kontrakt API, moduł współdzielony, usuwanie danych — baseline, testy obszaru, scenariusz błędu i jedno niezależne review). Zawsze podaje krótkie podsumowanie oraz instrukcję odbioru krok po kroku wyłącznie w końcowej wiadomości czatu. Niezwiązane zastane awarie zgłasza jako ograniczenie, bez naprawy. Inne skille, review, QA i publikacja pozostają osobnymi zleceniami.

Osobne manual-qa/auto-test/test-review wynikają ze zlecenia lub konkretnego ryzyka.

Przy feedbacku wznowienie zachowuje branch, kontrakt, dowody i liczniki problemów. Dwie nieskuteczne próby tego samego problemu zatrzymują zależną pętlę; nowy defekt ma własny licznik. Blokada pozostawia issue In progress z powodem. Testy i dokumentacja zmienione po odbiorze wymagają oceny wpływu, nie automatycznego unieważnienia wszystkich dowodów przez nowe SHA.

## Osobne zadanie testowe

Zwykły task tworzy potrzebne testy podczas `raven-auto-implement`. Poniższa ścieżka dotyczy osobno zleconych testów lub ochrony przed zmianą.

```text
Issue testowe → In progress + wykonawca
│
▼
raven-test
Dodaj testy, reprodukcję błędu lub ochronę refaktoru
│
▼
raven-test-review
Niezależnie oceń skuteczność ochrony
│  uwagi → raven-test → ponowne review
▼
raven-pr (odbiór wskazanej wersji) → CI + zgoda merge → raven-merge → issue Done

Skrót: raven-auto-test
Zawiera wykonanie, review i poprawki w zakresie.
```

---



<details>
<summary>Instalacja i utrzymanie</summary>

## Instalacja, doctor i rozwój

Repo jest źródłem dystrybucji. Python 3.10+ i środowisko lokalne:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python tools/raven.py doctor
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/raven.py sync --to "$HOME/.codex/skills"
# Po przejrzeniu pełnego diffu i w zakresie zgody na instalację:
.venv/bin/python tools/raven.py sync --to "$HOME/.codex/skills" --apply
.venv/bin/python tools/raven.py doctor --installed "$HOME/.codex/skills"
```

Sync obejmuje zarejestrowaną rodzinę Raven, nie inne skille. Tworzy backup dotkniętych katalogów, usuwa nieaktualne pliki tych skilli i wycofane raven-pilot-* / raven-seed / raven-implement. Nie zmienia globalnego AGENTS.md. Przejrzyj różnice i nie nadpisuj niezwiązanych lokalnych modyfikacji; sync nie jest automatycznym scaleniem. Symlinki i kolizje plik/katalog wymagają uporządkowania przed zapisem. Instalacja nie potwierdza odświeżenia katalogu aktywnego UI.

W globalnych instrukcjach wskaż: raven-workflow wywołuj wyłącznie ręcznie jako tutorial i pomoc. Pozostałe skille wywołuj bezpośrednio, bez obowiązkowego routera. Rozwijając skille, użyj raven-create-skill i dostępnego hostowi skill-creator; nie instaluj ani nie publikuj zmian bez objęcia tego zleceniem.

Doctor sprawdza frontmatter, nazwy, lokalne odsyłacze, katalog i [kontrakt](workflow-contract.json), a `--installed` również zgodność instalacji. `doctor --json` daje raport maszynowy. Kontrakt deklaruje zależności, nie wykonuje workflow: `initial_artifacts` to wymagane zewnętrzne dowody/decyzje, nie fikcyjne zgody. Standardowy PR następuje po raven-test; wczesny nieodebrany draft jest osobnym wyjątkiem i nie blokuje lokalnej implementacji. Etap `implement` należy do raven-auto-implement, a jego zasady (wejścia, poziomy weryfikacji, review tylko na `thorough`, finał w czacie) opisuje `auto_implementation`. Tracking, fingerprint/review i checkpointy nie są jego warunkami. Kontrakt nie przypina modeli agentów. Historyczne qa_required/tryb auto same nie przywracają QA; odrębne jawne zlecenie i rzeczywiste bramki projektu pozostają wiążące. Raven-test jest standardowym audytem/domknięciem regresji; dodatkowy auto-test/test-review/QA nie uruchamia się automatycznie. W standardowym workflow tracking issues jest wymagany, Project pozostaje widokiem; auto-implement nie wymaga trackingu.

Statyczny PASS nie dowodzi zachowania agenta ani prawdziwych uprawnień, CI i gotowości aplikacji. Zmiany instrukcji wymagają właściwych testów i niezależnych prób na rzeczywistych wejściach. Workflow [Raven integrity](.github/workflows/integrity.yml) uruchamia kontrole repo; sam YAML nie ustanawia required checks w GitHubie.

</details>

## Katalog wszystkich skilli — działanie i testy

**`raven-auto-implement` pisze i uruchamia testy razem z kodem.** `raven-plan` i `raven-test-plan` tylko je planują. `raven-implement-review` ocenia istniejącą implementację i testy; niezależne code review i szerokie QA zleca się osobno.

„Pisze testy” oznacza trwałe testy w repo. Sprawdzenie aplikacji w przeglądarce, analiza raportu lub odczyt CI to osobne czynności. Zakres nowych testów zależy od ryzyka zmiany i istniejącego pokrycia — nie każdy task wymaga każdej warstwy testów.

W kolumnie wyniku pliki przypisane do taska znajdują się domyślnie w `context/changes/<id>/`. Publikacja, merge i deploy pozostają w granicach zlecenia; samo review ani PASS nie zastępują decyzji użytkownika.

| Skill | Co wykonuje | Testy: pisanie i uruchamianie | Wynik i granica działania |
| --- | --- | --- | --- |
| [raven-agents-md](skills/raven-agents-md/SKILL.md) | Tworzy lub aktualizuje przewodnik dla agentów na podstawie struktury repo, komend, konfiguracji i historii. Zachowuje poprawne istniejące instrukcje. | Nie pisze testów aplikacji; dokumentuje wykryte komendy i zasady testowania. | `AGENTS.md` w repo lub wskazanym katalogu; nie inicjalizuje aplikacji. |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Prowadzi przez przekrojowe decyzje, porównuje opcje z PRD i istniejącym kodem, utrwala uzgodnienia. | Nie implementuje testów; uwzględnia wymagania jakościowe i testowalność. | `context/foundation/architecture.md`; nie implementuje wybranej architektury. |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Jeden bieżący agent wykonuje wskazany plan i aktualne polecenie, bez orkiestracji workflow. | **Tak: wykorzystuje i w razie luki dopisuje testy.** Poziom `quick` (typecheck + istniejące testy), `standard` (dodatkowo działanie w uruchomionej aplikacji) lub `thorough` (baseline, testy całego obszaru, scenariusz błędu, jedno niezależne review). | Zmiany i commity logicznych kroków (bez push/PR) oraz finał w czacie: poziom, co zmieniono, co zaobserwowano, ograniczenia i instrukcja odbioru. |
| [raven-auto-plan](skills/raven-auto-plan/SKILL.md) | Przygotowuje plan przez planistę, zleca niezależne review i poprawki w ograniczonej pętli. Podejmuje issue jako In progress. | Planuje testy i sprawdza kompletność weryfikacji; nie implementuje testów produktu. | `plan.md` i `plan-review.md`; kończy na gotowym planie i wskazaniu raven-auto-implement jako następnego kroku. |
| [raven-auto-test](skills/raven-auto-test/SKILL.md) | Koordynuje osobne zlecenie testów: autor testów → niezależny reviewer → poprawki i ponowne kontrole. | **Tak: pisze, uruchamia i niezależnie ocenia testy**, również ochronę przed refaktorem. Nie jest obowiązkowym etapem po implementacji. | Testy, dowody, checkpoint i ocena testów w repo; bez automatycznego merge/deploy. |
| [raven-browser](skills/raven-browser/SKILL.md) | Sprawdza działającą funkcję webową: formularze, nawigację, wynik akcji, wygląd i błędy. Domyślnie używa osobnej sesji Playwright CLI; osobiste Brave/MCP wymaga wyboru użytkownika. | Wykonuje scenariusze w przeglądarce, także tymczasowy kod Playwright do celowej weryfikacji i retestów; **nie zastępuje trwałych testów E2E** projektu. | Wynik scenariusza, screenshoty/logi i ograniczenia. Może służyć ponownej weryfikacji naprawionej regresji. |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Projektuje i zmienia skill Raven wraz z rzeczywistymi zależnościami, routingiem i dokumentacją; wymaga niezależnego review. | Waliduje skille, uruchamia doctor i odpowiednie testy repo; zmianę zachowania sprawdza przez izolowany forward-test. Nie testuje funkcji aplikacji przy okazji. | Pakiet instrukcji i potrzebnych helperów w repo skilli. Instalacja globalna oraz publikacja tylko w zakresie zlecenia. |
| [raven-domain-distillation](skills/raven-domain-distillation/SKILL.md) | Porównuje język dokumentów z modelem kodu przez niezależne analizy; wskazuje pojęcia, rozbieżności i niewiadome. | Nie pisze testów ani nie refaktoryzuje produktu; analizuje dostępne dowody. | `domain.md` i `glossary.md` w change lub foundation; dalsze zmiany wymagają planu. |
| [raven-frame](skills/raven-frame/SKILL.md) | Weryfikuje, czy opisany objaw, domniemana przyczyna i proponowane rozwiązanie rzeczywiście do siebie pasują. | Nie tworzy suite; zbiera dowody potrzebne do oceny hipotez. | `context/changes/<id>/frame.md`; nie zmienia kodu ani zatwierdzonych wymagań. |
| [raven-github-setup](skills/raven-github-setup/SKILL.md) | Przygotowuje lub uzupełnia repo/remote, tracking issues, etykiety statusu i politykę publikacji. Project pozostaje opcjonalny. | Nie pisze ani nie uruchamia testów aplikacji; weryfikuje konfigurację i wykonane zapisy GH. | Konfiguracja GitHub i `.raven/config.json`; samo przygotowanie nie daje zgody na push produktu lub merge. |
| [raven-hooks](skills/raven-hooks/SKILL.md) | Konfiguruje GitHub Actions dla istniejących komend lint, typecheck i właściwych testów. Sprawdza zgodność workflow ze stackiem. | Uruchamianie testów zapewnia CI; skill **nie służy do dopisywania testów zachowania produktu**. | Pliki workflow CI. Wymuszanie required checks wymaga osobnego zakresu; nie konfiguruje hooków sesji agenta. |
| [raven-implement-review](skills/raven-implement-review/SKILL.md) | Świeży reviewer porównuje implementację z wymaganiami i planem, ocenia kod, regresje oraz skuteczność testów. | Nie dopisuje ani nie poprawia ocenianych testów. Może uruchamiać kontrole potrzebne do weryfikacji dowodów. | `review.md` z zakresem, fingerprintem i konkretnymi uwagami; poprawki wracają do implementatora. Nie zastępuje odbioru człowieka. |
| [raven-init-stack](skills/raven-init-stack/SKILL.md) | Po uzgodnieniu wyborów generuje Better T Stack, instaluje zależności, przygotowuje lokalny PostgreSQL i konfigurację środowiska. | Sprawdza wygenerowany setup, typy i połączenie z bazą; **nie dodaje E2E** ani testów funkcji produktu. | Szkielet aplikacji, Compose/env i `context/foundation/tech-stack.md`; bez deploya i funkcji biznesowych. |
| [raven-issue-update](skills/raven-issue-update/SKILL.md) | Wplata dodatkowe wymaganie w zakres i AC jednego istniejącego issue; zachowuje treść, decyzje i postęp. | Nie pisze ani nie uruchamia testów produktu; weryfikuje zapis przez readback. | Zaktualizowany body issue lub no-op. Bez zmiany statusu/kolejki, planu, kodu i PRD; plan nie wymaga aktualizacji, bo wymaganie trafia do implementacji przez issue lub polecenie. |
| [raven-jira-roadmap](skills/raven-jira-roadmap/SKILL.md) | Czyta wskazane tickety/sprint/epikę Jira, ustala samodzielne wyniki i wiąże je z taskami wykonawczymi GH. | Nie pisze ani nie uruchamia testów; zachowuje kryteria i wymagane gwarancje przy podziale pracy. | Issues GH z linkami do wymagań Jira, zależnościami i kolejnością. Nie zapisuje do Jira ani nie kopiuje całych ticketów. |
| [raven-lesson](skills/raven-lesson/SKILL.md) | Utrwala uzgodnioną, powtarzalną regułę lub wzorzec wynikający z doświadczenia projektu. | Nie implementuje testów; opisuje regułę i dowody jej zastosowania. | `context/foundation/lessons.md`; nie przerabia produktu przy okazji. |
| [raven-manual-qa](skills/raven-manual-qa/SKILL.md) | Planuje i wykonuje dodatkowe eksploracyjne QA działającej funkcji, szuka defektów i dokumentuje reprodukcję. | **Sprawdza aplikację, ale nie generuje trwałej suite i nie naprawia produktu.** To osobne QA, nie obowiązkowy etap każdego taska. Auto-implement nie uruchamia osobnego QA automatycznie. | `qa-plan.md` i `qa-report.md` przy change; potwierdzone defekty i ograniczenia badania. |
| [raven-md](skills/raven-md/SKILL.md) | Tworzy lub celowo aktualizuje wskazany AGENTS.md na podstawie faktycznych plików, komend i konwencji; dopasowuje zakres do katalogu. | Nie pisze testów i nie uruchamia całej suite tylko dla dokumentacji; odróżnia znalezioną komendę od sprawdzonej. | Wskazany `AGENTS.md`; nie inicjalizuje stacku ani folderów kontekstu. |
| [raven-medusa-ecommerce-init](skills/raven-medusa-ecommerce-init/SKILL.md) | Uruchamia lub uzupełnia lokalny starter Medusa + Next.js: bazę, Redis, env, migracje, seed, admin i storefront. | Sprawdza start, bazę, właściwe build/typecheck i przepływ produkt → koszyk → checkout → zamówienie. Nie dodaje pełnego frameworka testów dla samego setupu. | Działające lokalne monorepo i instrukcja uruchomienia; bez rzeczywistych płatności, deploya i funkcji konkretnego sklepu. |
| [raven-merge](skills/raven-merge/SKILL.md) | Sprawdza odbiór, review, CI i aktualny SHA; wykonuje zlecony merge, potwierdza wynik i dopiero wtedy zamyka issue. | Nie pisze testów. Weryfikuje aktualne dowody i wymagane checki; FAIL/UNKNOWN nie stają się PASS. | Zmergowany PR i issue Done. Przy awarii zamknięcia issue wznawia samą finalizację, bez ponownego merge; bez deploya. |
| [raven-plan](skills/raven-plan/SKILL.md) | Podejmuje issue jako In progress, bada potrzebny kod i tworzy plan jednego rezultatu: zakres, decyzje, kroki, ryzyka i kryteria. | **Opisuje, jakie testy trzeba wykonać; nie implementuje testów ani produktu.** | `context/changes/<id>/plan.md` z kontraktem, planem testów i checkpointem. Review jest osobnym wywołaniem `raven-plan-review`. |
| [raven-plan-review](skills/raven-plan-review/SKILL.md) | Niezależnie ocenia wykonalność, zakres, decyzje techniczne i pokrycie wymagań w planie. Uwagi przekazuje autorowi do poprawy. | Sprawdza adekwatność zaplanowanych testów; nie implementuje ich ani produktu. | `plan-review.md` dla konkretnego fingerprintu; nie uruchamia implementacji. |
| [raven-pr](skills/raven-pr/SKILL.md) | Jawne wywołanie odbiera wskazaną jednoznaczną wersję i publikuje/aktualizuje PR; automatyczny lub nieodebrany draft nie odbiera wyniku. | Krótki preflight implementacji, raven-test/dowodów i aktualności. Konkretny brak wymaga zgody publikacji z luką, bez omijania merge/CI. | PR z linkiem do issue i wersji planu, zakresem i walidacją; nie zamyka issue, nie merguje i nie deployuje. |
| [raven-prd](skills/raven-prd/SKILL.md) | Przekształca shape-notes lub surowe ustalenia w PRD według schematu greenfield/brownfield, z wymaganiami i kryteriami odbioru. | Nie pisze testów; definiuje zachowania, które później trzeba zweryfikować. | `context/foundation/prd.md`; bez planowania implementacji wszystkich tasków i bez kodowania. |
| [raven-repo-map](skills/raven-repo-map/SKILL.md) | Mapuje istniejące repo: obszary produktu, zależności, historię zmian i miejsca ryzyka. Wskazuje, gdzie rozpocząć dalsze badanie. | Nie pisze testów; analizuje strukturę i istniejącą ochronę, bez refaktoryzacji. | `context/foundation/repo-map.md` z dowodami i ograniczeniami; nie uruchamia automatycznie kolejnego etapu. |
| [raven-research](skills/raven-research/SKILL.md) | Odpowiada na konkretne pytania o kod lub wykonalność, sprawdza źródła i zapisuje dowody oraz niewiadome. | Nie tworzy suite. Test/build uruchamia tylko wtedy, gdy wynik odpowiada na konkretne pytanie badawcze. | `context/changes/<id>/research.md`; bez przygotowania planu lub implementacji przy okazji. |
| [raven-roadmap](skills/raven-roadmap/SKILL.md) | Dzieli wymagania na samodzielnie dostarczalne taski, ustala AC, zależności i kolejność; zachowuje istniejące ID i decyzje. | Nie pisze testów; pilnuje, by podział zachował wymagane gwarancje i weryfikowalność wyników. | Roadmapa w GitHub Issues; nie tworzy lokalnego backlogu ani szczegółowych planów wszystkich tasków. |
| [raven-rule-review](skills/raven-rule-review/SKILL.md) | Ocenia AGENTS.md lub inny plik reguł w pięciu wymiarach, wskazuje konkretne problemy i priorytetowe poprawki. | Nie pisze testów produktu; sprawdza jakość i zgodność instrukcji ze źródłami. | `rule-review.md` przy change lub foundation; domyślnie nie przepisuje ocenianych zasad. |
| [raven-shape](skills/raven-shape/SKILL.md) | Prowadzi rozmowę o problemie, odbiorcach, MVP, regułach biznesowych, ograniczeniach i niewiadomych. Wznawia zapisane ustalenia. | Nie pisze ani nie uruchamia testów; zbiera scenariusze i oczekiwane zachowanie. | `context/foundation/shape-notes.md`; nie uruchamia automatycznie PRD, budowy ani publikacji. |
| [raven-test](skills/raven-test/SKILL.md) | Po ręcznej weryfikacji audytuje istniejącą ochronę i domyka tylko nazwane luki regresji; obsługuje też osobne zlecenia i before-change. | **Dodaje testy tylko dla nazwanych luk.** Wykorzystuje dobre istniejące testy i aktualne dowody; może zakończyć bez edycji z uzasadnieniem. | Pliki testów i dowody w `plan.md`; osobny `test-report.md` tylko gdy potrzebny. Checkpoint test_stage z oceną wystarczalności i jawnymi lukami; bez automatycznego dodatkowego review/QA. |
| [raven-test-plan](skills/raven-test-plan/SKILL.md) | Tworzy lub odświeża strategię testowania projektu: ryzyka, warstwy, cookbook i sposób wdrożenia ochrony. Tryb status tylko odczytuje stan. | **Nie pisze testów i nie wdraża CI.** Projektuje strategię; testy konkretnej zmiany powstają przy implementacji lub osobnym `raven-test`. | `context/foundation/test-plan.md`; taski wdrożenia ochrony i ich status pozostają w GH. |
| [raven-test-review](skills/raven-test-review/SKILL.md) | Świeży reviewer ocenia testy: źródło oczekiwań, asercje, wykrywanie regresji, mocki, izolację i cleanup. | Nie poprawia ani nie dopisuje ocenianych testów; weryfikuje dowody i potrzebne kontrole. Nie zastępuje autora testów. | `test-review.md` z oceną, lukami i finding IDs; poprawki wracają do autora. Zwykłe review change już obejmuje testy. |
| [raven-workflow](skills/raven-workflow/SKILL.md) | Wyłącznie ręcznie wywoływany tutorial, wprowadzenie i podpowiedzi: pomaga zrozumieć etapy i wybrać właściwy skill. | Nie pisze ani nie uruchamia testów w ramach tutorialu. | Objaśnienie w rozmowie; nie jest obowiązkowym krokiem ani automatycznym routerem przed innymi skillami. |
