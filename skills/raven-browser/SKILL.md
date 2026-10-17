---
name: raven-browser
description: >-
  Weryfikuj działającą aplikację domyślnie przez Playwright CLI w osobnej sesji. Tylko na wyraźne polecenie lub zgodę użytkownika na użycie przeglądarki przełączaj się na Brave przez Playwright MCP, zachowując jego profil i zalogowanie. Używaj także automatycznie przy implementowaniu lub poprawianiu funkcjonalności aplikacji webowej wymagających weryfikacji w przeglądarce: interakcje, formularze, nawigacja, logowanie, responsywność i wygląd. Nie uruchamiaj dla zmian wyłącznie dokumentacyjnych lub backendowych bez scenariusza przeglądarkowego.
---

# Raven Browser

Przy wykonywaniu lub delegowaniu pracy stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Sam routing/status nie uruchamia agentów.

## Wybór trybu

Domyślnie używaj **Playwright CLI** w osobnej sesji testowej. Automatyczna weryfikacja UI, polecenie „sprawdź aplikację”, wywołanie samego `raven-browser` ani instrukcja innego skilla o sprawdzeniu przeglądarkowym nie oznaczają wyboru osobistej przeglądarki.

Tryb **Brave przez MCP** wybierz tylko wtedy, gdy użytkownik jasno polecił użycie przeglądarki, np. „użyj przeglądarki”, „sprawdź w moim Brave” albo „użyj Brave MCP”. Respektuj taki wybór z wcześniejszej części bieżącego zadania, dopóki użytkownik go nie zmieni. Jawne wskazanie CLI lub innego konkretnego narzędzia ma pierwszeństwo przed ogólnym słowem „przeglądarka”. Zgoda udzielona na uzasadnioną prośbę agenta opisaną poniżej również wybiera tryb MCP. Koordynator przekazuje testerowi rzeczywisty wybór użytkownika; sam nie tworzy zgody na MCP.

## Domyślnie: Playwright CLI

1. Sprawdź dostępne `playwright-cli --help` i wersję narzędzia. Wykorzystaj istniejącą instalację projektu lub środowiska; jeśli jej brak, użyj `npx -y @playwright/cli --help` i tego samego prefiksu w dalszych komendach, bez instalacji globalnej. Respektuj przypiętą wersję projektu.
2. Używaj osobnej nazwanej sesji dla projektu i zadania (`-s=<projekt-zadanie>` przy każdym wywołaniu), bez podłączania osobistego profilu lub endpointu CDP. Otwórz URL aplikacji przez `playwright-cli -s=<projekt-zadanie> open <url>`; domyślny tryb jest headless.
3. Pobierz `snapshot`, czytaj potrzebne fragmenty pliku wskazanego w wyniku i wykonuj `click`, `fill`, `press` na referencjach z aktualnego snapshotu. Pozostałe komendy sprawdzaj w `--help`. Screenshoty służą także ocenie wyglądu; snapshot nie potwierdza layoutu.
4. Dla logowania użyj konta testowego lub istniejącego testowego `storageState` (po otwarciu sesji: `state-load <plik>`). Nie kopiuj cookies z osobistej przeglądarki. Snapshoty, logi i stan sesji przechowuj poza śledzonym kodem; sprawdź ignorowanie `.playwright-cli/` przed użyciem w repo. Nie wyświetlaj sekretów z plików ani wyników komend.
5. Po sprawdzeniu zamknij wyłącznie własną sesję (`playwright-cli -s=<projekt-zadanie> close`), chyba że jest potrzebna do dalszej pracy. Nie używaj zbiorowego zamykania sesji innych zadań.

Brak CLI, powłoki lub możliwości uruchomienia sesji zgłoś jako konkretną blokadę. Nie przełączaj się automatycznie na osobiste Brave/MCP i nie uruchamiaj jego skryptu konfiguracyjnego. CLI służy eksploracji; trwałe testy nadal uruchamia runner projektu. Dla powtarzalnego QA w `raven-auto-implement` obowiązuje także poniższy wariant.

### Powtarzalne scenariusze auto QA

W [wykonawczym QA auto-implement](../raven-auto-implement/references/browser-review.md) tester może po rozpoznaniu UI zapisać tymczasowe scenariusze Playwright i wykonywać je przez dostępne CLI albo istniejącą bibliotekę/runner. Osobny kontekst przeglądarki runnera spełnia tu wymóg izolowanej sesji; nie łącz go z profilem osobistym. Dla takiego replay nie wymagaj snapshotu przed każdym działaniem ani ponownej eksploracji strony: używaj sprawdzonych stabilnych locatorów, asercji i jawnego setup/cleanup. Błąd selektora wymaga ponownej obserwacji odpowiedniego fragmentu UI, nie zgadywania ani osłabiania Expected. Kod/config pozostaje tymczasowy; szczegóły przechowania, dowodów i napraw określa procedura QA.

