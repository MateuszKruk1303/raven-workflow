# TDD dla odpowiedniego kroku

Ta wewnętrzna procedura realizuje zaakceptowane zachowanie red → green → refactor według [kontraktu Git-first](../../../../raven-workflow/references/change-contract.md). Wykorzystuje lokalny plan/Progress/checkpoint. Nie udaje test-first dla gotowej implementacji.

1. Potwierdź kontrakt/fingerprint, bazę/drzewo, istniejący runner i źródło Expected. Sprawdź, czy zachowanie jeszcze nie istnieje i może być sensownie prowadzone testem. Scaffolding, konfiguracja i czyste dopracowanie wizualne zwykle wymagają innej kontroli; gotowy kod testuj normalnie przez raven-test/implement.
2. **RED:** napisz najmniejszy test następnego zachowania. Uruchom go i potwierdź konkretną asercję, nie błąd składni/importu/środowiska. Dla bugfixu Expected pochodzi z wymagań; before-change może zakończyć się udokumentowanym EXPECTED_RED.
3. **GREEN:** napisz minimalną poprawną implementację. Nie obchodź asercji, nie hardcoduj fixture ani nie rozluźniaj wymagań. Uruchom test i właściwe bliskie regresje.
4. **REFACTOR:** upraszczaj przy green, zachowując kontrakt i ochronę. Nie rozszerzaj zakresu o przyszłe abstrakcje. Powtarzaj dla kolejnego zachowania, aż krok i jego AC są spełnione.
5. Sprawdź skuteczność testów: oczekiwania niezależne od kodu, sensowne granice/błędy, izolacja i cleanup, najmniejsza skuteczna warstwa. Unikaj kopiowania produkcyjnych obliczeń, nadmiernego mockowania wnętrzności i snapshotów jako substytutu reguł biznesowych.
6. Wykonaj wymagane kontrole kroku, celowy staging własnych kodu/testów/dokumentów i logiczny commit w zleconym zakresie. Nie wymuszaj commitu dla każdej asercji ani zgody na jego tekst. Zapisz wyniki i Progress poza kontraktem. Odbiór człowieka nie wynika z GREEN.

Minor mieści się w kontrakcie; Structural wraca do decyzji. Dwie nieskuteczne próby tego samego problemu zatrzymują zależną pętlę z reprodukcją. Powrót do zwykłej implementacji nie resetuje postępu ani liczników. Końcowe niezależne review change obejmuje wymagania, kod i testy; nie uruchamiaj dodatkowego obowiązkowego test-review.
