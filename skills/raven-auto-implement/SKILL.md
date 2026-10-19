---
name: raven-auto-implement
description: "Zrealizuj wskazany plan lub polecenie użytkownika, zweryfikuj zmianę na poziomie `quick`, `standard` albo `thorough` dobranym do ryzyka i podsumuj wynik wyłącznie w końcowej wiadomości czatu."
---

# Raven Auto Implement

Zrealizuj wskazany plan razem z aktualnym poleceniem użytkownika i udowodnij, że zmiana działa w stopniu odpowiednim do jej ryzyka. Polecenie doprecyzowuje lub zmienia zakres planu bez ponownego planowania, plan-review ani sprawdzania fingerprintu. Czytaj plan i kod potrzebny do zmiany; nie odtwarzaj cyklu Raven.

## Zasady

- **Wejście.** Bez wskazanego planu specyfikacją jest polecenie użytkownika; pytaj tylko, gdy cel jest niejednoznaczny. Gdy plan rozjeżdża się z rzeczywistym kodem, odejdź od niego minimalnie i opisz w finale, co zmieniłeś i dlaczego.
- **Decyzje.** Rutynowe decyzje techniczne podejmuj samodzielnie. Pytaj tylko o brakującą decyzję produktową, która rzeczywiście blokuje wykonanie, i w tym czasie kontynuuj niezależną część.
- **Wykonawca.** Pracujesz jako jeden bieżący agent: bez delegowania, osobnego planisty, testera ani QA. Jedynym wyjątkiem jest niezależne review na poziomie `thorough`. Nie dodajesz etapów, bramek akceptacji, trackingu GitHub, raportów procesowych, checkpointów ani metryk.
- **Repo.** Przed zmianami zanotuj bazowy SHA. Zachowaj cudzą pracę w working tree. Respektuj instrukcje projektu (także `context/foundation/lessons.md`, jeśli istnieje), bezpieczeństwo oraz rzeczywiste ograniczenia narzędzi i uprawnień. Instrukcje projektu (AGENTS.md) mają pierwszeństwo przed minimalizmem weryfikacji: jeśli wymagają kontroli przed commitem, wykonaj je. Commituj logiczne kroki zgodnie z konwencją projektu; bez push i PR.
- **Testy.** Najpierw wykorzystaj istniejące testy; dodaj lub dostosuj test dla luki w zmienionym zachowaniu. Po każdej poprawce ponów kontrolę, która wykryła problem.
- **Zastane awarie.** Nie naprawiaj niezwiązanych zastanych awarii testów, fixture, locatorów ani infrastruktury. Zgłoś ograniczenie i — jeśli to możliwe — sprawdź zmienione zachowanie innym adekwatnym kanałem.
- **Niewykonana lub zablokowana kontrola nigdy nie jest raportowana jako zaliczona.**

## Wybór poziomu

Przed zmianami wybierz poziom i podaj go w jednym zdaniu z powodem. Użytkownik nadpisuje go słowem `quick`, `standard` lub `thorough` w poleceniu lub w trakcie pracy. Sam w trakcie pracy możesz poziom tylko podnieść, z adnotacją w finale — nigdy obniżyć.

- `quick` — zmiana nie zmienia zachowania: copy, style, rename, config, drobny refactor. Przy wątpliwości wybierz `standard`.
- `standard` — domyślny: zwykła funkcja lub poprawka bez sygnału ryzyka.
- `thorough` — zmiana dotyka choć jednego sygnału ryzyka:
  - pieniędzy, cen, rabatów, podatków, płatności;
  - koszyka, checkoutu, zamówień, stanów magazynowych;
  - auth, sesji, uprawnień, danych osobowych;
  - schematu DB, migracji, seedów;
  - kontraktu API między storefrontem a backendem;
  - modułu współdzielonego przez kilka obszarów;
  - usuwania lub nadpisywania danych.

Na poziomie `thorough` przeczytaj i wykonaj [references/thorough.md](references/thorough.md) zamiast kroków `quick` i `standard`; sekcje „Sprawdzenie działania”, „Budżet czasu” i „Finał” obowiązują nadal.

## `quick`

Ma udowodnić: zmiana się kompiluje i nie psuje istniejących testów.

1. Implementacja.
2. Typecheck dotkniętego workspace (np. tylko `apps/storefront`).
3. Istniejące testy zmienionych plików lub modułów.
4. Render tylko przy zmianie wizualnej.

Orientacyjny narzut weryfikacji: ~1–3 min.

## `standard`

Ma udowodnić: zmieniona funkcja działa w uruchomionej aplikacji.

1. Wszystko z `quick`.
2. Sprawdzenie działania (niżej) — happy path zmienionego zachowania.

Orientacyjny narzut weryfikacji: ~5–10 min (+~2 min przy zimnym starcie aplikacji).

### Sprawdzenie działania

Testy nie zastępują sprawdzenia, że funkcja działa. Uruchom aplikację (lub skorzystaj z już działającej) i przejdź zmienioną funkcję tak, jak zrobi to użytkownik lub klient API:

- UI → izolowana sesja Playwright i obserwowalny efekt na ekranie, według [wskazówek UI](references/browser-review.md);
- API/backend → wywołanie lokalnego endpointu i sprawdzenie odpowiedzi;
- logika bez interfejsu → test lub krótki skrypt wywołujący zmieniony kod.

Zapis danych potwierdź ponownym odczytem (reload, ponowny GET, widok w adminie). Scenariusze błędów sprawdzaj tylko, gdy zmiana dotyczy obsługi błędów albo wykryłeś problem. Gdy aplikacji nie da się uruchomić, wpisz to w finale jako ograniczenie, nie zaliczenie; jeśli to możliwe, sprawdź zachowanie innym kanałem i jasno opisz, co on faktycznie potwierdza.

## Budżet czasu

Narzuty są orientacyjne, nie limitem. Gdy weryfikacja wyraźnie przekracza narzut poziomu (np. ponad dwukrotnie), nie rozszerzaj jej dalej bez konkretnego wykrytego problemu, a w finale wskaż, co zajęło czas.

## Finał

Wynik podaj wyłącznie w końcowej wiadomości czatu; nie zapisuj ani nie kopiuj go do Markdown, planu, issue ani PR i nie twórz acceptance.md. Nie uruchamiaj kolejnego etapu. Finał zawiera:

- poziom (i ewentualne podniesienie z powodem);
- co zmieniono, w tym odejścia od planu (co, dlaczego);
- co sprawdzono — na `standard` także co konkretnie zaobserwowano i jakim kanałem;
- ograniczenia: niewykonane lub zablokowane kontrole i to, co pozostaje do sprawdzenia;
- instrukcję odbioru krok po kroku: konkretne akcje lub polecenia i oczekiwany efekt, ze szczegółowością dobraną do zmiany.

Przy blokadzie również podaj podsumowanie i instrukcję, jasno wskazując braki.