Granice roli mają pierwszeństwo przed poniższym poleceniem naprawy regresji: niezależny tester raportuje defekt implementatorowi, nie zmienia produktu ani trwałej suite. Wyraźny wybór osobistego Brave/MCP nadal obowiązuje; nie przenoś tego profilu do runnera.

### Wyjątkowa prośba o osobistą przeglądarkę

Jeżeli konkretne, potwierdzone ograniczenie CLI uniemożliwia rzetelne sprawdzenie wymaganego scenariusza, możesz poprosić użytkownika o użycie jego Brave przez MCP. Dotyczy to np. problemu odtwarzalnego wyłącznie w istniejącym profilu, zależności od rozszerzenia lub sesji SSO/urządzenia, której nie da się odtworzyć na koncie testowym, albo awarii CLI, której dostępne MCP pozwoli uniknąć. Nie zakładaj, że MCP rozwiąże problem: wskaż, dlaczego w tym przypadku ma pomóc.

Najpierw sprawdź przyczynę i wykonalne rozwiązanie w CLI w granicach zadania (np. poprawną komendę, konto testowe lub tryb headed). Nie powtarzaj bezskutecznych prób. Sam brak globalnej instalacji, wygoda, wolniejsze działanie lub pojedynczy nieudany test nie uzasadniają przejścia na osobistą sesję.

Prośba powinna wskazać: nieweryfikowalny scenariusz, zaobserwowaną blokadę i wykonane próby, powód użycia osobistej przeglądarki oraz konkretny zakres (URL, konto/rola, planowane działania). Przywołaj tę sekcję raven-browser jako podstawę prośby. W pętli delegowanej tester przekazuje te informacje koordynatorowi, który pyta użytkownika.

Poczekaj na wyraźną zgodę przed podłączeniem, uruchomieniem lub konfiguracją osobistej przeglądarki. Nie pytaj ponownie, jeśli użytkownik już upoważnił do tego samego zakresu. Do czasu decyzji możesz kontynuować niezależne kontrole; zablokowany scenariusz pozostaje BLOCKED/NOT VERIFIED. Odmowa lub brak odpowiedzi nie oznacza zgody. Zgoda na użycie przeglądarki nie rozszerza zakresu operacji na danych i nie oznacza automatycznie zgody na restart trwającej sesji. Sprawdzenie w osobistej sesji nie zastępuje powtarzalnego uruchomienia trwałych E2E w środowisku testowym.

