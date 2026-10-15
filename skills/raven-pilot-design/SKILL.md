---
name: raven-pilot-design
description: "DEPRECATED — historyczny Raven Pilot; nie używaj do nowej pracy. Prowadź lub wznów pełny redesign UI i UX działającego pilota po minimum funkcjonalnym: analiza podróży, wybór stylu i motywu, iteracje reprezentatywnych widoków, wdrożenie całej aplikacji oraz odbiór przed E2E. Używaj dla wieloetapowego projektowania produktu, nie dla pojedynczej poprawki CSS ani budowy brakujących funkcji MVP."
---

# Raven Pilot Design

> DEPRECATED: ten skill należy do historycznego Raven Pilot. Dla nowej pracy użyj [raven-workflow](../raven-workflow/SKILL.md). Zachowany do jawnie zleconej kontynuacji starego pilota; nie migruj ani nie usuwaj artefaktów automatycznie.


Celem jest produkt wygodny i wizualnie dopracowany w codziennych zadaniach. Prowadź pracę w krótkich pętlach: konkretna propozycja → obejrzenie przez użytkownika → feedback → poprawka. Nie projektuj całej aplikacji jednym promptem i nie zastępuj widoków opisami przyszłego wyglądu.

## Wejście i zakres

- Przeczytaj lokalne AGENTS.md, zakres produktu, roadmapę, ustalenia workflow oraz istniejący zapis redesignu. Obejrzyj aplikację i kod jej widoków, wspólnych komponentów oraz tokenów. Odróżnij funkcję działającą od samego formularza lub komponentu startera.
- Znajdź istniejący aktywny chunk redesignu, jeśli jest. Nie wybieraj ID na podstawie poprzedniego projektu. Archiwa służą wyłącznie jako źródło; nie edytuj ich. Nie uruchamiaj tego procesu automatycznie podczas zwykłej implementacji funkcji.
- Domyślna kolejność Raven Pilot to funkcjonalne MVP → design → E2E. Sprawdź rzeczywiste zależności. Niedokończone funkcje nazwij konkretnie; nie oznaczaj ich jako ukończonych, aby rozpocząć redesign. Wcześniejsze badanie kierunku jest możliwe na jawne zlecenie, ale nie potwierdza gotowości zależności.
- Rozpoznaj tryb: rozpoczęcie, samo prepare/projektowanie, implementacja uzgodnionego kierunku, feedback do widoku albo wznowienie. Samo prepare nie upoważnia do pełnego wdrożenia UI. Zlecenie całego redesignu obejmuje implementację po uzgodnieniu kierunku; nie pytaj ponownie o każdy widok lub zmianę kodu.
- Zachowaj istniejący stack, reguły biznesowe i możliwości produktu. Zmiany zachowania takie jak dodatkowy krok zakupu, usunięcie funkcji lub nowa reguła konta wymagają świadomego uzgodnienia. Nie traktuj decyzji o wyglądzie jako zgody na zmianę produktu.

## Lekki zapis i wznawianie

Utrzymuj **jedno źródło decyzji projektowych i postępu**: sekcję „Design” w istniejącym planie aktywnej zmiany, a gdy planu nie ma — jeden `context/pilot/design.md`. Wykorzystaj istniejący odpowiednik w projekcie; nie twórz równolegle obu dokumentów. Gdy później powstanie plan, odsyłaj do istniejącego źródła zamiast kopiować treść.

Zapis zawiera tylko:

- etap procesu i następny konkretny krok;
- uzgodniony kierunek: paleta z rolami, typografia, motyw, fotografia/ikony, gęstość, charakter interakcji;
- krótkie decyzje wraz z rozróżnieniem propozycji i akceptacji;
- tabelę podróży/widoków: zakres, status, najważniejszy feedback lub pozostały problem;
- ostatni wynik weryfikacji i zakres zaakceptowany przez użytkownika.

Status widoku rozróżnia co najmniej: do zaprojektowania, propozycja, do poprawy, wdrożony, sprawdzony, zaakceptowany. Wspólny wzorzec może mieć jeden wpis zamiast kilkunastu identycznych pozycji. Nie uznawaj „wdrożony” za „zaakceptowany”.

Przy wznowieniu przeczytaj ten zapis i sprawdź aktualny kod/ekran. Zachowaj uzgodnione decyzje, nie zaczynaj ponownie wywiadu. Jeśli kod odbiega od zaakceptowanego kierunku, nazwij różnicę i rozlicz ją przed kontynuacją. Po feedbacku aktualizuj istniejący wpis; nie dopisuj kroniki rozmowy.

Bez handoffów, osobnych raportów na każdą sesję, kopii planów, masowych manifestów i screenshotów w repo. Podglądy, alternatywne szkice i screenshoty trzymaj tymczasowo poza repo; trwałe grafiki produktu są częścią kodu i mają inne przeznaczenie. Nie zapisuj sekretów ani danych rzeczywistych użytkowników.

