---
name: raven-medusa-ecommerce-init
description: "Inicjalizuj lub dokończ lokalne monorepo Medusa + Next.js z oficjalnego startera: Docker Compose, envy, migracje, seed, admin i działający storefront. Używaj do przygotowania środowiska ecommerce przed implementacją produktu; nie do wdrożenia produkcyjnego."
---

# Raven Medusa Ecommerce Init

Uruchom kompletne środowisko developerskie w bieżącym katalogu projektu. Domyślnie aplikacje działają na hoście z hot reload, a PostgreSQL i Redis w Docker Compose. Każdy sklep jest osobną aplikacją, repozytorium i zestawem danych. Reużywalny jest ten workflow.

## Wynik

- Oficjalny starter Medusa: backend i Admin w `apps/backend`, Next.js w `apps/storefront`, wspólny workspace i lockfile.
- Zgodne wersje Node LTS i pnpm zapisane w projekcie; zachowana orkiestracja startera.
- PostgreSQL i Redis z healthcheckami oraz trwałymi, odizolowanymi wolumenami.
- Rzeczywiste lokalne pliki env, bezpieczne sekrety, konto administratora i publishable key storefrontu.
- Migracje, przykładowy katalog, region, ceny, dostawa lokalna oraz lokalny checkout z manualnym/systemowym providerem płatności dostępnym w wybranej wersji.
- Polecenia do setupu, developmentu, zatrzymania i wznowienia oraz sprawdzony przepływ produkt → koszyk → zamówienie.

Nie dodawaj drugiego backendu, ORM, systemu autoryzacji, CMS ani własnego frameworka ecommerce. Nie implementuj wymagań konkretnego sklepu, integracji kurierskich, płatności na żywo ani infrastruktury produkcyjnej. Nie uruchamiaj `raven-init-stack`: to inny stack. Samo tworzenie lub edytowanie tego skilla nie oznacza polecenia inicjalizacji aplikacji.

## 1. Rozpoznaj projekt i aktualny starter

Przeczytaj lokalne `AGENTS.md`, istniejące manifesty i ustalenia projektu. Zachowaj `context/`, instrukcje agenta, `.git` i pliki użytkownika. PRD ani inne skille Raven nie są warunkiem uruchomienia. Nazwę wywnioskuj z projektu lub argumentu użytkownika; sprowadź ją do poprawnego sluga, nie interpretuj jako ścieżki lub kodu powłoki.

Przed generowaniem sprawdź aktualne źródła:

