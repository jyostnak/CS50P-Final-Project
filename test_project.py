from project import calculate_percentage, load_scores, save_scores, format_time
import pytest
import csv

def test_calculate_percentage():
    assert calculate_percentage(4, 5) == 4/5*100
    assert calculate_percentage(6, 6) == 100
    assert calculate_percentage(8, 9) == 8/9*100


def test_fromat_time():
    assert format_time(125) == "02:05"
    assert format_time(60) == "01:00"
    assert format_time(9) == "00:09"

def test_save_scores():
    save_scores(8, 10, "Science", "Easy")

    with open("scores.csv", newline="") as file:
        rows = list(csv.reader(file))

    assert rows[-1] == [
        rows[-1][0],  # date changes every day
        "Science",
        "Easy",
        "8",
        "10"
    ]


def test_load_scores():
    with open("score.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Date", "Subject", "Difficulty", "Your Score", "Total Questions"]
        )
        writer.writerow(
            ["2026-06-04", "Science", "Easy", "8", "10"]
        )

    scores = load_scores()

    assert scores[0]["Subject"] == "Science"
    assert scores[0]["Difficulty"] == "Easy"
    assert scores[0]["Your Score"] == "8"
