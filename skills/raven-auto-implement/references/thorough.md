# Poziom `thorough`

Ma udowodnić: funkcja działa, nie psuje swojego obszaru i wytrzymuje typowe błędy. Zasady wspólne, sprawdzenie działania i format finału pozostają jak w [SKILL.md](../SKILL.md); ten plik zastępuje tylko kroki poziomu.

## Kroki

1. **Baseline.** Przed edycją uruchom testy dotkniętego obszaru, aby oddzielić zastane awarie od wprowadzonych.
2. **Implementacja.**
3. **Statyczne kontrole.** Lint i typecheck wszystkich dotkniętych workspace.
4. **Testy obszaru.** Wszystkie testy unit i e2e dotkniętego obszaru (cały spec modułu, nie tylko nowy przypadek); porównaj wynik z baseline.
5. **Sprawdzenie działania** jako pełna ścieżka end-to-end od wejścia do trwałego skutku, plus co najmniej jeden scenariusz błędu dobrany do ryzyka zmiany.
6. **Niezależne review** (domyślnie, jedna runda — niżej).

Orientacyjny narzut weryfikacji: ~25–45 min, w tym review z poprawkami ~10–20 min.

## Niezależne review

Uruchom jednego świeżego agenta bez transkryptu autora. Przekaż mu polecenie użytkownika, wskazany issue lub plan, diff od bazowego SHA do HEAD wraz z niezacommitowanymi zmianami i nowymi plikami oraz wyniki kontroli. Reviewer pracuje read-only i ocenia zgodność z wymaganiami, poprawność oraz skuteczność testów, wskazując konkretne lokalizacje.

Wykonaj jedną rundę poprawek dla potwierdzonych uwag i ponów kontrole, które dotyczą poprawionego kodu. Uwag, których nie poprawiasz, nie ukrywaj: trafiają do finału z uzasadnieniem. Nie uruchamiaj kolejnych rund review. Gdy host nie pozwala uruchomić świeżego agenta, zgłoś brak review w finale jako ograniczenie; samoocena autora nie jest review.

## Dodatki w finale

Oprócz elementów z SKILL.md podaj:

- ryzyka rezydualne;
- wynik review i co z nim zrobiono (poprawione / odrzucone z uzasadnieniem);
- w instrukcji odbioru krok negatywny: co powinno się nie udać i jak to wygląda.
