---
name: raven-merge
description: Zmerguj PR wskazanego change Raven (np. C-03) i ustaw jego status Done na powiązanym GitHub Project. Wznawia także finalizację już zmergowanego PR; nie publikuje kodu ani nie wdraża aplikacji.
---

# Raven Merge

Stosuj [wspólną politykę ról](../raven-workflow/references/agent-policy.md) oraz [kontrakt GitHub](../raven-auto-plan/references/github-contract.md). To etap wykonawczy. Zlecenie „użyj raven-merge dla C-03” upoważnia do merge właściwego PR oraz jawnego zapisu Done dla tego change na właściwym boardzie, bez kolejnej zgody. Samo pytanie o status lub gotowość pozostaje odczytowe. Nie uruchamiaj tego skilla automatycznie po raven-pr.

Sukces wymaga dwóch potwierdzonych wyników w tej kolejności: `merged_pr` → `board_done`. Kolejka merge, włączone auto-merge, zamknięty PR lub sam kod wyjścia polecenia nie są dowodem merge. Nie kończ na samym merge.

## 1. Ustal change, PR i board przed zapisem

Odczytaj instrukcje projektu i `context/foundation/github.json`. Raven ID jest lokalne dla powiązanego repo/Project: znajdź dokładnie wskazane change issue, potwierdź jego pełny URL, etykietę, wymagania, plan, taski i istotne decyzje. Repo `repository` przechowuje artefakty; PR szukaj w `code_repository`, jeśli istnieje, w przeciwnym razie w tym samym repo. Nie wybieraj repo z bieżącego brancha ani globalnego wyniku wyszukiwania samego C-ID.

Wyszukaj wszystkie powiązane PR, również closed/merged, z paginacją. Porównaj link do issue, marker `<!-- raven:pr change=C-03 -->`, head repo/branch, base i rzeczywisty zakres diffu z całym change. Tytuł lub marker bez repo i powiązań nie wystarcza. Potwierdź docelową gałąź finalizacji według kontraktu projektu (domyślnie default branch). Sam merge do gałęzi pośredniej nie kończy change.

- Jeden jednoznaczny PR obejmujący cały change: kontynuuj. Zweryfikuj istniejące dowody odbioru i wymaganych testów dla jego wersji; nie wykonuj ponownie całego review produktu.
- Wiele PR: rozstrzygnij z istniejących decyzji, który jest finalnym PR, a które są historyczne/zastąpione lub już dostarczyły część zakresu. Gdy więcej niż jeden nadal wymaga merge albo pełny zakres pozostaje niejasny, zatrzymaj się i podaj kandydatów; nie merguj seryjnie ani nie oznaczaj całego change Done po częściowym PR.
- Brak PR, PR częściowy bez dowodu dostarczenia reszty lub closed bez merge: nie ma sukcesu. Podaj konkretny brak; nie twórz ani nie otwieraj PR przy okazji.
- PR już merged: odzyskaj dowody jego SHA, merge commit, daty i docelowej gałęzi oraz dostarczenia pełnego zakresu. Pomiń operację merge i przejdź do finalizacji boarda.

Przed merge odczytaj rzeczywisty Project wskazany w manifestcie, item powiązany z **issue change** (nie item PR ani taska), jego content node ID/URL, kanoniczne pole wskazane przez `fields.status.id` oraz jego opcję Done. Pole może nazywać się `Status` albo `Raven Status`; wybieraj je po ID z powiązania, nie po literalnej nazwie ani pierwszym pasującym polu. Na serwerze potwierdź przynależność pola do tego Project, typ single-select oraz rzeczywisty ID opcji Done zgodny z `fields.status.options`. Nie ufaj samemu manifestowi ani pierwszej stronie listy. Sprawdź dostęp do odczytu i możliwość zapisu Project, korzystając z dostępnych uprawnień konta/tokena; dla PR wymagającego merge sprawdź również uprawnienie merge w repo kodu. Już zmergowany PR wymaga tylko odczytu dowodów i uprawnień do finalizacji boarda. Sam udany odczyt nie dowodzi prawa zapisu. Brak potwierdzenia wymaganych uprawnień, itemu, pola/opcji albo rozbieżna konfiguracja blokuje merge; nazwij brak do naprawy w setupie. Nie twórz nowego boarda, pól ani zastępczego itemu. Ta kontrola ogranicza częściowy sukces, ale nie gwarantuje przyszłego zapisu po zmianie uprawnień.

## 2. Wykonaj merge sprawdzonej wersji

