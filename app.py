from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from questions import QUESTIONS
import random
import time

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

EXAM_DURATION = 30 * 60  # 30 minutes


def get_exam_questions():
    if "exam_questions" not in session:
        q = [dict(item) for item in QUESTIONS]
        random.shuffle(q)
        for item in q:
            item["options"] = list(item["options"])
            random.shuffle(item["options"])
        session["exam_questions"] = q
        session["answers"] = {}
        session["started_at"] = time.time()
    return session["exam_questions"]


def remaining_seconds():
    started = session.get("started_at")
    if started is None:
        return EXAM_DURATION
    return max(0, int(EXAM_DURATION - (time.time() - started)))


@app.route("/")
def index():
    # Reset an old exam when the candidate returns to the start page.
    session.clear()
    return render_template("index.html", total=len(QUESTIONS), duration=30)


@app.route("/start", methods=["POST"])
def start():
    session.clear()
    get_exam_questions()
    return redirect(url_for("exam", number=1))


@app.route("/exam/<int:number>")
def exam(number):
    questions = get_exam_questions()

    if remaining_seconds() <= 0:
        return redirect(url_for("submit"))

    if number < 1 or number > len(questions):
        return redirect(url_for("exam", number=1))

    answers = session.get("answers", {})
    current = questions[number - 1]

    return render_template(
        "exam.html",
        question=current,
        number=number,
        total=len(questions),
        answers=answers,
        remaining=remaining_seconds(),
    )


@app.route("/answer", methods=["POST"])
def answer():
    questions = get_exam_questions()

    if remaining_seconds() <= 0:
        return jsonify({"ok": False, "expired": True})

    number = int(request.form["number"])
    selected = request.form.get("answer")

    if 1 <= number <= len(questions) and selected:
        answers = session.get("answers", {})
        answers[str(number - 1)] = selected
        session["answers"] = answers
        session.modified = True

    return jsonify({"ok": True})


@app.route("/submit", methods=["GET", "POST"])
def submit():
    questions = get_exam_questions()
    answers = session.get("answers", {})

    score = sum(
        1 for i, q in enumerate(questions)
        if answers.get(str(i)) == q["answer"]
    )

    total = len(questions)
    unanswered = sum(1 for i in range(total) if str(i) not in answers)
    percentage = (score / total) * 100 if total else 0

    if percentage >= 70:
        grade = "Excellent"
    elif percentage >= 50:
        grade = "Good"
    elif percentage >= 40:
        grade = "Pass"
    else:
        grade = "Needs Improvement"

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        unanswered=unanswered,
        grade=grade,
    )


if __name__ == "__main__":
    app.run(debug=True)
