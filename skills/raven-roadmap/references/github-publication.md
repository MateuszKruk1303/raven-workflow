# Zapis roadmapy w GitHub Issues

GitHub Issues jest jedynym trackerem roadmapy. Każdy issue opisuje osobno dostarczalny wynik, AC, linki do wymagań i zależnych issues; nie kopiuje planu implementacji. Nie twórz issues dla faz, lokalnej roadmapy ani drugiej kolejki. Project jest opcjonalnym widokiem.

Przed zapisem sprawdź pokrycie wymagań, [granice change](../../raven-workflow/references/change-scope.md), unikalne ID, DAG, prawdziwe zależności i zachowanie decyzji/postępu. Zmiana produktu wymaga użytkownika; rutynowy podział uzgodnionego zakresu wykonaj sam. Nie ustawiaj In progress podczas samego układania kolejki — dopiero zlecone planowanie lub implementacja podejmują konkretny task.

Dla wskazanych issues używaj ich numerów i dokładnego repo. Tworzenie roadmapy może wymagać jednego ograniczonego odczytu istniejącej kolejki w objętym zleceniem zakresie, z potrzebną paginacją; nie powtarzaj tego przy każdym change. Przed tworzeniem sprawdź istniejące powiązanie; nie duplikuj issue po timeout. Aktualizuj tylko różnice, zachowuj ludzkie treści, assignees i statusy. Zapis sprawdź readback; po dwóch nieskutecznych próbach zachowaj konkretny payload jako checkpoint operacji, nie konkurencyjną roadmapę, i nazwij brak. Nie publikuj w innym repo jako fallback błędu dostępu.
