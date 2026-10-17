# Raven Workflow — cookbook

Raven przechowuje plan, wymagania, checklistę i checkpoint w `context/changes/<id>/plan.md`. Kod, testy i dokumenty mają wspólną historię Git. GitHub Issues jest obowiązkowym trackerem tasków, właścicieli, stanu projektu i roadmapy. Jeden issue odpowiada jednemu change, a Project jest opcjonalnym widokiem. PR służy współpracy, review i CI. Testy powstają z implementacją, a jedno niezależne review ocenia wymagania, kod i testy.

## Start i wznowienie

Wskaż repo i change ID, branch, lokalny plan albo PR. Agent zaczyna od [routera](skills/raven-workflow/SKILL.md), instrukcji projektu i krótkiego checkpointu. Nie potrzebuje historii rozmowy ani całego archiwum komentarzy GH. Nowy change domyślnie używa osobnego brancha w aktualnym checkout. Worktree służy pracy równoległej, potrzebie izolacji lub wyraźnemu życzeniu użytkownika; wznowienie zachowuje istniejący branch i katalog.

> Użyj raven-workflow. Sprawdź lokalny change C-03 i wskaż następny krok, bez rozpoczynania implementacji.

[Kontrakt pracy](skills/raven-workflow/references/change-contract.md) określa źródła prawdy, zgodę i dowody. Akceptacja dotyczy fingerprintu kontraktu (wymagania, podejście, kroki i testy). Zmiana checkboxa lub checkpointu nie unieważnia zgody; zmiana kontraktu wymaga ponownej decyzji. Planowanie/review pracują na Astra/high, implementacja i autor testów na Sol/low: [polityka ról](skills/raven-workflow/references/agent-policy.md).

## Greenfield

Shape → PRD → architektura → stack → instrukcje repo, strategia testów i CI → roadmapa → cykl change. Wybierz jeden bootstrapper (Better T Stack, Medusa lub gotowy stack). Nie odtwarzaj istniejącego setupu. Roadmapa żyje w GitHub Issues; nie tworzymy lokalnej roadmapy ani drugiego backlogu. Przed pierwszym taskiem uzupełnij brakujące repo/tracking przez raven-github-setup.

Diagram pokazuje kolejność wywołań od pomysłu do pierwszego dostarczonego taska, z wariantem **auto** dla planowania i implementacji. Węzły „lub” oznaczają wybór jednego skilla; gotowego setupu nie powtarzaj. Decyzje użytkownika są oznaczone osobno.

```mermaid
flowchart TB
  G0["raven-workflow<br/>Ustal punkt startowy i brakujące przygotowanie"]
  G1["raven-shape<br/>Dopracuj problem, odbiorców i zakres produktu"]
  G2["raven-prd<br/>Zapisz wymagania i kryteria odbioru produktu"]
  G3["raven-architecture<br/>Ustal przekrojowe decyzje architektoniczne"]
  G4["raven-init-stack lub raven-medusa-ecommerce-init<br/>Uruchom wybrany szkielet i środowisko projektu"]
  G5["raven-agents-md lub raven-md<br/>Przygotuj instrukcje pracy agentów w repo"]
  G6["raven-test-plan<br/>Ustal ryzyka, strategię testów i sposób weryfikacji"]
  G7["raven-github-setup<br/>Przygotuj repo GH, tracking issues i politykę publikacji"]
  G8["raven-hooks<br/>Skonfiguruj CI dla właściwych kontroli projektu"]
  G9["raven-roadmap<br/>Utwórz taski w GH i ustal zależności oraz kolejność"]
  G10["raven-auto-plan dla wybranego issue<br/>Ustaw In progress i wykonawcę; przygotuj plan z review"]
  G11["Użytkownik<br/>Zaakceptuj konkretną wersję planu"]
  G12["raven-pr — wcześnie, jeśli autoryzowany<br/>Opublikuj draft z planem i powiązaniem issue"]
  G13["raven-auto-implement<br/>Zaimplementuj, dodaj testy, wykonaj review i poprawki"]
  G14["raven-pr<br/>Zaktualizuj PR lub opublikuj go teraz; uruchom CI"]
  G15["Użytkownik + CI<br/>Odbierz wynik, potwierdź kontrole i zleć merge"]
  G16["raven-merge<br/>Zmerguj sprawdzony PR, potem zamknij issue jako Done"]
  G0 --> G1 --> G2 --> G3 --> G4 --> G5 --> G6 --> G7 --> G8 --> G9 --> G10 --> G11 --> G12 --> G13 --> G14 --> G15 --> G16
```

