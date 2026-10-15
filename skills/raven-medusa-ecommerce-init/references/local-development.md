# Kontrakt lokalnego developmentu

Czytaj przy tworzeniu konfiguracji, envów i bootstrapu. Nazwy zmiennych i API sprawdzaj w wygenerowanej wersji startera; poniższe przykłady nie zastępują jego kodu.

## Compose i izolacja

Skopiuj asset Compose jako `compose.yaml`, jeśli projekt nie ma już konfiguracji; istniejącą konfigurację scal. Wybierz stabilny `COMPOSE_PROJECT_NAME`, np. slug projektu i krótki hash jego rzeczywistej ścieżki. Zapisz go w env i zachowuj przy kolejnych uruchomieniach. Nie używaj globalnych `container_name`, zewnętrznych wspólnych sieci ani nazw wolumenów współdzielonych między sklepami.

Szablon używa PostgreSQL 17 i Redis 7 jako punktu wyjścia. Potwierdź kompatybilność wybranej Medusy i przypnij konkretny obraz/tag lub digest. Nie zmieniaj major wersji PostgreSQL przy istniejącym wolumenie. PostgreSQL 18+ wymaga osobnego sprawdzenia układu katalogów i mountów.

Porty bazy i Redis binduj do loopback. Aplikacje na hoście używają `127.0.0.1` i opublikowanego portu, nie nazw DNS usług Compose. Uruchom `docker compose config --quiet`; nie wypisuj rozwiniętej konfiguracji z hasłami. Nie włączaj publicznych tuneli ani portów routera.

