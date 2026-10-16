# Wewnętrzna procedura Raven

To część implementacji skilla Raven, nie osobna komenda. Czytaj ją wraz z nadrzędnym SKILL.md, który określa tryb manual/auto i uprawnienia. Wszystkie szablony, referencje i skrypty są dostarczone lokalnie w tym katalogu. Nie wyszukuj ani nie instaluj innych pakietów workflow.

**Obowiązujące zasady wykonania:** [kontrakt GitHub](../../../../raven-auto-plan/references/github-contract.md). Ścieżki change/plan/research/review i strategii testów w tej procedurze oznaczają kopie robocze w artifact_dir poza repo, odtwarzane z GitHuba. Kod i testy pozostają w repo_root. Lokalne wykrywanie stanu zastąp odczytem issues, snapshotów i checkpointów. Pomijaj lokalną synchronizację roadmapy, archiwizację, staging kontekstu i commit epilogu dokumentacji; nie wykonuj ich także przez helpery. Status Done pochodzi wyłącznie z potwierdzonego merge i konfiguracji projektu. Odwołania do publikacji PR nie upoważniają do audytu, zamykania issues ani automatycznego wywołania tego etapu. Zakończenie procedury oddaje wynik nadrzędnemu skillowi; jego reguły decydują o dalszym review i handoffie. Osobny research jest decyzją użytkownika. Tryb before-change i aktualne zasady review testów mają pierwszeństwo przed domyślną kolejnością testów.

# Raven E2E — Wykonywanie planu E2E opartego na ryzyku

Realizujesz zatwierdzony plan techniczny z `context/changes/<change-id>/plan.md` do poziomu **pokrycia przeglądarkowego**, po jednej fazie i jednym ryzyku naraz. Agent może wygenerować *przechodzący* test E2E w kilka sekund; trudne jest zapewnienie, że **chroni rzeczywiste ryzyko** i **przetrwa jutrzejszy refaktoring**. Ta umiejętność prowadzi wyłącznie fazy, do których należy ta praca — ryzyko, które przekracza kilka granic systemu (auth, routing, API, DB) albo istnieje wyłącznie w wyrenderowanym UI — a dla każdej uruchamia pętlę:

```
PLAN     →  wybierz ryzyko, zbadaj działającą aplikację, odwzoruj przepływ (lub wypełnij szablon promptu)
GENERATE →  przekształć przepływ w test na podstawie wzorca seed + zasad E2E
REVIEW   →  sprawdź go względem pięciu antywzorców E2E agentów; ponownie zapromptuj po nazwie
VERIFY   →  uruchom go na zielono, a następnie potwierdź, że nie przechodzi, gdy ryzyko faktycznie się materializuje
```

To wewnętrzna procedura tworzenia trwałych testów przeglądarkowych, używana przez raven-test i raven-auto-test. Otrzymuje od nadrzędnego skilla change, zaakceptowany zakres, repo_root, artifact_dir i wersjonowane źródła z GH. Nie wybiera samodzielnie nowego ryzyka poza zakresem ani nie tworzy osobnego lokalnego workflow. Unit/integration wykonuje nadrzędny skill właściwą procedurą implementacji testów.

Podstawowa dyscyplina: **nie generuj testów E2E od zera.** Zacznij od ryzyka nazwanego przez fazę i kontroluj wynik agenta za pomocą dwóch dźwigni jakości — **testu seed** i **zasad E2E**. Prompt dostarcza tylko tego, czego te dwie rzeczy nie mogą zakodować: konkretnego ryzyka, przepływu oraz granic rzeczywistych i mockowanych.

```
context/foundation/test-plan.md  (ryzyka, do których odwołują się fazy planu)
        │
        ▼
   seed.spec.ts  +  zasady E2E  →  kształtują każdy wygenerowany test
        │                          (getByRole, izolacja, wait-for-state, rzeczywiste vs mockowane)
        ▼
   PLAN → GENERATE → REVIEW → VERIFY  →  jeden zrecenzowany test na ryzyko  →  CI
```

Agenci widzą **drzewo dostępności** (role, nazwy, stany w migawce YAML z referencjami elementów), a nie piksele — dzięki temu naturalnie tworzą testy oparte na `getByRole`, a nie selektorach CSS.

Ścieżka planu: `$ARGUMENTS`

## Co zakłada ta umiejętność — i czego nie zrobi

- **Setup jest osobną procedurą wewnętrzną.** Przy brakującej konfiguracji lub seedzie wykonaj [setup E2E](../e2e-setup/procedure.md) w ramach uzgodnionego zakresu i wróć do tej procedury. Nie odsyłaj do ponownego wywołania raven-test. Nie podłączaj CI; tym zajmuje się raven-hooks.
- **Funkcja pod testem istnieje.** Testy zabezpieczają działającą funkcję albo zastane zachowanie w trybie before-change. Gdy do reprodukcji brakuje funkcji produktu, zgłoś to koordynatorowi; nie implementuj jej w etapie testów. Oczekiwany RED bugfixu obsługuje kontrakt before-change.
- **Używa dwóch dźwigni jakości; nie tworzy ich.** Test seed jest pisany przez wewnętrzną procedurę setupu E2E; zasady E2E są dostarczane z tą umiejętnością (`references/e2e-quality-rules.md`), a nie w pliku zasad twojego asystenta AI. Ta umiejętność modeluje każdy wygenerowany test na ich podstawie i sprawdza względem nich, ale nigdy nie przepisuje seed. Dopuszczalne jest dodawanie małych helperów testowych potrzebnych specyfikacji (np. oczekiwania na hydration w `tests/e2e/`).
- **Prowadzi jeden zrecenzowany test na ryzyko, nie masowe pokrycie.** W przeciwieństwie do „generuj testy dla każdej strony”, ta umiejętność zapisuje mały zestaw związany z ryzykiem i utwardza każdy przez przegląd oraz celowe zepsucie. E2E to najdroższa i najbardziej podatna na flaky warstwa — celem nigdy nie jest liczba pokrycia; celem jest chronione ryzyko.
- **Bramkuje każdą fazę na podstawie tego, czy E2E faktycznie pasuje i czy aplikacja jest gotowa.** Niektóre fazy (czysta logika, konfiguracja, scaffolding) nigdy nie powinny otrzymać testu E2E. Funkcji, które nie są zbudowane, nie da się obsłużyć w przeglądarce. Te przypadki są przekierowywane lub zatrzymywane zgodnie z opisem poniżej.

