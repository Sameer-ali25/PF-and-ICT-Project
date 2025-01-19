from flask import Flask, render_template, request, redirect, url_for,flash 
import random

app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Required for flashing messages

EASY_LEVEL_ATTEMPTS = 10
HARD_LEVEL_ATTEMPTS = 5

# Global variables to store game state
answer = None
attempts_remaining = 0

def set_difficulty(level_chosen):
    if level_chosen == 'easy':
        return EASY_LEVEL_ATTEMPTS
    elif level_chosen == 'hard':
        return HARD_LEVEL_ATTEMPTS
    else:
        return HARD_LEVEL_ATTEMPTS  # Default to hard if invalid

def check_answer(guessed_number):
    global attempts_remaining
    if guessed_number < answer:
        attempts_remaining -= 1
        return "Your guess is too low."
    elif guessed_number > answer:
        attempts_remaining -= 1
        return "Your guess is too high."
    else:
        return f"Your guess is right! The answer is {answer}."

@app.route('/')
def start_game():
    return render_template('start_game.html')

@app.route('/play', methods=['POST', 'GET'])
def play_game():
    global answer, attempts_remaining
    if request.method == 'POST':
        if 'level' in request.form:
            level = request.form['level']
            answer = random.randint(1, 100)
            attempts_remaining = set_difficulty(level)
            flash(f'Game started! You have {attempts_remaining} attempts.')
            return redirect(url_for('play_game'))

        if 'guess' in request.form:
            guessed_number = request.form.get('guessed_number', type=int)
            message = check_answer(guessed_number)

            if attempts_remaining <= 0:
                flash("You are out of guesses. The answer was: " + str(answer))
                return redirect(url_for('start_game'))
            else:
                flash(message)

    return render_template('play_game.html', attempts_remaining=attempts_remaining)

if __name__ == '__main__':
    app.run(debug=True)