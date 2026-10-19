---
name: raven-auto-test
description: "Wykonaj osobne zlecenie testów lub before-change z niezależnym review i ograniczoną pętlą napraw. Nie jest dodatkowym obowiązkowym etapem zwykłego change."
---

# Raven Auto Test

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Koordynuj autora testów Sol/low i jednego świeżego reviewera Astra/high. Autor stosuje [raven-test](../raven-test/SKILL.md), reviewer [kontrakt test-review](../raven-test/references/test-review.md). Przekaż obu te same wersje wymagań, zakres/base/head i publiczne decyzje; reviewer nie dziedziczy transkryptu autora.

Odtwórz plan/checkpoint i bieżące dowody. Autor dodaje testy oraz uruchamia potrzebne kontrole; reviewer sprawdza skuteczność asercji, źródło Expected, pokrycie ryzyk i izolację. Potwierdzone błędy w zleconym zakresie wracają automatycznie do autora. Po dwóch nieskutecznych próbach tego samego problemu zatrzymaj zależną pętlę z reprodukcją. Zmiana kontraktu lub nieobjęte działanie zewnętrzne wraca do decyzji użytkownika.

Raporty i checkpoint zapisuj w repo. Normalne pełne review change może pokryć testy; nie uruchamiaj dodatkowego review tego samego zakresu tylko dla odhaczenia skilla. Osobne zlecenie auto-test obejmuje opisane review. Oddaj wynik, luki i następny krok; nie wykonuj merge/deploy ani publikacji poza polityką.

Standardowy raven-test po ręcznej weryfikacji może zakończyć się audytem istniejącej wystarczającej ochrony bez edycji i bez tego koordynatora. Nie uruchamiaj auto-test automatycznie dla każdego change; jego jawne wywołanie obejmuje niezależne review. Autor najpierw audytuje dowody i dodaje tylko nazwane luki, zachowując już dostarczone testy.
