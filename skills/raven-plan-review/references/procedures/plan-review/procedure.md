# Niezależne review planu

Oceń pełny lokalny kontrakt i jego [granice](../../../../raven-workflow/references/change-scope.md), źródła wymagań oraz potrzebny kod. Przypnij fingerprint. Reviewer nie zna transkryptu autora i nie poprawia planu.

Sprawdź:
- jeden rezultat i pokrycie wymagań bez niezamówionego zakresu; nie naprawiaj szerokiego change mnożeniem tasków;
- wykonalność względem rzeczywistych plików, zależności i API; nie ufać fikcyjnym ścieżkom;
- spójność decyzji z istniejącą architekturą i gwarancjami;
- błędy, granice, migrację/rollback i zależności, gdy dotyczą zakresu;
- obserwowalne AC oraz testy powstające wraz z implementacją; osobno audyt/domknięcie regresji raven-test po ręcznej weryfikacji, z reuse istniejącej ochrony i tylko nazwanymi lukami; brak powielania warstw dla statystyki;
- przekazanie dowodów wykonawcy w checkpointcie i instrukcji ręcznej wyłącznie w końcowej wiadomości czatu dla auto, bez zapisywania kroków w artefaktach; brak pozornego odbioru z PASS lub automatycznego draftu;
- kompletność istotnych decyzji bez projektowania wszystkich detali i przyszłych changes.

Każdy finding ma stabilne ID, ważność (critical/warning/suggestion), kotwicę, konkretny scenariusz/skutek, dowód i rekomendację. Wysiłek decyzji jest odrębny od ważności. Przy rzeczywistym kompromisie podaj opcje i tradeoff; oczywisty defekt nie potrzebuje sztucznego menu. Nie zgłaszaj preferencji stylistycznej jako blokady.

Zapisz `plan-review.md`: fingerprint, źródła, sprawdzone obszary, kontrole, findings, werdykt i ograniczenia. Koordynator przekazuje autoryzowane naprawy autorowi i wraca po ocenę dotkniętych obszarów. Dwie nieskuteczne próby tego samego problemu zatrzymują pętlę. Review nie uruchamia implementacji ani nie wymaga komentarza GH. Gotowy plan z aktualnym review można przekazać do raven-auto-implement bez etapu akceptacji planu.
