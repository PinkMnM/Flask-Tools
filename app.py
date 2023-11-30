from flask import Flask, flash, request, redirect, render_template, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config["SECRET_KEY"] = "its_a_secret_to_everyone"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

SURVEY_SESSION_KEY = "survey_responses"


@app.route("/")
def homepage():
    return render_template(
        "survey.html",
        title=surveys.satisfaction_survey.title,
        instructions=surveys.satisfaction_survey.instructions,
    )


@app.route("/questions/<int:q>")
def question(q):
    responses = session.get(SURVEY_SESSION_KEY, [])

    if len(responses) == len(surveys.satisfaction_survey.questions):
        flash("You have completed the survey; redirected to the complete page.")
        return redirect("/complete")

    if q != len(responses):
        flash("Invalid/completed survey page; redirected to the appropriate question.")
        return redirect(url_for("question", q=len(responses)))

    current_question = surveys.satisfaction_survey.questions[q]
    return render_template(
        "question.html",
        q=q,
        question=current_question.question,
        choices=current_question.choices,
    )


@app.route("/answer", methods=["POST"])
def answer():
    responses = session.get(SURVEY_SESSION_KEY, [])
    responses += list(request.form.values())
    session[SURVEY_SESSION_KEY] = responses
    return redirect(url_for("question", q=len(responses)))


@app.route("/complete")
def complete():
    responses = session.get(SURVEY_SESSION_KEY, [])

    if len(responses) != len(surveys.satisfaction_survey.questions):
        flash(
            "Invalid/completed inaccessible survey page; redirected to the appropriate question."
        )
        return redirect(url_for("question", q=len(responses)))

    return render_template("complete.html")


if __name__ == "__main__":
    app.run()
