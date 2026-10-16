---
name: raven-auto-plan
description: Przygotuj lub popraw plan change w GitHubie przez zawsze wykonywany cykl utworzenia tożsamości zmiany, planowania i niezależnego review. Publikuje plan i taski w GH, czeka na decyzję użytkownika; nie uruchamia researchu ani implementacji automatycznie.
---

# Raven Auto Plan

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Procedury własne

Procedury do odczytu przez wykonawcę właściwej roli (E2E tylko gdy wybrano tę warstwę): [new](references/procedures/new/procedure.md); [plan](../raven-plan/references/procedures/plan/procedure.md); [plan-review](../raven-plan-review/references/procedures/plan-review/procedure.md). Ich referencje i helpery znajdują się obok. To kompletna implementacja etapu; nie odczytuj innej instalacji skilli. Przekazując zadanie agentowi, przekaż ścieżki procedur jego roli oraz kontrakt GH; koordynator nie musi ładować instrukcji wykonawczych innych ról. Poniższe nazwy etapów oznaczają te procedury; nie wywołuj rekurencyjnie bieżącego skilla.


Jeden skill prowadzi cały cykl **tożsamość zmiany → plan → niezależne review → decyzja użytkownika**. Korzystaj z lokalnych procedur tożsamości zmiany, planowania i review, zamiast zastępować je skróconą checklistą. Wszystkie trzy etapy są obowiązkowe; przy wznowieniu uznaj już ukończone etapy tej samej wersji. GitHub przechowuje kontekst, plan, taski, raporty i decyzje.

## Wejście i kontrakt

Najpierw przeczytaj [wspólny kontrakt GitHub](references/github-contract.md). Obowiązuje także przy poprawkach i wznowieniu. Planista czyta procedurę planowania, szablon planu, Progress i reguły wywiadu; reviewer procedurę plan-review. Koordynator czyta procedurę new tylko przy tworzeniu tożsamości. Instrukcje Raven nadpisują wyłącznie transport, orkiestrację oraz opisane poniżej przejścia wymagające decyzji; zachowaj pozostałe wymagania merytoryczne Raven.

Wejście: URL/numer issue, Raven ID, „następny change” lub kontynuacja bieżącego planowania. Rozróżnij utworzenie planu, poprawki, decyzję po review, wznowienie i status tylko do odczytu. Ustal docelowy change przed publikacją. Nie uruchamiaj roadmapy od nowa.

## 1. Tożsamość zmiany — odpowiednik new

Przeczytaj cały change, jego taski, istotne komentarze, dokumentację produktu i lokalne lessons. Istniejące issue z roadmapy już stanowi tożsamość zmiany: nie twórz jego kopii ani nowego issue, tylko zapewnij trwałe ID, zakres i odsyłacze do kontekstu. Jeśli użytkownik jawnie zleca nową zmianę, zainicjuj ją zgodnie z istniejącym kontraktem Raven w GH. Sprawdź duplikaty również w zamkniętych issues; nigdy nie nadpisuj ukończonej pracy.

Zachowaj cel `raven-plan`: jedna tożsamość łączy wymaganie, plan, wykonanie i review. Walidacja lokalnego kebab-case dotyczy jedynie roboczego slug adaptera, nie wymusza zmiany Raven ID typu C-03. Nie wymagaj `context/changes/`, nie zapisuj lokalnego kanonicznego change.md i nie kończ etapu sugestią ręcznego uruchomienia kolejnego skilla. Ustaw Preparing, jeśli stan i zakres na to pozwalają.

## 2. Planowanie — raven-plan

Utwórz świeżego planistę bez dziedziczenia transkryptu (`fork_turns="none"` lub odpowiednik). To jawnie delegowany workflow. Przekaż absolutne ścieżki instrukcji raven-plan, niniejszego skilla i kontraktu GH, repo_root, artifact_dir, pełne wymagania i materiały pobrane z GH, lessons, znane decyzje oraz zadanie przygotowania całego planu. Planista pracuje według wywiadu, analizy, struktury i kryteriów raven-plan. Komunikuje pytania przez koordynatora; nie podejmuje decyzji produktowych za użytkownika i nie zapisuje GH.

