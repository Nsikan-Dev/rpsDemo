import sqlite3 as sqlite_db
from flask import Flask, request, jsonify, render_template
import random
app = Flask(__name__)

def createGame(playerOne,playerOneScore,playerTwo,playerTwoScore):
    con = sqlite_db.connect('my-test.db')
    sql = 'INSERT INTO GAMERECORD (playerOne, playerOneScore, playerTwo, playerTwoScore) values(?, ?, ?, ?)'
    data = (
        playerOne,
        playerOneScore,
        playerTwo,
        playerTwoScore
    )
    
    try:
        con.execute(sql, data)
    except:
        print("Failed to create game.")
    
    con.commit()
    con.close()

    return 'added game record'

def returnGameCount():
    con = sqlite_db.connect('my-test.db')
    data = con.execute("SELECT * FROM GAMERECORD")
    return len(data.fetchall())

def returnCurrentGame():
    id = returnGameCount()
    con = sqlite_db.connect('my-test.db')
    data = con.execute("SELECT * FROM GAMERECORD WHERE id = :id", {"id": id})
    return data.fetchone()

def makeSelection():
    options = ["rock","paper","scissors"]
    return random.choice(options)

def compareSelections(sel1,sel2):
    selectionDict = {}
    selectionDict["rock"] = 1
    selectionDict["paper"] = 2
    selectionDict["scissors"] = 3

    if ((selectionDict[sel1] - selectionDict[sel2]) == 1) or ((selectionDict[sel1] - selectionDict[sel2]) == -2):
        return sel1
    elif ((selectionDict[sel1] - selectionDict[sel2]) == -1) or ((selectionDict[sel1] - selectionDict[sel2]) == 2):
        return sel2

    return False

def updateGame(id, field, value):
    con = sqlite_db.connect('my-test.db')
    print(f"Update {str(id)} {field} {value}")
    if (field == "playerOneScore"):
        con.execute("UPDATE GAMERECORD SET playerOneScore = :value WHERE id = :id", {"id": id, "value": value})
        con.commit()
    elif (field == "playerTwoScore"):
        con.execute("UPDATE GAMERECORD SET playerTwoScore = :value WHERE id = :id", {"id": id, "value": value})
        con.commit()


@app.route('/')
def enterPlayerOneName():
    return render_template("intro.html")

@app.route('/enterPlayerTwoName', methods = ['GET', 'POST'])
def enterPlayerTwoName():
    
    playerOneName = request.form["player_name_input"]
    if not playerOneName:
        return render_template("error.html", message = "No value for player one")
    
    if request.form.get('computer_input'):
        playerTwoName = "Computer"
        # create game entry
        createGame(playerOneName,0,playerTwoName,0)
        # return rendering of turn 1
        id = returnGameCount()
        return render_template("player1turn.html", gameId = id, playerOne = playerOneName, player1Score = 0, playerTwo = playerTwoName, player2Score = 0)


    else:
        return render_template("player2.html", playerOne = playerOneName)

@app.route('/acceptPlayerTwoName', methods = ['POST'])
def acceptPlayerTwoName():
    playerOneName = request.form["player_one_name_input"]
    if not playerOneName:
        return render_template("error.html", message = "No value for player one")

    playerTwoName = request.form["player_two_name_input"]
    if not playerTwoName:
        return render_template("error.html", message = "No value for player two")

    createGame(playerOneName,0,playerTwoName,0)
    id = returnGameCount()
    
    return render_template("player1turn.html", gameId = id, playerOne = playerOneName, player1Score = 0, playerTwo = playerTwoName, player2Score = 0)

@app.route('/acceptPlayerOneSelection', methods = ['POST'])
def acceptPlayerOneSelection():
    # get game values
    currentGame = returnCurrentGame()
    id = currentGame[0]
    playerOneName = currentGame[1]
    playerOneScore = currentGame[2]
    playerTwoName = currentGame[3]
    playerTwoScore = currentGame[4]

    # get player 1 selection
    playerOneSelection = request.form["rps"]

    if (playerTwoName == "Computer"):
        # make selection
        computerSelection = makeSelection()
        # compare selections
        winner = compareSelections(playerOneSelection,computerSelection)
        # declare winner
        if (winner == playerOneSelection):
            winner = playerOneName
            playerOneScore+=1
            updateGame(id, "playerOneScore", playerOneScore)
        elif (winner == computerSelection):
            winner = playerTwoName
            playerTwoScore+=1
            updateGame(id, "playerTwoScore", playerTwoScore)

        return render_template("score.html",
                                winner = winner,
                                gameId = id, 
                                playerOne = playerOneName, 
                                player1Score = playerOneScore, 
                                playerTwo = playerTwoName, 
                                player2Score = playerTwoScore)

    # render player 2 entry page
    return render_template("player2turn.html", 
                            player1Selection = playerOneSelection,
                            gameId = id, 
                            playerOne = playerOneName, 
                            player1Score = playerOneScore, 
                            playerTwo = playerTwoName, 
                            player2Score = playerTwoScore)


