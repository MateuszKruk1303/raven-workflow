# Testy przed zmianą brownfield

Tryb `before-change` jest jawnym wyjątkiem od domyślnego wykonywania raven-test/auto-test po oddaniu implementacji. Wymaga zaakceptowanego zakresu testów w planie change, ale nie gotowej implementacji ani jej odbioru. Zapisz tryb i bazowy SHA w test_sources, checkpointcie i raporcie; nie edytuj równolegle produktu.

Dla refaktoru wybierz zachowania, które mają pozostać niezmienione. Zaobserwowany wynik bazowej wersji jest kandydatem do kontraktu charakteryzacyjnego, nie automatycznie poprawnym wymaganiem. Zachowaj reprodukowalne wejścia/wyjścia i decyzję, co chronić; nie utrwalaj znanego buga jako wymagania. Sprawdź testy na bazie oraz ich zdolność wykrywania istotnej zmiany zachowania. Nie wymagaj testu każdej prywatnej funkcji.

Dla bugfixu oczekiwany wynik pochodzi z wymagań. Potwierdź RED na bazie wynikający z właściwej asercji, nie z awarii infrastruktury. Zapisz EXPECTED_RED i reprodukcję. Nie osłabiaj asercji ani nie poprawiaj produktu w etapie testów. Taki wynik może kończyć etap reprodukcji; nie oznacza PASS produktu lub gotowości do PR. Bramka zielonych testów źródłowego implementatora nie może wymusić pozornej naprawy: jeśli repo zabrania commitu RED, zachowaj patch testu i checkpoint do zastosowania w fazie poprawki, nie omijaj hooka.

Manualny raven-test oddaje wynik do osobno zlecanego raven-test-review. Auto-test zachowuje świeżego niezależnego reviewera i pętlę napraw wad testów; oczekiwany RED nie jest wadą testu ani powodem pętli napraw produktu. Reviewer otrzymuje te same źródła i kontrakt baseline, ocenia jakość zabezpieczenia/reprodukcji. PASS review testu może współistnieć z EXPECTED_RED wykonania.

Po zmianie produktu ponownie uruchom zabezpieczenia i potrzebne regresje na finalnym SHA. Oczekiwany RED musi przejść w GREEN. Uzupełnij pokrycie nowych wymagań i niezależne review według zwykłego etapu końcowego. Nie duplikuj poprawnych testów ani nie przenoś starego PASS na nowy kod.
