# Raport sesji i obserwacja workflow

Telemetrię wykonuj tylko na jawne żądanie użytkownika; domyślna implementacja jej nie zbiera. Na żądanie raport powstaje raz przy przekazaniu lub rzeczywistym blockerze, bez osobnego agenta zbierającego statystyki i bez odpytywania liczników w pętli. Nie opóźniaj pytania o blocker analizą kosztów. Telemetria jest pomocnicza: jej brak nie blokuje produktu. Nie dodawaj limitu czasu ani budżetu tokenów.

## Zapis początku i końca

Przy zwykłym checkpointcie startowym dodaj w `run.telemetry`: `session_id` (unikalny identyfikator tego wznowienia), `root_thread_id` jeśli znany, `started_at` w UTC. Przy końcu dodaj `ended_at` i ścieżkę raportu. ID wątku odczytaj z runtime, jeśli udostępniony, albo z jednoznacznych metadanych bieżącej rozmowy; nie wybieraj dowolnej ostatniej sesji innego projektu. Brak ID oznacza brak automatycznej części pomiaru.

Każde wznowienie ma osobne okno czasu i katalog `sessions/<session_id>/` w aktywnym chunku. Nie nadpisuj wcześniejszych raportów. Zachowaj ten sam root_thread_id przy wznowieniu w tej rozmowie, ale nowy zakres czasu; wątki potomne są wybierane z lokalnego indeksu i filtrowane oknem. W tym czasie koordynator nie zleca niepowiązanych zadań w tym samym drzewie. Pomiar z przeszłości oznacz jako retrospektywny i podaj granice; nie podszywaj aktualnego state pod historyczny wynik.

## Dane i generowanie

1. Z istniejących implementation/review/state przygotuj `sessions/<session_id>/notes.json`: wynik i wykonany zakres, kontrole i pokryte AC, poprawki według T-ID, blockery/trudności z przyczyną i dowodem, potrzebne działanie, 1–3 wnioski do następnej sesji. Notatki są oceną koordynatora, nie danymi automatycznie zmierzonymi. Nie kopiuj sekretów, surowych promptów, poleceń ze zmiennymi środowiska ani logów API. Nie trzeba dopisywać notatki po każdym narzędziu.
2. Uruchom lokalnie [session_report.py](../scripts/session_report.py) z konkretnymi argumentami (poniżej przykład składni, nie prawdziwe ID):

```sh
python3 /Users/mati/.codex/skills/raven-pilot-implement/scripts/session_report.py \
  --root-thread THREAD_ID \
  --since 2026-10-04T15:05:00Z --until 2026-10-04T16:06:10Z \
  --session-id 20261004-implementation-01 \
  --notes context/pilot/chunks/CHUNK/sessions/20261004-implementation-01/notes.json \
  --output-dir context/pilot/chunks/CHUNK/sessions/20261004-implementation-01
```

3. Generator czyta lokalny indeks Codex w trybie read-only i wyłącznie JSONL wskazanego drzewa. Domyślna ścieżka indeksu to `~/.codex/state_5.sqlite`; `--database` pozwala wskazać inną. To format lokalnego runtime, nie gwarantowane publiczne API. Brak indeksu/rekordów oznacza dane niepełne/null i ostrzeżenie, nigdy wymyślone zero. Przy niedostępności narzędzia zapisz ręcznie wynik i braki pomiaru, bez instalowania zależności lub żądania uprawnień tylko dla telemetrii.
4. Wynik: `metrics.json` do porównań i `report.md` do czytania. Link umieść w handoff oraz bieżącym state przy tym samym końcowym checkpointcie. W odpowiedzi użytkownikowi wystarczy link, kilka liczb i najważniejszy wniosek; nie wklejaj całego raportu do kontekstu wszystkich agentów.

## Jak czytać i porównywać

- Tokeny i wywołania modelu per agent/model/effort; cache jest częścią wejścia, reasoning częścią wyjścia. Sumujemy per-response usage, nie narastające liczniki. Koszt finansowy, zużycie abonamentu i tokeny per zadanie nie są wyliczane.
- Wywołania narzędzi modelu (w tym exec, send_message, wait_agent) oraz operacje wewnętrzne (shell/MCP) są osobnymi widokami. Nie dodawaj ich do jednej sumy.
- Czas okna to czas ścienny; suma wait wielu agentów może zachodzić na pracę i przekraczać ten czas. Nie nazywaj jej „zmarnowanym czasem”. Niezerowy exit może być zwykłym brakiem wyniku wyszukiwania, a nie błędem produktu.
- Porównuj podobne zakresy: wynik/pełne AC, wywołania, cache/wejście poza cache/wyjście, poprawki, przeszkody środowiska i udział koordynacji. Zmiana liczby agentów sama nie dowodzi oszczędności. Przy wielokrotnych rolach w jednym wątku nie przypisuj jego wszystkich tokenów jednej funkcji tylko po nazwie agenta.
- Raport kończy pomiar na `--until`; własne generowanie raportu i późniejsza odpowiedź mogą leżeć poza oknem. Granicę zawsze pokazuj jawnie.
