CREATE TABLE region (
	id_regionu SERIAL,
	region VARCHAR,
	PRIMARY KEY(id_regionu)
);
CREATE TABLE wojewodztwo (
	id_wojewodztwa SERIAL,
	id_regionu INTEGER,
	wojewodztwo VARCHAR,
	PRIMARY KEY(id_wojewodztwa),
	FOREIGN KEY(id_regionu) REFERENCES region(id_regionu)
);
CREATE TABLE miejsce(
	id_miejsca SERIAL,
	id_wojewodztwa INTEGER,
	miasto VARCHAR,
	PRIMARY KEY(id_miejsca),
	FOREIGN KEY(id_wojewodztwa) REFERENCES wojewodztwo(id_wojewodztwa)
);

CREATE TABLE rok (
	id_roku SERIAL,
	rok INTEGER,  -- np. 2023
	PRIMARY KEY(id_roku)
);

CREATE TABLE kwartal (
	id_kwartalu SERIAL,
	id_roku INTEGER,
	kwartal INTEGER,  -- np. 1, 2, 3, 4
	PRIMARY KEY(id_kwartalu),
	FOREIGN KEY(id_roku) REFERENCES rok(id_roku)
);

CREATE TABLE data (
	id_daty SERIAL,
	id_kwartalu INTEGER,
	date DATE,
	PRIMARY KEY (id_daty),
	FOREIGN KEY(id_kwartalu) REFERENCES kwartal(id_kwartalu)
);


CREATE TABLE operator (
	id_operatora SERIAL,
	operator VARCHAR,
	PRIMARY KEY (id_operatora)
);

CREATE TABLE wyslane_sms (
	id_daty INTEGER,
	id_miejsca INTEGER,
	id_operatora INTEGER,
	ilosc_sms INTEGER,
	rozmiar_sms REAL,
	PRIMARY KEY(id_daty, id_miejsca, id_operatora),
	FOREIGN KEY(id_daty) REFERENCES data(id_daty),
	FOREIGN KEY(id_miejsca) REFERENCES miejsce(id_miejsca),
	FOREIGN KEY(id_operatora) REFERENCES operator(id_operatora)
);

-- region
INSERT INTO region (region) VALUES
('Zachod'),
('Wschod');

-- wojewodztwo
INSERT INTO wojewodztwo (id_regionu, wojewodztwo) VALUES
(1, 'Pomorskie'),
(1, 'Warmińsko-Mazurskie'),
(2, 'Małopolskie');

-- miejsce
INSERT INTO miejsce (id_wojewodztwa, miasto) VALUES
(1, 'Gdańsk'),
(2, 'Olsztyn'),
(3, 'Kraków');

-- rok
INSERT INTO rok (rok) VALUES
(2023),
(2024);

-- kwartal
INSERT INTO kwartal (id_roku, kwartal) VALUES
(1, 1),  -- Q1 2023
(1, 2),  -- Q2 2023
(2, 1);  -- Q1 2024

-- data
INSERT INTO data (id_kwartalu, date) VALUES
(1, '2023-01-15'),
(2, '2023-05-10'),
(3, '2024-02-20');

-- operator
INSERT INTO operator (operator) VALUES
('Orange'),
('Play'),
('Plus');

-- wyslane_sms
INSERT INTO wyslane_sms (id_daty, id_miejsca, id_operatora, ilosc_sms, rozmiar_sms) VALUES
(1, 1, 1, 100, 1234.5),  -- Gdańsk, Orange, 15.01.2023
(2, 2, 2, 200, 980.0),   -- Olsztyn, Play, 10.05.2023
(3, 3, 3, 500, 1450.2);  -- Kraków, Plus, 20.02.2024

---napisz funkcje która po wprowadzeniu miasta, operatora oraz roku wyświetli łączną liczbę
--wysłanych SMS 
SELECT ilosc_sms FROM wyslane_sms
NATURAL JOIN miejsce
NATURAL JOIN operator
NATURAL JOIN data
NATURAL JOIN kwartal
NATURAL JOIN rok
WHERE operator = 'Orange'
	AND rok = 2023
	AND miasto = 'Gdańsk';

CREATE OR REPLACE FUNCTION get_sms(operator_ VARCHAR, rok_ INTEGER, miasto_ VARCHAR)
RETURNS INTEGER AS
$$
DECLARE 
	sms INTEGER;
BEGIN
	SELECT ilosc_sms INTO sms FROM wyslane_sms
	NATURAL JOIN miejsce
	NATURAL JOIN operator
	NATURAL JOIN data
	NATURAL JOIN kwartal
	NATURAL JOIN rok
	WHERE operator = operator_
		AND rok = rok_
		AND miasto = miasto_;
	RETURN sms;
END;
$$ LANGUAGE PLPGSQL;

SELECT get_sms('Orange', 2023, 'Gdańsk');


--oraz funkcje która po wprowadzeniu operatora, okręgu oraz daty podaje
--średni rozmiar wysłanych sms 

CREATE OR REPLACE FUNCTION avg_sms_size(operator_ VARCHAR, region_ VARCHAR, data_ DATE)
RETURNS REAL AS
$$
DECLARE 
	avg_size REAL;
BEGIN
	SELECT (ilosc_sms / rozmiar_sms) INTO avg_size FROM wyslane_sms
	NATURAL JOIN miejsce
	NATURAL JOIN operator
	NATURAL JOIN data
	NATURAL JOIN wojewodztwo
	NATURAL JOIN region
	WHERE operator = operator_
		AND data1::date = data_::date
		AND region = region_;
	RETURN avg_size;
END;
$$ LANGUAGE PLPGSQL;

SELECT avg_sms_size('Orange','Zachod','2023-01-15');
