# Ochrona przed zmianą

Użyj dla niechronionego refaktoru lub reprodukcji bugfixu w zleconym zakresie. Ustal istniejący change/branch, bazowy kod i oczekiwane zachowanie. Nie wymagaj zakończonej implementacji ani odbioru użytkownika.

Test charakteryzacyjny zapisuje świadomie chronione zachowanie, nie legalizuje przypadkowo błędnej reguły. Dla bugfixu wymaganie jest Expected, a test na starej wersji może mieć `EXPECTED_RED`: zapisz konkretną asercję, obserwowany błąd i źródło oczekiwania. Błąd runnera lub środowiska nie dowodzi reprodukcji.

Zapisz dowody w `test-report.md` i checkpoint w lokalnym planie, z bazowym SHA/tree i wersją wymagań. Implementacja później pokazuje GREEN na poprawionym kodzie. Nie osłabiaj asercji. Niezależną ocenę ochrony można wykonać przed ryzykowną zmianą; końcowe review change nadal obejmuje aktualny kod i testy. Ten tryb nie wymaga issues, Project ani snapshotów GH.
