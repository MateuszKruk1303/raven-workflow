# Granice change i dekompozycja

Wspólne zasady dla roadmapy i planowania. Nie ustanawiają nowego etapu, statusu ani punktacji.

## Jednostka pracy

**Change** dostarcza jeden ograniczony rezultat, który można osobno zrealizować, zweryfikować i zmergować. Nie musi sam umożliwiać premiery produktu; pełny proces użytkownika może wymagać wielu changes. Nie wymuszaj flag funkcji tylko po to, by uzasadnić podział. **Task/faza** jest krokiem wykonania tego jednego rezultatu. Fragment z własnym niezależnym odbiorem jest kandydatem na osobny change, a nie automatycznie kolejnym taskiem.

Zachowaj pionowy zakres: potrzebne UI, API, model danych i walidacja należą do rezultatu. Nie dziel zmian według warstw i nie łącz niezależnych funkcji dlatego, że korzystają z tego samego modelu, ekranu lub procesu. Zależność między rezultatami opisuje kolejność; sama nie uzasadnia ich sklejenia.

Zabezpieczenia konieczne do poprawności funkcji pozostają z nią. Przykładowo ponowienie płatności, brak podwójnego obciążenia i obsługa pobranej kwoty bez zamówienia nie są późniejszym „hardeningiem”. Konieczność zabezpieczenia nie upoważnia jednak do dobudowania niezamówionych podsystemów.

Change techniczny jest uzasadniony wykazanym problemem lub nazwanym rezultatem, który odblokowuje. Jeżeli potrzebna praca naturalnie mieści się w pierwszym konsumencie, wykonaj ją tam; potencjalna reużywalność nie uzasadnia osobnej infrastruktury „na przyszłość”.

## Kontrola granic

Przed publikacją change w roadmapie oraz przy planowaniu sprawdź:

1. Czy opis nazywa jeden wynik, czy listę funkcji spiętą ogólnym tytułem?
2. Czy fragmenty można niezależnie pokazać i odebrać przy spełnieniu ich zależności?
3. Czy fragment wymaga osobnego wyboru dostawcy, kontraktu integracji lub rozstrzygnięcia ryzyka? To sygnał możliwej osobnej granicy, nie automatyczny nakaz podziału.
4. Czy błąd jednej części powinien blokować odbiór i merge pozostałych? Odróżnij konieczne gwarancje jednej funkcji od niezależnych wyników.
5. Czy kryteria odbioru sprawdzają jedną funkcję wraz z jej błędami i wyjątkami, czy kilka osobnych demonstracji?

Typowo change ma jeden główny wynik i 1–2 istotne fazy implementacji. Testy należą do kroków realizacji; nie traktuj dodatkowej czynności testowej jako niezależnego wyniku. Trzy lub więcej faz implementacji albo kilka integracji to ostrzeżenie do ponownej oceny granic, nie limit. Nie twórz tasków w roadmapie tylko po to, by je policzyć. Liczba plików, FR, checkboxów i estymacje nie mierzą właściwego rozmiaru change. Więcej tasków nie naprawia zbyt szerokiego zakresu.

Większy change jest dopuszczalny, gdy krótkie rzeczowe uzasadnienie wskazuje nierozdzielną gwarancję lub konkretny skutek podziału, przez który części nie da się samodzielnie odebrać. Samo „to checkout” lub „wspólny model” nie wystarcza. Zapisz uzasadnienie w istniejącym opisie zakresu/podejścia, bez nowego formularza.

## Roadmapa

W zleconym tworzeniu lub aktualizacji roadmapy dziel sensowne niezależne rezultaty autonomicznie. Pytaj, gdy propozycja zmienia wymagania lub priorytety albo odracza konieczne zachowanie; zwykła sekwencja zależnych changes nie jest takim odroczeniem. Prośba o status lub plan pojedynczego issue nie upoważnia do reorganizacji kolejki.

Pokryj cały uzgodniony PRD: wymaganie ma przypisany rezultat, dowód wcześniejszego dostarczenia albo jawnie zatwierdzone odroczenie. Dalsze changes opisuj przez wynik, granice, źródła, zależności i obserwowalne kryteria odbioru. Nie rozstrzygaj teraz szczegółów przyszłych integracji. Utrzymuj acykliczny graf zależności (DAG). Milestones są opcjonalnym grupowaniem; nie dodawaj epik ani kolejnej obowiązkowej hierarchii.

## Planowanie jednego change

Po odczytaniu wymagań, istniejących decyzji i postępu, **przed szczegółowym researchem i wywiadem**, zastosuj kontrolę granic. Istnienie issue nie dowodzi poprawnego podziału. Wystarczy kontekst potrzebny do oceny wyniku; nie badaj wszystkich integracji, by dopiero potem odkryć zbyt duży zakres.

Gdy zakres jest zbyt szeroki, przedstaw krótki powód, proponowane wyniki i zależności, mapowanie dotychczasowych wymagań oraz rekomendowany pierwszy change. Nie planuj szczegółowo wszystkich części. Planowanie może zaproponować podział; zapis zmian istniejącej kolejki wymaga autoryzacji użytkownika obejmującej tę reorganizację. Jeśli jej jeszcze nie ma, czekaj na tę decyzję przed reorganizacją kolejki lub szczegółowym planowaniem wybranego nowego zakresu.

Drugą kontrolę wykonaj przed dopracowaniem struktury faz. Nowy niezależny rezultat odkryty w researchu wraca do propozycji podziału, zamiast stawać się kolejną fazą. Gdy odkrycie wymaga istotnego rozszerzenia bieżącego rezultatu, pokaż wpływ i uzyskaj decyzję użytkownika. Nowe rozszerzenie nie jest rutynowym uzupełnieniem planu.

**Brak otwartych pytań** oznacza rozstrzygnięte wymagania, granice i istotne decyzje architektoniczne tego change. Nie wymaga zaprojektowania przyszłych changes ani każdej decyzji implementacyjnej. Zostaw wykonawcy detale, gdy kontrakt, ograniczenia i sposób weryfikacji są znane. Każde dodatkowe badanie musi odpowiadać na konkretną lukę mogącą zmienić zakres, wykonalność, kontrakt lub kryteria odbioru; zakończ je po rozstrzygnięciu tej luki.

Każdy change ma własny odbiór i właściwy zakres trwałych testów. Nie odkładaj całej weryfikacji na koniec wieloetapowego procesu produktu. Mały change otrzymuje proporcjonalny plan, bez sztucznych tasków ani obowiązku testów każdej warstwy.

## Podział istniejącej pracy

Zachowaj historię, identyfikatory, decyzje, źródła, dowody i postęp. Propozycja pokazuje mapowanie starego zakresu na nowe rezultaty oraz wpływ na istniejące taski i zależności. Nie pytaj ponownie o uzgodnionych dostawców ani reguły biznesowe; badaj tylko rzeczywistą nową lukę lub sprzeczność.

Po autoryzacji aktualizuj wyłącznie objęte nią issues. Zachowaj odsyłacze do historycznych planów. Nie zamykaj ani nie usuwaj issues/tasków bez osobnego jawnego zlecenia. Samo planowanie, regeneracja opisu lub aktualizacja instrukcji Raven nie migrują istniejących roadmap.
