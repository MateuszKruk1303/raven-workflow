# Narzędzia przeglądarkowe Raven

Wybór narzędzia określa [raven-browser](../../../../../raven-browser/SKILL.md). Przeczytaj go przed eksploracją: domyślnie Playwright CLI w osobnej nazwanej sesji; Brave/MCP tylko na wyraźne polecenie lub zgodę użytkownika na użycie przeglądarki. Samo zlecenie E2E ani brak CLI nie oznaczają wyboru MCP. Zachowaj jawny wybór użytkownika z bieżącego zadania.

Wykorzystaj istniejące CLI projektu lub środowiska i sprawdź `--help`. Jeśli go brak, użyj `npx -y @playwright/cli --help` oraz tego samego prefiksu w kolejnych komendach, respektując przypiętą wersję projektu. Nie instaluj globalnego CLI, dodatkowych skilli ani manifestu instalatora workflow. Setup testów nie obiecuje instalacji narzędzia w środowisku agenta.

Używaj dedykowanej sesji nazwanej dla projektu i zadania przy każdym wywołaniu; nie steruj globalną sesją `default`. Brak powłoki lub możliwości uruchomienia CLI oznacza blokadę eksploracji, bez automatycznego przejścia na MCP. Jeśli potwierdzone ograniczenie CLI uniemożliwia rzetelny test, zastosuj sekcję „Wyjątkowa prośba o osobistą przeglądarkę” w raven-browser: uzasadnij potrzebę, opisz zakres i poczekaj na zgodę. Gdy użytkownik wybrał MCP, wykonaj połączenie zgodnie z raven-browser; brak MCP także raportuj jako blokadę, nie zaliczoną kontrolę.

Trwałe testy używają odizolowanych kont i danych. Nie eksportuj prywatnej sesji do repo ani CI. Specy uruchamia runner projektu, zwykle Playwright Test, według lockfile i konfiguracji. Instalacja runnera i jego przeglądarki w procedurze setupu jest odrębna od wyboru narzędzia eksploracji. Wynik eksploracji nie zastępuje uruchomienia suite.

Logi, screenshoty i storageState mogą zawierać dane wrażliwe: przechowuj je poza śledzonym kodem, publikuj tylko potrzebne zredagowane dowody. Zamknij wyłącznie sesję uruchomioną do tego zadania.
