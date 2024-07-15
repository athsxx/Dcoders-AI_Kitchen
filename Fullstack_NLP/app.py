from flask import Flask, request, jsonify, render_template
import csv
import spacy
import re
import gensim
from gensim.models import Word2Vec

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

measurement_units = [
    "cup", "cups", "tablespoon", "tablespoons", "teaspoon", "teaspoons",
    "tbsp", "tsp", "ounce", "ounces", "oz", "pound", "pounds", "lb", "lbs",
    "gram", "grams", "g", "kilogram", "kilograms", "kg", "liter", "liters", "ml"
]
common_utensils = ["pan", "pot", "knife", "spoon", "fork", "bowl", "plate", "grater", "whisker", "blender", "oven", "stove", "skillet", "fryer", "toaster", 'tong', 'glass', 'ladle', 'masher', 'mixer', 'peeler', 'plates', 'rolling pin', 'spatula', 'strainer']

def remove_bracketed_content(text):
    return re.sub(r'\[.*?\]|\(.*?\)', '', text)

def preprocess_text(text):
    text = remove_bracketed_content(text)
    doc = nlp(text.lower())
    return [token.text for token in doc if not token.is_stop and not token.is_punct and token.text.isalpha()]

def read_recipes_from_csv(filename):
    recipes = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipes.append(row)
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipes.append(row)
    return recipes

filename = "veg_recipes.csv"
recipes = read_recipes_from_csv(filename)
all_texts = []
for recipe in recipes:
    combined_text = recipe["TranslatedRecipeName"] + " " + recipe["TranslatedIngredients"] + " " + recipe["TranslatedInstructions"]
    all_texts.append(preprocess_text(combined_text))

model = Word2Vec(sentences=all_texts, vector_size=100, window=5, min_count=1, workers=4)

def extract_ingredients_w2v(ingredients_text):
    cleaned_text = remove_bracketed_content(ingredients_text)
    ingredients = []
    doc = nlp(cleaned_text)
    current_ingredient = []
    for token in doc:
        if token.pos_ in ["NOUN", "ADJ", "PROPN"] and token.text.lower() not in measurement_units and not token.like_num:
            current_ingredient.append(token.text.lower())
        else:
            if current_ingredient:
                ingredients.append(" ".join(current_ingredient))
                current_ingredient = []
    if current_ingredient:
        ingredients.append(" ".join(current_ingredient))
    return ingredients

def extract_utensils_and_instructions_w2v(text):
    utensils = []
    for utensil in common_utensils:
        if utensil in text.lower():
            utensils.append(utensil)
    instructions = []
    doc = nlp(text)
    for sentence in doc.sents:
        if any(token.pos_ == "VERB" and token.dep_ == "ROOT" for token in sentence):
            instructions.append(sentence.text.strip())
    return utensils, instructions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_recipe', methods=['POST'])
def analyze_recipe():
    data = request.get_json()
    chosen_recipe = data.get('recipe_name')
    for recipe in recipes:
        if recipe["TranslatedRecipeName"] == chosen_recipe:
            ingredients_text = recipe["TranslatedIngredients"]
            instructions_text = recipe["TranslatedInstructions"]
            ingredients = extract_ingredients_w2v(ingredients_text)
            utensils, instructions = extract_utensils_and_instructions_w2v(instructions_text)
            return jsonify({
                'ingredients': ingredients,
                'utensils': utensils,
                'instructions': instructions
            })
    return jsonify({'error': 'Recipe not found'})

if __name__ == '__main__':
    app.run(debug=True)
