# Zgodność odsyłacza do kontraktu

Aktualny kontrakt to [praca Git-first](../../raven-workflow/references/change-contract.md). Czytaj go dla planów, postępu, review, uprawnień i publikacji. Ten plik zachowuje ścieżkę historycznych odsyłaczy; nie ustanawia osobnego transportu artefaktów.

Plan, checklistę i checkpoint przechowuj w repo. GitHub PR służy współpracy i CI; Issues są wymaganym trackerem, Project opcjonalnym widokiem. Nie twórz snapshotów planu ani issues dla faz; jeden issue odpowiada jednemu taskowi/change. Historyczne snapshoty pozostają dowodami swojej epoki; nie migruj ich automatycznie ani nie uruchamiaj helpera snapshot_fingerprint.py do nowych planów.
