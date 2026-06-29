# Project name: Smart Study Companion
# Name: K.Jyostna
# GitHub username: jyostnak
# edX username: Jyostnakondepi
# Hyderabad, India
# 05-06-2026
from datetime import datetime
import time
import html
import requests
import matplotlib.pyplot as plt
import random
import csv
import os


def main():
    while True:
        print("\n=== SMART STUDY COMPANION ===")
        try:
            choice = input("\n1.Take quiz\n2.View progress chart\n3.Pomodoro timer\n4.View previous scores\n5.Exit\nWhat would you like to do? ")
            if choice == "1":
                get_questions()
            elif choice == "2":
                get_chart()
            elif choice == "3":
                pomodoro_timer()
            elif choice == "4":
                view_score()
            elif choice == "5":
                break
            else:
                raise KeyError
        except KeyError:
            print("Invalid input.")




def get_questions():
    while True:
        try:
            subject = int(input("1. Computer Science\n2. Mathematics\n3. Science\n4. History\n5. Geography\n6. General Knowledge\n7. Politics\n8. Art\n9. Gadgets\nChoose subject:"))
            subjects = {
            1: 18,  # Computer Science
            2: 19,  # Mathematics
            3: 17,  # Science & Nature
            4: 23,  # History
            5: 22,  # Geography
            6: 9,   # General Knowledge
            7: 24,  # Politics
            8: 25,  # Art
            9: 30  # Science: Gadgets
        }
            subject_names = {
        1: "Computer Science",
        2: "Mathematics",
        3: "Science",
        4: "History",
        5: "Geography",
        6: "General Knowledge",
        7: "Politics",
        8: "Art",
        9: "Gadgets"
    }
            subject_name = subject_names[subject]
            category = subjects[subject]
            amount = input("How many questions? ")
            difficult = input("1.Easy\n2.Medium\n3.Hard\nChoose difficulty: ")
            difficulties = {
            "1": "easy",
            "2": "medium",
            "3": "hard"
        }

            difficulty = difficulties[difficult]
            diff = difficulty.capitalize()
            response = requests.get(f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}")
            data = response.json()
            questions = data['results']
            score = 0
            for q in questions:
                print(html.unescape(q["question"]))

                if q["type"] == 'multiple':
                    options = []
                    options.extend([html.unescape(x) for x in q["incorrect_answers"]])
                    options.append(html.unescape(q['correct_answer']))
                    random.shuffle(options)
                    for i, op in enumerate(options, start = 1):
                        print(f'{i}. {op}')
                    correct_option = options.index(q['correct_answer']) + 1
                    i = 0
                    while i <= 2:
                        try:
                            user_ans = int(input('Answer: '))
                            selected_option = options[user_ans - 1]
                            if user_ans == correct_option:
                                print("Correct answer!")
                                score += 1
                                break
                            else:
                                if i == 2:
                                    print(f"Correct answer: {q["correct_answer"]}")
                                else:
                                    print("Oops.. Try again!")
                        except ValueError:
                            print("Please enter valid option number.")
                        except IndexError:
                            print("Please enter a valid option number.")

                        i += 1

                if q["type"] == "boolean":
                        while True:
                            try:
                                user_anstf = input("Answer(True/False): ").strip().lower().capitalize()
                                if user_anstf in ["True", "False"]:
                                    if user_anstf == (q["correct_answer"]):
                                        print("Correct answer!")
                                        score += 1
                                        break
                                    else:
                                        print("Uh-ohh.. That was wrong!")
                                        print(f'Correct answer: {q["correct_answer"]}')
                                        break
                                else:
                                    raise ValueError
                            except ValueError:
                                print("This is a True/False question.")
                                print("Please enter only True or False.")

            print(f"Score: {score}/{amount}")
            ask = input("Do you want to save the score? (Yes/No) ").lower()
            if ask in ["yes", "no"]:
                if ask == "yes":
                    save_scores(score, amount, subject_name, diff)
            else:
                raise KeyError
            return score, amount, subject_name, diff
        except KeyError:
            print("Invalid input.")
        except ValueError:
            print("Invalid input.")



def save_scores(score, amount, subject_name, diff):
    date = datetime.today().date().isoformat()
    file_exists = os.path.isfile("scores.csv")
    with open("scores.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                ["Date", "Subject", "Difficulty", "Your Score", "Total Questions"]
            )
        writer.writerow([
            date,
            subject_name,
            diff,
            score,
            amount
        ])



def load_scores():
    scores = []
    try:
        with open("scores.csv", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scores.append(row)
    except FileNotFoundError:
        print("File not found")
    return scores



def calculate_percentage(score, total):
    return (score/total)*100



def get_chart():
    scores = load_scores()
    dates = []
    percentages = []
    for row in scores:
        dates.append(row["Date"])

        percentage = calculate_percentage(
            int(row["Your Score"]),
            int(row["Total Questions"])
        )
        percentages.append(percentage)

    plt.plot(dates, percentages, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Percentage")
    plt.title("Quiz Performance Over Time")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.savefig("Progress.png")
    print("Chart saved!")


def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"



def countdown(seconds):
    while seconds > 0:
        print(format_time(seconds), end="\r")
        time.sleep(1)
        seconds -= 1

    print("00:00")


def pomodoro_timer():
    try:
        study = int(input("Study minutes: "))
        break_time = int(input("Break minutes: "))

        print("Study session started!")
        countdown(study * 60)

        print("\nBreak time!")
        countdown(break_time * 60)

        print("\nSession complete!")
    except ValueError:
        print("Please enter a number.")


def view_score():
    scores = load_scores()

    if not scores:
        print("No scores found.")
        return
    for row in scores:
        print(
            f"{row['Date']}|"
            f"{row['Subject']}|"
            f"{row['Difficulty']} | "
            f"{row['Your Score']}/{row['Total Questions']}"
        )




if __name__ == "__main__":
    main()
