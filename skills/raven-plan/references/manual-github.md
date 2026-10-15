# Manualny adapter GitHub

Przeczytaj [wspólny kontrakt GitHub](../../raven-auto-plan/references/github-contract.md). Oba tryby używają tych samych issues, tasków, snapshotów, fingerprintów, Progress, raportów i decyzji. Nie twórz osobnych artefaktów dla trybu manualnego. Zmiana trybu nie restartuje ukończonych etapów ani nie przenosi akceptacji na nową wersję.

Manual oznacza osobno zlecane etapy, nie uproszczone kryteria jakości. Wykonuj procedury wskazane lokalnymi linkami w SKILL.md wraz z ich referencjami i helperami. Ścieżki względne rozwiązuj względem katalogu procedury. Kontrakt GH i nadrzędny skill określają transport, stan oraz zakres wykonania.

## Transport zamiast lokalnego źródła prawdy

- Wejście to URL issue/raportu, numer z jednoznacznym repo, Raven ID albo bieżąca rozmowa. Zamiast szukać najnowszego lokalnego folderu, rozwiąż właściwy change i pobierz pełny kontekst z GH. Raport-comment URL jest odpowiednikiem ścieżki zapisanego raportu do wznowienia triage.
- Odtwórz `change.md`, `plan.md`, `plan-brief.md`, research, raporty i Progress w artifact_dir poza śledzonym repo; repo_root wskazuje rzeczywisty kod. Ścieżki `context/changes/...` lokalnej procedury oznaczają tę kopię roboczą. Zachowaj źródłowe szablony i markery raportów.
- Plan/brief → oznaczone bloki rodzica i kontrakty sub-issues; Progress → właściwe taski; research, review, decyzje i checkpointy → komentarze rodzica. Follow-ups/review-fixes → komentarz decyzji z ID uwag, zakresem i stanem wykonania. Lokalny status change.md jest tylko reprezentacją, Project przechowuje rzeczywisty status.
- Nie wykonuj lokalnej synchronizacji roadmapy, bootstrap stagingu kontekstu ani epilogu commitującego kopie dokumentacji. Commity kodu i bramki Raven pozostają. Zachowaj lokalne lessons oraz instrukcje projektu; nie przenoś ich do GH.
- Główny agent jest koordynatorem zapisów GH także wtedy, gdy sam planuje/implementuje/reviewuje. Podagenci zwracają wyniki, nie publikują. Po każdym trwałym kroku opublikuj i odczytaj wynik; po błędzie wznów zapis zamiast ponawiać pracę.
- Raporty historyczne są niezmienne. Decyzje triage publikuj oddzielnie, wiążąc je z raportem, wersją/SHA i ID uwagi; roboczy raport może przedstawiać złożony aktualny stan. Naprawa tworzy nową wersję planu lub kodu i wymaga odpowiedniej ponownej weryfikacji. Nie oznaczaj samej decyzji „napraw” jako FIXED.

## Granice trybu manualnego

Nie uruchamiaj automatycznie kolejnego skilla, niezależnego testera ani pętli napraw z raven-auto-implement. Samo wywołanie review nie upoważnia do naprawy jego uwag. Zachowaj źródłowy interaktywny triage i wykonaj poprawki wyraźnie wybrane przez użytkownika, bez wymagania ponownego wpisania nazwy skilla. Decyzja „review tej fazy” w implementacji jest jawnym zleceniem raven-implement-review.

Zachowaj wybór wykonania lokalnie/delegowania, manual gates, decyzje między fazami i rytuał commitów z Raven, uwzględniając uprawnienia już udzielone przez użytkownika. Nie narzucaj automatycznego delegowania całej realizacji. Delegowanie analiz przewidziane przez źródłowy skill nadal jest dozwolone; manual nie oznacza zakazu podagentów.

Kolejne etapy wskazuj nazwami skilli Raven. Nie wywołuj research ani lesson bez zlecenia. raven-pr jest osobno zlecanym etapem publikacji, a Done następuje dopiero po merge.

Nie dziedzicz z wariantu auto obowiązkowego świeżego planisty, reviewera po testerze ani automatycznych retestów. Przy review zachowaj źródłowe delegowanie i uczciwie nazwij zakres niezależności: sam osobny skill w tej samej sesji nie jest świeżym kontekstem. Jeśli użytkownik zażąda niezależnego review, użyj świeżego agenta bez transkryptu autora lub zgłoś brak takiej możliwości.

Korzystaj z dostępnego interfejsu pytań hosta, a gdy go brak — z rozmowy. To nadpisuje wyłącznie wymóg konkretnego narzędzia w Raven; zachowaj merytoryczne pytania, rekomendacje, kompromisy i oczekiwanie na potrzebną odpowiedź. Nie zakładaj decyzji użytkownika.

Ready wymaga review, akceptacji aktualnego planu i spełnienia zależności. Sam zapis planu nie wystarcza. Nie ustawiaj Done ani nie zamykaj issues. PR, push, merge i deploy nie są skutkiem ukończenia etapu manualnego.
