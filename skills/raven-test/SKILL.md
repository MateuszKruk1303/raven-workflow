---
name: raven-test
description: "Zapewnij trwałą ochronę testami dla change, bugfixu lub refaktoru: wykorzystaj istniejące testy, dopisz tylko brakujące, a przed ryzykowną zmianą zabezpiecz obecne zachowanie (before-change)."
---

# Raven Test

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md) i [dyscyplinę wykonania](references/implementation-discipline.md).

Jedyny skill do trwałych testów. Na żądanie: domknięcie regresji po zmianie, osobne zadanie testowe albo ochrona przed zmianą. `raven-auto-implement` sam dopisuje testy potrzebne do swojej zmiany; ten skill jest na dodatkowe lub osobne potrzeby.

## Kroki

1. **Mapa.** Dla każdego AC (z issue, planu lub polecenia) i istotnego ryzyka ustal: jaki istniejący test go chroni i jaką asercją. Brak takiego testu to nazwana luka. Expected wyprowadzaj z wymagań, nie z outputu implementacji.
2. **Luki.** Dopisuj testy tylko dla nazwanych luk. Dobra istniejąca ochrona zostaje bez zmian i bez duplikatów. Najtańsza skuteczna warstwa: unit dla logiki, integration dla granic DB/usług/API, E2E dla realnego przepływu w UI. Nie dodawaj frameworka ani warstw na zapas.
3. **E2E.** Gdy potrzebne, czytaj tylko potrzebne: [setup Playwright](references/procedures/e2e-setup/procedure.md) i [pisanie testów](references/procedures/e2e/procedure.md). Dla nowego zachowania prowadzonego testem: [TDD](references/procedures/tdd/procedure.md).
4. **Skuteczność.** Każdy nowy test musi móc nie przejść: niezależne Expected, sensowna asercja skutku, izolacja i cleanup, mocki tylko na zewnętrznych granicach. Przy niepewności zrób kontrolowaną perturbację kodu i bezwarunkowo ją cofnij. Nie osłabiaj asercji dla zielonego wyniku.
5. **Uruchomienie.** Nowe i zmienione testy plus zależne regresje. Pełną suite tylko z konkretnego powodu.

## Before-change

Przed refaktorem bez ochrony: test charakteryzacyjny utrwala świadomie chronione zachowanie, nie przypadkowy błąd. Dla bugfixu test na starym kodzie może zakończyć się `EXPECTED_RED`: podaj asercję, obserwowany błąd i źródło oczekiwania. Błąd runnera lub środowiska nie dowodzi reprodukcji.

## Defekt produktu

Wykryty defekt w zakresie zlecenia napraw proporcjonalnie i podaj w czacie aktualną instrukcję odbioru. Defekt poza zakresem zgłoś bez naprawy.

## Finał

W czacie: mapa AC → test, zamknięte i otwarte luki, uruchomione polecenia z wynikiem. **Zakończenie bez nowych testów jest poprawne**, gdy mapa pokazuje wystarczającą ochronę. Testy commituj w logicznych krokach. Nie publikuj PR z samego zlecenia testów.
