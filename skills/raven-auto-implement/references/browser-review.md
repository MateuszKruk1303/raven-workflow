# Techniczne sprawdzenie UI

Używaj tylko gdy zmienione zachowanie wymaga przeglądarki. Zakres wynika z konkretnej zmiany; ten plik nie wprowadza osobnego QA, krytycznej ścieżki ani raportu.

Technikę izolowanej sesji opisuje [raven-browser](../../raven-browser/SKILL.md). Korzystaj z niej w bieżącym agencie, bez importowania polityki modeli, delegowania ani procesu QA. Preferuj istniejący test lub izolowaną sesję Playwright; osobista przeglądarka wymaga upoważnienia użytkownika.

Sprawdź obserwowalny skutek interakcji. Gdy zmiana dotyczy trwałego zapisu, potwierdź go ponownym odczytem; dla wyglądu obejrzyj render. Do ponowień można zachować mały tymczasowy scenariusz ze sprawdzonymi locatorami i asercjami. Nie wdrażaj nowego frameworka ani nie naprawiaj niezwiązanego harnessu. Zablokowany test zgłoś jako ograniczenie; alternatywny kanał potwierdza tylko zachowanie, które faktycznie obserwuje.

Używaj własnych danych testowych i sprzątaj tylko je. Nie wykonuj rzeczywistych płatności, wysyłek, publikacji ani operacji na cudzych danych bez upoważnienia; nie resetuj współdzielonej bazy i nie ujawniaj sekretów.