Uzgodnienia o zachowaniu, zakresie i architekturze nadal wymagają udziału użytkownika. Nie pytaj o fakty możliwe do sprawdzenia w kodzie ani o decyzje już zapisane. Zachowaj rozróżnienie znajdowania lokalnych faktów i decyzji produktowych z Raven. Zachowaj wywiad Raven, ocenę złożoności/budżetu oraz akceptację struktury, bez ponownego pytania o zatwierdzone ustalenia. Pytania obsługuje koordynator narzędziem dostępnym w hoście lub zwykłym czatem; brak natywnej funkcji u planisty nie blokuje procesu i nie jest zgodą na zgadywanie odpowiedzi. Jest to jawne nadpisanie wymogu konkretnego interfejsu pytań w Raven. Koordynator przekazuje odpowiedzi i aktualizuje uzgodniony kontekst; może kontynuować z tym samym planistą podczas wywiadu. Po zakończeniu planowania nie używa go jako reviewera.

**Research jest wyłącznie decyzją użytkownika.** Czytanie kodu i dokumentacji konieczne do napisania planu pozostaje analizą w ramach raven-plan. Nie wywołuj `raven-research` ani nie twórz osobnego projektu badawczego samodzielnie. Gdy niewiadoma blokuje rozsądny plan, wskaż pytanie, skutek i zaproponuj osobny raven-research. Nie zastępuj odpowiedzi zgadywaniem. Jeśli research już jest w change, wykorzystaj go; powtórnie sprawdzaj tylko nieaktualne lub sprzeczne ustalenia. Nie uruchamiaj automatycznie framingu ani lesson.

Planista przygotowuje pełne plan.md i plan-brief.md w adapterze, zgodnie ze źródłowymi szablonami: stan końcowy, fazy, konkretne pliki i kontrakty, wyłączenia, kryteria automatyczne/ręczne, ryzyka i Progress. Nie implementuje kodu. Rozróżnia bramki implementacyjne, późniejsze sprawdzenie użytkownika i ewentualne osobne fazy testów/checków; PR jest dopiero finalizacją po tych etapach. Wyróżnia wymagane testy/checki przed merge, nie wymyśla nieistniejących poleceń ani nie wymusza E2E sprzecznych z zasadami projektu.

## 3. Publikacja planu w change

Koordynator sprawdza kompletność artefaktów i mapuje je zgodnie z kontraktem GH: brief i część przekrojowa do rodzica, fazy do sub-issues, weryfikacja i Progress do właściwych tasków. Nie gubi szczegółów planu podczas przeniesienia. Zachowaj istniejące ID i ludzkie fragmenty; nie nadpisuj rozpoczętej pracy. Ustaw natywne relacje i kolejność. Nie zostawiaj drugiej wersji w repo.

Po potwierdzeniu publikacji utwórz kompletny snapshot vN i fingerprint. Zapis planu jest częścią zlecenia, nie kolejną bramką zgody. Plan jest jeszcze niezatwierdzony, taski nie stają się automatycznie Ready. Niedokończona publikacja blokuje review tej wersji; wznów ją zamiast tworzyć duplikaty.

## 4. Niezależne plan-review — zawsze

Poczekaj na zakończenie planisty. Uruchom NOWEGO reviewera bez jego historii rozmowy. Przekaż repo_root, źródłowe wymagania i lessons, opublikowany snapshot z hashem, taski i mapowanie do lokalnego adaptera oraz absolutną ścieżkę [plan-review](../raven-plan-review/references/procedures/plan-review/procedure.md). Reviewer wykonuje ten skill, wraz z ugruntowaniem w kodzie i pięcioma wymiarami: End-State Alignment, Lean Execution, Architectural Fitness, Blind Spots, Plan Completeness. Zachowaj jego domyślny tryb i przewidziane odczyty/delegowanie, w granicach dostępnych slotów.

Reviewer ocenia całość rodzic + taski + zależności, nie tylko tekst głównego issue. W raporcie lokalizacja wskazuje issue i sekcję/fazę; dowody kodowe mają path:line. Walidacja Progress dotyczy wygenerowanej reprezentacji Raven. Jawnie planowane nowe pliki nie są błędem tylko dlatego, że jeszcze nie istnieją; odróżniaj je od nieistniejących zależności, które plan zakłada jako obecne.

