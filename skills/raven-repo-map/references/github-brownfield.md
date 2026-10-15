# Raporty brownfield w GitHubie

Przeczytaj wspólny [kontrakt Raven](../../raven-auto-plan/references/github-contract.md). Obowiązują jego identyfikatory, odczyt pełnych komentarzy, odporność na powtórzenia, wersje, paginacja i odczyt zwrotny.

## Miejsce i zapis

Dla analizy taska używaj istniejącego change. Dla mapy całego repo, słownika domeny lub przeglądu instrukcji użyj osobnego issue artefaktu w skonfigurowanym repo. Przed utworzeniem wyszukaj marker typu `<!-- raven:artifact kind=repo-map scope=SCOPE -->` (odpowiednio domain/rules) i sprawdź zakres. Dedykowane issue dokumentacji nie jest change implementacyjnym, nie potrzebuje fikcyjnego planu ani statusu Done. Nie twórz osobnego issue dla każdej rundy.

Wywołanie skilla z docelowym projektem upoważnia do publikacji jego raportu i indeksu w tym miejscu. Brak jednoznacznego celu GH wymaga ustalenia celu przed zapisem; można w tym czasie zbadać lokalny kod. Nie wybieraj przypadkowego prywatnego repo.

Każda runda: marker HTML `raven:TYPE scope=SCOPE round=N`, czas, repo kodu, base/head SHA lub informacja o braku Git, dirty state, zakres, wersje/hash wejść, metoda, dowody, wnioski i ograniczenia. Zachowuj wcześniejsze rundy, aktualizuj tylko własny indeks bieżących linków. Wyniki surowe potrzebne do odtworzenia ustaleń publikuj jako ponumerowane komentarze evidence z manifestem/hashami; nie zapisuj wyłącznie nietrwałych lokalnych ścieżek. Przy limitach podziel payload i opublikuj manifest dopiero po weryfikacji części. Nie wrzucaj pełnego dumpu repo, sekretów ani niepotrzebnych danych osobowych.

Tylko koordynator zapisuje zdalnie. Przed zapisem sprawdź cudze zmiany i marker, po zapisie odczytaj wynik. Kopie robocze poza śledzonym repo nie są źródłem prawdy. Przy błędzie zachowaj niezapisany payload i zgłoś częściową publikację. Permalinki tylko do rzeczywiście zdalnych commitów; lokalne dowody oznacz path:line + SHA/dirty state.

## Dwa repozytoria

Domyślnie repo kodu i artefaktów są tym samym repo. Gdy użytkownik wskazuje oddzielne miejsce artefaktów, zapisz jawne powiązanie w github.json: istniejące repo/Project wskazują artefakty, opcjonalne `code_repository` wskazuje owner/name kodu. Zweryfikuj obie tożsamości; nie przenoś istniejących issues przy zmianie konfiguracji. Repo_root/worktree, HEAD, testy i PR odnoszą się do code_repository. Numery issues są zawsze kwalifikowane pełnym repo/URL. Uprawnienia do Project i repo artefaktów sprawdzaj oddzielnie.

Przy Jira wymagania pochodzą z jawnie wersjonowanego snapshotu źródła, a plan/review z GH. Nierozstrzygnięty rozjazd wersji nie może zostać ukryty lokalnym plikiem lub nową interpretacją agenta. Żaden raport analityczny nie zatwierdza planu, nie implementuje rozwiązania i nie ustawia Done.
