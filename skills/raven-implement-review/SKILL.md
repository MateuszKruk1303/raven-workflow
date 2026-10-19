---
name: raven-implement-review
description: "Przeprowadź jedno niezależne review change: zgodność z wymaganiami, poprawność kodu i skuteczność testów. Zapisz raport w repo dla ocenianego zakresu i fingerprintu."
---

# Raven Implement Review

Stosuj [politykę ról i dowodów](../raven-workflow/references/agent-policy.md) oraz [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Świeży reviewer Astra/high nie dziedziczy transkryptu autora i nie edytuje produktu. Przeczytaj [procedurę review](references/procedures/impl-review/procedure.md). Przyjmij change/plan/branch/PR, wymagania i publiczne decyzje; ustal rzeczywisty base/head i dirty state, nie wyznaczaj bazy na podstawie daty planu.

Normalne review obejmuje kod **oraz testy i wymagania**. Zweryfikuj mapę kryteriów na dowody, zachowania błędów, integracje, regresje, adekwatność asercji i luki. Testy autora są dowodem, nie wyrocznią wymagań. Nie wymagaj wcześniejszego osobnego testera ani ponownego test-review po pozytywnym pełnym review.

Zapisz `review.md` z zakresem, fingerprintem, kontrolami, oceną i konkretnymi finding IDs. Dodatkowe role rekomenduj tylko przy nazwanym ryzyku. Koordynator realizuje autoryzowane rutynowe poprawki w zakresie i odświeża potrzebną część review; wybór nowego zakresu/ryzyka należy do użytkownika. Raport nie jest odbiorem człowieka ani zgodą na merge.

Oceniaj bieżące testy i gotowość implementacji do ręcznej weryfikacji. Raport review nie udaje wykonania późniejszego raven-test ani nie zamyka audytu regresji samym PASS. Wskaż istniejącą ochronę i konkretne luki do ponownego użycia, bez odkładania wymaganej poprawności kodu.
