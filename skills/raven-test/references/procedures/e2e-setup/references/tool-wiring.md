# Narzędzia przeglądarkowe Raven

Użyj dostępnego narzędzia przeglądarkowego zgodnego z instrukcjami projektu. Dla własnej przeglądarki użytkownika czytaj raven-browser; trwałe testy używają odizolowanych kont i danych. Nie eksportuj prywatnej sesji do repo ani CI.

Nie ma wymaganego manifestu instalatora workflow. Środowisko agenta ustal z bieżącej sesji i instrukcji repo, nie z domyślnego katalogu skilli. Nie instaluj dodatkowych skilli ani narzędzi globalnych jako warunku wykonania testów.

Jeśli projekt korzysta z playwright-cli, sprawdź jego dostępność i --help. Używaj istniejącej wersji oraz dedykowanej sesji nazwanej dla projektu; nie steruj globalną sesją default współdzieloną z innymi projektami. Dla brakującego narzędzia wykorzystaj dostępne browser MCP lub uzgodniony setup lokalny. Nie wymyślaj składni narzędzia.

Trwałe specy uruchamia runner projektu, zwykle Playwright Test, według lockfile i konfiguracji. Wynik eksploracji przeglądarki nie zastępuje uruchomienia suite. Logi, screenshoty i storageState mogą zawierać dane wrażliwe: przechowuj je poza śledzonym kodem, publikuj tylko potrzebne zredagowane dowody. Zamknij wyłącznie sesję uruchomioną do tego zadania.
