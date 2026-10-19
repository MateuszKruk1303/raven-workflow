---
name: raven-repo-map
description: Zbuduj lub odśwież mapę istniejącego repo na podstawie historii Git, zależności i obszarów produktu. Wide Scan przed pracą brownfield; raport i dowody w repo, bez refaktoryzacji.
---

# Raven Repo Map

Procedura Wide Scan tworzy mapę istniejącego repo w context/foundation/repo-map.md. Mapa pomaga wybrać miejsce dalszej analizy, nie zastępuje czytania kodu konkretnej zmiany.

Przeczytaj [kontrakt raportów brownfield](references/github-brownfield.md). Przyjmij repo, opcjonalny obszar i okno historii oraz istniejący raport mapy. Dla nowej mapy projektu zapisz jeden lokalny raport według kontraktu. Dla zadania ograniczonego do jednego modułu nie narzucaj mapowania całego systemu.

## Wide Scan

1. Ustal repo_root, HEAD, dirty state, zakres i dostępność historii. Przeczytaj instrukcje, manifesty, entrypointy i układ katalogów. Wyklucz zależności vendor, wygenerowane pliki i sekrety. Nie czytaj całego repo do kontekstu.
2. Zbierz tanie, odtwarzalne sygnały CLI: historia/churn, współzmienność plików, importy i zależności, autorzy obszarów. Używaj istniejących narzędzi; zapisuj komendy, zakres dat, wykluczenia i surowe wyniki potrzebne do uzasadnienia. Przy shallow clone zaznacz ograniczenia, nie wnioskuj o braku historii. Statyczne importy nie dowodzą wszystkich zależności runtime, współzmienność nie dowodzi przyczynowości.
3. Dla dużego repo deleguj niezależne odczytowe analizy historii, zależności i autorstwa. Przekaż identyczny zakres/SHA; tylko koordynator publikuje. Bez delegacji wykonaj te same analizy kolejno i podaj ograniczenie. Opcjonalnie użyj dostępnej historii PR, revertów i issues; niedostępność nie blokuje mapy lokalnego kodu.
4. Połącz wyniki wokół funkcji produktu i przepływów, nie listy folderów. Sprawdź reprezentatywny kod dla wniosków. Rozróżniaj dowód, interpretację i niewiadomą; częste zmiany ani liczba autorów same nie oznaczają złego kodu. Autorstwo wskazuje możliwego rozmówcę, nie aktualną odpowiedzialność ani ocenę pracownika. Nie kontaktuj tych osób.
5. Zapisz mapę i dowody w repo; historię zachowuje Git. Przy odświeżeniu podaj różnice względem poprzedniej wersji i ponownie zweryfikuj zmienione obszary; nie nadpisuj historii.

## Wynik

Metadane według kontraktu, następnie:
- **TL;DR**: gdzie zacząć i najważniejsze ograniczenia.
- **Teren**: funkcje, rdzeń/peryferie, granice modułów i aktywność.
- **Realne powiązania**: zależności, współzmienność, warstwy, cykle z dowodami.
- **Strefy ryzyka**: konkretne scenariusze i wpływ, nie rankingi plików bez interpretacji.
- **Kogo zapytać**: sygnały z historii z zastrzeżeniem aktualności.
- **Pierwszy dzień**: 5–8 plików wejściowych, albo mniej dla małego zakresu, i powód wyboru.
- **Ograniczenia**: okno historii, narzędzia, nieznane elementy, koszt dalszej weryfikacji.

Zakończ linkiem do mapy i propozycją jednego obszaru Deep Focus przez raven-research. Nie uruchamiaj researchu, planowania, refaktoryzacji ani zmiany AGENTS.md automatycznie.
