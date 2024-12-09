from flask import Flask, render_template, request
from textblob import TextBlob
import spacy

app = Flask(__name__)

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

@app.route('/')
def index():
    return render_template('index.html', responses=[])

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']

    # Analyze with spaCy
    doc = nlp(text)

    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Perform sentiment analysis
    blob = TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    sentiment_text = "Positive" if sentiment_polarity > 0 else "Negative" if sentiment_polarity < 0 else "Neutral"

    # Classify intent
    if text.endswith('?'):
        intent = "Question"
    elif "feel" in text or "am" in text:
        intent = "Emotion"
    elif any(word in text.lower() for word in ["want", "need", "like", "hope"]):
        intent = "Desire"
    else:
        intent = "Statement"

    # Append response
    new_response = {
        "text": text,
        "entities": entities if entities else "No named entities found.",
        "sentiment": sentiment_text,
        "intent": intent,
        "message": "Analysis complete."
    }

    # Retrieve previous responses and append the new one
    responses = request.form.get('responses', '[]')
    responses_list = eval(responses) if responses else []
    responses_list.append(new_response)

    return render_template('index.html', responses=responses_list)

if __name__ == '__main__':
    app.run(debug=True)