Dokumentacja komend: [Playwright CLI](https://github.com/microsoft/playwright-cli).

## Na wyraźne polecenie lub zgodę użytkownika: Brave przez MCP

Tylko w tym trybie pracuj w prawdziwym Brave użytkownika przez MCP `brave`. Domyślne połączenie to `http://127.0.0.1:9222`; zwykłe uruchomienie Brave z ikony nie włącza tego portu. Nie zastępuj tego osobnym Chromium, przeglądarką w aplikacji ani nowym profilem bez uzgodnienia — celem jest istniejąca sesja użytkownika.

### Wymagania środowiska Brave/MCP

Ten wariant jest dostosowany do macOS i Brave w `/Applications/Brave Browser.app`. Wymaga Python 3 oraz dostępnego serwera Playwright MCP `brave`; konfiguracja MCP należy do środowiska agenta i nie przenosi się przez samo skopiowanie skilli. Skrypt uruchamiający Brave obsługuje macOS. Na innym systemie zgłoś brak tego wariantu połączenia i uzgodnij sposób dostępu do przeglądarki, zachowując preferencję użytkownika; nie zastępuj jego profilu po cichu. Pozostałe etapy Raven nie wymagają macOS.

### Połączenie Brave/MCP

1. Odkryj dostępne narzędzia MCP `brave` i sprawdź połączenie przez `browser_tabs`. Jeżeli działa, korzystaj z niego bez restartu.
2. Gdy endpoint nie odpowiada, uruchom `python3 <katalog-skilla>/scripts/ensure_brave.py`. Skrypt ponownie wykorzystuje aktywny endpoint albo uruchamia zamknięte Brave z portem 9222.
3. Jeżeli Brave już działa bez portu, potrzebny jest restart. Jeśli użytkownik zlecił uruchomienie/restart Brave pod MCP, poinformuj go i wykonaj skrypt z `--restart`. Przy automatycznej weryfikacji nie zamykaj trwającej prywatnej sesji bez istniejącego upoważnienia; zapytaj wyłącznie o niezbędny restart. Nigdy nie wymuszaj zamknięcia, nie odrzucaj niezapisanych formularzy. Skrypt kończy pracę, gdy przeglądarka nie zamknie się łagodnie.
4. Zweryfikuj ponownie `browser_tabs`. Sam działający port lub zapis konfiguracji nie oznacza działającego MCP.

Jeżeli serwera brak w konfiguracji, sprawdź `codex mcp get brave`. Dodaj brakujący wpis (z uwzględnieniem uprawnień zapisu poza repozytorium):

```sh
codex mcp add brave -- npx -y @playwright/mcp@latest --cdp-endpoint http://127.0.0.1:9222
```

Nie nadpisuj odmiennej istniejącej konfiguracji bez sprawdzenia jej przeznaczenia. Jeżeli wpis istnieje, ale narzędzia nie są dostępne w bieżącej sesji, powiedz, że trzeba ponownie uruchomić Codex CLI. Nie traktuj tego jako błędu strony.

Po nieudanym starcie sprawdź parametry procesu oraz komunikat skryptu. Nie powtarzaj restartów w pętli. Nie kopiuj cookies ani profilu, nie czytaj haseł i nie obchodź ograniczeń profilu przez wyłączanie zabezpieczeń. Jeśli wersja Brave odrzuca debugowanie bieżącego profilu, zgłoś ten konkretny problem zamiast obiecywać zachowanie sesji w nowym profilu.

## Weryfikacja implementowanych funkcjonalności

Po zmianie zachowania widocznego w przeglądarce użyj tego skilla bez oczekiwania na osobne polecenie „przetestuj”.

- Odczytaj polecenie uruchomienia, port i routing projektu; wykorzystaj istniejący serwer albo uruchom właściwy. W aplikacji wieloorganizacyjnej otwórz host i organizację objęte zadaniem, nie przypadkowy localhost.
- W trybie CLI używaj własnej nazwanej sesji; w trybie Brave/MCP utwórz własną kartę testową przez `browser_tabs` z `action: new` i zapamiętaj ją. Zachowaj prywatne karty użytkownika i nie nawiguj po niezwiązanych kontach.
- Przed interakcją pobierz snapshot. Używaj odnośników i selektorów wynikających z aktualnie zaobserwowanej strony. Wykonuj nawigację, kliknięcia, formularze i screenshoty narzędziem wybranym według powyższej reguły: domyślnie CLI, MCP na wyraźne polecenie lub zgodę użytkownika.
- Przejdź rzeczywisty scenariusz zmienionej funkcjonalności. Sprawdź wynik po akcji, a nie tylko widoczność przycisku: np. zapis, ponowne odczytanie danych, walidację błędnych danych lub zmianę adresu. Dobierz przypadki do ryzyka zmiany.
- Przy zmianach wyglądu obejrzyj screenshot i sprawdź istotny rozmiar mobilny oraz desktopowy; przy zmianie rozmiaru współdzielonego okna przywróć poprzedni rozmiar. Przy formularzach uwzględnij klawiaturę i widoczność komunikatów.
- Sprawdź błędy konsoli i nieudane żądania związane ze scenariuszem. Nie uznawaj każdego ostrzeżenia zewnętrznego serwisu za regresję aplikacji.
- Korzystaj z danych testowych. Zalogowanie w osobistym profilu nie oznacza zgody na zakup, wysłanie wiadomości, publikację lub usunięcie rzeczywistych danych. Zakres działań wynika z zadania użytkownika.
- Napraw znalezioną regresję i ponownie sprawdź dotknięty scenariusz. Bieżąca weryfikacja przez CLI lub MCP nie zastępuje wymaganych testów projektu.
- Zapisuj screenshoty i logi w istniejącym katalogu artefaktów projektu lub katalogu tymczasowym; nie dodawaj prywatnych danych do repozytorium. Zamykaj wyłącznie własne karty testowe, jeśli nie są potrzebne do przeglądu wyniku. Pozostaw przeglądarkę użytkownikowi.

W podsumowaniu podaj sprawdzony scenariusz, wynik i istotne ograniczenia. Nie deklaruj zaliczonej weryfikacji, jeśli blokowało ją logowanie, brak wybranego narzędzia, niedziałający serwer lub brak danych. Informuj o użyciu osobistego Brave krótko, bez powtarzania całej instrukcji konfiguracji.