## Przegląd faz

```
SETUP            →  Odczytaj plan z GH, potwierdź infrastrukturę (uzupełnij procedurą e2e-setup, jeśli brakuje) + możliwość uruchomienia aplikacji, przeczytaj seed + zasady, rozpocznij checklistę postępu
Dla każdej fazy:
  ├─ GATE        →  Czy to ryzyko jest na poziomie przeglądarki ORAZ czy funkcja jest zbudowana ORAZ czy test E2E nie istnieje? Jeśli nie → przekieruj lub zatrzymaj
  ├─ PLAN/GENERATE/REVIEW/VERIFY  →  Wykonuj pętlę dla każdego ryzyka w fazie, aż jego kryteria sukcesu zostaną spełnione
  └─ PHASE END   →  Właściwe E2E zielone → bramka ręczna → rytuał commitu → decyzja o następnej fazie (schowek)
Po zleconych fazach → raport dla nadrzędnego skilla i właściwe review testów
```

Zachowaj checkpointy faz i uzgodniony zakres. W manualu stosuj decyzje między fazami; w auto kontynuuj uzgodnione fazy bez pytania o każdą, zachowując rzeczywiste wymagane decyzje i manual checks.

---

## Konfiguracja

1. **Rozwiąż kontekst z nadrzędnego skilla.** Użyj wskazanego issue, zatwierdzonego zakresu i snapshotu z GH. Brak lokalnego folderu nie oznacza samodzielnego trybu risk-id. Jeśli źródła są niepełne, zwróć konkretną blokadę koordynatorowi. Kopie planu i strategii w artifact_dir są reprezentacją danych GH, nie kanonicznymi plikami repo.

2. **Przeczytaj plan w całości** — każdą fazę, każdy blok Changes Required, każde kryterium Success Criteria. Nigdy nie używaj limit/offset; potrzebujesz pełnego kontekstu. Sekcja `## Progress` na dole jest **roboczą reprezentacją stanu wykonania z GH** — checkmarki (`- [x]`) znajdują się WYŁĄCZNIE tam. Bloki faz mają zwykłe wypunktowania `- `, bez checkboxów. Zanotuj, które fazy odwołują się do ryzyka w `context/foundation/test-plan.md`, które potrzebuje pokrycia na poziomie przeglądarki; to właśnie te fazy prowadzi ta umiejętność.

3. **Przeczytaj `context/foundation/test-plan.md`**, jeśli istnieje — zawiera mapę ryzyk chronionych przez każdą fazę E2E (wpływ, prawdopodobieństwo, zachowanie dowodzące ochrony). Jednostką pracy jest tutaj ryzyko, nie plik.

4. **Przeczytaj `context/foundation/lessons.md`**, jeśli istnieje, i przyswój każdy wpis przed rozpoczęciem dowolnej fazy — są to zaakceptowane przez zespół powtarzalne zasady i muszą kształtować każdy wybór testowy w tym uruchomieniu.

5. **Potwierdź infrastrukturę E2E z `/raven-test` oraz możliwość uruchomienia aplikacji (lekka kontrola — nie badaj całego świata):**
   - Jeśli istnieje `context/foundation/test-stack.md`, przeczytaj jego sekcję `## E2E` — rejestruje runner i wersję, ścieżkę konfiguracji, polecenia dla pojedynczej specyfikacji i pełnego zestawu, base URL i port, polecenie serwera webowego, projekt konfiguracji auth i ścieżkę `storageState`, a także ścieżkę seed. Użyj tych informacji i pomiń skanowanie. Port faktycznie używany przez uruchomienie to `E2E_PORT` z pliku env, gdy jest ustawiony. Wpisy mock-server w `webServer` w formie tablicy nie są tam rejestrowane; przeczytaj je w konfiguracji. Jeśli wygląda nieaktualnie (odwołuje się do plików lub konfiguracji, które już nie istnieją), zgłoś to użytkownikowi i przejdź do szybkiego skanowania.
   - W przeciwnym razie wykonaj **szybkie** skanowanie: jedno wyszukiwanie plików dla `playwright.config.*` / `*.spec.ts`, następnie przeczytaj konfigurację i jedną specyfikację, aby poznać polecenie uruchamiające **pojedynczą** specyfikację, konfigurację auth (`storageState` / projekt `setup`) oraz sposób uruchamiania aplikacji (blok `webServer` lub polecenie dev-server).
   - **Jeśli brakuje konfiguracji lub seeda**, wykonaj [setup E2E](../e2e-setup/procedure.md) w uzgodnionym zakresie. Po jego weryfikacji kontynuuj tutaj. Przy nieuzgodnionej zmianie infrastruktury zgłoś potrzebną decyzję; nie zapętlaj wywołań raven-test.

   - **Wynik konfiguracji nie został jeszcze zacommitowany?** Jeśli `git status` pokazuje, że pliki z `/raven-test` są niezacommitowane (konfiguracja, seed, `test-stack.md`), zaproponuj ich commit teraz, zanim to uruchomienie zmodyfikuje którykolwiek z nich (`chore: set up Playwright E2E`, staged by path; Recommended). Później konfiguracja zawiera również wpis mocka z tego uruchomienia, a ich rozdzielenie wymaga częściowego stage'owania.

6. **Przeczytaj dwie dźwignie jakości.** Wykonują ciężką pracę — prompt pozostaje zwięzły. Ta umiejętność je czyta i nigdy nie przepisuje.
   - **Test seed** (`seed.spec.ts`, ścieżka z `test-stack.md` lub skanowania): wzorzec, według którego modelowany jest każdy wygenerowany test. *To, co pokazujesz, to, co dostajesz* — jeśli seed używa `getByRole`, wygenerowane testy również; jeśli zawiera `waitForTimeout`, odziedziczy go każdy wygenerowany test. `references/seed-test-pattern.md` wyjaśnia cztery wzorce obecne w dobrym seed; zobacz także `references/browser-driven-generation.md`.
   - **Zasady E2E**: przeczytaj `references/e2e-quality-rules.md` — zasady, których przestrzega każdy wygenerowany test, wraz z uzasadnieniem każdej z nich. Znajdują się przy tej umiejętności, nie w pliku zasad twojego asystenta AI. Jeśli starsza konfiguracja pozostawiła tam blok zasad E2E, ta referencja ma pierwszeństwo tam, gdzie się różnią.

