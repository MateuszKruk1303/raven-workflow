# Praca na taskach GitHub

Pracujemy na taskach w GitHub Issues. Body issue opisuje wymagania biznesowe i kryteria odbioru. Jeśli źródłem jest Jira, issue linkuje ticket bez kopiowania treści.

## Task, plan, branch

- Jeden issue to jeden branch i jeden PR. Drobna zmiana z doskoku nie potrzebuje issue ani planu.
- Plan (`context/changes/<id>/plan.md`) jest opcjonalnym, jednorazowym kontekstem roboczym agenta: wynik, decyzje, podejście, weryfikacja. Nie jest kontraktem. Nie wersjonuj go, nie trzymaj w nim checkpointów, statusów ani raportów. Nowe wymaganie trafia do issue albo do polecenia, bez aktualizacji planu.
- Stan pracy czytaj z issue (stan, assignee), brancha, commitów i PR, nie z pamięci rozmowy. Nie skanuj boarda. Gdy użytkownik nie wskazał taska, a kolejność nie jest jednoznaczna, zapytaj.
- Podejmując issue (`raven-plan` albo `raven-auto-implement` bez wcześniejszego planu), przypisz się i ustaw etykietę `in-progress` (oraz status In progress, jeśli projekt używa GitHub Project).
- Dla nowego issue utwórz branch z aktualnej bazy (`git pull --ff-only`) według konwencji projektu. Przy wznowieniu użyj istniejącego brancha. Branch po zmergowanym PR nie wskazuje kolejnego taska.
- Nie commituj ani nie pushuj bezpośrednio na branch domyślny. Drobna zmiana bez issue też dostaje krótki branch według konwencji projektu.
- Zachowaj cudze zmiany w working tree. Nie przełączaj brancha ani nie aktualizuj bazy, gdy kolidują; zapytaj, jak je zachować. Bez samoczynnego stash, reset ani commitu cudzych zmian.
- Commituj logiczne kroki zgodnie z konwencją projektu.

## Publikacja

- Push, PR i merge tylko na wyraźne polecenie użytkownika.
- PR linkuje issue (`Closes #N`), opisuje zmianę zwięźle i ma sekcję „Weryfikacja” (niżej).
- Merge wymaga zielonego wymaganego CI i zgody użytkownika. Po merge sprawdź, że issue jest zamknięty. Deploy to osobna operacja.

## Weryfikacja i raportowanie

- Niewykonana lub zablokowana kontrola nigdy nie jest raportowana jako zaliczona.
- Wyniki weryfikacji i instrukcję odbioru podawaj w końcowej wiadomości czatu. Nie twórz raportów, acceptance.md ani ich kopii w issue, chyba że użytkownik o to prosi.
- Wyjątkiem jest PR: sekcja „Weryfikacja” to krótki trwały ślad dla reviewera — poziom (`quick`/`standard`/`thorough`, jeśli był), wykonane kontrole z kanałem i wynikiem, czego nie sprawdzono. Tylko to, co faktycznie wykonano i widać w kontekście; bez dowodu wpisz „nie potwierdzono”. Lokalne kontrole nie są CI.
- Review lub test zlecony osobnemu agentowi wykonuje świeży kontekst bez transkryptu autora. Reviewer nie poprawia ocenianej pracy.

## Ograniczenia

- Brak dostępu do GitHub nie blokuje pracy lokalnej. Zgłoś niewykonaną operację; nie twórz lokalnego backlogu zastępczego.
- Historyczne artefakty (stare plany, checkpointy, raporty, pola akceptacji) zostaw bez zmian. Nie są bramkami i nie wymagają migracji.
