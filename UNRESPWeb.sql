PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Experiences(id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, sense TEXT, smell TEXT, throat TEXT,  eyes TEXT, skin TEXT, tired TEXT, nausea TEXT, otherObs TEXT, windDir TEXT, windSpeed TEXT, precip TEXT, latitude REAL, longitude REAL, submitted DATETIME DEFAULT CURRENT_TIMESTAMP);
COMMIT;