7. **Zaktualizuj `change.md`**: ustaw `status: implementing` (tylko jeśli obecnie jest w `{planned, plan_reviewed}`) i `updated: <today>`.

8. **Rozpocznij checklistę postępu w rozmowie**: jeden wiersz dla każdej `## Phase N:`, którą zamierzasz prowadzić (`- [ ] Phase N: [Phase Name]`). Oznacz bieżącą fazę jako w toku przed jej rozpoczęciem i zaznacz ją, gdy jej kryteria sukcesu przejdą. Checklista jest wyłącznie widokiem dla użytkownika — `## Progress` w `plan.md` pozostaje źródłem prawdy.

9. **Znajdź punkt startowy**: przeskanuj `## Progress` — pierwsze `- [ ]` w kolejności dokumentu to miejsce startu. Jeśli przekazano argument `phase N`, przejdź do pierwszego `- [ ]` pod `### Phase N:`.

> **Konwencja schowka.** Gdziekolwiek ta umiejętność mówi *skopiuj `X` do schowka*, prześlij dokładny ciąg `X` do schowka platformy — spróbuj `pbcopy` (macOS), potem `clip.exe` (Windows/WSL), następnie `xclip -selection clipboard` (Linux) lub `Set-Clipboard` w PowerShell, a jeśli żadne nie istnieje, przejdź dalej po cichu. Następnie wyświetl skopiowane polecenie w osobnym wierszu z sufiksem `(✓ copied)`.

> **Pytanie użytkownika — niezależne od hosta.** Gdziekolwiek ta umiejętność mówi *zapytaj użytkownika*, użyj dowolnej możliwości interaktywnego zadawania pytań udostępnianej przez twojego asystenta programistycznego AI; nie koduj na sztywno nazwy jednego narzędzia. Przed pierwszym pytaniem sprawdź dostępne możliwości pod kątem takiej, która zadaje użytkownikowi pytanie strukturalne (parametr `question` oraz pole `options`/`choices`), i użyj pierwszego dopasowania. Jeśli nie istnieje żadna, zapytaj zwykłą wiadomością rozmowną, wymieniając oznaczone opcje, i czekaj na odpowiedź — nigdy nie blokuj procedury. Gdy pytasz po raz pierwszy, powiedz, której możliwości użyto (lub że nastąpił fallback do zwykłego czatu). Poniższe bloki opcji podają pytanie, etykiety i ich opisy; odwzoruj je na dostępny schemat bez zmiany ich znaczenia.

---

## Bramka kwalifikacji E2E — uruchamiaj przed każdą fazą (sterowaną planem) / raz (samodzielnie)

Zanim zaplanujesz pojedynczy test dla fazy, zdecyduj o trzech rzeczach w tej kolejności:

1. **Dopasowanie do poziomu przeglądarki** — ryzyko fazy rzeczywiście potrzebuje pokrycia end-to-end.
2. **Obecność funkcji** — funkcja pod testem jest już zbudowana, a aplikację można uruchomić.
3. **Brak testu** — przechodzący test E2E dla tego ryzyka jeszcze nie istnieje.

Faza kwalifikuje się do tej umiejętności tylko wtedy, gdy spełnione są wszystkie trzy warunki.

### Kontrola dopasowania do poziomu przeglądarki

Ryzyko potrzebuje E2E, gdy **przekracza kilka granic systemu** (auth, routing, API, DB) albo **istnieje wyłącznie w wyrenderowanym UI**. Jeśli ryzyko może udowodnić izolowana funkcja, kontrakt endpointu albo test integracyjny, E2E jest niewłaściwym (wolnym, kruchym) narzędziem — poprowadź je przez `/raven-test` lub `/raven-implement`.

| Godne E2E — prowadź tutaj | Niegodne E2E — przekieruj do /raven-test lub /raven-implement |
|---|---|
| Pełne przepływy użytkownika przez auth → routing → API → DB | Czyste funkcje, parsery, walidatory, obliczanie flag |
| Dane przetrwają rzeczywiste przeładowanie/nawigację strony SSR | Kontrakt statusu/kształtu/auth/bramkowania pojedynczego endpointu |
| Stan istniejący wyłącznie w wyrenderowanym, interaktywnym UI | Logika biznesowa z jasnymi wejściami/wyjściami |
| Wieloetapowe podróże, których test jednostkowy nie może odtworzyć | Wszystko, co może udowodnić izolowana funkcja lub test integracyjny |
| Ryzyka pojawiające się tylko podczas integracji rzeczywistych granic | Konfiguracja, scaffolding, podłączenie infrastruktury, dokumentacja |

### Kontrola obecności funkcji (odwrotność /raven-test)

E2E prowadzi **działającą aplikację**, więc funkcja musi już istnieć. Sprawdź `Changes Required` fazy i wykonaj ukierunkowane wyszukiwanie tras, stron, komponentów i endpointów, których dotyka przepływ, a następnie potwierdź, że aplikacja faktycznie się uruchamia.

Jeśli funkcja pod testem **nie jest jeszcze zbudowana**, ZATRZYMAJ się — przeglądarka nie ma czego obsługiwać. Wypisz ten blok, uzupełniając konkretne dowody:

```
Ryzyko E2E fazy [N] potrzebuje działającej funkcji, ale funkcja nie jest jeszcze zbudowana.

E2E działa względem prawdziwej aplikacji; implementacja musi istnieć, zanim przeglądarka będzie mogła ją obsługiwać. Tutaj znalazłem jej brak:
- [dowód trasy/strony/komponentu/endpointu]

Najpierw ją zbuduj, a potem wróć po warstwę E2E:
→ /raven-implement <change-id> phase [N]
```

Skopiuj `/raven-implement <change-id> phase [N]` do schowka, wyświetl je z `(✓ copied)` i ZATRZYMAJ się.

### Kontrola braku testu

