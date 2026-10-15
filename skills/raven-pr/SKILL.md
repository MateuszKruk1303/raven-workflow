---
name: raven-pr
description: Utwórz lub zaktualizuj PR dla change Raven z opisem rzeczywistych zmian, linkiem do issue i istotnymi kompromisami lub decyzjami niewyjaśnionymi w artefaktach issue. Nie wykonuje audytu gotowości, testów ani merge.
---

# Raven PR

Na zlecenie użytkownika opublikuj PR. To krok publikacji, nie dodatkowy etap review ani weryfikacji gotowości. Decyzja o momencie utworzenia PR należy do użytkownika; nie wymagaj formalnego zakończenia wcześniejszych etapów, raportu testera, akceptacji review ani zielonego CI.

Przeczytaj [wspólny kontrakt GitHub](../raven-auto-plan/references/github-contract.md) w zakresie tożsamości change, zapisu i powiązań. Wywołanie obejmuje zwykły push gałęzi zmiany oraz utworzenie/aktualizację PR. Nie oznacza merge, deploya ani zmiany statusów Project.

## Przygotuj opis na podstawie zmiany

Ustal właściwe repo, branch, docelową gałąź i change issue. Przeczytaj diff oraz istotne artefakty i decyzje w issue, aby opisać rzeczywisty rezultat i zidentyfikować kontekst, którego reviewer nie znajdzie w istniejącej dokumentacji. Nie odtwarzaj audytu całego workflow. Przy niejednoznacznym zakresie ustal tylko brakujące informacje.

Tytuł i opis dopasuj do szablonu repo. Prowadź opis od problemu i wynikowego zachowania. Zawrzyj:

- krótki opis zmian i ich celu, z konkretnym przykładem przed/po, jeśli pomaga;
- link do change issue i ewentualnie do artefaktu potrzebnego reviewerowi;
- istotne kompromisy, odstępstwa, ograniczenia i uzasadnienia decyzji, których nie wyjaśniają artefakty issue.

Nie kopiuj całego planu, raportów ani historii rozmowy. Nie wymyślaj kompromisów lub uzasadnień; brakującą istotną intencję ustal z użytkownikiem. Pomijaj puste sekcje. Wyniki weryfikacji przytocz krótko, jeśli są dostępne i pomagają ocenić zmianę lub wymaga ich szablon; nie uruchamiaj testów, nie odpytuj CI ani nie sprawdzaj kompletności checklist w ramach tego skilla. Nie deklaruj niepotwierdzonego PASS lub gotowości do merge.

## Opublikuj

Przed publikacją sprawdź diff, remote i zakres commitów, aby nie wysłać niezamierzonych zmian. Nie dodawaj automatycznie niezacommitowanego kodu, nie zmieniaj cudzych plików ani stagingu. Jeśli brak commitu uniemożliwia opublikowanie żądanego zakresu, nazwij konkretny brak. Nie wykonuj force-push.

Wyszukaj istniejący PR dla właściwego head/base i change, także po niepewnym wyniku wcześniejszego zapisu. Aktualizuj istniejący otwarty PR, zachowując ręczne dopiski. Zamkniętego lub zmergowanego PR nie otwieraj ponownie ani nie duplikuj bez zlecenia. Użyj markera `<!-- raven:pr change=C-03 -->` z rzeczywistym ID do powiązania i idempotencji.

Pushuj gałąź i utwórz PR bez dodatkowego pytania o zgodę na już zleconą publikację. Domyślnie zwykły PR; draft na życzenie użytkownika. Przy aktualizacji zachowaj dotychczasowy stan draft, chyba że użytkownik zlecił jego zmianę. Nie ustawiaj draft wyłącznie dlatego, że checki są nieznane lub oczekujące.

Powiąż issue przez `Closes #...`, jeśli PR dostarcza jego pełny zakres; dla pracy częściowej użyj `Refs #...`. Uwzględnij rzeczywiście objęte taski, bez obietnicy zamknięcia nieukończonego zakresu. Nie zamykaj issues bezpośrednio, nie ustawiaj Done, nie konfiguruj ani nie audytuj automatyzacji Project. Merge pozostaje osobnym działaniem użytkownika.

Treść przekaż argumentem strukturalnym lub przez --body-file, bez interpolowania jej do shella. Odczytaj utworzony/zaktualizowany PR, aby potwierdzić publikację i powiązania. Zakończ linkiem do PR i krótką informacją, co opublikowano; nie przejmuj monitorowania CI ani napraw kodu.

W Raven workflow raven-test jest obowiązkowym osobnym etapem przed PR. Ten skill nie uruchamia go ani nie audytuje jego raportu; zachowuje rolę publikacji. Checki Actions startują po PR zgodnie z konfiguracją repo.

Etap trwałych testów ma dwa warianty: raven-test → osobno raven-test-review (manual) albo raven-auto-test (pisanie, uruchomienie, niezależne review i poprawki wad testów w jednym cyklu). Oba używają tego samego change i źródeł; wybór należy do użytkownika. Samo ukończenie manualnego raven-test nie oznacza ukończenia review testów.

Przy oddzielnym code_repository PR i push wykonuj w repo kodu. Issues repo artefaktów linkuj pełnym URL jako Refs; nie używaj niekwalifikowanego #numer ani nie obiecuj automatycznego zamknięcia przez merge. Closes dla innego repo stosuj tylko przy jawnie ustalonym powiązaniu i potwierdzonym zakresie; konfiguracja synchronizacji Project pozostaje poza tym skillem. Nie dodawaj linków do prywatnych artefaktów do szerszego/publicznego PR bez ustalonej zgody na takie powiązanie.
