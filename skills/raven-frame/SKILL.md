---
name: raven-frame
description: "Zweryfikuj założenia przed planowaniem. Oddziel obserwację od przyczyny i rozwiązania; zapisz Frame Brief z dowodami w lokalnym change."
---

# Raven Frame

Stosuj [kontrakt pracy Git-first](../raven-workflow/references/change-contract.md).

Przeczytaj [procedurę frame](references/procedures/frame/procedure.md). Wejście to opis, lokalny change/research, PR albo wskazane źródło wymagań. Odczytaj pełny istotny kontekst, nie całą historię GH. Wykorzystaj już rozstrzygnięte obserwacje i zakres, zamiast wymuszać ponowny wywiad.

Oddziel dosłowną obserwację, proponowaną przyczynę i rozwiązanie. Badaj wiarygodne hipotezy z dowodami; przy dużym zakresie procedura dopuszcza niezależne analizy read-only. Nie potwierdzaj hipotezy jedynie dlatego, że podał ją użytkownik. Nie wymyślaj przeformułowania, jeśli dowody wspierają pierwotny problem.

Zapisz `context/changes/<id>/frame.md` z obserwacją, hipotezami, dowodami, pewnością, potwierdzonym/przeformułowanym problemem i wpływem na plan. Nowy raport może utworzyć lokalny folder; nie wymaga issue ani change.md. Zachowaj historyczne źródła, nie migruj archiwów. Zmiana zakresu planu wymaga decyzji; samo frame nie zmienia kodu, wymagań ani zapisanych decyzji.
