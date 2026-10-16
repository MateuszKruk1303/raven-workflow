---
name: raven-workflow
description: Przewodnik i router aktualnego workflow Raven. Ustal etap projektu lub change z GitHuba, wybierz właściwy skill i kolejność manual/auto. Użyj przy rozpoczęciu lub wznowieniu pracy Raven, pytaniu o następny krok lub pulę skilli; nie uruchamia całego cyklu automatycznie.
---

# Raven Workflow

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](references/agent-policy.md). Sam routing/status nie uruchamia agentów.

To kanoniczna mapa kolejności i odpowiedzialności skilli Raven. Stan pracy pochodzi z GitHuba, nie z pamięci rozmowy. Szczegółowe wykonanie należy do wybranego skilla: przed użyciem przeczytaj jego SKILL.md i wymagane referencje. Nie ładuj wszystkich skilli naraz. Jawne zlecenie konkretnego etapu ma pierwszeństwo przed proponowaniem pełnej sekwencji.

## Rozpoczęcie nowej sesji

1. Odczytaj instrukcje bieżącego repo i ustal intencję: pytanie/status, przygotowanie, planowanie, wykonanie czy poprawki. Dyskusja i status nie upoważniają do zapisów ani automatycznego rozpoczęcia implementacji.
2. Jeśli potrzebny jest stan change, przeczytaj [kontrakt GitHub](../raven-auto-plan/references/github-contract.md), github.json, rzeczywiste issue/taski, snapshoty, raporty i decyzje. Odczytaj branch/HEAD przy pracy z kodem. Brak lokalnego plan.md, markerów w PRD lub historii rozmowy nie oznacza braku wykonanej pracy w GH.
3. Jawne issue/Raven ID identyfikuje zakres. Przy prośbie o następny change użyj Raven Order, zależności i rzeczywistej gotowości; nie utożsamiaj roadmapy z zatwierdzonym planem. Brak dostępu do GH to brak danych, nie pusta kolejka.
4. Ustal ostatni ukończony etap dla aktualnej wersji planu/kodu. Wznów checkpoint zamiast powtarzać pracę. Błąd publikacji wymaga dokończenia zapisu, nie ponownej implementacji.
5. Podaj krótko: stan, istotna luka i następny skill. Jeśli użytkownik zlecił wykonanie tego kroku, przejdź do niego. Sam router nie wybiera auto ani nie przeskakuje decyzji użytkownika. Przy braku wyboru manual/auto zaproponuj odpowiednią opcję i ustal tryb przed zależnym wykonaniem.

## Przygotowanie projektu

Kolejność orientacyjna dla nowego produktu; nie odtwarzaj istniejącego setupu:

| Skill | Rezultat / moment |
| --- | --- |
| [raven-shape](../raven-shape/SKILL.md) | Dopracowanie problemu, produktu i zakresu |
| [raven-prd](../raven-prd/SKILL.md) | Wymagania produktu |
| [raven-github-setup](../raven-github-setup/SKILL.md) | Repo/Project, pola i lokalne powiązanie |
| [raven-roadmap](../raven-roadmap/SKILL.md) | Changes, kolejność i zależności w GH |
| [raven-architecture](../raven-architecture/SKILL.md) | Interaktywny obraz architektury w context/foundation/architecture.md na podstawie wymagań, kodu i dostępnej roadmapy; decyzje, opcje i uzasadnienia |
| [raven-init-stack](../raven-init-stack/SKILL.md) | Szkielet wybranego stacku Raven |
| [raven-medusa-ecommerce-init](../raven-medusa-ecommerce-init/SKILL.md) | Alternatywa setupu dla projektu Medusa, nie dodatkowy obowiązkowy krok |
| [raven-agents-md](../raven-agents-md/SKILL.md) | Instrukcje repo na podstawie rzeczywistego projektu |
| [raven-test-plan](../raven-test-plan/SKILL.md) | Globalna strategia testów po przygotowaniu stacku, najlepiej przed planowaniem pierwszego ficzera |
| [raven-hooks](../raven-hooks/SKILL.md) | GitHub Actions dopasowane do istniejących komend i runnerów, wykonywane po PR |

