DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Quizzes;
DROP TABLE IF EXISTS Results;

CREATE TABLE Students
    (id  INTEGER PRIMARY KEY,
    firstname  TEXT NOT NULL,
    lastname   TEXT NOT NULL );

CREATE TABLE Quizzes
     (id INTEGER PRIMARY KEY,
     subject TEXT,
     quiznum INTEGER,
     date  DATETIME  );

CREATE TABLE Results
    (studentid INTEGER,
    quizid      INTEGER,
    score        INTEGER,
    FOREIGN KEY (studentid)  REFERENCES Students(id),
    FOREIGN KEY (quizid) REFERENCES Quizzes(id) );
    