Draft można opublikować już podczas planowania, jeśli obejmuje go wcześniejsza zgoda; nie trzeba czekać na akceptację planu. Bez zgody na wczesną publikację pomiń pierwszy `raven-pr`. Dla kolejnego taska wróć do `raven-auto-plan`, wykorzystując gotowe przygotowanie projektu.

| Krok | Dane wejściowe | Wynik i miejsce zapisu |
| --- | --- | --- |
| Shape | Pomysł, rozmowa i materiały użytkownika | Uzgodniony problem i zakres w `context/foundation/shape-notes.md`. |
| PRD | Notatki i decyzje | Wymagania i kryteria produktu w `context/foundation/prd.md`. |
| Architektura | PRD i ograniczenia | Decyzje potrzebne przed implementacją w `context/foundation/architecture.md`. |
| Warsztat | Architektura i wybrany stack | Działający szkielet, instrukcje repo, strategia w `context/foundation/test-plan.md` i właściwe CI. |
| Roadmapa | Wymagania oraz działający szkielet | Kolejność samodzielnie odbieralnych zmian; szczegółowy plan powstaje dopiero dla wybranego change. |

> Użyj raven-shape. Chcę zbudować […]. Ustalmy problem, odbiorców i najmniejszy kompletny zakres produktu.

## Brownfield

Zakres lub wznowienie → opcjonalna mapa nieznanego obszaru → rzeczywiste braki instrukcji/test strategy/CI → opcjonalny frame/research/domena → plan. Mała zmiana w znanym miejscu nie potrzebuje mapowania całego repo ani Project. Jira może pozostać źródłem wymagań. Issue GH śledzi wykonanie, linkując ticket i jego wersję, bez kopiowania treści.

Diagram pokazuje wejście do istniejącego projektu i realizację jednego taska w wariancie **auto**. Kroki oznaczone „jeśli” wykonuj tylko przy wskazanej potrzebie. Przy wznowieniu `raven-workflow` kieruje od razu do brakującego etapu, bez ponownego przechodzenia całego diagramu.

```mermaid
flowchart TB
  B0["raven-workflow<br/>Odczytaj wskazany task, repo i checkpoint; ustal etap"]
  B1["raven-repo-map — jeśli obszar jest nieznany<br/>Rozpoznaj kod, zależności i istniejące testy"]
  B2["raven-agents-md lub raven-md — jeśli brakuje instrukcji<br/>Uzupełnij AGENTS.md na podstawie repo"]
  B3["raven-test-plan — jeśli brakuje strategii<br/>Ustal ryzyka i potrzebną ochronę testową"]
  B4["raven-github-setup — jeśli brakuje konfiguracji GH<br/>Uzupełnij repo, tracking issues i politykę publikacji"]
  B5["raven-hooks — jeśli brakuje właściwego CI<br/>Dodaj kontrole zgodne z istniejącym stackiem"]
  B6["raven-frame — jeśli problem lub przyczyna są niejasne<br/>Zweryfikuj objaw, założenia i oczekiwany rezultat"]
  B7["raven-research — jeśli brakuje wiedzy o kodzie<br/>Zbierz dowody potrzebne do zaplanowania zmiany"]
  B8["raven-domain-distillation — jeśli model domeny jest niejasny<br/>Porównaj język wymagań z istniejącym kodem"]
  B9["raven-architecture — jeśli potrzebna jest decyzja przekrojowa<br/>Ustal podejście i ograniczenia zmiany"]
  B10["raven-roadmap — jeśli zlecono uporządkowanie kolejki<br/>Ustal taski GH i zależności; dla źródeł Jira użyj raven-jira-roadmap"]
  B11["raven-auto-plan dla wybranego issue<br/>Ustaw In progress i wykonawcę; przygotuj plan z review"]
  B12["Użytkownik<br/>Zaakceptuj konkretną wersję planu"]
  B13["raven-pr — wcześnie, jeśli autoryzowany<br/>Opublikuj draft z planem i powiązaniem issue"]
  B14["raven-auto-implement<br/>Zmień kod wraz z testami; wykonaj review i poprawki"]
  B15["raven-pr<br/>Zaktualizuj PR lub opublikuj go teraz; uruchom CI"]
  B16["Użytkownik + CI<br/>Odbierz wynik, potwierdź kontrole i zleć merge"]
  B17["raven-merge<br/>Zmerguj sprawdzony PR, potem zamknij issue jako Done"]
  B0 --> B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> B7 --> B8 --> B9 --> B10 --> B11 --> B12 --> B13 --> B14 --> B15 --> B16 --> B17
```

