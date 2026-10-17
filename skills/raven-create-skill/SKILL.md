---
name: raven-create-skill
description: Zaprojektuj, dopracuj w rozmowie i utwórz lub zmień skill Raven wraz z rzeczywistymi zależnościami, routingiem, cookbookiem i walidacją. Użyj przy rozwijaniu rodziny Raven; nie do realizacji funkcji aplikacji ani samego pytania o pomysł na skill.
---

# Raven Create Skill

Rozwijaj Raven jako spójny proces. Wynik to działający pakiet zmian w repo skilli: instrukcje, potrzebne zasoby, integracja i dowody sprawdzenia. Utworzenie nowego katalogu nie jest celem samym w sobie — rozszerzenie istniejącego skilla może lepiej rozwiązywać potrzebę.

Stosuj [wspólną politykę ról, modeli i dowodów](../raven-workflow/references/agent-policy.md). Projektowanie **i autorstwo instrukcji tworzonych lub zmienianych przez ten metaskill** wykonuje `gpt-6-astra` / `high`; końcowe review wykonuje osobna świeża Astra/high, bez transkryptu autora. Ustaw rzeczywiste parametry uruchomienia, nie tylko deklarację w promptcie. Delegowany autor/reviewer nie uruchamia ponownie całego metaskilla. Pytania użytkownika obsługuje koordynator.

## 1. Ustal repo i zakres

Przeczytaj raven-workflow, a następnie ogólny `skill-creator` z lokalizacji podanej przez katalog skilli hosta. Stosuj jego zasady tworzenia instrukcji i progressive disclosure; nie kopiuj jego treści do Raven. Jeśli zależność jest niedostępna, nazwij brak i kontynuuj rozpoznanie, ale nie deklaruj zakończonej walidacji procesu tworzenia.

Znajdź wskazane repo źródłowe Raven: zawiera `skills/raven-workflow/SKILL.md`, `workflow-contract.json` i `tools/raven.py`. Sprawdź instrukcje repo, Git status oraz zakres istniejących zmian. Zainstalowana kopia skilla nie jest dowodem lokalizacji repo. Jeśli repo nie jest wskazane i cwd go nie identyfikuje, poproś o ścieżkę; nie szukaj po całym dysku ani nie twórz nowego repo. Nie edytuj wyłącznie instalacji globalnej. Zachowaj cudze zmiany, w szczególności w routerze i README.

Rozróżnij rozmowę o pomyśle od zlecenia utworzenia/zmiany. Dyskusja nie uruchamia zapisów. Przy zleceniu wykonania zapis skilla i koniecznych integracji jest objęty zadaniem. Nie wymuszaj aplikacyjnego cyklu plan → implementacja → testy ani tworzenia issue GH tylko dlatego, że rozwijasz same skille.

## 2. Dopracuj zachowanie w rozmowie

Najpierw odczytaj katalog i najbliższe istniejące skille. Pytaj o rzeczywiste niewiadome, zwykle jedno pytanie lub małą powiązaną grupę. Nie pytaj ponownie o ustalenia dostępne w rozmowie. Gdy zakres jest kompletny, przejdź do wykonania bez sztucznego wywiadu.

Ustal i krótko podsumuj:

- problem użytkownika oraz 2–3 realistyczne przykłady wywołania, w tym przypadek, którego skill nie powinien obsługiwać;
- wejścia, źródła prawdy, wynik i obserwowalne warunki ukończenia;
- miejsce w workflow: opcjonalne narzędzie, wariant istniejącego etapu czy nowy etap;
- co wykonuje agent, jakie decyzje należą do użytkownika i jakie zapisy obejmuje wywołanie;
- modele, narzędzia i zachowanie przy brakujących możliwościach, przerwaniu oraz wznowieniu.

Porównaj nowy skill z rozszerzeniem istniejącego. Zarekomenduj rozwiązanie i wyjaśnij istotny kompromis. Nie zmieniaj wybranego przez użytkownika celu ani nie dodawaj obowiązkowego etapu pod pozorem integracji. Zmiana znaczenia istniejącego procesu (np. nowa bramka, automatyczne zapisy do innej usługi, inna odpowiedzialność za akceptację) wymaga jawnej decyzji użytkownika, chyba że już ją podjął. Pokaż konkretnie dotychczasowe i proponowane zachowanie; nie pytaj o zgodę na rutynowe odsyłacze, testy lub katalog.

## 3. Sprawdź zależności i przygotuj pakiet

Użyj `rg` do wyszukania wywołań, odsyłaczy i nazw artefaktów. Czytaj tylko znalezionych producentów/konsumentów oraz ich wspólne kontrakty. Nie przepisuj całej rodziny Raven. Przed edycją wskaż krótko dotknięte pliki i powód każdej integracji.

