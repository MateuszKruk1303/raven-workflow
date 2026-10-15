---
name: raven-pilot-shape
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Dopracuj wizję pilota, hipotezę wartości i granice MVP w krótkiej rozmowie. Użyj przy nowym pomyśle lub zmianie wizji w workflow Raven Pilot, przed PRD."
---

# Raven Pilot Shape

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


## Wspólny kontrakt

Przed pracą przeczytaj [kontrakt workflow](../raven-pilot-implement/references/contract.md). Jest częścią tego pakietu; nie wymaga uruchomienia implementacji. Gdy brakuje pliku, zgłoś niepełną instalację zamiast zgadywać zasady. Zachowuj język użytkownika.

Celem jest najszybsze zdobycie wiarygodnej informacji od rzeczywistych użytkowników. Wynik: `context/pilot/shape-notes.md`.

1. Przeczytaj podany opis, istniejące notatki i dokumenty produktu. W istniejącym projekcie wznów `context/pilot/shape-notes.md`; wcześniejsze dokumenty produktu i PRD wykorzystaj jako źródła, zachowując je bez zmian. Nie rozpoczynaj wywiadu od zera, jeśli odpowiedzi są dostępne.
2. Ustal: odbiorcę, jego problem i obecne obejście, proponowaną wartość, najważniejszą hipotezę, sposób dotarcia do pierwszych użytkowników oraz obserwowalny sygnał sukcesu/porażki. Próg sukcesu jest propozycją, dopóki użytkownik go nie ustali.
3. Oddziel wizję docelową od minimalnego pilota. Zapisz kluczowe podróże użytkownika, wyłączenia, akceptowane ręczne operacje i uproszczenia. Uwzględnij ograniczenia danych, kosztów i czasu, jeśli są znane. Nie dokładaj funkcji tylko dlatego, że podobne produkty je mają.
4. Pytaj wyłącznie według polityki pytań w kontrakcie. Krótkie sesje można wznawiać: po każdej istotnej odpowiedzi utrwal stan i pozostałe rzeczywiste niewiadome. Nie wymuszaj liczby rund ani wyboru liczby pytań.
5. Zapisz: źródła, wizję, odbiorców/problem, hipotezę, scenariusze, zakres pilota, poza zakresem, plan walidacji, ograniczenia, decyzje, jawne założenia i otwarte pytania. Rozróżnij wypowiedzi użytkownika od rekomendacji agenta.
6. Stack jest stały lub już zapisany w projekcie; nie uruchamiaj wyboru technologii. Po ukształtowaniu wizji wskaż `$raven-pilot-prd`. Samo wywołanie shape nie autoryzuje budowy produktu.