Jeżeli pracujesz w istniejącym Raven chunku, jego `state.json` pozostaje jedynym źródłem stanu wykonania. Wewnętrzny etap designu nie zastępuje statusu chunka. Przed zmianą stanu lub projekcji roadmapy przeczytaj [synchronizację Raven](../raven-pilot-implement/references/synchronization.md) i zastosuj jej blokady oraz atomowy zapis. Nie nadpisuj równoległej sesji ani stanu na podstawie pamięci. Zachowaj wymagane istniejące pola/dowody, bez produkowania ich duplikatów. Ten skill zastępuje rozbudowane artefakty opisowe jednym zapisem designu; lokalne instrukcje mają pierwszeństwo.

## 1. Rozpoznanie produktu

Ustal główne role, zadania i miejsca powrotu. Inwentaryzuj **podróże**, a następnie ich widoki: wejście → decyzja → akcja → wynik → powrót. Uwzględnij autoryzację, zarządzanie własnymi danymi i administrację, jeśli należą do produktu. Nie utożsamiaj pełnego redesignu z samą stroną główną.

Z faktycznego użycia aplikacji wyprowadź najważniejsze problemy: niewidoczna akcja, utrata kontekstu, zbyt ciężki formularz, nieczytelna hierarchia, zbędne wyjaśnienia lub niespójne zachowania. Przedstaw krótko kilka problemów o największym wpływie, bez obszernego audytu na zapas. Nie przypisuj obserwacji użytkownikom ani nie deklaruj badań, których nie przeprowadzono.

Zapytaj tylko o brakujące decyzje, które zmienią projekt: odbiorców, charakter marki, istniejące zasoby, inspiracje i rzeczy niepożądane. Pytania rozłóż na krótkie rundy powiązane z pokazywanymi propozycjami. Preferencje już podane są wejściem do pracy, nie tematem ponownego wywiadu.

## 2. Prepare: kierunek graficzny i UX

Poświęć tej fazie realną uwagę. Przełóż określenia typu „premium”, „przyjazny”, „lekki” na widoczne decyzje o kompozycji, kolorach, typografii i zdjęciach. Nie uznawaj domyślnego shadcn ani innego startera za docelowy styl.

Jeśli kierunek nie jest ustalony, pokaż zwykle 2–3 istotnie różne, spójne propozycje na tym samym reprezentatywnym fragmencie aplikacji i tych samych przykładowych danych. Nie twórz pozornych wariantów różniących się tylko kolorem przycisku. Gdy użytkownik ma jednoznaczną wizję, dopracuj ją zamiast obowiązkowo mnożyć alternatywy.

Propozycja ma być widoczna: tymczasowy podgląd, makieta lub lokalny prototyp, wraz z krótkim uzasadnieniem. Dobierz dostępne narzędzie do celu, bez narzucania zewnętrznego serwisu lub biblioteki. Jeśli wizualny podgląd jest niedostępny, nazwij ograniczenie; opis słowny nie jest odbiorem wyglądu. Inspiracje traktuj jako źródło zasad, nie gotowe zasoby do skopiowania. Nie dodawaj fontów, zdjęć ani usług wymagających zakupu bez uzgodnienia.

Wybierz z użytkownikiem kierunek i doprecyzuj:

- role kolorów: tło/powierzchnie, tekst, marka, główna akcja i statusy; kontrast i zastosowanie, nie tylko listę hexów;
- rodzinę i hierarchię typografii, odstępy, szerokości, gęstość oraz kształt elementów;
- motyw lub motywy, fotografię, ikony i ruch; nie dodawaj dark mode ani nie usuwaj istniejącego bez decyzji;
- nawigację, hierarchię akcji i prowadzenie najważniejszych formularzy na telefonie oraz komputerze.

**UX bez tekstozy:** użytkownika prowadzą układ, hierarchia i trafne etykiety. Jedna wyraźna główna akcja na krok, krótkie komunikaty, przykłady przy trudnych polach i pomoc kontekstowa zamiast stałych akapitów instrukcji. Nie wyjaśniaj w UI architektury ani procesu developmentu. Skracanie nie może ukrywać kosztu, konsekwencji akcji, przyczyny błędu lub informacji potrzebnej do świadomej decyzji. Ikona bez zrozumiałej etykiety nie jest automatycznie lepsza od tekstu.

Zapisz wybór i otwarte kwestie. Akceptacja palety nie oznacza akceptacji wszystkich widoków. Nie kontynuuj zależnych prac w oczekiwaniu na wymagany wybór kierunku; możesz porządkować inwentaryzację i analizować niezmieniane zachowania.

## 3. Reprezentatywne widoki i pętle feedbacku

Wybierz niewielki zestaw, który sprawdzi różne wyzwania produktu: np. odkrywanie/lista, szczegóły i złożony formularz lub rozmowa. Dobór wynika z konkretnej aplikacji. Użyj realistycznej długości tekstów i treści przykładowych, w tym pustych danych oraz długich nazw.

