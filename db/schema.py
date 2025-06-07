create_table_genders = """
CREATE TABLE genders (
    gender TEXT PRIMARY KEY NOT NULL,
    created_at DATETIME NOT NULL default CURRENT_TIMESTAMP
);
"""

create_table_blood_types = """
CREATE TABLE blood_types (
    blood_type TEXT PRIMARY KEY NOT NULL,
    created_at DATETIME  NOT NULL default CURRENT_TIMESTAMP
);
"""

create_table_organ_names = """
CREATE TABLE organ_names (
    organ_name TEXT PRIMARY KEY NOT NULL,
    created_at DATETIME  NOT NULL default CURRENT_TIMESTAMP
);
"""

create_table_organs = """
CREATE TABLE organs (
    organ_id         INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    organ_name TEXT NOT NULL,
    blood_type TEXT NOT NULL,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (organ_name) REFERENCES organ_names(organ_name) ON UPDATE CASCADE,
    FOREIGN KEY (blood_type) REFERENCES blood_types(blood_type) ON UPDATE CASCADE
);
"""

create_table_donors = """
CREATE TABLE donors (
    donor_id            INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name                TEXT      NOT NULL,
    registration_date   DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    birthdate           DATETIME  NOT NULL,
    blood_type          TEXT      NOT NULL,
    possible_extraction DATETIME  NOT NULL,
    gender              TEXT      NOT NULL,
    height              INT,
    weight              INT,
    phone TEXT, 
    address TEXT,
    notes TEXT,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (gender) REFERENCES genders (gender) ON UPDATE CASCADE,
    FOREIGN KEY (blood_type) REFERENCES blood_types (blood_type) ON UPDATE CASCADE
);
"""

create_table_acceptors = """
CREATE TABLE acceptors (
    acceptor_id        INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name               TEXT not null,
    registration_date  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    birthdate          DATETIME  NOT NULL,
    blood_type         TEXT,
    gender             TEXT NOT NULL,
    height             INT,
    weight             INT,
    phone TEXT,
    address TEXT,
    notes TEXT,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (gender) REFERENCES genders(gender) ON UPDATE CASCADE,
    FOREIGN KEY (blood_type) REFERENCES blood_types(blood_type) ON UPDATE CASCADE
    );
"""

create_table_donor_photos = """
CREATE TABLE donor_photos (
    donor_id            INTEGER NOT NULL, 
    photo BINARY NOT NULL,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id) ON DELETE CASCADE 
);"""

create_table_acceptor_photos = """
CREATE TABLE acceptor_photos (
    acceptor_id  INTEGER NOT NULL, 
    photo BINARY NOT NULL,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (acceptor_id) REFERENCES acceptors(acceptor_id) ON DELETE CASCADE 
);
"""

create_table_donated_organs = """
CREATE TABLE donated_organs (
    donor_id  INTEGER NOT NULL,
    organ_name TEXT NOT NULL,
    extraction_ts DATETIME NOT NULL,
    expiration_ts DATETIME,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id) ON DELETE CASCADE,
    FOREIGN KEY (organ_name) REFERENCES organ_names(organ_name) ON UPDATE CASCADE
);"""

create_awaited_organs = """
CREATE TABLE awaited_organs (
    acceptor_id INTEGER NOT NULL,
    organ_name TEXT,
    created_at  DATETIME  NOT NULL default CURRENT_TIMESTAMP,
    FOREIGN KEY (acceptor_id) REFERENCES acceptors(acceptor_id) ON DELETE CASCADE,
    FOREIGN KEY (organ_name) REFERENCES organ_names(organ_name) ON UPDATE CASCADE
);"""

all_tables = (
    create_table_genders,
    create_table_blood_types,
    create_table_organ_names,
    create_table_organs,
    create_table_donors,
    create_table_acceptors,
    create_table_donor_photos,
    create_table_acceptor_photos,
    create_table_donated_organs,
    create_awaited_organs,
)
