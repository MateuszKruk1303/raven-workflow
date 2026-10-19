---
name: raven-rule-review
description: "Oceń AGENTS.md lub inny plik instrukcji AI w pięciu wymiarach. Zapisz raport lokalnie; bez automatycznego przepisywania zasad."
---

# Raven Rule Review

Stosuj [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [procedurę](references/procedures/rule-review/procedure.md) i [kontrakt raportów](../raven-repo-map/references/github-brownfield.md). Zachowaj pięć kontroli: długość, fragmenty kodu/config, precyzja, nadmiarowa wiedza i kolejność, z wyjątkami, scorecard, path:line i Top 3 actions.

Oceniaj wskazany plik i niezbędny kontekst repo. Raport zapisz jako `rule-review.md` w change albo context/foundation, z hashem pliku, SHA/dirty state i konkretnymi poprawkami. Prywatnych globalnych instrukcji nie kopiuj do publikowanego repo bez zgody; przedstaw wtedy raport w rozmowie lub uzgodnionym miejscu.

Domyślnie nie edytuj instrukcji. Jeśli użytkownik już zlecił poprawki, wykonaj je w zakresie i sprawdź diff; samo review nie upoważnia do przepisywania zasad. Nie otwieraj PR ani nie aktualizuj trackera poza autoryzacją.
