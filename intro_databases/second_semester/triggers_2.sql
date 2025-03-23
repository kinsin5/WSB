/*Na potrzeby zadań utwórz tablice pracownicy(id_pracownika, imie, nazwisko, miasto, pensja)
1. Utwórz w języku PL/pgSQL funkcję PIT(dochód REAL) służącą do wyliczania należnego podatku
dochodowego od osób fizycznych według skali podatkowej. Obliczenia powinny odbywać się według
następującego algorytmu:
- jeżeli "dochód"<= 85528 zł, to podatek należny wynosi 18% z "dochód" minus 556,02 zł
- jeżeli "dochód" > 85528 zł, to podatek należny wynosi 14839 zł plus 32% z ("dochód" - 85528 zł)
Następnie sprawdź działanie funkcji PIT() na tabeli pracownicy:
select nazwisko, pensja, pit(pensja) from pracownicy; */

INSERT INTO pracownicy (id_pracownika, imie, nazwisko, miasto, pensja)
VALUES 
(6, 'Jan', 'Kowalski', 'Warszawa', 90000);

SELECT * FROM pracownicy;

CREATE OR REPLACE FUNCTION pit(dochod REAL)
RETURNS REAL AS
$$
DECLARE
	podatek REAL;
BEGIN
	IF dochod > 85528 THEN
		podatek := 14839 + (dochod - 85528) * 0.32;
	ELSE
		podatek := (dochod - 556.02) * 0.18;
	END IF;
	RETURN podatek;
END;
$$ LANGUAGE PLPGSQL;

SELECT nazwisko, pensja, pit(pensja) FROM pracownicy;

/*2. Utwórz w języku PL/pgSQL funkcję HIRE(id_pracownika INT, imie VARCHAR, nazwisko
VARCHAR, miasto VARCHAR, pensja REAL) służącą do wstawienia nowego rekordu do tabeli
PRACOWNICY. Funkcja powinna zwracać wartość tekstową:
- "OK", jeżeli wstawianie rekordu odbędzie się bez zgłoszenia wyjątku
- "DUPLIKAT ID", jeżeli podczas próby wstawienia rekordu zostanie zgłoszony wyjątek
UNIQUE_VIOLATION
Następnie sprawdź działanie funkcji HIRE():
select hire(6, 'Jan', 'Kowalski', 'Poznan', 100);
select hire(5, 'Anna', 'Nowak', 'Poznan', 200); 
 */
 
CREATE OR REPLACE FUNCTION HIRE
 	(id_pracownika INT, imie VARCHAR, nazwisko VARCHAR, miasto VARCHAR, pensja REAL)
RETURNS VARCHAR AS
$$
BEGIN
	EXECUTE 
		FORMAT('INSERT INTO pracownicy(id_pracownika, imie, nazwisko, miasto, pensja) 
			   VALUES ($1, $2, $3, $4, $5)') USING id_pracownika, imie, nazwisko, miasto, pensja;
	RETURN 'OK';
EXCEPTION
	WHEN UNIQUE_VIOLATION THEN
		RETURN 'DUPLIKAT ID';
END;
$$ LANGUAGE PLPGSQL;

SELECT HIRE(7, 'Anna', 'Nowak', 'Poznan', 200);
select hire(5, 'Anna', 'Nowak', 'Poznan', 200); 

SELECT * FROM pracownicy;

DELETE FROM pracownicy
WHERE id_pracownika = 7;


/*
3. Utwórz wyzwalacz DOUBLE_SALARY i związaną z nim procedurę wyzwalaną
DOUBLE_SALARY_FUN, który każdemu nowo wstawianemu do tabeli PRACOWNICY rekordowi
podwoi wartość kolumny PENSJA.
Następnie sprawdź działanie wyzwalacza:
insert into pracownicy values(10, 'Jan', 'Kowalski', 'Poznan', 100);
select * from pracownicy where id_pracownika=10;
*/

CREATE OR REPLACE FUNCTION DOUBLE_SALARY_FUN()
RETURNS TRIGGER AS 
$$
BEGIN
	NEW.pensja := NEW.pensja * 2;
	RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER DOUBLE_SALARY
BEFORE INSERT ON pracownicy
FOR EACH ROW EXECUTE PROCEDURE DOUBLE_SALARY_FUN();

insert into pracownicy values(10, 'Jan', 'Kowalski', 'Poznan', 100);
select * from pracownicy where id_pracownika=10;

