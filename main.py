import os
import pickle
from random import choice
from flask import Flask, render_template, request

app = Flask(__name__)
db_file = 'db.pickle'

def load_database():
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            return pickle.load(file)
    return {'guesses': [], 'computer_number': choice(range(1, 101))}

def save_database(database):
    with open(db_file, 'wb') as file:
        pickle.dump(database, file)

db = load_database()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        guess = int(request.form['number_guess'])
        message = check_number_show_message(guess, db['computer_number'])
        db['guesses'].append(message)
        print(db['guesses'])
        print(db['computer_number'])
        save_database(db)

    return render_template('index.html', guesses=reversed(db['guesses']))

@app.route('/reset')
def reset():
    db['computer_number'] = choice(range(1, 101))
    db['guesses'] = []
    save_database(db)
    return render_template('index.html', guesses=db['guesses'])

# Computer's guess and client guess
def check_number_show_message(guessed_number, computer_number):
    if guessed_number < computer_number:
        return f"{guessed_number} is too low"
    elif guessed_number > computer_number:
        return f"{guessed_number} is too high"
    elif guessed_number == computer_number:
        return f"{guessed_number} is right"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
