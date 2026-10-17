---
name: raven-github-setup
description: "Przygotuj lub uzupełnij wskazane repo GitHub i politykę publikacji Raven. Przygotuj wymagany tracking issues; Project jest opcjonalny."
---

# Raven Github Setup

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Ustal rzeczywisty zakres setupu: remote/repo, polityka publikacji i wymagany tracking GitHub Issues. Zweryfikuj Issues oraz etykiety in-progress/blocked (lub ich istniejące mapowanie), utwórz tylko brakujące elementy objęte setupem. Nie twórz testowych tasków ani Project jako domyślnej infrastruktury.

Odczytaj remotes, instrukcje, `.raven/config.json` i historyczne `context/foundation/github.json`, jeśli wskazane. Zweryfikuj tożsamość konta i pełne owner/repo bez ujawniania tokenów. Wybierz cel z jawnego wskazania, istniejącego powiązania lub jednoznacznego remote; konflikty rozstrzygnij przed zapisem. Brak dostępu nie oznacza braku zasobu.

Zlecone nowe repo twórz prywatne. Zachowaj widoczność istniejącego repo, chyba że użytkownik wyraźnie zleci jej zmianę. Dla poufnych artefaktów wybierz zatwierdzone prywatne miejsce; prywatny Project nie ukrywa treści publicznego repo. Nie kopiuj danych firmy do osobistego repo przez domysł.

Zapisz `.raven/config.json` zgodnie z kontraktem pracy: repository, publication i tracker typu github-issues z nazwami etykiet. Domyślny `mode: local` nie upoważnia do push/PR. `draft-pr` i `authorized_by` zapisuj tylko dla rzeczywiście udzielonej polityki z jej zakresem i źródłem. Nie traktuj setupu ani tokena jako zgody publikacji produktu.

Jeżeli zlecono Project, odczytaj istniejące zasoby/pola/opcje po ID z paginacją; zachowaj ludzkie statusy i automatyzacje. Potwierdź prywatność, uprawnienia i readback osobno dla repo i Project. Utwórz wyłącznie brakujące zlecone elementy; nie usuwaj cudzych pól, nie włączaj auto-add/auto-close. Utrwal opcjonalne mapowanie w konfiguracji jako widok tych samych issues, bez drugiego stanu wykonania. [Referencja](references/github-contract.md) opisuje granice.

Nie commituj/pushuj, nie twórz testowych issues/PR, nie konfiguruj sekretów, CI, branch protection ani deploya przy okazji. Oddaj wynik odczytu i konkretne pozostałe braki. Nie migruj historycznych artefaktów ani nie uruchamiaj roadmapy automatycznie.