Pełne kontenery aplikacji stosuj, gdy użytkownik tego chce. Wtedy oprzyj się na [oficjalnej konfiguracji Docker](https://docs.medusajs.com/learn/installation/docker), uwzględniając workspace pnpm, osobne zależności kontenera i hot reload. Rozróżnij URL wewnętrzny backendu od URL dostępnego w przeglądarce. `http://medusa:9000` nie nadaje się jako publiczny URL klienta uruchomionego w przeglądarce hosta.

## Envy i dane dostępowe

| Plik domyślny | Zawartość |
|---|---|
| `.env` | Projekt Compose, obrazy, porty i dane lokalnej bazy |
| `apps/backend/.env` | Połączenia backendu, CORS, JWT/cookie secrets |
| `apps/storefront/.env.local` | Publiczny adres backendu, publishable key, region i adres storefrontu |
| `.local/dev-credentials.json` | Lokalny login administratora i wygenerowane hasło |
| Szablony `.env.example` / `.env.template` | Te same nazwy zmiennych, bez prawdziwych sekretów |

Zachowaj konwencję szablonów startera. Rzeczywiste envy i plik credentials mają być ignorowane w Git; `git check-ignore` nie zastępuje sprawdzenia, czy sekret nie jest już śledzony. Nie przepisuj historii Git. Ogranicz uprawnienia plików z sekretami, np. do `0600` na POSIX. Nie wyświetlaj ich zawartości w logach ani raporcie.

Generuj sekrety kryptograficznym RNG: co najmniej 32 bajty dla JWT i cookie, losowe hasło bazy i administratora. Zachowuj istniejące wartości. Zmiana `POSTGRES_PASSWORD` przy istniejącym wolumenie nie zmienia hasła roli w bazie; nie naprawiaj tego usunięciem danych. Nie przechowuj hasła admina w package.json ani argumentach zapisanych w dokumentacji. Jeżeli CLI wymaga hasła w argv, nie loguj komendy z rozwiniętą wartością.

Wartości połączeń zapisuj literalnie w env konsumenta. Nie zakładaj, że dotenv, Next i Compose identycznie rozwijają odwołania do innych zmiennych. Poprawnie koduj hasło w URL PostgreSQL lub generuj hasło URL-safe. Przed operacjami na bazie sprawdź efektywną konfigurację procesu, uwzględniając zmienne powłoki mające pierwszeństwo przed plikiem.

Typowe zmienne backendu:

- `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `COOKIE_SECRET`.
- `STORE_CORS`: rzeczywisty origin storefrontu.
- `ADMIN_CORS`: origin Admina i serwera developerskiego, jeśli potrzebny.
- `AUTH_CORS`: originy storefrontu i Admina wymagane przez ich logowanie.

Nie kopiuj domen dokumentacji ani wildcardów do CORS bez potrzeby. `localhost` i `127.0.0.1` to różne originy; wybierz spójne URL-e. Zmiana portu musi dotrzeć także do polecenia uruchamiającego aplikację, CORS, redirectów i serwowania plików.

Typowe zmienne storefrontu:

- `NEXT_PUBLIC_MEDUSA_BACKEND_URL`, `NEXT_PUBLIC_MEDUSA_PUBLISHABLE_KEY`.
- `NEXT_PUBLIC_DEFAULT_REGION`: kod kraju obsługiwanego przez rzeczywisty region w bazie.
- `NEXT_PUBLIC_BASE_URL`: lokalny adres z `http`, jeżeli nie skonfigurowano TLS.

Sprawdź kod SDK i server actions: inna wersja może używać `MEDUSA_BACKEND_URL` lub innych nazw. Nie dodawaj nieodczytywanych envów. Publishable key jest publiczny; klucz administracyjny i sekrety backendu nigdy nie trafiają do `NEXT_PUBLIC_*`. Stripe, Cloud i S3 pozostaw opcjonalne, bez fałszywych kluczy mających sugerować działającą integrację.

## Medusa, Redis i pliki

Scal konfigurację z `medusa-config.ts`. Jeżeli lokalna baza wymaga wyłączenia SSL, ogranicz to do lokalnej konfiguracji; nie wyłączaj SSL uniwersalnie dla wdrożeń.

`REDIS_URL` sam nie konfiguruje modułów. Sprawdź [konfigurację Medusy](https://docs.medusajs.com/learn/configurations/medusa-config) oraz [oficjalnych providerów Redis](https://docs.medusajs.com/learn/deployment/general). Domyślnie podłącz `projectConfig.redisUrl` do sesji i natywny `@medusajs/medusa/event-bus-redis` do event busa, z wersją zgodną z backendem. Przetestuj start i działanie; nie dodawaj duplikatu modułu obecnego już w starterze.

Pozostałe moduły pozostaw zgodne ze starterem. Jeśli jego funkcje wymagają współdzielonego workflow engine lub lockingu, zastosuj aktualnych natywnych providerów Redis. Nie kopiuj historycznych nazw opcji z innych wersji. Nie dodawaj opcjonalnych feature flags i modułu cache wyłącznie dlatego, że Redis już działa. W dokumentacji setupu podaj, które funkcje korzystają z Redis, a które pozostają lokalne/in-memory.

Użyj [lokalnego providera plików](https://docs.medusajs.com/resources/architectural-modules/file/local). Sprawdź rzeczywisty katalog uploadu i publiczny `backend_url` wybranej wersji, dostępność obrazu z hosta i konfigurację Next Images. Upload wykonuj przez Medusę; samo wrzucenie pliku do katalogu nie weryfikuje providera. Ignoruj uploady w Git, zachowuj je przy restartach. Nie dodawaj MinIO lub Mailpit bez rzeczywistej potrzeby; wysyłka maili nie jest częścią lokalnego checkoutu, jeśli starter jej nie wymaga.

## Migracje i bootstrap

Sprawdź oficjalny seed i CLI wybranej wersji. Przykładowo migracje mogą działać przez `pnpm --dir apps/backend exec medusa db:migrate`, a seed przez skrypt `medusa exec`; używaj faktycznych skryptów startera i właściwego cwd. Zatrzymaj operację przy wskazaniu bazy spoza lokalnego Compose tego projektu, chyba że użytkownik wyraźnie wskazał i autoryzował inne środowisko developerskie.

Zapewnij spójne powiązania store → sales channel → publishable key oraz region → kraj/waluta/ceny, lokalizację i dostępność magazynu, fulfillment i opcję dostawy. Korzystaj z oficjalnych workflows i SDK wybranej wersji, nie bezpośrednich insertów do wewnętrznych tabel.

Przy ponowieniu sprawdzaj każdą grupę wymaganych encji i uzupełniaj brakujące. Wykorzystuj stabilne identyfikatory/handle lub własne oznaczenie danych demonstracyjnych; „istnieje jakiś produkt” nie wystarcza. Kontroluj wynik częściowo zakończonego seeda. Publikowany klucz ma obsługiwać kanał produktów wyświetlanych przez storefront. Jeśli klucza nie można ponownie odczytać, zachowaj wcześniej bezpiecznie zapisaną wartość; nie twórz nowego przy każdym starcie.

Admina utwórz tylko, gdy go brakuje. Jeśli konto istnieje, ale hasło nie jest dostępne, nie resetuj go automatycznie: podaj konkretny problem dostępu. Błędy inne niż jednoznaczne „encja istnieje” muszą przerywać bootstrap.

Stosuj kraj/walutę ustalone w projekcie; dla polskiego sklepu PL/PLN. Bez ustaleń można zachować demonstracyjny region startera. Nie ustawiaj samego `NEXT_PUBLIC_DEFAULT_REGION=pl` bez regionu i cen w bazie.

Do sprawdzenia checkoutu użyj dostępnego natywnego manualnego/systemowego providera płatności i lokalnej opcji dostawy. Zweryfikuj, że storefront potrafi je obsłużyć. W razie potrzeby dodaj minimalną obsługę istniejącego providera wyłącznie dla developmentu; nie buduj własnego systemu płatności. Nie włączaj automatycznie płatności testowych wymagających zewnętrznego konta. Ustalony brak rzeczywistej płatności lub wysyłki maila opisz jako zakres środowiska, nie jako działającą integrację.

## Polecenia i odbiór

`setup` odpowiada za przygotowanie i uzupełnianie środowiska; `dev` tylko za jego start i HMR. Wykorzystaj orkiestrator startera. Każdy skrypt ma propagować błędy, korzystać z właściwego env i sprzątać wyłącznie własne procesy. Unikaj globalnego `pkill` i dopisywania `|| true` do migracji lub seedowania.

Weryfikacja obejmuje rzeczywisty drugi setup i restart bez usuwania wolumenów. Nie zastępuj tego kontrolą składni. Zapisz wykonane polecenia, wersje CLI/Medusy/Next/Node/pnpm/obrazów oraz wyniki bez sekretów. Nie ogłaszaj gotowego środowiska, jeśli Docker, logowanie lub checkout nadal są zablokowane.
