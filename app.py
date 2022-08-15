"""Adoption Agency application."""
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'SECRET_KEY'

connect_db(app)
db.create_all()


# Homepage

@app.route("/")
def home():
    """Render list of pets"""
    av_pets = Pet.query.filter_by(available=True).all()
    not_av_pets = Pet.query.filter_by(available=False).all()
    return render_template("homepage.html", av_pets=av_pets, not_av_pets=not_av_pets)


@app.route("/add", methods=['GET', 'POST'])
def add_pet():
    """Render create pet form and validate the data to add new pet to DB"""

    form = AddPetForm()

    if form.validate_on_submit():
        """If CSRF Token is received, it's a post request and data is valid we will process teh data to create a new pet"""
        name = form.name.data
        species = form.species.data
        if form.photo_url.data == "":
            photo_url = 'https://www.tibs.org.tw/images/default.jpg'
        else:
            photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(name=name, species=species,
                      photo_url=photo_url, age=age, notes=notes)

        db.session.add(new_pet)
        db.session.commit()

        return redirect("/")

    else:
        """The form will be rendered if it's the first time visiting the page, the CSRF Token wasn't sent or was invalid or if the form data wasn't valid"""
        return render_template("add_pet_form.html", form=form)


@app.route("/<int:pet_id>", methods=['GET', 'POST'])
def show_pet(pet_id):
    """Show info on a single pet."""

    pet = Pet.query.get_or_404(pet_id)

    form = EditPetForm()

    if form.validate_on_submit():
        """When the CSRF Token and the data is valid on a POST request, the current pet will be edited"""
        if form.photo_url.data == "":
            photo_url = pet.photo_url
        else:
            photo_url = form.photo_url.data
        notes = form.notes.data
        available = form.available.data

        pet.photo_url = photo_url
        pet.notes = notes
        pet.available = available

        db.session.add(pet)
        db.session.commit()

        flash(f"{pet.name} was edited successfully")

        return redirect(f"/{pet.id}")

    else:
        """The form will be rendered if it's the first time visiting the page, the CSRF Token wasn't sent or was invalid or if the form data wasn't valid"""
        return render_template("details.html", pet=pet, form=form)