Wykonaj szybkie wyszukiwanie istniejącej specyfikacji pokrywającej to ryzyko. Jeśli **przechodzący** test E2E dla ryzyka już istnieje, nie generuj go ponownie: uruchom go na zielono i uruchom każde celowe zepsucie, o którym twierdzi wiersz Progress tej fazy. Odwracaj tylko te wiersze, których twierdzenie właśnie udowodniono, z jednym wierszem dowodu dla każdego (specyfikacja + wynik). Wiersz, którego twierdzenie jest fałszywe — wskazuje specyfikację, która nie powinna istnieć, albo zepsucie, którego przeglądarka nie może wykryć (np. guard na poziomie strony duplikuje kontrolę middleware) — pozostaje `[ ]`: powiedz dlaczego i zaproponuj użytkownikowi poprawkę planu; nigdy nie przepisuj planu ani nie odwracaj go, aby przejść dalej. Taka faza nie może zostać ukończona: nie dostaje commitu, a ty przechodzisz do decyzji o następnej fazie z fazą oznaczoną jako **blocked on the plan fix**; podsumowanie ukończenia ją wymienia. Test pokrywający tylko **część** ryzyka (zwykle seed) go nie dyskwalifikuje. Jeśli **zbudowany** aspekt ryzyka nie ma testu, poprowadź ten aspekt i nazwij go w tytule testu oraz nagłówku pochodzenia, np. `// risk: auth-gate-roundtrip — facet: a signed-in session reaches /dashboard; the signed-out redirect is covered by seed.spec.ts`. Jeśli pozostały wyłącznie niezbudowane aspekty, użyj powyższego przekierowania dotyczącego obecności funkcji. Jeśli test istnieje, ale **nie przechodzi**, jest to zadanie debugowania, nie generowania — skieruj użytkownika do przepływu debugowania od nieprzechodzącego testu do przyczyny źródłowej, zamiast pozwalać narzędziu auto-fix po cichu przepisać asercję. (Zobacz granicę auto-heal w wytycznych E2E.)

### Jak zastosować bramkę

- Jeśli wszystkie trzy są spełnione, stwierdź to w jednym wierszu i przejdź do pętli plan → generate → review → verify.
- Jeśli ryzyko **wyraźnie nie jest na poziomie przeglądarki**, uruchom **przekierowanie** (poniżej).
- Jeśli jest **mieszane**, ale nieprzeglądarki aspekt **ma już test** (unit/integration), nazwij ten aspekt i jego test w jednym wierszu, a następnie kontynuuj z częścią na poziomie przeglądarki — bez pytania.
- Jeśli jest **mieszane lub niejednoznaczne** (np. faza częściowo będąca kontraktem endpointu, a częściowo przepływem wyrenderowanego UI), zapytaj użytkownika:

  - question: "Phase [N] mixes an isolated-function risk and a browser-level flow. How should I drive it?"
    header: "E2E gate"
    options:
    - label: "E2E the browser-level part (Recommended)"
      description: "I'll plan→generate→review→verify the cross-boundary flow and redirect the isolated-function part to /raven-test."
    - label: "Redirect whole phase to /raven-test"
      description: "Hand the entire phase off — copy the resume command to the clipboard."
    - label: "E2E the whole phase anyway"
      description: "Force browser-level coverage even for the parts a unit test would prove. Slower, more brittle."
    multiSelect: false

### Przekieruj fazę niebędącą E2E

Określ, *dlaczego* faza nie pasuje do poziomu przeglądarki (jedno lub dwa zdania, oparte na powyższej tabeli), a następnie zapytaj użytkownika:

- question: "Phase [N] isn't a good E2E fit. How do you want to handle it?"
  header: "Not E2E-worthy"
  options:
  - label: "Hand off to /raven-test"
    description: "Copy `/raven-test <change-id> phase N` to the clipboard. Start a fresh session, run it, then resume E2E on the next phase."
  - label: "Hand off to /raven-implement"
    description: "Copy `/raven-implement <change-id> phase N` to the clipboard if test-first doesn't fit either."

  Oznacz jako **(Recommended)** `/raven-test`, gdy faza dodaje testowalną logikę, oraz `/raven-implement`, gdy dotyczy dokumentacji, konfiguracji lub scaffolding.
  - label: "E2E inline here anyway"
    description: "I'll generate a browser-level test despite the cost — then continue to the next phase's gate."
  - label: "Skip — already done"
    description: "Mark the phase's Progress rows and move to the next phase."
  multiSelect: false

**Przy „Hand off”:** skopiuj wybrane polecenie wznowienia do schowka, wypisz poniższy blok i ZATRZYMAJ się — druga umiejętność odwróci wiersze Progress tej fazy i przeprowadzi własny rytuał commitu. Powiedz użytkownikowi, aby później wznowił E2E.

```
Faza [N] nie jest materiałem na poziom przeglądarki — [jednowierszowy powód].

→ /Raven-<tdd|implement> <change-id> phase [N] (✓ copied)

Rozpocznij świeżą sesję, uruchom to, a następnie wróć z:
→ /raven-test <change-id> phase [next E2E phase]
```

Wypisz wybraną umiejętność, nie zawsze `/raven-test`. Wypisz ostatnie dwa wiersze („Rozpocznij świeżą sesję…” oraz polecenie `/raven-test`) tylko wtedy, gdy pozostała późniejsza faza; gdy była to ostatnia faza, zakończ podsumowaniem ukończenia.

**Przy „Skip”:** odwróć wiersze `#### Automated` fazy z `[ ]` → `[x]` (bez SHA, ponieważ nic nie zostało zacommitowane) — tylko wiersze, których twierdzenie jest prawdziwe (zobacz powyższą zasadę pokrytego ryzyka). Wiersze `#### Manual` pozostają dla użytkownika. Następnie przejdź do kolejnej fazy. Edycję Progress i dowody przekaż koordynatorowi do publikacji w GH; nie twórz commitu dokumentującego postęp.

---

## Cykl Plan → Generate → Review → Verify

W ramach kwalifikującej się fazy pracuj ryzyko po ryzyku. Każdy krok `#### Automated` w Progress fazy (lub każde odrębne ryzyko na poziomie przeglądarki w Changes Required) to jedno okrążenie pętli. Utrzymuj pętlę zwięzłą — jedno ryzyko, jeden zrecenzowany test, zweryfikowany przed przejściem dalej.

