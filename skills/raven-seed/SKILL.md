---
name: raven-seed
description: "Zainicjalizuj strukturę folderów na pliki kontekstowe skilli Raven. Twórz brakujące katalogi context/pilot, context/pilot/chunks i archive/raven-pilot oraz README, zachowując istniejące pliki. Nie inicjalizuje stacku aplikacji."
---

# Raven Seed

Przygotuj w katalogu projektu miejsce na dokumenty Raven. Nazwa wywołania to `$raven-seed`. To inicjalizacja kontekstu, niezależna od `$raven-init-stack` i `$raven-pilot-init`.

## Struktura

```text
context/
└── pilot/
    ├── README.md
    └── chunks/
        └── README.md
archive/
└── raven-pilot/
    └── README.md
```

Ścieżki odpowiadają obecnym skillom `raven-pilot-*`. Twórz wyłącznie strukturę opisaną powyżej.

## Wykonanie

1. Ustal katalog projektu z polecenia lub cwd i przeczytaj obowiązujące instrukcje. Nie inicjalizuj kontekstu w katalogu instalacji skilla. Jawna ścieżka projektu ma pierwszeństwo.
2. Sprawdź całą strukturę przed zapisem. Rozwiąż symlinki: jeśli ścieżka wychodzi poza projekt, wskaż konflikt zamiast pisać poza nim. Plik w miejscu katalogu lub katalog w miejscu README także jest konfliktem; nie usuwaj go.
3. Utwórz każdy brakujący katalog i README niezależnie. Istniejące pliki, również puste lub z inną treścią, zachowaj bajt w bajt. Użyj tworzenia wyłącznego (`open(..., 'x')` albo odpowiednika), aby nie nadpisać pliku utworzonego w międzyczasie. Brakujące katalogi nadrzędne twórz w razie potrzeby.
4. Respektuj lokalne zakazy zapisu do archiwum. W takim przypadku przygotuj dozwoloną część, oznacz archiwum jako zablokowane i wyjaśnij powód. Nie obchodź zakazu inną ścieżką. W pozostałych przypadkach wolno utworzyć sam katalog archiwum i jego brakujący README, ale nie zmieniać istniejących archiwalnych dokumentów ani chunków.
5. Sprawdź obecność sześciu elementów i wypisz dla każdego `created`, `present` albo `blocked` z powodem. Nie raportuj pełnego ukończenia, jeśli jakikolwiek element jest zablokowany.

## Treść nowych README

### `context/pilot/README.md`

```markdown
# Kontekst Raven

Żywe dokumenty produktu: shape-notes.md, prd.md i roadmap.md. Tworzą je odpowiednie skille Raven, gdy istnieje treść do zapisania. Setup.md dokumentuje inicjalizację, a opcjonalny workflow.md jawne nadpisania konfiguracji workflow.

Dokumenty aktualizujemy w miejscu, zachowując ustalenia i źródła. Nie tworzymy pustego PRD, roadmapy ani pozornej akceptacji.

Rozpocznij od $raven-shape lub krótszego $raven-pilot-shape, następnie $raven-pilot-prd i $raven-pilot-roadmap. Aktywne chunki znajdują się w chunks/; zamknięte w archive/raven-pilot/ względem katalogu projektu.
```

### `context/pilot/chunks/README.md`

```markdown
# Aktywne chunki Raven

Każdy chunk ma własny katalog C-01-slug/ przygotowywany przez $raven-pilot-prepare. Plan, state.json, decyzje, zadania, sesje i raporty powstają dopiero w odpowiednim etapie pracy; nie tworzymy ich jako pustych szablonów.

Kolejność: prepare → implement → review → test → archive. State.json jest źródłem stanu wykonania, a roadmapa jego aktualizowanym widokiem. Zweryfikowany chunk przenosi $raven-pilot-archive do archive/raven-pilot/ względem katalogu projektu.
```

### `archive/raven-pilot/README.md`

```markdown
# Archiwum Raven

Zamknięte chunki przeniesione przez $raven-pilot-archive z context/pilot/chunks/. Zawartość zarchiwizowanych chunków jest niezmienna. Dalszą pracę otwieramy jako nowy chunk przez $raven-pilot-prepare; nie poprawiamy dokumentów ani stanu w archiwum.
```

## Granice

Ponowne uruchomienie przy pełnej strukturze nie zmienia niczego. Nie twórz shape-notes.md, PRD, roadmapy, workflow.md, state.json ani przykładowego chunka. Nie zmieniaj AGENTS.md, konfiguracji aplikacji, istniejących dokumentów ani skilli. Nie instaluj zależności i nie uruchamiaj automatycznie następnego etapu. Zakończ krótkim podsumowaniem i wskaż `$raven-shape` jako możliwy następny krok.
