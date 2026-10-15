---
name: raven-browser
description: >-
  Uruchamiaj i podłączaj własną przeglądarkę Brave użytkownika na macOS do Playwright MCP, zachowując jego profil i zalogowanie. Używaj także automatycznie przy implementowaniu lub poprawianiu funkcjonalności aplikacji webowej wymagających weryfikacji w przeglądarce: interakcje, formularze, nawigacja, logowanie, responsywność i wygląd. Nie uruchamiaj dla zmian wyłącznie dokumentacyjnych lub backendowych bez scenariusza przeglądarkowego.
---

# Raven Browser

Pracuj w prawdziwym Brave użytkownika przez MCP `brave`. Domyślne połączenie to `http://127.0.0.1:9222`; zwykłe uruchomienie Brave z ikony nie włącza tego portu. Nie zastępuj tego osobnym Chromium, przeglądarką w aplikacji ani nowym profilem bez uzgodnienia — celem jest istniejąca sesja użytkownika.

## Wymagania środowiska

Ten wariant jest dostosowany do macOS i Brave w `/Applications/Brave Browser.app`. Wymaga Python 3 oraz dostępnego serwera Playwright MCP `brave`; konfiguracja MCP należy do środowiska agenta i nie przenosi się przez samo skopiowanie skilli. Skrypt uruchamiający Brave obsługuje macOS. Na innym systemie zgłoś brak tego wariantu połączenia i uzgodnij sposób dostępu do przeglądarki, zachowując preferencję użytkownika; nie zastępuj jego profilu po cichu. Pozostałe etapy Raven nie wymagają macOS.

## Połączenie

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
- Utwórz własną kartę testową przez `browser_tabs` z `action: new`; zapamiętaj ją. Zachowaj prywatne karty użytkownika i nie nawiguj po niezwiązanych kontach.
- Przed interakcją pobierz snapshot. Używaj odnośników i selektorów wynikających z aktualnie zaobserwowanej strony. Preferuj narzędzia MCP do nawigacji, kliknięć, formularzy i screenshotów.
- Przejdź rzeczywisty scenariusz zmienionej funkcjonalności. Sprawdź wynik po akcji, a nie tylko widoczność przycisku: np. zapis, ponowne odczytanie danych, walidację błędnych danych lub zmianę adresu. Dobierz przypadki do ryzyka zmiany.
- Przy zmianach wyglądu obejrzyj screenshot i sprawdź istotny rozmiar mobilny oraz desktopowy; przy zmianie rozmiaru współdzielonego okna przywróć poprzedni rozmiar. Przy formularzach uwzględnij klawiaturę i widoczność komunikatów.
- Sprawdź błędy konsoli i nieudane żądania związane ze scenariuszem. Nie uznawaj każdego ostrzeżenia zewnętrznego serwisu za regresję aplikacji.
- Korzystaj z danych testowych. Zalogowanie w osobistym profilu nie oznacza zgody na zakup, wysłanie wiadomości, publikację lub usunięcie rzeczywistych danych. Zakres działań wynika z zadania użytkownika.
- Napraw znalezioną regresję i ponownie sprawdź dotknięty scenariusz. Weryfikacja ręczna przez MCP nie zastępuje wymaganych testów projektu.
- Zapisuj screenshoty i logi w istniejącym katalogu artefaktów projektu lub katalogu tymczasowym; nie dodawaj prywatnych danych do repozytorium. Zamykaj wyłącznie własne karty testowe, jeśli nie są potrzebne do przeglądu wyniku. Pozostaw przeglądarkę użytkownikowi.

W podsumowaniu podaj sprawdzony scenariusz, wynik i istotne ograniczenia. Nie deklaruj zaliczonej weryfikacji, jeśli blokowało ją logowanie, brak MCP, niedziałający serwer lub brak danych. Informuj o użyciu osobistego Brave krótko, bez powtarzania całej instrukcji konfiguracji.
