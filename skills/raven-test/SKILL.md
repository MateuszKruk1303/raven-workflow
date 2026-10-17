---
name: raven-test
description: "Dodaj lub popraw trwałe testy w osobnym zleceniu, zabezpiecz refaktor albo reprodukcję błędu. Normalna implementacja Raven tworzy testy w swoim zakresie; ten skill nie jest obowiązkowym późnym etapem."
---

# Raven Test

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przyjmij change, lokalny plan, PR lub jasno opisany zakres testów. Odczytaj wymagania, kod, istniejący runner, strategię i dowody. Expected pochodzi z wymagań, nie z kopiowania aktualnego outputu. Przeczytaj [źródła i review testów](references/test-review.md); dla ochrony przed zmianą [before-change](references/before-change.md).

Dobierz najtańszą skuteczną warstwę: unit dla logiki, integration dla granic DB/usług/API, E2E dla rzeczywistego przepływu/UI. Brak globalnej strategii nie blokuje konkretnego testu. Nie twórz kolejnej infrastruktury lub testów każdej warstwy dla statystyki. Jeśli istniejąca ochrona wystarcza, przedstaw jej dowód.

Realizuj [dyscyplinę implementacji](../raven-implement/references/procedures/implement/procedure.md). Dla E2E czytaj wyłącznie potrzebne [setup](references/procedures/e2e-setup/procedure.md) i [wykonanie](references/procedures/e2e/procedure.md). Zachowaj seed, izolację danych, cleanup i powtórny przebieg potrzebny do sprawdzenia izolacji. Nie kopiuj prywatnej sesji użytkownika do repo lub CI.

Uruchom nowe/zmienione testy i właściwe regresje. Kontrolowane zepsucie zachowania stosuj, gdy rozstrzyga ryzyko pozornej asercji, w izolacji z bezwarunkowym przywróceniem. Błąd składni nie jest dowodem ochrony reguły biznesowej. Nie osłabiaj Expected po ujawnieniu defektu. Potwierdzony defekt produktu w już zleconym zakresie napraw w ramach autoryzacji; poza nim zgłoś reprodukcję i potrzebną decyzję. Dwie nieskuteczne próby jednego problemu zatrzymują pętlę.

Zapisz `test-report.md` obok planu: źródła/wersje, fingerprint, base/head/tree, macierz kryterium/ryzyko → test → warstwa → wynik, polecenia, wykorzystane pokrycie i luki. Aktualizuj checklistę/checkpoint. Samodzielny manualny etap kończy się raportem; osobne raven-test-review wywołuje się na zlecenie lub według ryzyka. Gdy testy są częścią normalnego change, jego jedno review obejmuje je razem z kodem. Nie odtwarzaj dodatkowego obowiązkowego cyklu test-review przed PR.