### Budżet testów na fazę

E2E jest drogie i podatne na flaky, więc budżet jest **ścisły** — zazwyczaj **jeden test na ryzyko**, a rzadko więcej niż **1–3 na fazę**. Wybierz przepływ, który udowadnia ryzyko i wykryłby rzeczywistą regresję. Chronisz nazwane ryzyko, nie gonisz za pokryciem. Nie generuj testu na stronę ani na przycisk.

### PLAN — wybierz ryzyko i odwzoruj przepływ

1. Opisz kontrakt jednym zdaniem: **wejście** = jedno ryzyko na poziomie przeglądarki; **wyjście** = zrecenzowany test E2E, który *nie przechodzi, gdy to ryzyko się materializuje*. Jeśli ryzyko fazy nie jest konkretne, pobierz obserwowalny wynik biznesowy z `test-plan.md` lub Success Criteria fazy przed planowaniem. W samodzielnym uruchomieniu, którego ryzyka lub obserwowalnego wyniku nie rozwiązał krok 1 konfiguracji, najpierw zapytaj o nie użytkownika.
2. Wybierz ścieżkę — ten sam kontrakt w obu przypadkach:
   - **Sterowana przeglądarką** (domyślnie): aplikacja musi być najpierw uruchomiona. Uruchom build, potem uruchom preview na porcie rozwiązywanym przez konfigurację (`E2E_PORT` z pliku env, w przeciwnym razie port z `test-stack.md`) **w tle**, tymi samymi poleceniami co wpis `webServer` aplikacji. Jeśli przepływ wywołuje zewnętrzne API, które mockujesz, najpierw uruchom mock i skieruj na niego build (`references/mocking-external-apis.md`, kroki 4–5), w przeciwnym razie eksploracja wydaje prawdziwe pieniądze. Zatrzymaj wszystko przed VERIFY (krok 8). Następnie samodzielnie eksploruj działającą aplikację przez `playwright-cli` z powłoki (`open`, `snapshot`, `click <ref>`, `fill`, `press`; migawki to pliki YAML na dysku, które odczytujesz z powrotem), a następnie zaplanuj i wygeneruj specyfikację na podstawie tego, co zobaczyłeś. Wybierz narzędzie według [tool-wiring.md](../e2e-setup/references/tool-wiring.md): domyślnie CLI, MCP tylko na wyraźne polecenie lub zgodę użytkownika. W trybie MCP wykonaj te same kroki jego narzędziami. Brak CLI lub powłoki nie upoważnia do zmiany trybu. Eksploruj **migawkę dostępności** (nie screenshoty) i odwzoruj przepływ dla tego ryzyka — happy path oraz przypadek brzegowy/błędu implikowany przez ryzyko. Modeluj plan na `seed.spec.ts` — **jakość seed to jakość testu.** Zobacz `references/browser-driven-generation.md`, aby poznać polecenia i pełną dyscyplinę (najpierw skonfiguruj stronę, migawka zamiast screenshotów, scenariusze niezależne i w dowolnej kolejności).
   - **Szablon promptu** (bez działającej przeglądarki, najprościej): wypełnij `references/e2e-prompt-template.md` ryzykiem, kotwicą badawczą, scenariuszem biznesowym i granicami rzeczywistymi vs mockowanymi, a następnie zapisz specyfikację na podstawie odczytu aplikacji. Pozostaw plik szablonu bez zmian; zapisz *nowy* plik promptu dla tego konkretnego ryzyka. Użyj tego, gdy wybrane narzędzie eksploracji jest niedostępne albo przepływ jest prosty i dobrze zrozumiany. Oznacz pochodzenie speca jako analizę kodu, nie obserwację przeglądarki. Nie zastępuje to wymaganej eksploracji na żywo; jej brak pozostaje BLOCKED/NOT VERIFIED. Wynik testu pochodzi dopiero z uruchomienia runnera.
3. Rozdziel z góry granice **rzeczywiste** od **mockowanych**. **E2E ≠ zero mockowania.** Granice wewnętrzne (auth, routing, DB) pozostają rzeczywiste — tam ukrywa się ryzyko integracji. Mockuj drogie lub niedeterministyczne zewnętrzne API na warstwie sieciowej. Dla API, które aplikacja wywołuje **po stronie serwera**, `page.route()` na poziomie przeglądarki go nie przechwyci. Użyj zamiast tego lokalnego serwera mock zgodnie z `references/mocking-external-apis.md`; wymaga to zmiany produkcyjnej, którą musi zatwierdzić użytkownik.

### GENERATE — utwórz test za pomocą dźwigni

4. Wygeneruj test, stosując konwencje już zakodowane przez seed i zasady — nie powtarzaj ich w prompcie. Na ścieżce sterowanej przeglądarką **wykonaj każdy krok na żywo** i zapisz specyfikację na podstawie tego, co faktycznie ujawniło uruchomienie (odporne lokalizatory, rzeczywiste oczekiwania), a nie zgadywania. Zasadniczo wynik musi używać **lokalizatorów opartych na rolach**, być **uruchamialny niezależnie** (własne setup/action/assertion/cleanup), **czekać na stan**, a nie czas, **uwierzytelniać bez UI**, używać **unikalnych danych testowych** oraz mieć nazwę, która **wiąże go z ryzykiem** (nie `test('test 1', ...)`). Plik zasad (`references/e2e-quality-rules.md`) zawiera składnię dla poszczególnych narzędzi.
5. **Jeden test na plik**, umieszczony zgodnie z konwencją projektu (domyślnie: katalog e2e na poziomie projektu, np. `tests/e2e/<feature>.spec.ts`). Nazwa pliku to przyjazna fs nazwa scenariusza; `describe` odpowiada elementowi planu/ryzyka najwyższego poziomu; umieść tekst każdego kroku planu jako komentarz przed akcjami, które go realizują, i zachowaj nagłówek pochodzenia łączący specyfikację z jej ryzykiem oraz seed.

### REVIEW — pięć antywzorców, ponowne promptowanie po nazwie

