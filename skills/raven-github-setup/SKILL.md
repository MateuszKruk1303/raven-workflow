---
name: raven-github-setup
description: Przygotuj lub uzupełnij prywatne repozytorium GitHub i prywatny Project dla workflow Raven, z polami, etykietami i lokalnym powiązaniem w context/foundation/github.json. Użyj do setupu lub naprawy konfiguracji GitHuba projektu; nie do tworzenia roadmapy ani realizacji tasków.
---

# Raven GitHub Setup

Przygotuj GitHub jako miejsce roadmapy, changes i tasków projektu. Działa dla greenfield i brownfield. Wynik: **prywatne repozytorium, prywatny GitHub Project, zweryfikowane pola/etykiety oraz powiązanie w `context/foundation/github.json`**. Pełny wynik i następny krok przedstaw w czacie, bez osobnego handoff.md.

Wywołanie setupu upoważnia do utworzenia brakujących zasobów i addytywnego uzupełnienia konfiguracji w jednoznacznie wskazanym celu. Nie pytaj o zgodę na każdą etykietę czy pole. Samo tworzenie lub omawianie tego skilla nie uruchamia setupu.

## Granice

- Repozytorium oraz Project muszą być **private**, niezależnie od siebie. Nie zakładaj, że prywatność repozytorium ustawia prywatność Project.
- Nowe zasoby twórz jako prywatne; jeśli API tworzenia Project nie przyjmuje widoczności, sprawdź udokumentowaną prywatną wartość domyślną i potwierdź odczytem natychmiast po utworzeniu. Nie dodawaj treści projektu przed potwierdzeniem prywatności.
- Jeśli wskazane istniejące repo/Project jest publiczne, zgłoś konkretny konflikt. Ustal, czy zmienić jego widoczność, czy wybrać inny prywatny zasób; nie zmieniaj widoczności istniejącego projektu po cichu. Nie deklaruj pełnego setupu z publicznym zasobem.
- Nie publikuj kodu, nie commituj, nie pushuj, nie twórz testowych issues/PR-ów ani wiadomości. Nie konfiguruj CI, sekretów, deployu, branch protection, automerge, płatnych usług, zespołów ani uprawnień innych osób.
- Nie twórz roadmapy z PRD i nie importuj starego backlogu bez osobnego zlecenia. Przygotowujesz miejsce pracy; planowanie i publikacja uzgodnionych changes to kolejny etap.
- Nie przenoś istniejącego context/ ani archiwów. Nie twórz drugiej roadmapy w Markdown. PRD, instrukcje i lessons pozostają w repo. Wymagania change, research, plany, raporty i checkpointy są kanonicznie w GitHubie; kopie robocze poza repo nie są drugim źródłem prawdy.

## 1. Rozpoznaj cel i dostęp

Przeczytaj AGENTS.md i istniejące `context/foundation/github.json`, README oraz nazwę projektu z PRD, jeśli istnieje. Status draft PRD ani brak PRD nie blokują setupu infrastruktury planowania.

Sprawdź katalog główny Git, remotes i tożsamość zalogowaną do GitHuba przez dostępny connector lub `gh`. Nie wypisuj tokenów ani URL-i zawierających poświadczenia. Preferuj istniejący dostęp; używaj pełnych owner/repo i jawnego właściciela Project, nie przypadkowych domyślnych wartości CLI.

Wybierz cel w kolejności: jawne wskazanie użytkownika → zweryfikowane lokalne powiązanie → jednoznaczny remote. Przy braku repo użyj właściciela zalogowanego konta osobistego i nazwy projektu, jeśli są jednoznaczne; ogłoś wybrany cel przed zapisem. Jeśli istnieje repo o tej nazwie, sprawdź tożsamość zamiast automatycznie przypinać je lub dodawać sufiks. Sprzeczne remotes, konto, manifest lub kilka pasujących Projects wymagają jednego konkretnego pytania. Nie zgaduj między różnymi projektami.

Sprawdź uprawnienia do repozytorium i Projects osobno. Brak scope dostępu do Projects to nie brak samego Project. Poproś o logowanie/uzupełnienie konkretnego dostępu tylko wtedy, gdy faktycznie go brakuje. Nie zmieniaj konta ani metody autoryzacji bez potrzeby. Sprawdź aktualne `gh ... --help` i [referencję GitHub](references/github-contract.md); nie zakładaj obsługi API z pamięci.

## 2. Uzgodnij stan docelowy z istniejącym

Domyślny kontrakt nowego projektu:

| Element | Konfiguracja |
|---|---|
| Repozytorium | private, Issues włączone |
| Project | private, nazwa projektu aplikacji, powiązany z repo |
| Typ pracy | etykiety `raven:change` oraz `raven:task` |
| Stan | pole single-select `Raven Status`: Backlog, Preparing, Ready, In progress, Review, Blocked, Done |
| Kolejność | pole number `Raven Order` |
| Trwała tożsamość | pole text `Raven ID` |

Project należy do konta użytkownika lub wskazanej organizacji, a jest powiązany z repozytorium. Domyślnie jeden Project na projekt aplikacji, nie osobny na każdy change czy milestone. Zachowaj zastanego właściciela.

