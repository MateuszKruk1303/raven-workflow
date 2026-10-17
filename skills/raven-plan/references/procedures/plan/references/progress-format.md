# Postęp wykonania

`## Progress` w `context/changes/<id>/plan.md` jest kanoniczną checklistą. Leży poza blokiem `raven:contract`, wskazuje stabilne ID kroków kontraktu i nie zmienia jego fingerprintu.

- `[ ]`: niewykonane lub niezweryfikowane; nazwij blokadę, gdy istnieje.
- `[x]`: twierdzenie potwierdzone dowodem. Przy wyniku wskaż polecenie/raport, zakres kodu i ograniczenia.

Nie odhaczaj odbioru człowieka na podstawie kontroli agenta. Nie oznaczaj pominiętego testu jako PASS. Zmiana kodu unieważnia zależne dowody; aktualizuj odpowiednie wiersze i checkpoint. Historyczne wyniki pozostają w Git.

Checkpoint zapisuje następny krok, branch/base/head, stan drzewa, fingerprint i źródło akceptacji, review/CI/PR, liczniki prób oraz istotne nierozwiązane kwestie. Przy przerwaniu zapisz stan przed handoffem, bez nowej kopii planu w issues. Manual i auto używają tego samego formatu.