6. Nigdy nie ufaj wygenerowanemu testowi E2E na pierwszy rzut oka. Przejrzyj go względem pięciu antywzorców E2E agentów w `references/e2e-anti-patterns.md`: Naive assertion, Brittle selector, Shared state, Hardcoded wait, No cleanup. „No cleanup” obejmuje cleanup, który istnieje, ale może zawieść po cichu: każde wywołanie cleanup musi asertywnie sprawdzać swój wynik, a wywołania API z `page.request` muszą przejść kontrolę origin/CSRF aplikacji (zobacz antywzorzec).
7. Dla każdego znalezionego antywzorca **ponownie zapromptuj po nazwie** — nigdy „napraw ten test”. Nazwij konkretny antywzorzec, wyjaśnij, *dlaczego* nie chroni ryzyka (albo dlaczego tworzy fałszywe błędy), i podaj **wzorzec docelowy**. Trzy elementy każdego ponownego promptu: co jest nie tak, dlaczego nie chroni ryzyka, co to zastępuje. Zobacz dyscyplinę ponownego promptowania w `references/e2e-anti-patterns.md`.

### VERIFY — zielony, a następnie powiązany z ryzykiem

8. **Zatrzymaj serwery, następnie uruchom tylko tę specyfikację.** Zatrzymaj każdy serwer uruchomiony na potrzeby eksploracji oraz każdego demona preview, którego pozostawił. Potwierdź, że port jest wolny (`lsof -nP -iTCP:<port> -sTCP:LISTEN` lub `netstat -ano | findstr :<port>` nic nie wypisuje), aby `webServer` konfiguracji zbudował i uruchomił bieżący kod. Przy `reuseExistingServer` nadal działający serwer jest po cichu używany ponownie: jego build poprzedza celowe zepsucie, więc zepsucie nigdy nie dociera do aplikacji, a test pozostaje **fałszywie zielony**. Uruchom specyfikację poleceniem projektu dla pojedynczej specyfikacji i potwierdź, że przechodzi. Krótko pokaż użytkownikowi zielony wynik.
9. **Pytanie kontrolne:** *czy ten test nie przeszedłby, gdyby ryzyko z `test-plan.md` stało się prawdą?* Jeśli nie, asercja jest dekoracyjna — wróć do GENERATE/REVIEW. Aby to skonkretyzować, wykonaj **celowe zepsucie**: tymczasowo odwróć lub osłab zachowanie produkcyjne, na które celuje ryzyko (lub cel kluczowej asercji testu), uruchom ponownie, gdy port wciąż jest wolny (aby `webServer` przebudował aplikację z zepsuciem), i potwierdź, że test staje się czerwony na asercji ryzyka (czerwony wynik z timeoutu, logowania albo wyścigu hydration niczego nie dowodzi — uruchom ponownie). Preferuj zepsucie pozostawiające nietkniętą ścieżkę obsługiwaną przez cleanup; w każdym razie poniższa kontrola pozostałości działa także po tym czerwonym uruchomieniu. Jeśli pozostaje zielony po zepsuciu rzeczy, którą ma chronić, asercja nie chroni niczego — napraw ją przed przejściem dalej. **Natychmiast cofnij celowe zepsucie**; nigdy go nie commituj.
   Następnie sprawdź cleanup w ten sam sposób — po zielonym uruchomieniu **oraz** po uruchomieniu z celowym zepsuciem (czerwone uruchomienie często zatrzymuje się w połowie przepływu i pozostawia pośrednie rekordy, np. szkice niezapisanej sesji): wyszukaj dane własne testu w każdej tabeli, do której przepływ zapisuje (sesje logowania tworzone przez projekt setup przy każdym uruchomieniu są oczekiwane, nie są pozostałością) (to samo wyszukiwanie, którego używa cleanup, UI aplikacji lub baza danych) i potwierdź, że **nic nie pozostało**. Unikalne identyfikatory ukrywają uszkodzony cleanup — kolejne uruchomienie nie koliduje, dane tylko się gromadzą. Jeśli cokolwiek pozostaje, cleanup jest uszkodzony: napraw go (REVIEW, „No cleanup”) i uruchom ponownie. Aby znaleźć dane, test potrzebuje możliwego do odnalezienia tokenu: zapisz go w teście (`test.info().annotations.push({ type: 'test-data', description: token })` pokazuje go w raporcie), zamiast przeszukiwać logi serwera.
10. **Oznacz krok jako ukończony.** Odwróć dokładnie wiersz tego kroku w `## Progress`: `- [ ] N.M <title>` → `- [x] N.M <title>` (bez SHA jeszcze — SHA trafia na końcu fazy). Następnie wróć do PLAN dla następnego ryzyka.

Nigdy nie używaj `test.skip()` / `test.fixme()`, aby „przejść” fazę — pominięty test jest niewidoczny. Test, którego nie da się doprowadzić do przechodzenia względem prawdziwej aplikacji, jest sygnałem do zbadania (funkcji, przepływu lub flaky), a nie do wyciszenia.

Powtarzaj PLAN→GENERATE→REVIEW→VERIFY, aż każdy krok `#### Automated` w fazie będzie `[x]` i zostaną spełnione kryteria sukcesu fazy.

W uruchomieniu **samodzielnym** nie ma fazy ani `## Progress`: po tym, jak VERIFY potwierdzi zielony wynik oraz celowe zepsucie, uruchom lint/format projektu dla każdego zmodyfikowanego pliku (serwery mock i helpery uruchamiają reguły, których specyfikacje nie uruchamiają), następnie **zatrzymaj się** — zgłoś plik specyfikacji i ryzyko, które chroni, wymień każdy plik zmieniony poza katalogiem testów (zmiany produkcyjne, konfiguracja) do przeglądu przez użytkownika i zaproponuj commit (`test: <risk> e2e`, staged by path), bez wykonywania go bez pytania. Pomiń poniższy rytuał ukończenia fazy.

---

## Ukończenie fazy (tylko sterowane planem)

Gdy wszystkie wiersze `#### Automated` w `### Phase N:` mają `[x]`, wykonaj rytuał końca fazy (odzwierciedla `/raven-implement` i `/raven-test` — jeden commit Conventional-Commits na fazę, a następnie zapisanie jego krótkiego SHA z powrotem w wierszach, które odwrócono).

