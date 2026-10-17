# Raven Workflow

[Greenfield](#greenfield) · [Brownfield](#brownfield) · [Realizacja taska — manual](#realizacja-taska--manual) · [Skróty auto](#skróty-auto)

Diagramy czytaj od góry. `JEŚLI` oznacza krok warunkowy, `LUB` — wybór jednego skilla. Zaczęty task wznawiaj od zapisanego etapu.

## Greenfield

```text
raven-workflow
Ustal punkt startowy i brakujące przygotowanie
│
▼
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
Przejdź do diagramu „Realizacja taska — manual”
```

## Brownfield

```text
raven-workflow
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
Przejdź do diagramu „Realizacja taska — manual”
```

Dla znanego taska w przygotowanym repo przejdź bezpośrednio od `raven-workflow` do realizacji. Rozpoznanie będące częścią zleconego planowania odbywa się już po oznaczeniu issue jako In progress.

## Realizacja taska — manual

Wspólna ścieżka dla greenfield i brownfield. Jeden issue = jeden change. Plan, plan testów i checkpoint są w `context/changes/<id>/plan.md` na branchu; domyślnie bez dodatkowego worktree.

```text
raven-plan
Najpierw: issue → In progress + wykonawca
Potem: wymagania, plan implementacji i plan testów
│  zapis: plan.md; bez implementacji
│
├─ raven-pr — JEŚLI publikacja jest autoryzowana
│  Utwórz wczesny draft: link do issue i planu.
│  Aktualizuj ten sam PR w trakcie pracy.
│
▼
raven-plan-review
Niezależnie sprawdź zakres, wykonalność i testy
│
├─ Uwagi blokujące → raven-plan → ponowne review
│  Zmiany zakresu wymagają decyzji użytkownika.
│
▼
UŻYTKOWNIK: zaakceptuj konkretną wersję planu
│  review agenta nie zastępuje tej decyzji
▼
raven-implement
Wykonaj zatwierdzony plan wraz z testami
│  zapis: kod, testy, postęp i dowody w planie
│
├─ Zmiana kontraktu → plan → review → akceptacja
│  Zwykłe poprawki w zakresie nie restartują planu.
│
▼
raven-implement-review
Niezależnie oceń wymagania, kod i skuteczność testów
│
├─ Defekty → raven-implement → ponowne review
│  Naprawy i ponowna ocena dotyczą zmienionego zakresu.
│
▼
raven-pr
Zaktualizuj istniejący PR lub opublikuj nowy
│  publikacja w zakresie zgody; CI sprawdza wersję PR
▼
JEŚLI potrzebne dodatkowe QA
raven-manual-qa
Sprawdź działającą funkcję i zapisz defekty
│  bez automatycznego poprawiania produktu
│  defekty wracają do implementacji i review
▼
UŻYTKOWNIK: odbierz wynik i zleć merge
CI: wszystkie wymagane kontrole muszą przejść
│  issue nadal In progress
▼
raven-merge
Zweryfikuj bramki i zmerguj sprawdzony PR
│
├─ Merge niepotwierdzony → nie zamykaj issue
├─ Merge OK, zapis issue zawiódł
│  Wznów tylko finalizację issue, bez ponownego merge.
│
▼
ISSUE → DONE
Dopiero po potwierdzonym merge
│
▼
Następny issue → raven-plan
Deploy wymaga osobnego zlecenia.
```

Blokada na dowolnym etapie: issue pozostaje otwarte, otrzymuje `blocked` i krótki powód. Po rozwiązaniu blokady kontynuuj od checkpointu. Dwie nieskuteczne próby naprawy tego samego problemu zatrzymują pętlę.

## Skróty auto

Auto zastępuje wybrane wywołania manualne; nie usuwa decyzji użytkownika ani bramek merge.

```text
raven-auto-plan
└─ raven-plan → raven-plan-review → poprawki
   ↓
   Akceptacja użytkownika

raven-auto-implement
└─ raven-implement → raven-implement-review → poprawki
   ↓
   Odbiór użytkownika + CI → raven-merge
```

## Osobne zadanie testowe

Zwykły task tworzy testy podczas `raven-implement`. Poniższa ścieżka dotyczy osobno zleconych testów lub ochrony przed zmianą.

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
raven-pr → odbiór + CI → raven-merge → issue Done

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

Sync obejmuje zarejestrowaną rodzinę Raven, nie inne skille. Tworzy backup dotkniętych katalogów, usuwa nieaktualne pliki tych skilli i wycofane raven-pilot-* / raven-seed. Nie zmienia globalnego AGENTS.md. Przejrzyj różnice i nie nadpisuj niezwiązanych lokalnych modyfikacji; sync nie jest automatycznym scaleniem. Symlinki i kolizje plik/katalog wymagają uporządkowania przed zapisem. Instalacja nie potwierdza odświeżenia katalogu aktywnego UI.

W globalnych instrukcjach wskaż: raven-workflow wywołuj wyłącznie ręcznie jako tutorial i pomoc. Pozostałe skille wywołuj bezpośrednio, bez obowiązkowego routera. Rozwijając skille, użyj raven-create-skill i dostępnego hostowi skill-creator; nie instaluj ani nie publikuj zmian bez objęcia tego zleceniem.

Doctor sprawdza frontmatter, nazwy, lokalne odsyłacze, katalog, politykę ról i [kontrakt](workflow-contract.json), a `--installed` również zgodność instalacji. `doctor --json` daje raport maszynowy. Kontrakt deklaruje zależności, nie wykonuje workflow: `initial_artifacts` to wymagane zewnętrzne dowody/decyzje, nie fikcyjne zgody. PR jest operacją boczną i nie blokuje lokalnej implementacji. Opcjonalne dodatkowe QA/testy są poza standardowym cyklem; tracking issues jest wymagany, Project pozostaje widokiem.

Statyczny PASS nie dowodzi zachowania agenta ani prawdziwych uprawnień, CI i gotowości aplikacji. Zmiany instrukcji wymagają właściwych testów i niezależnych prób na rzeczywistych wejściach. Workflow [Raven integrity](.github/workflows/integrity.yml) uruchamia kontrole repo; sam YAML nie ustanawia required checks w GitHubie.

</details>

## Katalog wszystkich skilli — działanie i testy

**`raven-implement` pisze i uruchamia testy razem z kodem.** `raven-plan` i `raven-test-plan` tylko je planują. `raven-implement-review` ocenia istniejącą implementację i testy; `raven-auto-implement` łączy realizację, niezależne review i poprawki.

„Pisze testy” oznacza trwałe testy w repo. Sprawdzenie aplikacji w przeglądarce, analiza raportu lub odczyt CI to osobne czynności. Zakres nowych testów zależy od ryzyka zmiany i istniejącego pokrycia — nie każdy task wymaga każdej warstwy testów.

W kolumnie wyniku pliki przypisane do taska znajdują się domyślnie w `context/changes/<id>/`. Publikacja, merge i deploy pozostają w granicach zlecenia; samo review ani PASS nie zastępują decyzji użytkownika.

| Skill | Co wykonuje | Testy: pisanie i uruchamianie | Wynik i granica działania |
| --- | --- | --- | --- |
| [raven-agents-md](skills/raven-agents-md/SKILL.md) | Tworzy lub aktualizuje przewodnik dla agentów na podstawie struktury repo, komend, konfiguracji i historii. Zachowuje poprawne istniejące instrukcje. | Nie pisze testów aplikacji; dokumentuje wykryte komendy i zasady testowania. | `AGENTS.md` w repo lub wskazanym katalogu; nie inicjalizuje aplikacji. |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Prowadzi przez przekrojowe decyzje, porównuje opcje z PRD i istniejącym kodem, utrwala uzgodnienia. | Nie implementuje testów; uwzględnia wymagania jakościowe i testowalność. | `context/foundation/architecture.md`; nie implementuje wybranej architektury. |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Realizuje zaakceptowany plan, następnie uruchamia jedno świeże review wymagań, kodu i testów. Zleca poprawki oraz ponowną ocenę dotkniętego zakresu. | **Tak: pisze i uruchamia potrzebne trwałe testy wraz z kodem.** Dobiera warstwy do ryzyka; dodatkowy tester tylko z uzasadnieniem. | Kod, testy, checkpoint i dowody w `plan.md`, `review.md`. Oddaje wynik do odbioru; nie merguje automatycznie. |
| [raven-auto-plan](skills/raven-auto-plan/SKILL.md) | Przygotowuje plan przez planistę, zleca niezależne review i poprawki w ograniczonej pętli. Podejmuje issue jako In progress. | Planuje testy i sprawdza kompletność weryfikacji; nie implementuje testów produktu. | `plan.md` i `plan-review.md`; kończy na przekazaniu planu do akceptacji człowieka. |
| [raven-auto-test](skills/raven-auto-test/SKILL.md) | Koordynuje osobne zlecenie testów: autor testów → niezależny reviewer → poprawki i ponowne kontrole. | **Tak: pisze, uruchamia i niezależnie ocenia testy**, również ochronę przed refaktorem. Nie jest obowiązkowym etapem po implementacji. | Testy, dowody, checkpoint i ocena testów w repo; bez automatycznego merge/deploy. |
| [raven-browser](skills/raven-browser/SKILL.md) | Sprawdza działającą funkcję webową: formularze, nawigację, wynik akcji, wygląd i błędy. Domyślnie używa osobnej sesji Playwright CLI; osobiste Brave/MCP wymaga wyboru użytkownika. | Wykonuje scenariusze w przeglądarce; **nie zastępuje trwałych testów E2E** uruchamianych runnerem projektu. | Wynik scenariusza, screenshoty/logi i ograniczenia. Może służyć ponownej weryfikacji naprawionej regresji. |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Projektuje i zmienia skill Raven wraz z rzeczywistymi zależnościami, routingiem i dokumentacją; wymaga niezależnego review. | Waliduje skille, uruchamia doctor i odpowiednie testy repo; zmianę zachowania sprawdza przez izolowany forward-test. Nie testuje funkcji aplikacji przy okazji. | Pakiet instrukcji i potrzebnych helperów w repo skilli. Instalacja globalna oraz publikacja tylko w zakresie zlecenia. |
| [raven-domain-distillation](skills/raven-domain-distillation/SKILL.md) | Porównuje język dokumentów z modelem kodu przez niezależne analizy; wskazuje pojęcia, rozbieżności i niewiadome. | Nie pisze testów ani nie refaktoryzuje produktu; analizuje dostępne dowody. | `domain.md` i `glossary.md` w change lub foundation; dalsze zmiany wymagają planu. |
| [raven-frame](skills/raven-frame/SKILL.md) | Weryfikuje, czy opisany objaw, domniemana przyczyna i proponowane rozwiązanie rzeczywiście do siebie pasują. | Nie tworzy suite; zbiera dowody potrzebne do oceny hipotez. | `context/changes/<id>/frame.md`; nie zmienia kodu ani zatwierdzonych wymagań. |
| [raven-github-setup](skills/raven-github-setup/SKILL.md) | Przygotowuje lub uzupełnia repo/remote, tracking issues, etykiety statusu i politykę publikacji. Project pozostaje opcjonalny. | Nie pisze ani nie uruchamia testów aplikacji; weryfikuje konfigurację i wykonane zapisy GH. | Konfiguracja GitHub i `.raven/config.json`; samo przygotowanie nie daje zgody na push produktu lub merge. |
| [raven-hooks](skills/raven-hooks/SKILL.md) | Konfiguruje GitHub Actions dla istniejących komend lint, typecheck i właściwych testów. Sprawdza zgodność workflow ze stackiem. | Uruchamianie testów zapewnia CI; skill **nie służy do dopisywania testów zachowania produktu**. | Pliki workflow CI. Wymuszanie required checks wymaga osobnego zakresu; nie konfiguruje hooków sesji agenta. |
| [raven-implement](skills/raven-implement/SKILL.md) | Wykonuje lub wznawia zatwierdzony plan po jego review; podejmuje issue, zmienia kod, naprawia błędy w zakresie i zapisuje postęp. | **Tak: pisze i uruchamia potrzebne testy razem z implementacją** — unit/integration/E2E zależnie od ryzyka. Brak nowych testów wymaga uzasadnienia istniejącą ochroną lub charakterem zmiany. | Kod, testy, wyniki i checkpoint w `plan.md`. **Nie obejmuje samodzielnego niezależnego review** — następny skill to `raven-implement-review`. |
| [raven-implement-review](skills/raven-implement-review/SKILL.md) | Świeży reviewer porównuje implementację z wymaganiami i planem, ocenia kod, regresje oraz skuteczność testów. | Nie dopisuje ani nie poprawia ocenianych testów. Może uruchamiać kontrole potrzebne do weryfikacji dowodów. | `review.md` z zakresem, fingerprintem i konkretnymi uwagami; poprawki wracają do implementatora. Nie zastępuje odbioru człowieka. |
| [raven-init-stack](skills/raven-init-stack/SKILL.md) | Po uzgodnieniu wyborów generuje Better T Stack, instaluje zależności, przygotowuje lokalny PostgreSQL i konfigurację środowiska. | Sprawdza wygenerowany setup, typy i połączenie z bazą; **nie dodaje E2E** ani testów funkcji produktu. | Szkielet aplikacji, Compose/env i `context/foundation/tech-stack.md`; bez deploya i funkcji biznesowych. |
| [raven-jira-roadmap](skills/raven-jira-roadmap/SKILL.md) | Czyta wskazane tickety/sprint/epikę Jira, ustala samodzielne wyniki i wiąże je z taskami wykonawczymi GH. | Nie pisze ani nie uruchamia testów; zachowuje kryteria i wymagane gwarancje przy podziale pracy. | Issues GH z linkami do wymagań Jira, zależnościami i kolejnością. Nie zapisuje do Jira ani nie kopiuje całych ticketów. |
| [raven-lesson](skills/raven-lesson/SKILL.md) | Utrwala uzgodnioną, powtarzalną regułę lub wzorzec wynikający z doświadczenia projektu. | Nie implementuje testów; opisuje regułę i dowody jej zastosowania. | `context/foundation/lessons.md`; nie przerabia produktu przy okazji. |
| [raven-manual-qa](skills/raven-manual-qa/SKILL.md) | Planuje i wykonuje dodatkowe eksploracyjne QA działającej funkcji, szuka defektów i dokumentuje reprodukcję. | **Sprawdza aplikację, ale nie generuje trwałej suite i nie naprawia produktu.** To osobne QA, nie obowiązkowy etap każdego taska. | `qa-plan.md` i `qa-report.md` przy change; potwierdzone defekty i ograniczenia badania. |
| [raven-md](skills/raven-md/SKILL.md) | Tworzy lub celowo aktualizuje wskazany AGENTS.md na podstawie faktycznych plików, komend i konwencji; dopasowuje zakres do katalogu. | Nie pisze testów i nie uruchamia całej suite tylko dla dokumentacji; odróżnia znalezioną komendę od sprawdzonej. | Wskazany `AGENTS.md`; nie inicjalizuje stacku ani folderów kontekstu. |
| [raven-medusa-ecommerce-init](skills/raven-medusa-ecommerce-init/SKILL.md) | Uruchamia lub uzupełnia lokalny starter Medusa + Next.js: bazę, Redis, env, migracje, seed, admin i storefront. | Sprawdza start, bazę, właściwe build/typecheck i przepływ produkt → koszyk → checkout → zamówienie. Nie dodaje pełnego frameworka testów dla samego setupu. | Działające lokalne monorepo i instrukcja uruchomienia; bez rzeczywistych płatności, deploya i funkcji konkretnego sklepu. |
| [raven-merge](skills/raven-merge/SKILL.md) | Sprawdza akceptację, odbiór, review, CI i aktualny SHA; wykonuje zlecony merge, potwierdza wynik i dopiero wtedy zamyka issue. | Nie pisze testów. Weryfikuje aktualne dowody i wymagane checki; FAIL/UNKNOWN nie stają się PASS. | Zmergowany PR i issue Done. Przy awarii zamknięcia issue wznawia samą finalizację, bez ponownego merge; bez deploya. |
| [raven-plan](skills/raven-plan/SKILL.md) | Podejmuje issue jako In progress, bada potrzebny kod i tworzy plan jednego rezultatu: zakres, decyzje, kroki, ryzyka i kryteria. | **Opisuje, jakie testy trzeba wykonać; nie implementuje testów ani produktu.** | `context/changes/<id>/plan.md` z kontraktem, planem testów i checkpointem. Review jest osobnym wywołaniem `raven-plan-review`. |
| [raven-plan-review](skills/raven-plan-review/SKILL.md) | Niezależnie ocenia wykonalność, zakres, decyzje techniczne i pokrycie wymagań w planie. Uwagi przekazuje autorowi do poprawy. | Sprawdza adekwatność zaplanowanych testów; nie implementuje ich ani produktu. | `plan-review.md` dla konkretnego fingerprintu; nie jest akceptacją użytkownika ani startem implementacji. |
| [raven-pr](skills/raven-pr/SKILL.md) | Przygotowuje logiczne commity własnego zakresu, push i utworzenie lub aktualizację tego samego PR; wcześnie może wystawić draft. | Nie dopisuje testów. Przed ready sprawdza wykonanie, testy i review; draft może powstać wcześniej. Zapis PR może uruchomić CI. | PR z linkiem do issue i wersji planu, zakresem i walidacją; nie zamyka issue, nie merguje i nie deployuje. |
| [raven-prd](skills/raven-prd/SKILL.md) | Przekształca shape-notes lub surowe ustalenia w PRD według schematu greenfield/brownfield, z wymaganiami i kryteriami odbioru. | Nie pisze testów; definiuje zachowania, które później trzeba zweryfikować. | `context/foundation/prd.md`; bez planowania implementacji wszystkich tasków i bez kodowania. |
| [raven-repo-map](skills/raven-repo-map/SKILL.md) | Mapuje istniejące repo: obszary produktu, zależności, historię zmian i miejsca ryzyka. Wskazuje, gdzie rozpocząć dalsze badanie. | Nie pisze testów; analizuje strukturę i istniejącą ochronę, bez refaktoryzacji. | `context/foundation/repo-map.md` z dowodami i ograniczeniami; nie uruchamia automatycznie kolejnego etapu. |
| [raven-research](skills/raven-research/SKILL.md) | Odpowiada na konkretne pytania o kod lub wykonalność, sprawdza źródła i zapisuje dowody oraz niewiadome. | Nie tworzy suite. Test/build uruchamia tylko wtedy, gdy wynik odpowiada na konkretne pytanie badawcze. | `context/changes/<id>/research.md`; bez przygotowania planu lub implementacji przy okazji. |
| [raven-roadmap](skills/raven-roadmap/SKILL.md) | Dzieli wymagania na samodzielnie dostarczalne taski, ustala AC, zależności i kolejność; zachowuje istniejące ID i decyzje. | Nie pisze testów; pilnuje, by podział zachował wymagane gwarancje i weryfikowalność wyników. | Roadmapa w GitHub Issues; nie tworzy lokalnego backlogu ani szczegółowych planów wszystkich tasków. |
| [raven-rule-review](skills/raven-rule-review/SKILL.md) | Ocenia AGENTS.md lub inny plik reguł w pięciu wymiarach, wskazuje konkretne problemy i priorytetowe poprawki. | Nie pisze testów produktu; sprawdza jakość i zgodność instrukcji ze źródłami. | `rule-review.md` przy change lub foundation; domyślnie nie przepisuje ocenianych zasad. |
| [raven-shape](skills/raven-shape/SKILL.md) | Prowadzi rozmowę o problemie, odbiorcach, MVP, regułach biznesowych, ograniczeniach i niewiadomych. Wznawia zapisane ustalenia. | Nie pisze ani nie uruchamia testów; zbiera scenariusze i oczekiwane zachowanie. | `context/foundation/shape-notes.md`; nie uruchamia automatycznie PRD, budowy ani publikacji. |
| [raven-test](skills/raven-test/SKILL.md) | Dodaje lub poprawia testy w osobnym zleceniu, odtwarza błąd lub zabezpiecza refaktor; wykorzystuje istniejące narzędzia. | **Tak: pisze i uruchamia trwałe testy oraz właściwe regresje.** Dobiera unit/integration/E2E do ryzyka, bez obowiązku wszystkich warstw. | Pliki testów i dowody w `plan.md`; osobny `test-report.md` tylko gdy potrzebny. Review osobno lub w pełnym review change; defekty produktu naprawia wyłącznie w zleconym zakresie. |
| [raven-test-plan](skills/raven-test-plan/SKILL.md) | Tworzy lub odświeża strategię testowania projektu: ryzyka, warstwy, cookbook i sposób wdrożenia ochrony. Tryb status tylko odczytuje stan. | **Nie pisze testów i nie wdraża CI.** Projektuje strategię; testy konkretnej zmiany powstają przy implementacji lub osobnym `raven-test`. | `context/foundation/test-plan.md`; taski wdrożenia ochrony i ich status pozostają w GH. |
| [raven-test-review](skills/raven-test-review/SKILL.md) | Świeży reviewer ocenia testy: źródło oczekiwań, asercje, wykrywanie regresji, mocki, izolację i cleanup. | Nie poprawia ani nie dopisuje ocenianych testów; weryfikuje dowody i potrzebne kontrole. Nie zastępuje autora testów. | `test-review.md` z oceną, lukami i finding IDs; poprawki wracają do autora. Zwykłe review change już obejmuje testy. |
| [raven-workflow](skills/raven-workflow/SKILL.md) | Wyłącznie ręcznie wywoływany tutorial, wprowadzenie i podpowiedzi: pomaga zrozumieć etapy i wybrać właściwy skill. | Nie pisze ani nie uruchamia testów w ramach tutorialu. | Objaśnienie w rozmowie; nie jest obowiązkowym krokiem ani automatycznym routerem przed innymi skillami. |