@app.route('/acceptPlayerTwoSelection', methods = ['POST'])
def acceptPlayerTwoSelection():
    # get game values
    currentGame = returnCurrentGame()
    id = currentGame[0]
    playerOneName = currentGame[1]
    playerOneScore = currentGame[2]
    playerTwoName = currentGame[3]
    playerTwoScore = currentGame[4]

    # get player 1 selection
    playerOneSelection = request.form["player_one_selection"]
    playerTwoSelection = request.form["rps"]

    
    # compare selections
    winner = compareSelections(playerOneSelection,playerTwoSelection)
    # declare winner
    if (winner == playerOneSelection):
        winner = playerOneName
        playerOneScore+=1
        updateGame(id, "playerOneScore", playerOneScore)
    elif (winner == playerTwoSelection):
        winner = playerTwoName
        playerTwoScore+=1
        updateGame(id, "playerTwoScore", playerTwoScore)

    return render_template("score.html",
                            winner = winner,
                            gameId = id, 
                            playerOne = playerOneName, 
                            player1Score = playerOneScore, 
                            playerTwo = playerTwoName, 
                            player2Score = playerTwoScore)

@app.route('/continueOrNot', methods=['POST'])
def continueOrNot():
    playerSelection = request.form["rps"]
    if not playerSelection:
        return render_template("error.html", message = "New game oe new turn?")

    if (playerSelection == "new_game"):
        return render_template("intro.html")
    
    elif (playerSelection == "new_turn"):
        currentGame = returnCurrentGame()
        id = currentGame[0]
        playerOneName = currentGame[1]
        playerOneScore = currentGame[2]
        playerTwoName = currentGame[3]
        playerTwoScore = currentGame[4]

        return render_template("player1turn.html", 
                                gameId = id, 
                                playerOne = playerOneName, 
                                player1Score = playerOneScore, 
                                playerTwo = playerTwoName, 
                                player2Score = playerTwoScore)

    return render_template("error.html", message = "New game or new turn?")


# API functions
@app.route('/api/v1/turn/create', methods=['POST'])
def createNewTurn():
    con = sqlite_db.connect('my-test.db')
    sql = 'INSERT INTO TURNRECORD (gameId, playerOneName, playerOneSelection, playerTwoName, playerTwoSelection) values(?, ?, ?, ?, ?)'
    data = (
        request.form["gameId"],
        request.form["playerOneName"],
        request.form["playerOneSelection"],
        request.form["playerTwoName"],
        request.form["playerTwoSelection"]
    )

    try:
        con.execute(sql, data)
    except:
        print("Failed to create turn.")

    return 'turn created'

@app.route('/api/v1/turns/all', methods=['GET'])
def turns_all():
    con = sqlite_db.connect('my-test.db')
    with con:
        data = con.execute("SELECT * FROM TURNRECORD")
    return jsonify(data.fetchall())

@app.route('/api/v1/game/create', methods=['POST'])
def createNewGame():
    con = sqlite_db.connect('my-test.db')
    sql = 'INSERT INTO GAMERECORD (playerOne, playerOneScore, playerTwo, playerTwoScore) values(?, ?, ?, ?)'
    data = (
        request.form["playerOne"],
        request.form["playerOneScore"],
        request.form["playerTwo"],
        request.form["playerTwoScore"]
    )
    
    try:
        con.execute(sql, data)
    except:
        print("Failed to create game.")
    
    con.commit()
    con.close()

    return 'added game record'

@app.route('/api/v1/games/all', methods=['GET'])
def games_all():
    con = sqlite_db.connect('my-test.db')
    with con:
        data = con.execute("SELECT * FROM GAMERECORD")
    return jsonify(data.fetchall())