Dla małego taska w znanym, przygotowanym repo przejdź od `raven-workflow` prosto do `raven-auto-plan`. Rozpoznanie prowadzone już w ramach zleconego planowania odbywa się po ustawieniu issue In progress. Wczesny draft podlega tej samej zasadzie co w greenfield: może powstać podczas planowania albo zostać pominięty do późniejszej publikacji.

W obu diagramach wariant **manual** zastępuje `raven-auto-plan` parą `raven-plan` → `raven-plan-review`, a `raven-auto-implement` parą `raven-implement` → `raven-implement-review`. Akceptacja planu i odbiór użytkownika pozostają w tych samych miejscach. `raven-test`, `raven-auto-test` i `raven-manual-qa` są dodatkowymi narzędziami na osobne zlecenie lub konkretne ryzyko, nie kolejnymi obowiązkowymi etapami.

| Krok | Dane wejściowe | Wynik |
| --- | --- | --- |
| Rozpoznanie lub wznowienie | Zlecenie, instrukcje repo, Git, wskazany plan/PR | Jednoznaczny zakres i następny krok; sam status niczego nie zapisuje. |
| Mapa, gdy potrzebna | Kod, testy, dokumentacja i wybrana historia Git | Lokalna mapa potrzebnego obszaru, bez pełnego skanu przy każdym zadaniu. |
| Uzupełnienie warsztatu | Istniejące komendy, runnery i CI | Sprawdzone uruchamianie oraz weryfikacja; zachowany stack i konwencje. |
| Frame/research, gdy potrzebne | Objaw, wymagania i dowody z kodu | Potwierdzony problem i ustalenia przy zmianie, bez obowiązkowego issue. |
| Plan | Wymagania, ustalenia i aktualny kod | `context/changes/<id>/plan.md` na branchu zmiany; dalej wspólny cykl. |

Istniejący projekt nie wymaga odtworzenia PRD całego produktu. Roadmapę twórz lub reorganizuj wtedy, gdy obejmuje to zlecenie.

> Użyj raven-plan dla issue #12 w owner/repo. Przygotuj plan poprawki, wykorzystując istniejący kod i testy. Kod i plan na razie lokalnie, bez push/PR.

## Cykl change

```mermaid
flowchart TD
  T[Issue: In progress + assignee] --> P[Plan lokalny]
  P --> R[Review planu]
  R --> A[Akceptacja fingerprintu]
  A --> I[Implementacja i testy]
  I --> V[Jedno niezależne review wymagań, kodu i testów]
  V -->|Defekt w zakresie| I
  V --> U[Odbiór użytkownika i aktualne CI]
  U --> M[Merge za zgodą]
  M --> DONE[Potwierdzony merge: issue Done]
  P -. Autoryzowana polityka .-> D[Wczesny draft PR]
  D -. Aktualizacje w toku pracy .-> I
  M -. Osobne zlecenie .-> DEP[Deploy]
```

Manual: raven-plan → raven-plan-review, potem raven-implement → raven-implement-review. Auto: raven-auto-plan i raven-auto-implement koordynują te same artefakty oraz ograniczone pętle napraw. Rutynowe poprawki w zleconym zakresie nie wymagają pytania po każdej komendzie. Po dwóch nieskutecznych próbach tego samego problemu agent zapisuje reprodukcję i potrzebną decyzję.

Wczesny draft PR wykorzystuje wcześniej autoryzowaną politykę `.raven/config.json`; zlecenie planowania/implementacji obejmuje podjęcie jego issue, ale nie daje praw push/PR. Bez niej kod i plan pozostają lokalne przy potwierdzonym trackingu GH, a raven-pr można zlecić dla przygotowanego wyniku. Merge wymaga aktualnych dowodów, CI, odbioru i zgody; „akceptuję, zmerguj” może potwierdzić obie decyzje. Issue pozostaje In progress podczas review i PR; dopiero potwierdzony raven-merge zamyka issue jako Done. Board jest opcjonalnym widokiem. Deploy pozostaje osobno.

Przykładowe osobne zlecenia dla jednej zmiany:

```text
Użyj raven-auto-plan dla C-03.
[Po review] Akceptuję przedstawiony plan. Użyj raven-auto-implement dla C-03.
[Jeżeli nie ma polityki wcześniejszej publikacji] Użyj raven-pr dla C-03.
[Po odbiorze i CI] Akceptuję wynik. Użyj raven-merge dla C-03.
```

## Artefakty i praca między sesjami