W nowym Project wykorzystaj wbudowane Status, jeśli można bezpiecznie uzyskać powyższe opcje przez dostępne API; w przeciwnym razie użyj `Raven Status`. **Dokładnie jedno pole jest kanonicznym statusem dla Ravena** — wskaż jego ID w powiązaniu. Nie twórz dodatkowego pola, gdy istniejące jednoznacznie pasuje. Nie usuwaj/nie zmieniaj opcji istniejących pól, nie resetuj wartości itemów i nie wyłączaj cudzych automatyzacji. Konflikt nazwy z innym typem pola lub semantyką wymaga wyjaśnienia, nie zgadywania.

Statusy są kontraktem późniejszych skilli, setup nie zmienia statusów zadań:
- Backlog: uzgodniony pomysł/rezultat, jeszcze nieprzygotowany.
- Preparing: dopracowanie zakresu, research lub plan.
- Ready: dopracowany zakres i spełnione zależności; samo istnienie issue nie oznacza gotowości.
- In progress: realizacja.
- Review: oczekujący przegląd/odbiór zgodny z trybem pracy.
- Blocked: przeszkoda z konkretną potrzebną decyzją/akcją.
- Done: wymagany zakres i właściwy odbiór zakończone. Sam merge lub zamknięcie issue nie dowodzi odbioru.

Zmiana = issue, task = issue powiązane jako natywne sub-issue; kolejność wykonania = natywne zależności blocked-by/blocking. Relacja rodzic–dziecko nie jest zależnością wykonania. Nie generuj ich bez realnych uzgodnionych zadań. Nie używaj organizacyjnych issue types jako wymaganego fundamentu osobistego konta. `Raven ID` zachowuje ID istniejących changes; nie renumeruj pracy. Task identyfikuj łącznie z change ID, aby T-01 w dwóch changes nie kolidowało. `Raven Order` wyraża priorytet kolejki, nie zastępuje grafu zależności.

## 3. Wykonaj tylko brakujące zmiany

Przed tworzeniem pobierz istniejące repo, Projects, pola, opcje, linki i etykiety z pełną paginacją. Dopasowuj przez zapisane ID i potwierdzoną tożsamość; nie tylko tytuł.

Utwórz lub wykorzystaj repo i Project, sprawdź ich prywatność, włącz Issues, jeśli potrzebne, połącz Project z repo i dodaj brakujące pola/etykiety. Nie twórz README, licencji ani pierwszego commita na zdalnym repo, jeśli kolidowałoby to z lokalną historią. Lokalny remote możesz dodać, jeśli go brakuje; nie nadpisuj istniejącego remote. Brak lokalnego Git sam w sobie nie blokuje utworzenia zasobów ani manifestu; nie inicjalizuj historii bez potrzeby/zlecenia.

Wielowierszowe opisy przekazuj przez pliki/argumenty strukturalne, nie interpolację do poleceń. Po timeout lub niejednoznacznym błędzie mutacji najpierw odczytaj stan — nie ponawiaj tworzenia w ciemno. Zapisuj potwierdzone ID na bieżąco; nie kasuj poprawnie utworzonych zasobów po częściowym błędzie.

Widoki: jeśli aktualne dostępne API/narzędzia pozwalają, przygotuj tabelę roadmapy (changes, kolejność) i tablicę pracy (kanoniczny status). Nie zakładaj możliwości edycji widoków w CLI. Jeśli jej brak, zachowaj istniejący widok i podaj link oraz krótką instrukcję ustawienia w czacie. Oznacz widoki jako pending, nie jako wykonane. Nie zastępuj brakującej funkcji fikcyjną konfiguracją JSON.

Nie włączaj automatycznego zamykania changes po merge, auto-add wszystkiego z repo ani automatycznego przejścia Review → Done. To polityka realizacji, nie setup. Powiązanie repo z Project nie oznacza, że wszystkie issues są automatycznie dodawane; późniejszy skill jawnie dodaje uzgodnione issues do Project.

## 4. Zapisz powiązanie i zweryfikuj

Utwórz/uzupełnij `context/foundation/github.json` według [kontraktu](references/github-contract.md). Nie zastępuj nieznanych kluczy. Zapis atomowy; nigdy sekretów, tokenów ani lokalnych danych logowania. To mapa identyfikatorów integracji, nie kopia roadmapy lub kolejki. Powtórne uruchomienie wykorzystuje ją i weryfikuje zasoby zdalnie.

Wykonaj ponowny odczyt repo, Project, połączenia, pól, opcji i etykiet. Potwierdź prywatność obu zasobów i zgodność ID/typów z manifestem. Sprawdź możliwość korzystania z sub-issues i zależności na podstawie dokumentacji/odczytów dostępnych dla konta; brak istniejących issues nie uzasadnia tworzenia testowych. Weryfikacja odczytem nie dowodzi uprawnienia do każdej przyszłej mutacji — raportuj tę granicę.

Status `ready`: wymagany setup i prywatność potwierdzone. `partial`: wymagany element niewykonany. Opcjonalne widoki mają własny stan i nie udają gotowości. Manifest po częściowym sukcesie umożliwia wznowienie bez duplikowania zasobów.

W czacie podaj: link do repo i Project, prywatność, utworzone/reużyte elementy, ewentualne braki oraz następny krok — opracowanie i opublikowanie uzgodnionej roadmapy. Nie uruchamiaj go automatycznie ani nie wskazuj nieistniejącego skilla jako dostępnego polecenia. Nie dodawaj technicznego raportu Markdown obok manifestu.
