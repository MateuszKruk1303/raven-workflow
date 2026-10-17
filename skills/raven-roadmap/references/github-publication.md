# Zapis roadmapy

Domyślnie zapisuj `context/roadmap.md`. Jeśli użytkownik wskazał jeden istniejący tracker jako źródło kolejki, aktualizuj go w zakresie autoryzacji i nie twórz lokalnego konkurencyjnego backlogu. Issue i Project są opcjonalne. Nie twórz task issues dla faz wykonania.

Przed zapisem sprawdź pokrycie wymagań, [granice change](../../raven-workflow/references/change-scope.md), unikalne ID, DAG, prawdziwe zależności oraz zachowanie istniejących decyzji/postępu. Zmiana produktu wymaga użytkownika; rutynową korektę podziału wynikającą z uzgodnionego zakresu wykonaj sam.

Zapis lokalny odczytaj i przejrzyj diff; historię przechowuje Git. Zapis trackera wskazuje dokładny zasób, zachowuje ludzkie treści i wymaga readback. Po timeout sprawdź stan przed ponowieniem. Nie publikuj do innego miejsca jako fallback błędu dostępu. Po dwóch nieskutecznych próbach zachowaj gotowy payload i nazwij brak. Nie kopiuj całej treści planów do trackera.
