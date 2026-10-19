---
name: raven-lesson
description: "Na wyraźne zlecenie zapisz jedną powtarzalną regułę projektu w context/foundation/lessons.md: agent proponuje wpis z kontekstu rozmowy, użytkownik akceptuje lub poprawia. Nie publikuje do GitHuba ani nie zmienia AGENTS.md."
---

# Raven Lesson

Dopisz jedną regułę do `context/foundation/lessons.md`. Plik czytają `raven-research`, `raven-plan`, `raven-auto-implement`, `raven-test` i `raven-implement-review`.

Lekcja to reguła, która będzie wracać i zmieniłaby sposób pracy — nie opis jednorazowej poprawki. Pojedynczy incydent bez wzorca odeślij do zwykłej poprawki.

## Kroki

1. **Propozycja.** Z polecenia i kontekstu rozmowy przygotuj wpis. Pytaj tylko o pole, którego nie da się rzetelnie ustalić; nie zmyślaj incydentu.

   ```markdown
   ## <Krótki tytuł reguły w trybie rozkazującym>

   - **Context**: <gdzie obowiązuje: obszar, typ zmiany lub wzorzec plików — konkretnie, nie „wszędzie”>
   - **Problem**: <co idzie nie tak bez reguły; incydent lub powtarzalny schemat>
   - **Rule**: <reguła w 1–2 zdaniach: „Zawsze…”, „Nigdy…”, „Przed X zrób Y”>
   - **Applies to**: <research, plan, auto-implement, test, implement-review albo all>
   ```

2. **Akceptacja.** Pokaż wpis i zapytaj: dodaj / popraw / anuluj. Jeśli użytkownik podał już gotową treść i jednoznacznie zatwierdził dokładny wpis, nie pytaj ponownie.
3. **Zapis.** Gdy pliku nie ma, utwórz go z nagłówkiem:

   ```markdown
   # Lessons Learned

   > Append-only register of recurring rules. Read by raven-research, raven-plan, raven-auto-implement, raven-test, raven-implement-review.
   ```

   Wpis dopisz na końcu. Nie zmieniaj, nie porządkuj ani nie usuwaj istniejących wpisów — poprawki starych reguł użytkownik robi ręcznie. Po zapisie odczytaj plik i potwierdź, że nowy wpis jest ostatni.

## Granice

Jeden wpis na wywołanie. Inne skille mogą zasugerować lekcję, ale jej nie zapisują. Bez publikacji do GitHuba, commitu, zmian kodu i automatycznego kopiowania do AGENTS.md (to osobne zlecenie przez `raven-md`). W czacie podaj ścieżkę i tytuł dodanej reguły.
