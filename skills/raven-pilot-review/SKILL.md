---
name: raven-pilot-review
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Przeprowadź ludzkie review gotowego chunka Raven Pilot, szybko nanieś feedback i zsynchronizuj plan z kodem. Zakończ jawną akceptacją zachowania przed osobnym etapem testów."
---

# Raven Pilot Review

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

Wejście: chunk `awaiting_review`, konkretne uwagi użytkownika lub wznowienie review. To interaktywna, krótka sesja. Nie uruchamiaj pełnej orkiestracji dla każdej drobnej uwagi.

1. Przeczytaj plan, handoff, stan i aktualny kod. Gdy użytkownik dopiero chce sprawdzić produkt, przedstaw instrukcję A–Z i miejsce na feedback; nie wymyślaj jego akceptacji.
2. Przy konkretnym feedbacku nanieś od razu zmiany w uzgodnionym zakresie. Pytaj tylko o rzeczywiste niejasności zgodnie z kontraktem. Duży nowy rezultat biznesowy zaproponuj jako następny chunk, zachowując pierwotny cel.
3. Zaktualizuj `plan.md`, AC, decyzje, dotknięte plany zadań i handoff tak, aby opisywały końcowe zachowanie. Podnieś `spec_revision` przy zmianie kontraktu, zachowaj krótki zapis powodu. Nie poprawiaj historycznego raportu review tak, jakby wcześniejszy błąd nigdy nie istniał.
4. Sprawdź zmieniony przepływ bezpośrednio i wykonaj odpowiednie istniejące kontrole. Nie twórz/edytuj testów ani infrastruktury testowej. Zmienione zachowanie wymaga ponownej akceptacji użytkownika; zgoda na poprawki nie jest automatycznie akceptacją ich wyniku.
5. Dopiero jawne „jest OK”, „akceptuję” lub „zabezpiecz to testami” odnoszące się do aktualnego rezultatu zapisuje `accepted` oraz `acceptance` z rewizją, aktualnym manifestem plików i treścią decyzji użytkownika. Milczenie i upływ czasu nie są akceptacją.
6. Wskaż `$raven-pilot-test <id>`. Jeśli użytkownik właśnie poprosił o testy zaakceptowanego flow, przejdź do tego skilla bez dodatkowego potwierdzenia. W innym razie zakończ sesję z aktualnym stanem.

Roadmapa zachowuje `in-progress`; etap przechodzi z `awaiting_review` na `accepted` dopiero po akceptacji. Po zmianie wymagań zsynchronizuj również zakres i rewizje, zanim zakończysz sesję. Synchronizuj według protokołu z kontraktu; sam raport w czacie nie zastępuje zapisanych artefaktów.