> **Twardy niezmiennik — commituj tylko na zielono.** Nigdy nie proponuj, nie stage'uj ani nie twórz commitu, gdy dowolny test w zakresie jest czerwony, pominięty dla pozorowania przejścia lub gdy celowe zepsucie nadal jest w drzewie. Commit jest oferowany **dopiero po tym, jak nowy test/testy E2E przejdą względem działającej aplikacji** i po cofnięciu wszystkich edycji celowego zepsucia. Czerwień celowego zepsucia jest przejściowym punktem kontrolnym, który pokazujesz użytkownikowi, nigdy granicą commitu.

Utrzymuj zestaw własnych zmienionych plików kodu, testów i konfiguracji repo. Wyklucz kopie planu, researchu, raportów i change.md z artifact_dir. Zestaw resetuje się na granicy fazy; Progress i dowody publikuje koordynator w GH.

1. **Uruchom specyfikację/specyfikacje E2E fazy** względem działającej aplikacji i potwierdź zielony wynik. (Pełne przejście E2E działa w CI, a nie przy każdej edycji — lokalnie potwierdzasz specyfikacje dodane przez tę fazę). Napraw wszelkie problemy przed commitem. Uruchom również lint/format projektu dla zmodyfikowanych plików — serwer mock lub helper często uruchamia reguły, których specyfikacje nie uruchamiają (globalne Node w `.mjs`), a hook pre-commit odrzuciłby commit.

2. **Bramka ręcznego potwierdzenia.** Jeśli plan wymaga kontroli wykonywanej przez użytkownika na tym etapie, przedstaw jej kroki i poczekaj na wynik. Nie traktuj kontroli wykonanej przez agenta jako wymagającej ponownego potwierdzenia. Gdy takich kontroli brak, kontynuuj zgodnie z trybem nadrzędnego skilla; auto nie pyta o każdą fazę ani komunikat commitu. Poniższy komunikat stosuj wyłącznie dla rzeczywiście oczekującej kontroli człowieka.

```
Phase [N] Complete (E2E) — Ready for Manual Verification

Automated verification passed:
- [E2E specs now green: list them]
- [deliberate-break check: which behavior you inverted and confirmed the test caught]

Please perform the manual verification steps from the plan:
- [manual items for this phase]

Let me know when manual testing is complete so I can commit.
```

   W **ostatniej fazie** zbierz także wszystkie wciąż oczekujące wiersze `#### Manual` z wcześniejszych faz (informacyjnie; bramka nadal tylko wstrzymuje, nie blokuje twardo).

3. **Wykryj niepowiązane brudne ścieżki.** Uruchom `git status --porcelain`; przetnij z ścieżkami **poza** zestawem zmodyfikowanych plików. Jeśli jakieś istnieją, przedstaw je i zapytaj użytkownika, czy commitować tylko zaplanowany zestaw (Recommended), zestage'ować wszystkie, czy przerwać. Jeśli nie ma żadnych, pomiń.

4. **Stage'uj jawnie po ścieżce** — `git add` każdy plik w zestawie zmodyfikowanych plików po nazwie. Nigdy `git add -A` / `git add .`.

5. **Kontrola pustego diffu.** `git diff --cached --quiet`; jeśli kod wyjścia to 0, wypisz, że faza nie miała diffu (wiersze pozostają bez SHA), ustaw `SHA=""` i przejdź do kroku 8.

6. **Zaproponuj komunikat Conventional-Commits** i poproś użytkownika o jego zatwierdzenie (zaakceptuj zgodnie z propozycją (Recommended) / edytuj subject / nadpisz). Subject: `test(<change-id>): <phase title> (p<N>)`. Zachowaj subject w granicy 72 znaków — skróć tytuł fazy, jeśli potrzeba. Wspomnij w body o charakterze E2E/poziomu przeglądarki i chronionym ryzyku. Uwzględnij wiersz `Refs:`, jeśli rozmowa zawiera prawdziwe referencje Jira/Linear/GitHub (nigdy nie wymyślaj ich z change-id ani brancha).

7. **Commituj** pojedynczym `git commit` z body heredoc, zgodnie z globalnym protokołem komunikatu commitu: zatwierdzony subject, następnie krótkie body wymieniające dodane specyfikacje + ryzyko chronione przez każdą z nich (oraz wiersz `Refs:`, gdy ma zastosowanie). Nigdy nie przekazuj flag `--no-verify` / `--amend` / omijających podpisywanie. Jeśli hook pre-commit zawiedzie, napraw przyczynę i wykonaj NOWY commit.

8. **Pobierz i zapisz z powrotem SHA.** `git rev-parse --short HEAD` → `SHA`. Dla każdego wiersza Progress odwróconego w tej fazie edytuj `- [x] N.M <title>` → `- [x] N.M <title> — <SHA>` .

9. **Zaktualizuj `change.md`**: `updated: <today>`; zachowaj `status: implementing` aż do ostatniej fazy.

10. **Zresetuj zestaw zmodyfikowanych plików** przed następną fazą.

### Decyzja o następnej fazie

Zapytaj użytkownika:

- question: "Phase [N] [complete | blocked on a plan fix] (E2E). How to proceed?"
  header: "Next phase"
  options:
  - label: "Continue to Phase [N+1] (Recommended)"
    description: "Stay in this context; run the E2E gate for the next phase and proceed."
  - label: "Start a fresh session first"
    description: "Copy the resume command to the clipboard. Start a fresh session for Phase [N+1]."
  - label: "Review this phase first"
    description: "Run /raven-implement-review to verify the implementation against the plan before continuing."
  multiSelect: false

**Continue:** przeczytaj następną fazę, oznacz ją jako w toku w checkliście, uruchom bramkę E2E, kontynuuj. Nie trzeba ponownie czytać całego planu.

**Review:** uruchom `/raven-implement-review @<path-to-plan> phase [N]`, następnie ponownie przedstaw decyzję kontynuacja/świeża sesja (bez opcji review).

Gdy Phase [N] była ostatnią fazą, pomiń to pytanie i przejdź do podsumowania ukończenia. Jeśli wiersze nadal są otwarte (faza zablokowana przez poprawkę planu, faza przekazana dalej), wypisz zamiast świętowania poniższe częściowe podsumowanie.