- [Next.js starter](https://docs.medusajs.com/resources/nextjs-starter)
- [create-medusa-app](https://docs.medusajs.com/resources/create-medusa-app)
- [Oficjalny starter DTC](https://github.com/medusajs/dtc-starter)
- [Docker](https://docs.medusajs.com/learn/installation/docker)

Użyj oficjalnego monorepo wskazanego przez aktualną dokumentację. Nie wybieraj historycznego, osobnego `nextjs-starter-medusa`, jeżeli dokumentacja oznacza go jako deprecated. Sprawdź rzeczywiste `engines`, `packageManager`, skrypty, envy i konfigurację startera: wymagania pakietów mogą być ostrzejsze od ogólnej strony instalacji.

Sprawdź Git, zgodny Node, pnpm, Docker Compose v2, działający daemon i dostępność portów. Nie zmieniaj globalnego toolchainu innych projektów. Użyj istniejącego managera wersji lub podaj konkretny brak. Gdy Docker nie działa, możesz przygotować pliki, ale nie deklaruj zakończonego setupu.

Rozwiąż i zapisz konkretną wersję generatora, sprawdź jej `--help`. Przykładowy kierunek, dopiero po potwierdzeniu flag:

```sh
pnpm dlx create-medusa-app@<wersja-cli> <nazwa> --with-nextjs-starter --skip-db --no-browser --use-pnpm
```

`--version` generatora może ustawiać wersję pakietów Medusy; nie traktuj tej flagi jako zwykłego wypisania wersji CLI. `--directory-path` może oznaczać katalog nadrzędny projektu. Sprawdź semantykę zamiast zgadywać.

## 2. Utwórz lub uzupełnij monorepo

Dla nowego projektu wygeneruj starter w osobnym katalogu tymczasowym poza docelowym repozytorium. Porównaj ścieżki i przenieś wynik do bieżącego katalogu, bez zagnieżdżania całego projektu w dodatkowym folderze. Nie kopiuj `.git`, `node_modules` ani artefaktów buildu. Instalację zależności wykonaj w miejscu docelowym. Scal istniejące pliki zamiast nadpisywać je w ciemno; sprawdzaj cele symlinków przed zapisem.

Dla istniejącego monorepo Medusy uzupełnij brakujące elementy bez regeneracji, automatycznego upgrade'u i rotowania sekretów. Jeśli katalog zawiera inną aplikację lub konfliktu nie można bezpiecznie scalić, przedstaw konkretny konflikt. Nie usuwaj projektu, by wymusić uruchomienie CLI. Po awarii popraw przyczynę przed ponowieniem; nie powtarzaj generowania na częściowym wyniku.

Zachowaj nazwy workspace'ów i strukturę oficjalnego startera, ustaw prywatny root workspace. Inicjalizuj Git tylko jeśli katalog nie należy do repozytorium/worktree; nie wykonuj automatycznie commitów, pushów ani tworzenia repozytorium zdalnego. Zatrzymaj wyłącznie własne procesy generatora, jeśli CLI zostawiło je uruchomione.

## 3. Podłącz infrastrukturę i envy

Przeczytaj [local-development.md](references/local-development.md) przy konfigurowaniu usług, envów i seedowania. Wykorzystaj [compose.local.yaml](assets/compose.local.yaml) i [compose.env.example](assets/compose.env.example) jako bazę; dostosuj je do zastanego projektu i potwierdzonych wersji.

Utwórz zarówno śledzone szablony, jak i rzeczywiste ignorowane pliki env. Domyślne porty: storefront 8000, backend/Admin 9000, PostgreSQL 5432, Redis 6379, Admin HMR 5173, jeśli używany. Przy kolizji wybierz wolny port i spójnie zmień komendy, URL-e, CORS oraz konfigurację uploadów. Nie zabijaj obcych procesów. Sam wpis `PORT` nie wystarcza: potwierdź, że skrypt go odczytuje.

Skonfiguruj Redis w kodzie Medusy, nie tylko w env: sesje i natywny event bus Redis, zgodnie z bieżącymi API. Zachowaj pozostałe moduły startera. Skonfiguruj lokalny provider plików bez zależności od S3. Sekrety generuj losowo i zachowuj przy ponowieniu.

## 4. Przygotuj dane i wygodne polecenia

Sprawdź konfigurację Compose bez wypisywania sekretów, uruchom usługi i poczekaj na healthchecki z ograniczonym czasem oczekiwania. Przed migracjami i seedem potwierdź, że efektywny `DATABASE_URL` wskazuje lokalną bazę tego projektu, nie odziedziczoną bazę zewnętrzną. Użyj oficjalnych migracji i mechanizmów seedowania wybranej wersji.

Zapewnij administratora, katalog, region z cenami, kanał sprzedaży, stany magazynowe oraz opcję dostawy i lokalnej płatności wystarczające do zamówienia. Publishable key musi być powiązany z właściwym kanałem i zapisany w env storefrontu. Dane logowania zapisz w ignorowanym pliku z ograniczonym dostępem; w raporcie podaj jego ścieżkę, nie hasło.

Setup musi być bezpieczny przy ponownym i częściowym wykonaniu. Nie zakładaj idempotencji oficjalnego seeda: sprawdź jego kod i rzeczywiste encje przed tworzeniem. Nie uznawaj dowolnego produktu ani samego pliku znacznika za dowód pełnego bootstrapu. Nie resetuj istniejących haseł, zamówień, kluczy ani wolumenów. Nie maskuj błędów połączenia jako „już istnieje”.

Dodaj lub dostosuj polecenia root workspace:

| Polecenie | Zachowanie |
|---|---|
| `pnpm run setup` | Zależności/infrastruktura, lokalne envy, migracje i bezpieczny bootstrap; można ponowić |
| `pnpm dev` | Zapewnia działającą infrastrukturę, uruchamia backend i storefront z hot reload; bez reseedowania |
| `pnpm infra:up` | Uruchamia PostgreSQL i Redis, czeka na gotowość |
| `pnpm infra:down` | Zatrzymuje Compose z zachowaniem danych |
| `pnpm infra:logs` | Logi usług |
| `pnpm db:migrate` | Migracje lokalnej bazy |
| `pnpm db:seed` | Bezpieczny bootstrap danych developerskich |

Zachowaj istniejące odpowiedniki i orkiestrator, jeśli realizują ten kontrakt. Skrypty uruchamiaj z właściwym cwd/env i propaguj błędy. `Ctrl+C` powinno kończyć oba własne procesy aplikacji; opisz, że infrastruktura pozostaje uruchomiona do `infra:down`. Nie dodawaj rozbudowanego process managera. Reset danych, jeśli opisany, ma być oddzielną, wyraźnie destrukcyjną operacją; nigdy nie wykonuj go jako weryfikacji setupu.

## 5. Zweryfikuj gotowość

Nie kończ na istnieniu plików. Sprawdź:

1. Zdrowe kontenery, endpoint zdrowia backendu, dostępność Admina i storefrontu, poprawne logowanie administratora.
2. Store API akceptuje publishable key, storefront pokazuje produkty i ceny we właściwym regionie.
3. W przeglądarce: produkt → wariant → koszyk → checkout z lokalną dostawą i manualną/systemową płatnością → zapisane zamówienie. Nie wykonuj rzeczywistej płatności. Brak wsparcia UI lub przeglądarki zgłoś; test API nie jest dowodem przejścia UI.
4. Upload lokalnego obrazu przez Medusę i jego wyświetlenie; hot reload backendu i storefrontu.
5. Drugie `pnpm run setup` nie dubluje danych ani kluczy. Zatrzymanie i ponowny start zachowują admina, katalog, zamówienie i upload. Nigdy `down -v` ani `docker system prune`.
6. Istniejące kontrole typów/build adekwatne do zmian. Nie dodawaj pełnego frameworka testowego tylko na potrzeby inicjalizacji.

Zapisz krótką instrukcję startu w README projektu: wersje, polecenia, URL-e, lokalizacje envów i danych logowania, zatrzymywanie/wznawianie, wykonane kontrole i braki. Nie zapisuj sekretów. Sam setup nie oznacza ukończenia biznesowego taska roadmapy ani gotowości produkcyjnej.

W odpowiedzi podaj polecenie startu, URL storefrontu i Admina, lokalizację danych logowania oraz wynik weryfikacji. Wyraźnie oznacz niewykonane kontrole i blokery; manualny checkout lokalny nie oznacza podłączonych płatności online.