Dopracowuj widoki kolejno lub w małych powiązanych grupach. Pokaż desktop i mobile oraz istotne interakcje. Zbieraj feedback o konkretach: hierarchia, czytelność, charakter, gęstość, znajdowanie akcji. Nie proś użytkownika o projektowanie każdego marginesu. Rozstrzygaj szczegóły wykonawcze samodzielnie w uzgodnionym kierunku.

Po feedbacku nanieś poprawki, pokaż dotknięty fragment i krótko określ, co się zmieniło. Zgoda na poprawkę nie jest odbiorem rezultatu. Jeśli zmiana dotyczy globalnego motywu lub nawigacji, ponownie sprawdź wcześniej dopracowane widoki; nie zostawiaj różnych generacji wyglądu.

Po zaakceptowaniu reprezentatywnych widoków utrwal wspólne tokeny i wzorce w istniejącym systemie komponentów. W trybie samego projektowania zapisz kontrakt do późniejszej implementacji zamiast przebudowywać produkcyjne UI. Unikaj osobnych stylów dla każdego ekranu i przedwczesnych abstrakcji opartych na jednym przykładzie.

## 4. Wdrożenie całych podróży

Pracuj po podróżach, dostarczając działające odcinki od wejścia do wyniku. Wykorzystuj zaakceptowane wzorce, ale oceniaj dopasowanie do zadania; panel operatora może potrzebować większej gęstości niż publiczny katalog. Nie kopiuj mechanicznie tej samej kompozycji na wszystkie ekrany.

Dla każdej podróży uwzględnij mające zastosowanie stany: ładowanie, treść, pusty wynik/pierwsze użycie, błąd i ponowienie, sukces, brak dostępu oraz niedostępny obiekt. Sprawdź walidację, zapisane dane po błędzie, oczekiwanie lub niepewność operacji, jeśli występują. Nie dodawaj sztucznych stanów ani nowej funkcjonalności dla wypełnienia checklisty.

Sprawdź konkretne ryzyka mobile: klawiatura ekranowa, widoczność akcji, długość formularza, obsługa filtrów, powrót z podstrony, pozycja przewijania. Klawiatura i dotyk muszą umożliwiać ukończenie zadania; pilnuj fokusu, etykiet, kontrastu i komunikowania stanu bez polegania wyłącznie na kolorze. Ruch powinien pomagać orientacji i respektować ograniczenie animacji.

Zachowuj dane, uprawnienia, linki bezpośrednie i powroty po logowaniu/płatności. Nie zmieniaj API, cen, limitów czy cyklu życia obiektów tylko po to, żeby uprościć makietę. Regresję napraw w zakresie redesignu; nową potrzebę biznesową oddziel do uzgodnienia.

## 5. Weryfikacja, odbiór i przekazanie do testów

Przy zmianach UI obejrzyj rzeczywisty render i wykonaj zadanie w działającej aplikacji. W środowisku Raven korzystaj z dostępnego [raven-browser](../raven-browser/SKILL.md), respektując sesję użytkownika; poza nim wykorzystaj uzgodnioną przeglądarkę/narzędzie. Same typy, build lub odczyt DOM nie potwierdzają wyglądu. Zrzuty do inspekcji zapisuj wyłącznie tymczasowo poza repo.

Uruchom wymagane lokalnie formatowanie, typy/build i adekwatne istniejące testy. Nie dodawaj ani nie edytuj testów E2E, snapshotów i ich konfiguracji w trakcie designu. W Raven tworzenie lub zmiana testów produktu należy do osobnego etapu `raven-pilot-test` po akceptacji; istniejące testy można uruchamiać, a nieaktualne oczekiwania zgłaszaj jawnie.

Odbiór końcowy obejmuje rzeczywiste zadania użytkownika w pełnych podróżach, na telefonie i komputerze. Przedstaw krótki scenariusz i pozwól użytkownikowi ocenić działanie. Odróżniaj własną weryfikację od feedbacku ludzi; nie deklaruj użyteczności na podstawie samych screenshotów. Sprawdź spójność między widokami oraz zwięzłość tekstu, nie tylko poprawność każdego ekranu osobno.

Zapytaj o odbiór konkretnego gotowego zakresu, jeśli użytkownik jeszcze go nie zaakceptował. Wymagane decyzje to kierunek, reprezentatywne widoki i finalny rezultat, nie zgoda na każde polecenie lub margines. Wcześniejsze jednoznaczne akceptacje zachowują ważność w niezmienionym zakresie. Nie ogłaszaj ukończenia całego redesignu, gdy pozostały nieodebrane podróże, znane istotne problemy albo brak wizualnej weryfikacji.

Po akceptacji zapisz zwięźle zakres, wynik kontroli, pozostałe ograniczenia i następny krok. W Raven skieruj do `$raven-pilot-test <id>` dla niewielkiego zestawu E2E krytycznych ścieżek i istniejących luk. Jeśli testy są już jawnie zlecone po akceptacji, przejdź do tego etapu bez ponownej zgody. Nie archiwizuj ani nie publikuj automatycznie aplikacji; zakończenie designu nie oznacza wdrożenia pilota.
