import tkinter as tk
from tkinter import messagebox


# ---------------- QUIZ DATA ----------------

questions = [
    {
        "question": "What does CPU stand for?",
        "options": [
            "Central Processing Unit",
            "Computer Personal Unit",
            "Central Program Utility",
            "Control Processing Unit"
        ],
        "answer": 0
    },
    {
        "question": "Which language is used for web page structure?",
        "options": [
            "Python",
            "HTML",
            "Java",
            "C++"
        ],
        "answer": 1
    },
    {
        "question": "Which device is used to enter data into a computer?",
        "options": [
            "Monitor",
            "Printer",
            "Keyboard",
            "Speaker"
        ],
        "answer": 2
    },
    {
        "question": "What is the full form of RAM?",
        "options": [
            "Read Access Memory",
            "Random Access Memory",
            "Run Access Memory",
            "Rapid Access Machine"
        ],
        "answer": 1
    },
    {
        "question": "Which one is an operating system?",
        "options": [
            "Google",
            "Windows",
            "Python",
            "HTML"
        ],
        "answer": 1
    }
]


# ---------------- SETTINGS ----------------

TIME_LIMIT = 10


# ---------------- VARIABLES ----------------

current_question = 0
score = 0
time_left = TIME_LIMIT
timer_id = None
user_answers = []


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Quiz Application with Timer")
root.geometry("700x500")
root.resizable(False, False)


# ---------------- FUNCTIONS ----------------

def start_timer():
    global time_left, timer_id

    time_left = TIME_LIMIT
    timer_label.config(text=f"Time Left: {time_left} seconds")

    if timer_id is not None:
        root.after_cancel(timer_id)

    countdown()


def countdown():
    global time_left, timer_id

    timer_label.config(text=f"Time Left: {time_left} seconds")

    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, countdown)
    else:
        submit_answer(timeout=True)


def load_question():
    global current_question

    if current_question >= len(questions):
        show_result()
        return

    question_data = questions[current_question]

    question_number_label.config(
        text=f"Question {current_question + 1} of {len(questions)}"
    )

    question_label.config(text=question_data["question"])

    selected_option.set(-1)

    for i in range(4):
        option_buttons[i].config(
            text=question_data["options"][i],
            value=i
        )

    submit_button.config(state=tk.NORMAL)

    start_timer()


def submit_answer(timeout=False):
    global current_question, score, timer_id

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    selected = selected_option.get()
    correct_answer = questions[current_question]["answer"]

    if timeout:
        user_answers.append("Time Out")
    elif selected == -1:
        messagebox.showwarning(
            "No Answer",
            "Please select an option."
        )
        start_timer()
        return
    else:
        user_answers.append(selected)

        if selected == correct_answer:
            score += 1

    current_question += 1

    load_question()


def show_result():
    global timer_id

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    for widget in root.winfo_children():
        widget.destroy()

    result_title = tk.Label(
        root,
        text="QUIZ COMPLETED!",
        font=("Arial", 24, "bold")
    )
    result_title.pack(pady=20)

    result_label = tk.Label(
        root,
        text=f"Your Score: {score} / {len(questions)}",
        font=("Arial", 20, "bold")
    )
    result_label.pack(pady=10)

    summary_title = tk.Label(
        root,
        text="Answer Summary",
        font=("Arial", 16, "bold")
    )
    summary_title.pack(pady=10)

    for i, answer in enumerate(user_answers):
        correct = questions[i]["answer"]

        if answer == "Time Out":
            text = f"Q{i + 1}: Time Out"
        elif answer == correct:
            text = f"Q{i + 1}: Correct"
        else:
            text = f"Q{i + 1}: Incorrect"

        summary = tk.Label(
            root,
            text=text,
            font=("Arial", 12)
        )
        summary.pack()

    restart_button = tk.Button(
        root,
        text="Restart Quiz",
        font=("Arial", 14, "bold"),
        command=restart_quiz
    )
    restart_button.pack(pady=20)

    exit_button = tk.Button(
        root,
        text="Exit",
        font=("Arial", 14, "bold"),
        command=root.destroy
    )
    exit_button.pack()


def restart_quiz():
    global current_question, score, user_answers

    current_question = 0
    score = 0
    user_answers = []

    create_quiz_screen()
    load_question()


def create_quiz_screen():

    for widget in root.winfo_children():
        widget.destroy()

    # Title
    title_label = tk.Label(
        root,
        text="QUIZ APPLICATION",
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=15)

    # Question number
    global question_number_label
    question_number_label = tk.Label(
        root,
        text="",
        font=("Arial", 14)
    )
    question_number_label.pack(pady=5)

    # Timer
    global timer_label
    timer_label = tk.Label(
        root,
        text="Time Left: 10 seconds",
        font=("Arial", 16, "bold")
    )
    timer_label.pack(pady=10)

    # Question
    global question_label
    question_label = tk.Label(
        root,
        text="",
        font=("Arial", 17, "bold"),
        wraplength=600
    )
    question_label.pack(pady=20)

    # Selected option
    global selected_option
    selected_option = tk.IntVar(value=-1)

    # Options
    global option_buttons
    option_buttons = []

    for i in range(4):
        button = tk.Radiobutton(
            root,
            text="",
            variable=selected_option,
            value=i,
            font=("Arial", 13),
            anchor="w",
            width=45
        )

        button.pack(pady=5)
        option_buttons.append(button)

    # Submit button
    global submit_button

    submit_button = tk.Button(
        root,
        text="SUBMIT ANSWER",
        font=("Arial", 14, "bold"),
        command=lambda: submit_answer(False)
    )
    submit_button.pack(pady=20)


# ---------------- START QUIZ ----------------

create_quiz_screen()
load_question()

root.mainloop()