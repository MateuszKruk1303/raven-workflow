---
name: raven-pr
description: "Opublikuj lub aktualizuj PR konkretnego change po domknięciu regresji. Jawne wywołanie oznacza odbiór jednoznacznej wersji; wczesny nieodebrany draft pozostaje osobnym trybem."
---

# Raven Pr

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Jawne wywołanie `raven-pr <id>` dla jednoznacznie wskazanego change i wersji oznacza **odbiór tej wersji przez użytkownika oraz zgodę na zwykły push i utworzenie/aktualizację właściwego PR**. Nie pytaj ponownie o tę samą decyzję. Zapisz jej rzeczywiste źródło, zakres i wersję w `user_acceptance`; agent rejestruje decyzję, nie tworzy jej sam. Przy kilku change/wersjach ustal wskazanie przed zależnym zapisem. Sam PASS, status, istnienie PR, polityka automatycznego draftu ani wywołanie auto/test nie są odbiorem. Jawnie nieodebrany draft również nie oznacza odbioru.

1. Ustal plan/issue, repo, branch, base/head/tree i własny zakres diffu; sprawdź staging/cudze zmiany. Znajdź właściwy PR po repo/head/base i powiązaniu z planem. Nie wyciągaj repo z samego ID i nie twórz duplikatu po timeout.
2. **Krótki preflight:** sprawdź wykonaną implementację, zakończenie raven-test lub równoważny historyczny audyt z rzeczywistymi dowodami i oceną wystarczalności oraz ich aktualność. Odczytaj aktualne osobno zlecone code review oraz wyniki QA, jeśli wymaga go odrębne jawne zlecenie lub bramka projektu/kontraktu; nie uruchamiaj pełnej weryfikacji ponownie. Samo historyczne `qa_required: true` lub tryb auto nie tworzy bramki QA; zachowaj historię. Ukończony auto-implement nie zastępuje code review ani domknięcia regresji. Brak testów, etapu albo wymaganych dowodów nazwij konkretnie i zapytaj dokładnie: **„Czy utworzyć PR mimo braku [konkretny brak] dla tego change?”** Po zgodzie publikuj z jawnymi brakami, bez fikcyjnego PASS; zgoda nie omija merge/CI. Brak implementacji pozwala tylko na jawnie ustalony incomplete draft. Jeżeli zgoda na konkretny brak już istnieje, zachowaj ją bez kolejnego pytania.
3. Przygotuj logiczne commity własnego kodu/testów/dokumentów, celowy staging i zwykły push do autoryzowanej gałęzi. Nie force-pushuj ani nie dołączaj cudzej pracy. Powiąż odebraną wersję roboczą z utworzonym commitem, sprawdzając brak zmiany treści w odbieranym zakresie. Nie przenoś odbioru na niezaakceptowaną functional delta.
4. Opisz problem i wynik, dokładny issue oraz wersjonowany plan, zakres, walidację i pozostałe luki. Użyj rzeczywistych markerów `<!-- raven-change:<id> -->` i `<!-- raven-issue:OWNER/REPO#N -->`. Linkuj issue bez closing keywords. Nie kopiuj raportów do komentarzy; dla CLI używaj body-file. Aktualizuj ten sam PR. Stan ready/draft odzwierciedla dowody i ustalenia; publikacja z brakami nie udaje gotowości do merge, lokalny wynik nie jest PASS CI.
5. Odczytaj repo/head/base/URL/stan po zapisie; timeout wymaga readback przed ponowieniem. Po dwóch nieskutecznych próbach tego samego zapisu zachowaj checkpoint/payload. Zapisz PR, wynik preflight, wyjątki, `user_acceptance` ze źródłem/zakresem/wersją oraz next. Nie zamykaj issue.

## Wczesny lub jawnie nieodebrany draft

Rzeczywista wcześniejsza polityka publikacji może upoważniać do draftu i jego aktualizacji w toku planowania/implementacji. To wyjątek od standardowego zakończonego cyklu: zapisz `publication.mode: unaccepted-draft`, źródło uprawnienia i braki, **bez odbioru**. Nie wyprowadzaj odbioru z automatycznej publikacji ani z faktu, że draft już istnieje. Wyraźne polecenie „wystaw nieodebrany draft” ma tę samą granicę. Późniejsze jawne raven-pr dla ukończonego jednoznacznego zakresu może zapisać odbiór.

[Runtime](../raven-workflow/references/runtime.md) potrafi utworzyć draft już wypchniętej gałęzi według zapisanej polityki; nie zastępuje preflight ani decyzji użytkownika. [Historia publikacji](references/publication-history.md) opisuje wznowienie. PR nie obejmuje merge, zamknięcia issue, zmian Project ani deploya.

Instrukcja ręczna jest wyłącznie w końcowej wiadomości czatu implementatora. Nie wymagaj acceptance.md ani nie twórz/aktualizuj go; nie kopiuj kroków odbioru do artefaktów. Historyczne pliki i pola zachowaj. Oceniaj rzeczywiste dowody i feedback, bez domniemanego odbioru.