Dla otwartego PR odczytaj aktualny head SHA, base, draft, mergeability, wymagane reviews/checki, rulesets/branch protection i ewentualną merge queue. Sprawdź także kontrole wymagane przez zaakceptowany plan, nawet gdy repo nie wymusza ich technicznie. Brak reguł potwierdź odczytem; brak dostępu lub wynik UNKNOWN nie znaczy braku wymagań. FAIL, brak wymaganej akceptacji, konflikt lub niewykonane wymagane kontrole zatrzymują merge. Pending pozostaje oczekiwaniem. Nie naprawiaj kodu, nie zmieniaj zabezpieczeń, nie zatwierdzaj PR w imieniu reviewera i nie stosuj bypassu/admin merge.

Wybierz metodę zgodną z jawną decyzją użytkownika i polityką repo. Jeśli nie określono metody, użyj pierwszej dozwolonej w kolejności squash → merge commit → rebase; podaj wybór bez dodatkowego pytania. Jawnie wymagana, lecz niedozwolona metoda jest konfliktem do rozstrzygnięcia. Wymagana kolejka korzysta z metody skonfigurowanej dla kolejki.

Użyj dostępnego connectora/API albo `gh`, sprawdzając jego wersję i pomoc. Każda operacja musi wskazywać dokładny PR i atomowo sprawdzać oczekiwany head SHA: w `gh pr merge` służy temu `--match-head-commit SHA`; metoda to odpowiednio `--squash`, `--merge` lub `--rebase`. Dla wymaganej kolejki nie wymuszaj strategii CLI. Bez obsługi warunku SHA wybierz obsługujące go narzędzie lub zatrzymaj zapis. Bezpośrednio przed nim odśwież tożsamość, base, head i bramki; zmiana SHA wymaga ponownej oceny dowodów, nie automatycznej akceptacji nowej wersji.

Nie używaj `--admin` ani `--delete-branch`. Nie włączaj opcjonalnego auto-merge tylko dla obejścia pending. Przy wymaganej kolejce żądanie może jedynie dodać PR do kolejki: odczytuj stan, a jeśli pozostaje pending, oddaj checkpoint z URL, sprawdzonym SHA i brakującym wynikiem. Nie zgłaszaj sukcesu i nie ustawiaj Done. Przy wznowieniu najpierw odczytaj stan; nie wysyłaj kolejnego żądania dla PR już queued/merged.

Po żądaniu, także timeout/błędzie, odczytaj serwerowy stan PR, `mergedAt`, merge commit i base oraz potwierdź, że zmergowano sprawdzoną wersję. Dopiero rzeczywisty merge do właściwego celu daje `merged_pr`. Nie zakładaj, że merge commit ma SHA równe head SHA (squash/rebase mogą je zmienić). Gdy wynik pozostaje nieznany, zatrzymaj finalizację z konkretnym checkpointem.

## 3. Zapisz Done i odczytaj wynik

Po dowodzie merge ponownie potwierdź powiązanie issue → item → Project, kanoniczne pole `fields.status` i jego opcję Done, następnie **jawnie zapisz Done w tym polu**, także gdy nie istnieje automatyzacja GH. Dla `gh project item-edit` użyj odczytanych `--id`, `--project-id`, `--field-id` i `--single-select-option-id`; connector/API musi wskazywać te same zasoby. Jeśli readback wykazuje już Done (automatyzacja lub poprzednia próba), zapis jest zbędny — potwierdź idempotentne ukończenie.

Odczytaj ponownie ten sam item, jego content i wartość tego samego kanonicznego pola `fields.status.id`. Dopiero potwierdzone Done daje `board_done`. Nie zastępuj tego zamknięciem issue ani komentarzem. Nie zamykaj zbiorczo tasków i nie zmieniaj ich statusów; istniejące powiązania zamykające issues muszą dotyczyć tylko potwierdzonego zakresu PR. Nie zapisuj do Jira, nie usuwaj gałęzi i nie uruchamiaj deploya.

Merge i zapis Project nie są transakcją. Jeśli drugi krok zawiedzie, zgłoś **PR merged, finalizacja boarda nieukończona**, podaj PR/merge SHA, URL change/Project, item/field/option ID i błąd bez sekretów. Po niepewnym zapisie najpierw readback; jeśli nadal brak Done, ponów tylko ten zapis po usunięciu przyczyny. Nie merguj ponownie, nie cofaj merge i nie przenoś change na inny board. Dwie nieudane próby tego samego zapisu wystarczą: pozostaw checkpoint i konkretną blokadę zamiast nieskończonej pętli.

Zakończ linkiem do PR, dowodem merge oraz linkiem do właściwego change/Project i potwierdzonym statusem albo dokładnym brakującym krokiem. Polecenia i zachowanie kolejki: [gh pr merge](https://cli.github.com/manual/gh_pr_merge), [gh project item-edit](https://cli.github.com/manual/gh_project_item-edit). Przy różnicy wersji sprawdź aktualną pomoc; statyczny doctor Raven nie weryfikuje zdalnych uprawnień, CI ani wykonania tych operacji.