**Fresh session:** skopiuj `/raven-test <change-id> phase [N+1]` do schowka (zgodnie z konwencją schowka) i wyświetl jako `→ /raven-test <change-id> phase [N+1] (✓ copied)`.

Jeśli polecono uruchomić wiele faz kolejno, pomiń to pytanie między fazami. Odwróć **ręczny** wiersz (i nadaj mu SHA fazy) dopiero po tym, jak użytkownik potwierdzi ten element; w przeciwnym razie pozostaw go dla niego.

---

## Śledzenie stanu i zakończenie

Kanoniczny Progress i checkpoint znajdują się w taskach/change GH. Roboczy plan w artifact_dir odzwierciedla te dane. Po fazie zwróć koordynatorowi zmiany Progress, SHA, polecenia i wyniki; koordynator publikuje je i odczytuje rezultat. Nie commituj plan.md, change.md ani innych kopii artefaktów, także w epilogu lub osobnym commicie postępu.

Zakończenie dotyczy wyłącznie zleconych faz testowych, nie wszystkich faz planu produktu. Raportuj wykonane, oczekujące i zablokowane kontrole oraz EXPECTED_RED, jeśli dopuszcza go before-change. Nie odhaczaj odbioru człowieka. Zwróć wynik nadrzędnemu skillowi: manual kończy się raportem do osobnego raven-test-review, auto przechodzi do świeżego niezależnego reviewera i ograniczonej pętli poprawek testów. Wewnętrzny REVIEW w pętli generowania testu nie zastępuje niezależnego review końcowego. Nie uruchamiaj review implementacji, PR ani merge automatycznie.

## Wytyczne E2E

Zasady kierujące każdym testem tutaj — referencje zawierają składnię i pełne uzasadnienie:

- **Obserwowalny rezultat użytkownika** przez rzeczywiste granice, nie wewnętrzne wywołanie — oraz **nie przechodzi, gdy jego ryzyko się materializuje**, co potwierdza kontrola celowego zepsucia, nie założenie.
- **Lokalizatory oparte na rolach**, **samowystarczalne i izolowane** (własne setup/action/assertion/cleanup, unikalne dane, auth bez UI, bezpieczne przy równoległych uruchomieniach w losowej kolejności) oraz **oczekiwanie na stan, nigdy na czas**. Pięć sposobów, na które agenci to naruszają, opisano w `references/e2e-anti-patterns.md`.
- **Chroń nazwane ryzyko, nie powierzchnię** — bez testu na stronę/przycisk, bez nadmiernego mockowania granic wewnętrznych (mock auth + DB i test nie sprawdza niczego, co może zepsuć się w integracji), bez asercji pikseli dla ryzyk funkcjonalnych (używaj deterministycznych narzędzi wizualnych dla tych przypadków).

**Rzeczywiste vs mockowane** to podstawowa wartość testu: granice wewnętrzne (auth, routing, DB) pozostają rzeczywiste — tam ukrywa się ryzyko integracji; mockuj tylko drogie lub niedeterministyczne zewnętrzne API na warstwie sieciowej.

**Vision** (screenshoty) jest dodatkiem dla ryzyk wyłącznie wizualnych (layout, z-index, animacja, canvas), nie domyślną opcją — migawki DOM weryfikują funkcję. **Narzędzia auto-healing** pomagają przy dryfie selektorów/timingu (kieruj ich wynik przez przegląd PR, nigdy nie commituj automatycznie), ale nigdy nie mogą „naprawiać” *zmienionego zachowania biznesowego* — maskuje to regresję, którą test ma wykryć. Oba zagadnienia opisano szczegółowo w `references/browser-driven-generation.md`; nieprzechodzący test E2E to zadanie debugowania, nie generowania ani healingu.

### Umieszczenie pliku

Postępuj zgodnie z konwencją odkrytą w Setup. Domyślnie, jeśli żadna nie istnieje: katalog e2e na poziomie projektu, `tests/e2e/<feature>.spec.ts`, jeden test na plik.

### Jeśli utkniesz

Używaj sub-agentów oszczędnie: do szybkiego wyszukiwania plików/wzorców albo wieloetapowej analizy nieznanego obszaru deleguj do sub-agenta, jeśli twój asystent programistyczny AI go ma, w przeciwnym razie wykonaj to inline. Najpierw upewnij się, że przeczytałeś odpowiedni kod oraz faktyczne drzewo dostępności działającej aplikacji; kod może ewoluować od czasu napisania planu.

## Inne stosy

Seed, zasady i szablon promptu są dostarczane dostrojone do Playwright, a narzędzie eksploracji wybiera wspólny kontrakt [tool-wiring.md](../e2e-setup/references/tool-wiring.md), zgodnie z raven-browser. W Cypress, WebdriverIO lub Selenium zakoduj idiomy twojego narzędzia (jego odpowiednik `getByRole`, mechanizm wait-for-state, izolację danych) we własnym wariancie tych dźwigni i używaj jego własnego runnera. Zasady są przenośne; składnia nie. Tabela mapowania w `references/e2e-quality-rules.md` (Other stacks) zawiera idiom Cypress i WebdriverIO / Selenium dla każdej zasady.

## Referencje

- `references/e2e-quality-rules.md` — zasady E2E + zasady nadrzędne + mapowanie dla nie-Playwright.
- `references/e2e-anti-patterns.md` — pięć antywzorców + dyscyplina ponownego promptowania.
- `references/seed-test-pattern.md` — wzorzec `seed.spec.ts` + cztery wzorce (sam seed jest pisany przez `/raven-test`).
- `references/e2e-prompt-template.md` — gotowy do wklejenia prompt generowania + działający przykład.
- `references/mocking-external-apis.md` — mockowanie zewnętrznego API wywoływanego przez aplikację po stronie serwera: base URL możliwy do nadpisania przez env, lokalny serwer mock jako dodatkowy wpis `webServer`, uwagi dotyczące stosów.
- `references/browser-driven-generation.md` — eksplorowanie aplikacji za pomocą `playwright-cli` w celu planowania i generowania jednej specyfikacji na ryzyko (przepływ pracy z drzewem dostępności, migawka zamiast screenshotów, jeden test na plik, pisanie na podstawie rzeczywistego wykonania, granica auto-heal).