- Utwórz lub zmień `skills/raven-<nazwa>/SKILL.md`: precyzyjny trigger, granice, wykonanie i handoff. Włącz odsyłacz do wspólnej polityki ról. Referencje i skrypty dodawaj tylko gdy skracają instrukcje lub zapewniają niezawodną, powtarzaną operację.
- Metadane UI twórz według `skill-creator/references/openai_yaml.md`, odszukanego względem skilla hosta. Nie wpisuj tam fikcyjnych ustawień modeli.
- Dodaj skill do listy `skills` w `workflow-contract.json`, routingu raven-workflow i jednego właściwego wiersza katalogu README. Rozszerz przepis/diagram tylko gdy zmienia się ścieżka użytkownika.
- Zmień powiązane skille wyłącznie tam, gdzie rzeczywiście zmieniają się wejścia, wyjścia, odpowiedzialności lub wywołania. Zachowaj kompatybilność i istniejące identyfikatory; nie migruj historycznych artefaktów projektów przy okazji.
- Opcjonalny helper nie staje się wpisem w `stages` standardowego cyklu. Przy uzgodnionej zmianie cyklu uaktualnij razem kontrakt, jego niezmienniki w doctorze, router, konsumentów i testy. Nie osłabiaj walidatora tylko po to, aby uzyskać PASS.

Wspólne zasady przechowuj w jednym miejscu. Nowy skill odwołuje się do wspólnego kontraktu Git-first, browsera lub niezależności, jeżeli faktycznie ich potrzebuje; nie duplikuj całych procedur i nie ładuj niepowiązanych referencji.

## 4. Zweryfikuj zachowanie i niezależnie oceń

W repo uruchom doctora oraz testy właściwe dla zmiany, używając jego udokumentowanego środowiska Python:

```bash
.venv/bin/python tools/raven.py doctor
.venv/bin/python -m unittest discover -s tests -v
```

Użyj także walidatora `quick_validate.py` z dostępnego `skill-creator` dla nowych/zmienionych skilli. Gdy `.venv` nie istnieje, przygotuj środowisko według README repo; nie instaluj zależności globalnie. Uruchom nowe/zmienione helpery na realistycznych danych. Brak środowiska jest niewykonaną kontrolą, nie PASS.

Dobierz próby z [referencji scenariuszy](references/verification.md). Statyczny doctor nie dowodzi zgodności znaczenia instrukcji. Dla zmiany zachowania wykonaj forward-test w izolacji: autor dostarcza rzeczywiste wejście i źródła, świeży reviewer sam wyprowadza przebieg, a koordynator porównuje wynik z ustalonym kontraktem. Nie podawaj reviewerowi oczekiwanej odpowiedzi ani hipotezy błędu. Nie publikuj testowych issue, nie steruj prywatną przeglądarką i nie uruchamiaj produkcyjnych zapisów w ramach próby.

Końcowy reviewer Astra/high otrzymuje wymagania użytkownika, publiczne decyzje, aktualny diff (także nowe pliki), zakres zmian, źródła i wyniki kontroli. Sprawdza spójność producent → konsument, granice uprawnień, niezależność, wznowienie, dublowanie zasad i koszt kontekstu. Pracuje read-only; raportuje konkretne błędy i lokalizacje. Gdy brak świeżego reviewera, oddaj draft i wskaż brak review; nie deklaruj pełnej gotowości.

Naprawiaj potwierdzone błędy w ustalonym zakresie. Po poprawce odśwież dotknięte testy i review. Po dwóch nieskutecznych próbach tego samego problemu zatrzymaj zależną pętlę z reprodukcją i decyzją potrzebną od użytkownika; zmiana agenta nie zeruje licznika. Uwagi zmieniające zakres wracają do decyzji, nie do automatycznej przebudowy.

## 5. Oddaj lub zainstaluj

Zakończ konkretnym pakietem: ścieżka skilla, zmienione integracje, przykład użycia, wyniki walidacji/review i ograniczenia. Nie twórz dodatkowego raportu w repo, jeśli nie jest potrzebny do wznowienia. Przy przerwie zachowaj krótki checkpoint w uzgodnionym artefakcie roboczym: decyzje, pliki, otwarte problemy, wyniki i następny krok; nie wznawiaj wywiadu od zera.

Instaluj globalnie tylko gdy jest to częścią zlecenia, również wcześniejszego w tej sesji. Uruchom `tools/raven.py sync --to <katalog-skilli>` bez `--apply`, przejrzyj cały diff instalacji i dopiero zastosuj `--apply`. Sync obejmuje całą zarejestrowaną rodzinę: nie nadpisuj niezwiązanych lokalnych modyfikacji, których użytkownik nie objął zleceniem. Przy takim konflikcie oddaj gotowy pakiet i ustal sposób scalenia przed instalacją. Po instalacji uruchom `doctor --installed <katalog-skilli>`; podaj wynik i ścieżkę backupu, jeśli powstał. Samo skopiowanie plików nie potwierdza odświeżenia katalogu skilli w aktywnym UI.

Commit, push, publikacja PR i zmiana konfiguracji modeli nie wynikają z samego tworzenia skilla. Wykonuj je tylko w zakresie zlecenia. Nie instaluj draftu jako zweryfikowanej wersji po FAIL/BLOCKED wymaganej kontroli.