| Miejsce | Odpowiedzialność |
| --- | --- |
| `context/foundation/` | Wymagania produktu, architektura i strategia testowania. |
| `context/changes/<id>/plan.md` | Jeden dokument: linki wymagań/issue, implementacja, plan testów, akceptacja, wyniki, postęp i checkpoint. |
| GitHub Issues | Taski/change, assignees, In progress/blocked/Done oraz roadmapa i zależności; bez lokalnej kopii kolejki. |
| Pliki obok planu | Research, review i raporty kontroli, tylko gdy potrzebne; PR może do nich linkować. |
| Git / branch / worktree | Rzeczywista wersja kodu, testów i dokumentów oraz ich historia. |
| PR i CI | Współpraca, feedback, wyniki kontroli i potwierdzenie merge. |
| `.raven/config.json` | Powiązanie repo i wcześniej ustalona polityka publikacji. |
| Lokalny journal runtime w katalogu Git | Odzyskiwanie przerwanych operacji; nie zastępuje wersjonowanego checkpointu. |

Odczyt/status niczego nie mutuje. Na początku zleconego planowania lub implementacji agent ustawia In progress i assignee konkretnego issue. Kolejne zapisy są zdarzeniowe: blokada/odblokowanie i merge; zgodny stan oznacza no-op, bez skanowania boarda. PR linkuje issue i pliki, bez kopiowania planów/raportów do GH. Jeśli merge się udał, a zamknięcie issue nie, wynik brzmi „PR merged; issue nadal wymaga finalizacji”; wznowienie nie powtarza merge.

Jedną zmianę edytuje jeden aktywny autor, identyfikowany również przez sesję. Reviewer pracuje odczytowo; przekazanie pracy jest jawne. Lokalny mutex runtime chroni pojedynczą operację i nie jest blokadą rozproszoną między komputerami.

Przy wznowieniu agent odczytuje konkretny issue, plan, checkpoint i rzeczywisty stan Git, a następnie potrzebny feedback PR. Niedokończona publikacja wznawia publikację, nie implementację. Brak GH nie potwierdza podjęcia taska: agent zgłasza tracking-unconfirmed, zachowuje checkpoint i może wykonać niezależne rozpoznanie read-only, bez rozpoczynania zależnego planowania/implementacji. Blokady są widoczne w issue; nieudany zapis pozostaje jawnie niepotwierdzony.

## Sytuacje szczególne

- Niechroniony refaktor: testy charakteryzacyjne before-change; bugfix: reprodukcja i oczekiwany RED, potem GREEN na poprawce.
- Dodatkowe ryzyko auth, migracji, rozliczeń lub współbieżności: dobierz tester/audyt do konkretnego problemu. Każdy normalny change nie potrzebuje dodatkowego testera i osobnego test-review.
- Samodzielna inwestycja w testy: raven-test lub raven-auto-test; globalna strategia: raven-test-plan. Dodatkowe eksploracyjne QA: raven-manual-qa przyjmuje change, PR lub issue.
- Historia starego Raven: zachowaj artefakty. Kontynuacja ustala mapowanie jawnie; aktualizacja skilli nie migruje archiwów.

[Runtime](skills/raven-workflow/references/runtime.md) zapewnia ograniczone start/status/resume, fingerprint, checkpoint, zdarzeniowy helper issue i draft PR dla już wypchniętej gałęzi. Nie zatwierdza planów, nie pushuje i nie jest silnikiem całego procesu.

## Katalog skilli

