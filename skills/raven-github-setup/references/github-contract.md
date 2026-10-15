# Powiązanie GitHub dla Ravena

## Lokalny manifest

Plik `context/foundation/github.json`, schema_version 1. ID i URL pochodzą z rzeczywistych odpowiedzi GitHuba, nigdy z domysłów. Null oznacza brak potwierdzonej wartości. Przykładowy kształt, nie gotowa konfiguracja:

```json
{
  "schema_version": 1,
  "setup_status": "partial",
  "repository": {
    "host": "github.com",
    "owner": null,
    "name": null,
    "node_id": null,
    "url": null,
    "visibility": null
  },
  "project": {
    "owner": null,
    "owner_type": null,
    "number": null,
    "node_id": null,
    "url": null,
    "visibility": null,
    "repository_link_verified": false
  },
  "fields": {
    "status": {"id": null, "name": null, "type": "SINGLE_SELECT", "options": {}},
    "order": {"id": null, "name": "Raven Order", "type": "NUMBER"},
    "identity": {"id": null, "name": "Raven ID", "type": "TEXT"}
  },
  "labels": {
    "change": {"name": "raven:change", "id": null},
    "task": {"name": "raven:task", "id": null}
  },
  "relationships": {
    "parent_child": "native_sub_issues",
    "dependencies": "native_issue_dependencies",
    "verification": "not_checked"
  },
  "views": {"status": "pending", "urls": []},
  "pending": [],
  "verified_at": null
}
```

W `fields.status.options` zapisz mapowanie nazwa → rzeczywisty option ID. `owner_type`: User lub Organization według API. Widoczność ma być private w obu zasobach. `verified_at` to czas rzeczywistego odczytu w ISO 8601; `pending` zawiera konkretne brakujące elementy i powody, bez sekretów. Nie zapisuj tablic zadań, ich statusów, bieżących sesji ani bezwzględnych ścieżek komputera.

## Narzędzia i ograniczenia

Preferuj connector GitHub lub zainstalowany `gh`. Sprawdź wersję i pomoc odpowiedniego polecenia przed mutacją. Operacje repo, Projects oraz issues mogą mieć różne uprawnienia. REST numeric issue ID, numer issue i GraphQL node ID nie są zamienne.

- Repo: `gh repo view`, `gh repo create --private`, `gh repo edit` dla włączenia Issues. Nie używaj `--push` w samym setupie.
- Project: `gh project list/create/view/link/field-list/field-create`. Tworzenie pól obsługuje TEXT, NUMBER, SINGLE_SELECT; odczytaj istniejące opcje przed ich zmianą.
- Jeśli zmiana istniejącego Status lub widoków nie jest dostępna w CLI, sprawdź aktualną dokumentację API. Nie usuwaj pola, by odtworzyć je z nowymi opcjami. Nie twierdź, że tworzenie nowego pola zmieniło wbudowany Status.
- Repo linkage nie dodaje automatycznie issues; późniejsze publikowanie korzysta z item-add lub odpowiedniego API.
- Native sub-issues i issue dependencies są odrębnymi API. Setup deklaruje kontrakt i rozpoznaje dostępność; dopiero publikacja rzeczywistych tasków tworzy relacje i weryfikuje mutacje.
- Uprawnienia i limity zależą od hosta oraz rodzaju tokenu. Przy odmowie 403/404 sprawdź cel i dostęp, nie uznawaj automatycznie zasobu za nieistniejący.

## Oficjalne źródła

Sprawdzone przy tworzeniu skilla 2026-10-14; przy niezgodności poleceń lub zmianie API użyj aktualnej dokumentacji.

- [Projects CLI](https://cli.github.com/manual/gh_project)
- [Tworzenie pól](https://cli.github.com/manual/gh_project_field-create)
- [Powiązanie Project z repo](https://cli.github.com/manual/gh_project_link)
- [Dodawanie issue do Project](https://cli.github.com/manual/gh_project_item-add)
- [Sub-issues REST](https://docs.github.com/en/rest/issues/sub-issues)
- [Issue dependencies REST](https://docs.github.com/en/rest/issues/issue-dependencies)
- [Widoczność Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-projects/managing-visibility-of-your-projects)

## Sprawdzenie ponownego uruchomienia

Rozważ przed zakończeniem: pusty projekt; istniejące prywatne repo bez Project; kompletny setup; częściowy zapis po utworzeniu Project; konflikt pola; publiczne repo lub Project; brak scope Projects. Żaden z tych stanów nie uzasadnia duplikacji, publikacji kodu ani resetowania istniejącej kolejki. Nie wykonuj zdalnych mutacji tylko po to, by przetestować skill podczas jego tworzenia.