raven-test-plan nie jest planem pojedynczego ficzera. Pierwsze uruchomienie tworzy strategię, kolejne wznawiają rollout; --status odczytuje stan, --refresh przygotowuje aktualizację. W młodym projekcie źródłami ryzyk są głównie PRD i wywiad, nie nieistniejąca historia kodu. Brak strategii globalnej nie blokuje planowania dobrze opisanego change.

W istniejącym projekcie zachowaj stack i dokumentację, uzupełniaj konkretne braki. Lokalny Git i ustalona baza są potrzebne przed implementacją z commitami/review, lecz nie blokują analizy planistycznej. Nie inicjalizuj ani nie publikuj repo tylko dlatego, że uruchomiono router.

## Wejście brownfield

Przy pierwszym wprowadzeniu Raven do istniejącego projektu pokaż jawnie kolejność przygotowania:

1. [raven-github-setup](../raven-github-setup/SKILL.md): zweryfikuj repo i przygotuj lub uzupełnij prywatny GitHub Project (board), pola/etykiety i powiązanie github.json. Wykorzystaj istniejące zasoby; nie zakładaj, że samo repo oznacza skonfigurowany board. Brak dostępu nie oznacza braku zasobu.
2. [raven-repo-map](../raven-repo-map/SKILL.md): zbuduj lub odśwież mapę funkcji/modułów, zależności, historii zmian i ryzyk; opublikuj wersjonowany wynik w powiązanym GH. Zakres mapy dopasuj do projektu lub wskazanego podsystemu.
3. Uzupełnij rzeczywiste braki instrukcji (raven-agents-md lub raven-md), strategii (raven-test-plan) i CI (raven-hooks). Nie przebudowuj zastanych narzędzi bez potrzeby.
4. Wybierz change i potrzebne analizy z tabeli poniżej, a następnie przejdź do planowania.

To ścieżka onboardingu, nie rytuał dla każdego ticketa. Przy istniejącym powiązaniu i aktualnej mapie wykorzystaj je ponownie; odśwież tylko nieaktualne elementy. Jawnie zlecony mały task w znanym obszarze nie wymaga pełnego skanu repo. Router nadal jedynie wskazuje kolejność: samo pytanie o proces nie upoważnia do tworzenia boarda ani publikowania mapy. Poniższe analizy wybieraj według konkretnych niewiadomych.

| Potrzeba | Skill | Wynik |
| --- | --- | --- |
| Nieznane repo lub duża powierzchnia zmian | [raven-repo-map](../raven-repo-map/SKILL.md) | Mapa funkcji, zależności i ryzyk w GH |
| Objaw połączony z niepotwierdzoną przyczyną | [raven-frame](../raven-frame/SKILL.md) | Zweryfikowane sformułowanie problemu w change |
| Zrozumienie konkretnej funkcji | [raven-research](../raven-research/SKILL.md) | Deep Focus oparty na mapie i kodzie |
| Niejednoznaczny język i granice domen | [raven-domain-distillation](../raven-domain-distillation/SKILL.md) | Niezależne porównanie dokumentów z kodem, słownik i rozbieżności |
| Przeładowane lub niejasne instrukcje | [raven-rule-review](../raven-rule-review/SKILL.md) | Ocena instrukcji i konkretne propozycje |
| Wybrane zadania z Jira | [raven-jira-roadmap](../raven-jira-roadmap/SKILL.md) | Roadmapa agenta w GH, bez zapisów do Jira |

Po przygotowaniu projektu: wybór change → ewentualne frame/research/domena → wspólny cykl plan/review/implementacja/odbiór/testy/PR. Dla jasno opisanego małego taska można od razu planować. Nie odtwarzaj greenfield shape/PRD/stacku dla samego wejścia do istniejącej aplikacji. raven-agents-md oraz raven-test-plan/raven-hooks uzupełniają rzeczywiste braki, nie wymagają przebudowy setupu.

