# Historia publikacji i wznowienie

Historia zmian kodu, planu i raportów to Git. Lokalny checkpoint wskazuje PR, head/base i ostatni potwierdzony wynik publikacji. Opis PR jest aktualnym podsumowaniem i linkiem do tych artefaktów, nie drugim edytowalnym planem.

Po timeout lub przerwaniu odczytaj dokładny PR dla autoryzowanego repo/head/base. Odróżnij open draft, open ready, closed bez merge i merged. Nie twórz duplikatu ani nie otwieraj closed PR automatycznie. Jeśli powiązanie jest niejednoznaczne, zatrzymaj zależny zapis i pokaż kandydatów. Zewnętrzne uprawnienie nadal musi obejmować operację.

Zmiana head wymaga oceny wpływu na konkretne dowody i odbiór. Functional delta wymaga ponownego odbioru zakresu; docs/test-only delta może zachować odbiór po udokumentowanej ocenie wpływu. Aktualizacja samego opisu nie oznacza nowej akceptacji. Zachowaj `user_acceptance` ze źródłem, zakresem i wersją; automatyczny draft go nie tworzy. Wznowienie zapisuje tylko brakujący wynik, nie powtarza implementacji. Po dwóch nieudanych próbach tego samego zapisu oddaj konkretny checkpoint.
