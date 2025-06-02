create_table_genders = """
CREATE TABLE genders (
    gender TEXT PRIMARY KEY
);
"""

create_table_blood_types = """
CREATE TABLE blood_types (
    blood_type TEXT PRIMARY KEY
);
"""

create_table_organ_names = """
CREATE TABLE organ_names (
    organ_name TEXT PRIMARY KEY
);
"""

create_table_organs = """
CREATE TABLE organs (
    organ_name TEXT,
    blood_type TEXT,
    FOREIGN KEY (organ_name) REFERENCES organ_names(organ_name),
    FOREIGN KEY (blood_type) REFErences blood_types(blood_type)
);
"""

create_table_donors = """
CREATE TABLE donors (
    donor_id            INT PRIMARY KEY,
    name                TEXT      NOT NULL,
    birthdate           TIMESTAMP NOT NULL,
    blood_type          TEXT      NOT NULL,
    possible_extraction TIMESTAMP NOT NULL,
    gender              TEXT      NOT NULL,
    height              INT,
    weight              INT,
    photo               BINARY,
    foreign key (gender) references genders (gender) 
);
"""

create_table_acceptors = """
CREATE TABLE acceptors (
    acceptor_id        INT PRIMARY KEY,
    name               TEXT not null,
    birthdate          TIMESTAMP NOT NULL,
    blood_type         TEXT,
    possible_transplantation TIMESTAMP NOT NULL,
    gender             TEXT NOT NULL,
    height             INT,
    weight             INT,
    photo BINARY,
    FOREIGN KEY (gender) REFERENCES genders(gender),
    FOREIGN KEY (blood_type) REFERENCES blood_types(blood_type)
    );
"""