| Skill | Zastosowanie |
| --- | --- |
| [raven-agents-md](skills/raven-agents-md/SKILL.md) | Onboarding AGENTS.md z rzeczywistego repo. |
| [raven-architecture](skills/raven-architecture/SKILL.md) | Przekrojowe decyzje architektoniczne. |
| [raven-auto-implement](skills/raven-auto-implement/SKILL.md) | Implementacja, testy, jedno review i naprawy w zakresie. |
| [raven-auto-plan](skills/raven-auto-plan/SKILL.md) | Plan i niezależne review do decyzji użytkownika. |
| [raven-auto-test](skills/raven-auto-test/SKILL.md) | Osobne zlecenie testów z niezależnym review i naprawami. |
| [raven-browser](skills/raven-browser/SKILL.md) | Osobna sesja Playwright CLI, zasady dostępu do przeglądarki. |
| [raven-create-skill](skills/raven-create-skill/SKILL.md) | Projektowanie i spójna aktualizacja rodziny Raven. |
| [raven-domain-distillation](skills/raven-domain-distillation/SKILL.md) | Niezależne porównanie języka dokumentów i kodu. |
| [raven-frame](skills/raven-frame/SKILL.md) | Oddzielenie obserwacji od założonej przyczyny. |
| [raven-github-setup](skills/raven-github-setup/SKILL.md) | Remote, wymagany tracking issues i polityka publikacji; Project opcjonalny. |
| [raven-hooks](skills/raven-hooks/SKILL.md) | GitHub Actions dla rzeczywistych kontroli projektu. |
| [raven-implement](skills/raven-implement/SKILL.md) | Realizacja planu wraz z testami. |
| [raven-implement-review](skills/raven-implement-review/SKILL.md) | Jedno review wymagań, kodu i testów. |
| [raven-init-stack](skills/raven-init-stack/SKILL.md) | Better T Stack i lokalna baza. |
| [raven-jira-roadmap](skills/raven-jira-roadmap/SKILL.md) | Jira jako źródło wymagań, issue GH jako tracking wykonania bez kopiowania treści. |
| [raven-lesson](skills/raven-lesson/SKILL.md) | Zapis jednej uzgodnionej powtarzalnej reguły. |
| [raven-manual-qa](skills/raven-manual-qa/SKILL.md) | Dodatkowa eksploracja UI i potwierdzone reprodukcje. |
| [raven-md](skills/raven-md/SKILL.md) | Tworzenie lub aktualizacja wskazanych instrukcji. |
| [raven-medusa-ecommerce-init](skills/raven-medusa-ecommerce-init/SKILL.md) | Medusa + Next.js: lokalne monorepo i środowisko. |
| [raven-merge](skills/raven-merge/SKILL.md) | Merge sprawdzonego PR, potem zweryfikowane zamknięcie jego issue. |
| [raven-plan](skills/raven-plan/SKILL.md) | Manualne przygotowanie lokalnego planu. |
| [raven-plan-review](skills/raven-plan-review/SKILL.md) | Niezależna ocena wykonalności i granic planu. |
| [raven-pr](skills/raven-pr/SKILL.md) | Wczesny draft lub aktualizacja PR, logiczne commity i zwykły push. |
| [raven-prd](skills/raven-prd/SKILL.md) | Wymagania produktu z notatek i decyzji. |
| [raven-repo-map](skills/raven-repo-map/SKILL.md) | Mapa nieznanego repo, zależności i ryzyk. |
| [raven-research](skills/raven-research/SKILL.md) | Ograniczone badanie kodu i lokalny raport dowodów. |
| [raven-roadmap](skills/raven-roadmap/SKILL.md) | Kolejność samodzielnych changes i zależności w GitHub Issues. |
| [raven-rule-review](skills/raven-rule-review/SKILL.md) | Ocena jakości instrukcji AI. |
| [raven-shape](skills/raven-shape/SKILL.md) | Dopracowanie problemu i zakresu produktu. |
| [raven-test](skills/raven-test/SKILL.md) | Osobne testy, before-change lub uzupełnienie ochrony. |
| [raven-test-plan](skills/raven-test-plan/SKILL.md) | Strategia testów, ryzyka i cookbook w repo. |
| [raven-test-review](skills/raven-test-review/SKILL.md) | Ocena konkretnych testów na zlecenie lub według ryzyka. |
| [raven-workflow](skills/raven-workflow/SKILL.md) | Router, status i wznowienie z repo. |

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

W globalnych instrukcjach wskaż: przy pracy Raven najpierw czytaj raven-workflow, następnie tylko skille potrzebne do zadania. Rozwijając skille, użyj raven-create-skill i dostępnego hostowi skill-creator; nie instaluj ani nie publikuj zmian bez objęcia tego zleceniem.

Doctor sprawdza frontmatter, nazwy, lokalne odsyłacze, katalog, politykę ról i [kontrakt](workflow-contract.json), a `--installed` również zgodność instalacji. `doctor --json` daje raport maszynowy. Kontrakt deklaruje zależności, nie wykonuje workflow: `initial_artifacts` to wymagane zewnętrzne dowody/decyzje, nie fikcyjne zgody. PR jest operacją boczną i nie blokuje lokalnej implementacji. Opcjonalne dodatkowe QA/testy są poza standardowym cyklem; tracking issues jest wymagany, Project pozostaje widokiem.

Statyczny PASS nie dowodzi zachowania agenta ani prawdziwych uprawnień, CI i gotowości aplikacji. Zmiany instrukcji wymagają właściwych testów i niezależnych prób na rzeczywistych wejściach. Workflow [Raven integrity](.github/workflows/integrity.yml) uruchamia kontrole repo; sam YAML nie ustanawia required checks w GitHubie.