Przed refaktorem bez ochrony zachowania zaplanuj i wykonaj testy charakteryzacyjne przez raven-test lub raven-auto-test w trybie before-change. To dodatkowa bramka przed zmianą kodu, nie zastępstwo końcowej weryfikacji po zmianie. Przy bugfixie test przed zmianą może prawidłowo wykazać oczekiwany RED. Szczegóły w [kontrakcie testów przed zmianą](../raven-test/references/before-change.md).

W wariancie Jira wymagania i biznesowy status pozostają w Jira, a wersjonowane plany/raporty/dowody w prywatnym repo artefaktów GH. Repo kodu może być inne. Wymaga to jawnego powiązania i konfiguracji finalizacji po merge; prywatność samego Project nie wystarcza.

## Architektura przekrojowa i research przed planem

`raven-architecture` prowadzi użytkownika przez decyzje dotyczące całego produktu i zapisuje architecture.md: odpowiedzialności, dane i pliki, integracje, środowiska oraz utrzymanie. W greenfield warto go wykonać po ustaleniu wymagań i dostępnej roadmapy; w brownfield można uzupełnić tylko potrzebny obszar. Nie jest obowiązkowym projektem przebudowy ani warunkiem każdego małego taska. Planowanie i research czytają istniejący dokument oraz respektują statusy decyzji.

Przy niepewnej wykonalności lub nieznanym fragmencie kodu użytkownik może rozpocząć change przez `raven-research`, a dopiero potem wywołać `raven-plan` albo `raven-auto-plan`. Research zapewnia tożsamość nowej zleconej zmiany lub wykorzystuje istniejącą, ustawia Backlog → Preparing i publikuje dowody, opcje, ryzyka i pytania w issue. Nie tworzy planu/tasków implementacyjnych ani Ready. Plan przejmuje to samo issue i wersjonowane raporty, weryfikując jedynie zmienione lub sprzeczne ustalenia. Przy jasno opisanej zmianie można od razu planować; czytanie kodu w planowaniu nie wymaga osobnego researchu.

## Powtarzalny cykl change

| Etap | Manual | Auto |
| --- | --- | --- |
| Research, gdy zlecony | [raven-research](../raven-research/SKILL.md) — rozpoczęcie lub badanie tego samego change | Ten sam osobno zlecany skill |
| Plan | [raven-plan](../raven-plan/SKILL.md) | [raven-auto-plan](../raven-auto-plan/SKILL.md) |
| Review planu | Osobno [raven-plan-review](../raven-plan-review/SKILL.md) | Wbudowane niezależne review |
| Decyzja o planie | Użytkownik akceptuje lub zleca poprawki | Użytkownik akceptuje lub zleca poprawki |
| Implementacja | [raven-implement](../raven-implement/SKILL.md) | [raven-auto-implement](../raven-auto-implement/SKILL.md) |
| Review implementacji | Osobno [raven-implement-review](../raven-implement-review/SKILL.md) | Wbudowany świeży reviewer po pozytywnym sprawdzeniu wymagań przez testera |
| Osobisty odbiór | Użytkownik sprawdza, zgłasza problemy i zleca poprawki | Tak samo |
| Trwałe testy | [raven-test](../raven-test/SKILL.md) | [raven-auto-test](../raven-auto-test/SKILL.md) |
| Review testów | Osobno [raven-test-review](../raven-test-review/SKILL.md) | Wbudowane niezależne review i poprawki wad testów |
| Publikacja | [raven-pr](../raven-pr/SKILL.md) na zlecenie | Ten sam skill na zlecenie |
| Finalizacja | Checki CI po PR → merge użytkownika → Done | Tak samo |

Można mieszać tryby między etapami na tym samym change. Plan, taski, raporty i decyzje mają wspólne formaty. Auto nie oznacza automatycznej zgody na kolejne etapy, zmianę wymagań lub merge.

