# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image
import numpy as np
import os, random, base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

model = load_model("all_labels.h5")
class_labels = ['n0', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'n8', 'n9']
class_names = ['alouatta_palliata', 'erythrocebus_patas', 'cacajao_calvus', 'macaca_fuscata', 'cebuella_pygmea', 'cebus_capucinus', 'mico_argentatus', 'saimiri_sciureus', 'aotus_nigriceps', 'trachypithecus_johnii']
image_dir = os.path.join("static", "images")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    prediction = None
    image_data = None

    if request.method == 'POST':
        image = request.files['image']
        img = Image.open(image).convert('RGB').resize((224, 224))
        img_array = img_to_array(img)
        img_preprocessed = preprocess_input(img_array)
        img_exp = np.expand_dims(img_preprocessed, axis=0)

        preds = model.predict(img_exp)
        prediction = class_names[np.argmax(preds)]

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        image_data = base64.b64encode(buffered.getvalue()).decode()

    return render_template("upload.html", prediction=prediction, image_data=image_data)

@app.route('/submit', methods=['GET', 'POST'])
def submit_page():
    if request.method == 'POST':
        user_guess = request.form.get('user_guess')
        session['user_guess'] = user_guess
        return redirect(url_for('game_page'))

    # GET request — pick image and show to user
    all_images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_name = random.choice(all_images)
    session['image_name'] = image_name
    return render_template("submit.html", class_names=class_names, image_name=image_name)


@app.route('/game', methods=['GET'])
def game_page():
    image_name = session.get('image_name')
    user_guess = session.get('user_guess')

    if not image_name or not user_guess:
        return redirect(url_for('submit_page'))

    image_path = os.path.join(image_dir, image_name)
    true_label = next((label for label in class_labels if label in image_name), "Unknown")
    if true_label != "Unknown":
        index = class_labels.index(true_label)
        true_label = class_names[index]


    img = Image.open(image_path).convert('RGB').resize((224, 224))
    img_array = img_to_array(img)
    img_preprocessed = preprocess_input(img_array)
    img_exp = np.expand_dims(img_preprocessed, axis=0)

    preds = model.predict(img_exp)
    print(preds)
    prediction = class_names[np.argmax(preds)]

    if user_guess == true_label and prediction == true_label:
        result_message = "🎉 Both you and the AI guessed correctly!"
    elif user_guess == true_label:
        result_message = "✅ You were right! AI missed it."
    elif prediction == true_label:
        result_message = "🧠 The AI guessed correctly! You missed it."
    else:
        result_message = "❌ Both guesses were incorrect."

    return render_template("game.html", image_name=image_name, prediction=prediction,
                           user_guess=user_guess, true_label=true_label,
                           result_message=result_message)

@app.route('/info')
def info():
    monkey_info = {
        "Alouatta palliata": "Mantled howler monkey, known for loud howling; found in Central and South America.",
        "Erythrocebus patas": "Patas monkey, fastest primate; lives in savannas and open woodlands in Africa.",
        "Cacajao calvus": "Bald uakari, red-faced monkey from the Amazon; known for short tails and red skin.",
        "Macaca fuscata": "Japanese macaque or snow monkey; lives in Japan, known for bathing in hot springs.",
        "Cebuella pygmaea": "Pygmy marmoset, the smallest monkey species; found in the Amazon rainforest.",
        "Cebus capucinus": "White-faced capuchin, highly intelligent and social; common in Central America.",
        "Mico argentatus": "Silvery marmoset; lives in the eastern Amazon Rainforest in Brazil.",
        "Saimiri sciureus": "Common squirrel monkey; agile and curious, lives in tropical forests in South America.",
        "Aotus nigriceps": "Black-headed night monkey; nocturnal species from the Amazon basin.",
        "Trachypithecus johnii": "Nilgiri langur; native to the Western Ghats in India, with glossy black fur."
    }
    return render_template("info.html", monkey_info=monkey_info)

if __name__ == '__main__':
    app.run(debug=True)
