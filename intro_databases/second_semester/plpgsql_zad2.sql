--1.
ALTER TABLE filmy
ADD UNIQUE(id_filmu);

--2.
CREATE FUNCTION dodaj_film(id INTEGER, tyt VARCHAR, 
	rok INTEGER, c REAL)
	
$$ LANGUAGE PLPGSQL;








. Utwórz funkcję o nazwie DODAJ_FILM(id INTEGER, tyt VARCHAR, rok INTEGER, c
REAL), służącą do wprowadzania nowej krotki do relacji 
FILMY. W przypadku, gdy podczas
wykonania funkcji wystąpi wyjątek naruszenia 
ograniczenia integralnościowego UNIQUE,
automatycznie zmodyfikuj wartość identyfikatora nowego
filmu tak, aby była niepowtarzalna
(np. aktualna wartość maksymalna + 1). 
Przetestuj działanie funkcji.
