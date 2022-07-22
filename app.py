from flask import Flask, render_template, redirect, request
from settings import parse_form, decode_settings, Settings
from randomizer import generate_page, talkatoo
import secrets

app = Flask(__name__)


@app.context_processor
def utility_processor():
    def get_number(value : str) -> str:
        output = 0
        for x in value:
            output += ord(x)
        return output
    return dict(get_number=get_number)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        settings = parse_form(request.form)
        try:
            card_mode = request.form['cardmode'] == 'on'
        except:
            card_mode = False

        if card_mode:
            if len(request.form['seed']) > 0:
                return redirect("/card/" + str(request.form['seed']) + "?settings=" + str(settings))
            else:
                return redirect("/card?settings=" + str(settings))
        else:
            if len(request.form['seed']) > 0:
                return redirect("/seed/" + str(request.form['seed']) + "?settings=" + str(settings))
            else:
                return redirect("/seed?settings=" + str(settings))
    return render_template('index.html')


@app.route("/seed")
@app.route("/seed/")
def get_seed():
    settings = request.args.get('settings')
    seed = secrets.token_hex(4)
    if settings is None:
        return redirect("/seed/" + seed)
    else:
        return redirect("/seed/" + seed + "?settings=" + settings)


@app.route("/seed/<seed>")
def randomizer(seed : int):
    if len(seed) != 8:
        return "Invalid seed length."
    else:
        try:
            seed_value = int(seed, 16)
        except ValueError:
            return "Seed can only contain hex."
    settings = request.args.get('settings')
    if settings is not None:
        settings_class = decode_settings(settings)
    else:
        return redirect("/seed/" + seed + "?settings=" + str(Settings()))

    return render_template('randomizer.html', seed=seed, moons=generate_page(seed_value, settings_class))


@app.route("/card")
@app.route("/card/")
def get_card():
    settings = request.args.get('settings')
    seed = secrets.token_hex(4)
    if settings is None:
        return redirect("/card/" + seed)
    else:
        return redirect("/card/" + seed + "?settings=" + settings)

@app.route("/card/<seed>")
def card(seed : int):
    if len(seed) != 8:
        return "Invalid seed length."
    else:
        try:
            seed_value = int(seed, 16)
        except ValueError:
            return "Seed can only contain hex."
    settings = request.args.get('settings')
    if settings is not None:
        settings_class = decode_settings(settings)
    else:
        return redirect("/card/" + seed + "?settings=" + str(Settings()))

    return render_template('card.html', seed=seed, moonData=talkatoo(seed_value, settings_class))