Reviewer nie edytuje planu/kodu, nie ustawia Ready, nie prowadzi triage i nie komunikuje się bezpośrednio z użytkownikiem. Kończy na raporcie SOUND/REVISE/RETHINK z uwagami i dowodami. Koordynator publikuje raport w change jako komentarz z wersją i fingerprintem; nie pyta osobno, czy go zapisać. Nie podmieniaj technicznego werdyktu z powodu akceptacji ryzyka.

Jeśli nie ma możliwości uruchomienia świeżego reviewera, zgłoś brak i przygotuj przekazanie do nowej sesji. Nie oznaczaj własnej samokontroli jako niezależnego review.

## 5. Decyzja, poprawki i zakończenie

W czacie pokaż zwięzły plan, zakres tasków, kryteria odbioru, uwagi z ID i linki. Użytkownik nie musi otwierać GH, aby rozumieć decyzję. Po każdym review zakończ rundę i czekaj: akceptacja konkretnej wersji, zlecone poprawki, zmiana kierunku lub zatrzymanie. Brak uwag nie zastępuje akceptacji. Nie wykonuj automatycznie zaleceń reviewera.

„Popraw F1 i F3, F2 akceptuję” oznacza zapis dokładnie tych decyzji, uruchomienie świeżego planisty do wskazanych poprawek, publikację nowej wersji i świeżego reviewera. Kolejne review sprawdza poprawki i ich wpływ na cały plan. Akceptowanych/odrzuconych uwag nie otwieraj ponownie bez nowego dowodu. „Popraw wszystkie” dotyczy bieżącego raportu, nie wszystkich przyszłych rund. Nie wymagaj potwierdzenia każdej edycji już zleconej poprawki. Przy niejasnym zakresie pytaj tylko o brakującą decyzję.

Przed zapisaniem akceptacji ponownie porównaj bieżące wymagania i kontrakty z fingerprintem raportu. Przy różnicy nie przypisuj zgody do nowej treści. Po akceptacji zapisz decyzję w GH; ustaw Ready dla change/tasków, których zależności i wymagania gotowości są spełnione. Przy pozostałej przeszkodzie zachowaj akceptację planu i jawnie opisz brak gotowości. Nie ustawiaj Done, nie implementuj i nie uruchamiaj raven-auto-implement bez zlecenia.

Przy wznowieniu z gotowym raportem przedstaw oczekującą decyzję, zamiast regenerować plan. Przy ukończonym, zaakceptowanym planie potwierdź jego wersję i dostępność do realizacji. Każdy handoff zawiera link change, wersję planu, wynik review i faktyczny stan zapisu w GH.

## Osobny obowiązkowy etap trwałych testów

Po oddaniu implementacji i sprawdzeniu użytkownika, przed PR, workflow wymaga raven-test. Plan wydziela odpowiednie fazy unit/integration/E2E dla tego etapu. Implementacja wykonuje swoje bieżące bramki, lecz nie realizuje odroczonych faz trwałych testów i nie uruchamia raven-test automatycznie. W handoffie wskaż go jako wymagany następny etap przed publikacją PR.

Etap trwałych testów ma dwa warianty: raven-test → osobno raven-test-review (manual) albo raven-auto-test (pisanie, uruchomienie, niezależne review i poprawki wad testów w jednym cyklu). Oba używają tego samego change i źródeł; wybór należy do użytkownika. Samo ukończenie manualnego raven-test nie oznacza ukończenia review testów.

## Przejęcie researchu i architektury

Jeśli przygotowanie rozpoczął `raven-research`, kontynuuj to samo change i jego Preparing. Tożsamość jest już zapewniona; nie twórz drugiego issue ani nie powtarzaj new. Przed wywiadem odczytaj raporty wskazane w indeksie oraz kolejne rundy i decyzje. Porównaj ich wejściowe wymagania, SHA/dowody i dirty state z bieżącym kodem. Ponownie badaj tylko zmienione lub sprzeczne ustalenia; rekomendacji nie traktuj jako decyzji użytkownika.

W planie/briefie podaj research ID/URL, przejęte wnioski, rozstrzygnięcia i pozostałe do weryfikacji ryzyka. Przeczytaj `context/foundation/architecture.md`, jeśli istnieje, i respektuj uzgodnione zasady; propozycje i odroczenia nie są zatwierdzonymi kontraktami. Materiały researchu i architekturę przekaż także delegowanemu planiście/reviewerowi. Sam research nie zastępuje planu, review ani akceptacji użytkownika.
