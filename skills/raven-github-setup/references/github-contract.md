# GitHub jako opcjonalna warstwa współpracy

Źródła stanu określa [kontrakt Git-first](../../raven-workflow/references/change-contract.md). Repo/remote i PR mogą wspierać współpracę, review i CI. Project/issues są opcjonalnym istniejącym trackerem; nie ma wymaganych pól Raven ani task issues.

Weryfikuj owner/repo, tożsamość i zakres uprawnień, widoczność oraz zlecony cel przed mutacją. Przy tworzeniu zasobów poufnych potwierdź prywatność przed dodaniem treści; prywatny board nie chroni publicznych issues. Nie zmieniaj istniejącej widoczności bez polecenia. Brak odczytu nie dowodzi braku zasobu, a udany odczyt nie dowodzi prawa zapisu.

Dla zleconego Project mapuj item/content, pole i opcję po zweryfikowanych ID; nie dopasowuj wyłącznie po nazwie. Zachowaj istniejące automatyzacje, statusy i ręczne fragmenty. Odczytaj rezultat, po timeout najpierw sprawdź istniejący stan. Dwie nieskuteczne próby kończą pętlę z checkpointem. Nie twórz testowych issues do sprawdzenia dostępu.

Korzystaj z dostępnego API/connectora lub aktualnej pomocy gh. Struktury z historycznego github.json są źródłem mapowania dla starej pracy, nie wymaganym manifestem nowych changes. Nowa konfiguracja `.raven/config.json` zapisuje tylko faktycznie potrzebne powiązanie i wcześniejszą politykę; nie nadaje praw.
