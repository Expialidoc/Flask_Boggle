from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "abbracadabbraaaa22223"

boggle_game = Boggle()

@app.route('/')
def show_board():
    """Show homepage."""
    board = boggle_game.make_board()
    session['board'] = board
    nplays = session.get("nplays", 0)
    highscore = session.get("highscore",0)

    return render_template("board.html", board = board, nplays=nplays, highscore=highscore)

@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response}) #jsonify since an AJAX request was made to server (boggle.js)

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update nplays, update high score if appropriate."""
    score = request.json["score"]
    print(request.form,request.json)
    highscore = session.get("highscore", 0)
    print(highscore)
    nplays = session.get("nplays", 0)
    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)
    # import pdb
    # pdb.set_trace()
    print(session['highscore'])
    return jsonify(brokeRecord=score > highscore)