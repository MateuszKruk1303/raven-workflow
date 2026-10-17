# Trwałe E2E: plan → generate → review → verify

Wewnętrzna procedura dla implementacji lub osobnego zlecenia testów, zgodna z [kontraktem Git-first](../../../../raven-workflow/references/change-contract.md). Nie tworzy drugiego workflow ani task issues. Czytaj lokalny kontrakt, strategię, test-stack, istniejący seed i tylko potrzebne referencje. Testy powstają z implementacją, a normalne review change obejmuje je razem z kodem.

## Setup i dobór ryzyka

Ustal źródła Expected, fingerprint, base/head/tree, zakres kroku i scenariusze chronione na poziomie przeglądarki. Nie wybieraj nowego niezależnego zakresu. Potwierdź istniejący runner i możliwość uruchomienia aplikacji. Jeśli są braki, zastosuj [e2e-setup](../e2e-setup/procedure.md) w zatwierdzonym zakresie. Nie instaluj drugiego runnera i nie konfiguruj CI przy okazji.

Sprawdź istniejące pokrycie: wykorzystaj skuteczny test zamiast duplikować asercje. Jeśli unit/integration chroni ryzyko lepiej, wybierz tę warstwę. Pominięcie nowego E2E wymaga rzeczywistego dowodu ochrony albo uzasadnienia nieadekwatności; nie odhaczaj testu niewykonanego jako PASS. Testy before-change mogą wykazać EXPECTED_RED zgodnie z [kontraktem](../../before-change.md).

## Plan i generowanie

1. Odczytaj [zasady jakości](references/e2e-quality-rules.md), [antywzorce](references/e2e-anti-patterns.md) i [wzorzec seed](references/seed-test-pattern.md). Każdy scenariusz ma źródło wymagania/ryzyka, warunki/dane, kroki i niezależny Expected, ustalony przed obserwacją outputu.
2. Dla eksploracji stosuj [browser-driven generation](references/browser-driven-generation.md) i [tool wiring](../e2e-setup/references/tool-wiring.md). Domyślnie Playwright CLI w osobnej sesji; przełączenie na prywatną przeglądarkę wymaga polecenia lub zgody według raven-browser. Najpierw rzeczywiście otwórz i przygotuj stronę, potem czytaj snapshot dostępności. Nie wymyślaj lokatorów. Screenshot używaj dla ryzyka wizualnego, nie jako zamiennik drzewa dostępności.
3. Uruchom build/preview z poleceń i portu test-stack/webServer; `E2E_PORT` ma pierwszeństwo, gdy konfiguracja je wspiera. Jeśli potrzebne zewnętrzne API są mockowane, zastosuj [mockowanie](references/mocking-external-apis.md) przed buildem/eksploracją. Nie wykonuj rzeczywistych płatności ani wiadomości na podstawie samego dostępu. Prowadź własne procesy i zatrzymaj je przed właściwym VERIFY, jeśli runner zarządza serwerem.
4. Przejdź happy path oraz istotny błąd/granicę. Generuj testy oparte na zaobserwowanych rolach/nazwach, na wzorcu seed i [szablonie generowania](references/e2e-prompt-template.md). Preferuj stabilne dostępne lokatory; unikaj arbitralnych sleep, kruchych selektorów, zależności od kolejności i współdzielonego mutable state. Używaj testowych kont i unikalnych rekordów z cleanup.

## Review i verify

Sprawdź każdy wygenerowany test: czy asercja wykrywa błąd, Expected ma niezależne źródło, mock nie omija badanego kontraktu, a lokator i oczekiwanie reprezentują użytkownika. Wewnętrzna samokontrola generowania nie jest niezależnym review końcowym. Normalny reviewer change może pokryć ten wymiar bez oddzielnego agenta.

Uruchom nowe/zmienione testy i odpowiednie regresje z właściwą konfiguracją. Wykonaj powtórny przebieg E2E, by sprawdzić izolację i cleanup. Przypadkowy sukces, retry bez reprodukcji i błąd runnera nie dowodzą poprawności. Gdy skuteczność asercji jest niepewna, wykonaj kontrolowaną perturbację w izolacji i bezwarunkowo przywróć kod. Błąd składni nie jest dowodem ochrony zachowania.

Naprawiaj potwierdzone defekty w zleconym zakresie. Nie osłabiaj testu dla green. Po dwóch nieskutecznych próbach jednego problemu zapisz reprodukcję, próby, blokadę i next; nowa sesja nie resetuje licznika. Nowe wymaganie lub nieobjęte działanie wraca do użytkownika.

Zapisz polecenia, wyniki, tree/HEAD, środowisko i luki w lokalnym test-report/checkpoint. Progress jest w planie poza blokiem kontraktu; dokumenty należą do repo i celowego stagingu. Nie wymagaj zgody na komunikat każdego commitu. Nie odhaczaj odbioru człowieka. Oddaj wynik wywołującemu skillowi; samo E2E nie publikuje PR, nie merguje i nie uruchamia dodatkowych etapów automatycznie.
