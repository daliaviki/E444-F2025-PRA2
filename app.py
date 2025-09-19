from datetime import datetime
from flask import Flask, render_template
from flask_moment import Moment
from flask import request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask import session

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-me"
moment = Moment(app)

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="PRA2",
        name="Dalia",                
        timestamp=datetime.utcnow()  
    )

class NameEmailForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    email = StringField("UofT email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = NameEmailForm()
    result = None

    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()

        # Check for changes compared to previous submission
        prev_name = session.get("prev_name")
        prev_email = session.get("prev_email")
        if prev_name is not None and prev_name != name:
            flash("Looks like you have changed your name!", "warning")
        if prev_email is not None and prev_email != email:
            flash("Looks like you have changed your email!", "warning")

        # Update stored values
        session["prev_name"] = name
        session["prev_email"] = email

        # UofT email check
        if "utoronto" in email.lower():
            result = f"Username: {name} — Email: {email}"
            flash("Thanks! UofT email verified.", "success")
        else:
            # Instead of a big heading, attach an error to the email field
            form.email.errors.append("Please use your UofT email address.")

    return render_template(
        "signup.html",
        title="Chapter 4 — Form",
        form=form,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)

