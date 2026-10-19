---
name: raven-plan-review
description: "Niezależnie oceń lokalny plan change względem wymagań i kodu. Raport z fingerprintem; rutynowe poprawki w zleconym zakresie, decyzje produktowe pozostają u użytkownika."
---

# Raven Plan Review

Stosuj [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [procedurę review](references/procedures/plan-review/procedure.md). Review wykonuje świeży reviewer, który nie tworzył ocenianego planu. Pakiet wejścia obejmuje pełny kontrakt, źródła/wersje, publiczne decyzje, potrzebny kod i [granice change](../raven-workflow/references/change-scope.md).

Zapisz `context/changes/<id>/plan-review.md`, wskazując fingerprint, dowody, realne ryzyka, ważność i konkretną poprawkę. Nie traktuj ilości faz lub plików jako punktacji. Oceniaj wykonalność, zachowanie, granice, zgodność architektury, testy i wystarczalność decyzji.

Reviewer pozostaje read-only wobec planu. Samo zlecenie review kończy się raportem; jeżeli użytkownik już zlecił poprawki albo cykl auto, koordynator przekazuje potwierdzone defekty autorowi bez ponownego pytania. Zmiana zakresu wraca do decyzji. Po naprawie oceń dotknięte obszary na nowym fingerprintcie. Po PASS wskaż `raven-auto-implement <id>` jako następny krok; samo review nie zleca implementacji.

Sprawdź rozdzielenie testów i kontroli implementacji od późniejszego domknięcia regresji raven-test po ręcznej weryfikacji. Auto przekazuje dowody wykonawcy, a instrukcję ręczną wyłącznie w końcowej wiadomości czatu; code review jest osobnym wywołaniem, szerokie QA opcjonalnym; późniejszy audyt nie oznacza obowiązku nowej suite ani kolejnego pełnego review.
