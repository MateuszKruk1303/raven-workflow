---
name: raven-github-setup
description: "Przygotuj lub uzupełnij repo GitHub do pracy na taskach: remote, włączone Issues, etykiety in-progress/blocked; Project tylko na zlecenie."
---

# Raven GitHub Setup

Stosuj [pracę na taskach GitHub](../raven-workflow/references/git-workflow.md).

1. **Cel.** Repo z jawnego wskazania albo jednoznacznego remote; konflikt rozstrzygnij przed zapisem. Sprawdź konto (`gh auth status`) i owner/repo bez ujawniania tokenów. Brak dostępu nie oznacza braku zasobu.
2. **Repo.** Zlecone nowe repo twórz jako prywatne; widoczności istniejącego nie zmieniaj bez polecenia. Poufnych treści firmy nie umieszczaj w osobistym repo przez domysł.
3. **Issues.** Sprawdź, że są włączone, oraz etykiety `in-progress` i `blocked` (albo ich istniejące odpowiedniki). Utwórz tylko brakujące.
4. **Project (opcjonalnie, na zlecenie).** Widok tych samych issues, nie drugi stan pracy. Pola i opcje mapuj po ID, zachowaj istniejące statusy i automatyzacje.

Nie twórz testowych issues ani PR, nie konfiguruj sekretów, CI, branch protection ani deploya przy okazji. W czacie: repo, wynik odczytu po zapisie i pozostałe braki.
