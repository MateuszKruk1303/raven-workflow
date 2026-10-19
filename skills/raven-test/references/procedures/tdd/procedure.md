# TDD dla odpowiedniego kroku

Ta wewnętrzna procedura realizuje uzgodnione zachowanie red → green → refactor według [pracy na taskach GitHub](../../../../raven-workflow/references/git-workflow.md). Nie udaje test-first dla gotowej implementacji.

1. Potwierdź wymaganie, istniejący runner i źródło Expected. Sprawdź, czy zachowanie jeszcze nie istnieje i może być sensownie prowadzone testem. Scaffolding, konfiguracja i czyste dopracowanie wizualne zwykle wymagają innej kontroli; gotowy kod testuj normalnie krokami raven-test (mapa AC → test, luki).
2. **RED:** napisz najmniejszy test następnego zachowania. Uruchom go i potwierdź konkretną asercję, nie błąd składni/importu/środowiska. Dla bugfixu Expected pochodzi z wymagań; before-change może zakończyć się udokumentowanym EXPECTED_RED.
3. **GREEN:** napisz minimalną poprawną implementację. Nie obchodź asercji, nie hardcoduj fixture ani nie rozluźniaj wymagań. Uruchom test i właściwe bliskie regresje.
4. **REFACTOR:** upraszczaj przy green, zachowując kontrakt i ochronę. Nie rozszerzaj zakresu o przyszłe abstrakcje. Powtarzaj dla kolejnego zachowania, aż krok i jego AC są spełnione.
5. Sprawdź skuteczność testów: oczekiwania niezależne od kodu, sensowne granice/błędy, izolacja i cleanup, najmniejsza skuteczna warstwa. Unikaj kopiowania produkcyjnych obliczeń, nadmiernego mockowania wnętrzności i snapshotów jako substytutu reguł biznesowych.
6. Wykonaj wymagane kontrole kroku, celowy staging własnych kodu/testów/dokumentów i logiczny commit w zleconym zakresie. Nie wymuszaj commitu dla każdej asercji ani zgody na jego tekst. Odbiór człowieka nie wynika z GREEN.

Drobna korekta mieści się w zakresie; zmiana struktury wraca do decyzji. Dwie nieskuteczne próby tego samego problemu zatrzymują pętlę z reprodukcją.
