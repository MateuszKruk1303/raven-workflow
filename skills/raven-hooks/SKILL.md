---
name: raven-hooks
description: Skonfiguruj GitHub Actions uruchamiające lint, typecheck i właściwe testy po wystawieniu lub aktualizacji PR, zgodnie ze stackiem i strategią projektu. Nie konfiguruje hooków sesji agenta.
---

# Raven Hooks

Seeduj lub uzupełnij checki GitHub Actions dla faktycznego stacku projektu. Nazwa oznacza tutaj CI po PR, nie lokalne hooki agenta. Nie implementuj testów produktu ani nie publikuj PR przy okazji setupu.

Przeczytaj [kontrakt GH](../raven-auto-plan/references/github-contract.md), instrukcje repo, manifesty/lockfile, konfigurację workspace, istniejące workflows, test-stack, strategię raven-test-plan i skrypty uruchamiania. Przyjmij wskazany change konfiguracyjny albo utwórz go zgodnie z kontraktem Raven, jeśli zlecenie nie ma jeszcze tożsamości. Nie zakładaj Node/Playwright ani pojedynczego pakietu.

## Zaprojektuj checki

Wykryj runtime i wersje, menedżer pakietów, komendy lint/format-check/typecheck, unit, integration, E2E i build, jeśli potrzebny. Dobierz checki zgodne z istniejącymi narzędziami i strategią; brak runnera/testów zgłoś jako lukę dla raven-test, nie twórz zielonego placeholdera. Nie każda warstwa musi być właściwa dla projektu.

Użyj jednego lub kilku workflow z osobnymi czytelnymi jobami według czasu i zależności, bez sztucznego mnożenia plików. Scal istniejącą konfigurację i zachowaj cudze joby. Triggery pull_request mają obejmować otwarcie, nowe commity i ponowne otwarcie PR; uwzględnij ready_for_review, jeśli filtrujesz drafty. Nie dodawaj deploya ani automatycznego merge.

Przed zapisaniem YAML zweryfikuj bieżącą składnię i wersje actions w oficjalnej dokumentacji GitHub oraz dokumentacji wykrytych narzędzi. Preferuj akcje przypięte do zweryfikowanego pełnego SHA z komentarzem wersji. Stosuj minimalne permissions, zwykle contents: read; nie uruchamiaj niezaufanego kodu PR przez pull_request_target z sekretami.

## Implementacja i sprawdzenie

- Instaluj zależności odtwarzalnie z lockfile; użyj rzeczywistych katalogów workspace, poprawnych kluczy cache i wersji runtime.
- Integration/E2E dostają izolowane usługi testowe, migracje/seed, healthcheck i cleanup. Zewnętrzne płatne/niedeterministyczne usługi zastępuj odpowiednimi fixture'ami/mockami. Nie używaj danych ani połączeń produkcyjnych.
- Dodaj timeouty, concurrency anulujące przestarzały run tego samego PR oraz diagnostykę awarii. Artefakty raportów/trace nie mogą zawierać sekretów ani prywatnych danych; ustaw rozsądną retencję.
- Testowe błędy muszą powodować FAIL joba. Nie stosuj continue-on-error, `|| true` ani pass-with-no-tests jako obejścia brakujących wymaganych kontroli. Filtry ścieżek nie mogą zostawiać wymaganych checków stale pending; nie dodawaj ich bez rozstrzygnięcia tego zachowania.
- Zweryfikuj YAML i workflow dostępnym walidatorem oraz rzeczywiste komendy lokalnie w możliwym zakresie. Jeśli walidator/środowisko są niedostępne, nazwij niewykonaną kontrolę; nie twierdź, że Actions przeszły przed rzeczywistym runem.

Zapisz konfigurację w repo i raport w change `<!-- raven:ci-setup -->`: joby, triggery, komendy, środowisko, pliki, walidacja, wymagane secrets/variables (same nazwy), ograniczenia fork PR. Ujawnij brakujące ustawienia bez wymyślania wartości. Nie zmieniaj branch protection/rulesets ani automatyzacji Done bez osobnego zlecenia; samo dodanie workflow nie oznacza, że check blokuje merge.

Handoff: co będzie uruchamiane po PR, co sprawdzono lokalnie i czego pierwszy run dopiero dowiedzie. Ponowne wywołanie aktualizuje konfigurację bez duplikatów. Nie zmieniaj kodu produktu dla zielonego CI i nie uruchamiaj raven-pr automatycznie.
