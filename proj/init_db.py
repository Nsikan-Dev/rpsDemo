import sqlite3

con = sqlite3.connect('my-test.db')
with con:
    con.execute("""
        CREATE TABLE GAMERECORD (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            playerOne TEXT,
            playerOneScore INTEGER DEFAULT 0,
            playerTwo TEXT,
            playerTwoScore INTEGER DEFAULT 0
        );
    """)

    con.execute("""
        CREATE TABLE TURNRECORD (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            gameId INTEGER,
            playerOne TEXT,
            playerOneSelection TEXT,
            playerTwo TEXT,
            playerTwoSelection TEXT, 
            FOREIGN KEY (gameId) REFERENCES GAMERECORD(id)
        );
    """)
con.commit()
con.close()