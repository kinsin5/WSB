CREATE TABLE pora_rozmowy(
	id_pory SERIAL,
	przedzial_godziny VARCHAR,
	PRIMARY KEY (id_pory)
);

CREATE TABLE miejsce_rozmowy(
	id_miejsca SERIAL,
	strona_swiata VARCHAR,
	wojewodztwo VARCHAR,
	miasto VARCHAR,
	PRIMARY KEY(id_miejsca)
);

CREATE TABLE rozmowca(
	id_rozmowcy SERIAL,
	przedzial_wieku VARCHAR,
	PRIMARY KEY(id_rozmowcy)
);
CREATE TABLE rozmowa_telefoniczna(
	id_miejsca INT REFERENCES miejsce_rozmowy(id_miejsca),
	id_rozmowcy INTEGER REFERENCES rozmowca(id_rozmowcy),
	id_pory INTEGER REFERENCES pora_rozmowy(id_pory),
	czas_rozmowy REAL,
	PRIMARY KEY(id_rozmowcy, id_miejsca, id_pory)
);

INSERT INTO miejsce_rozmowy 
VALUES
(1, 'Wschod', 'Lubelskie', 'Lublin'),
(2, 'Zachod', 'Wielkopolskie', 'Poznan');

INSERT INTO rozmowca 
VALUES
(1, '18-20 lat'),
(2, '45-65 lat');

INSERT INTO pora_rozmowy
VALUES
(1, '08:00-18:00'),
(2, '18:00=22:00');

INSERT INTO rozmowa_telefoniczna
VALUES
(1, 1, 1, 50.4),
(2, 2, 2, 114.5);

SELECT miasto, przedzial_wieku, czas_rozmowy FROM rozmowa_telefoniczna
NATURAL JOIN miejsce_rozmowy
NATURAL JOIN rozmowca;

/*-napisz funkcję która po wprowadzeniu miasta oraz przedziału wieku (lub godzin) podaje
średni czas trwania rozmowy tel.*/



CREATE OR REPLACE FUNCTION sr_rozmowy (mia VARCHAR, oper VARCHAR)
RETURNS REAL AS
$$
DECLARE
	sr_rozmowy REAL;
BEGIN
	IF oper LIKE '%lat' THEN
		SELECT AVG(czas_rozmowy) INTO sr_rozmowy FROM rozmowa_telefoniczna
		NATURAL JOIN rozmowca NATURAL JOIN miejsce_rozmowy
		WHERE miejsce_rozmowy.miasto = mia
		AND rozmowca.przedzial_wieku = oper;
		RETURN sr_rozmowy;
	ELSE
		SELECT AVG(czas_rozmowy) INTO sr_rozmowy FROM rozmowa_telefoniczna
		NATURAL JOIN pora_rozmowy NATURAL JOIN miejsce_rozmowy
		WHERE miejsce_rozmowy.miasto = mia
		AND pora_rozmowy.przedzial_godziny = oper;
		RETURN sr_rozmowy;
	END IF;
END;
$$ LANGUAGE PLPGSQL;


SELECT sr_rozmowy('Lublin', '18-20 lat');
SELECT sr_rozmowy('Lublin', '08:00-18:00');