W auto-implement autor i niezależny tester naprawiają potwierdzone niespełnienie wymagań w ograniczonej pętli. Dopiero po PASS wchodzi świeży reviewer techniczny z raportem i instrukcją ręcznego sprawdzenia. Uwagi techniczne rozstrzyga użytkownik. Bieżący tester nie generuje suite E2E.

Po odbiorze obowiązuje etap trwałych testów i ich review: manualna para lub auto-test. Dobór warstw wynika z wymagań i ryzyka; nie wymagaj unit/integration/E2E dla każdej zmiany. Reviewer testów dostaje te same wersje surowych źródeł co autor, bez jego transkryptu; stosuje [wspólny kontrakt niezależności i pragmatycznej oceny](../raven-test/references/test-review.md). Błąd produktu wykryty testami wraca do użytkownika i implementacji, nie jest ukrywany zmianą asercji.

Wywołanie raven-pr jest decyzją publikacji: skill grupuje niezacommitowane zmiany ticketa w logiczne commity, wykonuje commit i zwykły push oraz tworzy lub aktualizuje PR z aktualnym opisem i zachowaną historią poprawek. Zachowuje istniejące commity i obce zmiany. Nie uruchamia osobnych testów, nie audytuje kompletności wcześniejszych etapów ani CI; nie omija jednak hooków commit/push. Obowiązkowa kolejność jest zasadą workflow, nie dodatkową kontrolą w skillu PR. GitHub Actions i reguły merge muszą istnieć w konfiguracji repo; nie zakładaj ich działania z samej obecności skilli. Done dopiero po merge, a automatyczne przestawienie zależy od konfiguracji GH.

## Narzędzia używane według potrzeby

- [raven-create-skill](../raven-create-skill/SKILL.md): rozwijanie samej rodziny Raven — rozmowa, tworzenie/zmiana skilla, integracja i niezależne review. Działa w repo skilli; nie jest etapem dostarczania funkcji aplikacji.

- [raven-manual-qa](../raven-manual-qa/SKILL.md): osobno zlecane eksploracyjne QA w przeglądarce na podstawie issue; wymagania, edge cases i realistyczne próby nadużycia. Wskazówki programisty są opcjonalne, dane tester wyszukuje także w plikach projektu. Publikuje plan scenariuszy z ticketa i implementacji, uzupełnia go o wyniki wykonania, a w osobnym komentarzu testera raportuje wyłącznie problemy z Expected/Actual i reprodukcją albo krótki sukces; niepełne QA oznacza jawne ograniczenie. Nie zastępuje odbioru użytkownika ani trwałych testów i nie naprawia kodu.

- [raven-research](../raven-research/SKILL.md): osobno zlecane rozpoczęcie lub badanie change, wynik w GH wykorzystywany przez późniejszy plan; nie obowiązkowy krok każdego planowania.
- [raven-lesson](../raven-lesson/SKILL.md): osobno zlecana lekcja w lokalnym lessons.md, możliwe źródło późniejszej aktualizacji AGENTS.md.
- [raven-browser](../raven-browser/SKILL.md): dostęp do przeglądarki przy sprawdzaniu działającej aplikacji, nie zamiennik trwałych testów.
- [raven-md](../raven-md/SKILL.md): alternatywne tworzenie/aktualizacja instrukcji AGENTS.md; nie uruchamiaj rutynowo razem z raven-agents-md.
- Skille domenowe projektu obowiązują przy właściwej pracy, ale nie są kolejnymi etapami workflow.

## Historyczne artefakty

Skille dawnego Raven Pilot oraz raven-seed zostały wycofane. Istniejące dokumenty i archiwa projektów pozostają bez zmian. Na zlecenie kontynuacji starego pilota najpierw ustal mapowanie jego zakresu, decyzji i dowodów na aktualny workflow GH; nie przenoś ani nie usuwaj historii automatycznie.
