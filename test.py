from flask import Flask, render_template, request, jsonify
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from extraction.scrape_main import get_notification_data

nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)

# Load the JSON file and initialize the classifier and vectorizer
with open('example.json') as f:
    data = json.load(f)

X = [query['relevant_keywords'] for query in data]
y = [query['query_type'] for query in data]

vectorizer = CountVectorizer(token_pattern=r'\b\w+\b')
X_vectorized = vectorizer.fit_transform([" ".join(keywords) for keywords in X])

clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000)
clf.fit(X_vectorized, y)

# Retrieve initial notification data
initial_notification = get_notification_data()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['user_input']
        words = word_tokenize(text)
        tagged_words = pos_tag(words)

        user_keywords = []
        for word, tag in tagged_words:
            if tag.startswith('NN') or tag.startswith('JJ') or tag.startswith('PR'):
                user_keywords.append(word)

        user_query_vectorized = vectorizer.transform([" ".join(user_keywords)])

        predicted_label = clf.predict(user_query_vectorized)[0]
        relevant_info = "Relevant information not found"
        for item in data:
            if item['query_type'] == predicted_label:
                relevant_info = item['relevant_information']
                break

        response = {
            'predicted_label': predicted_label,
            'relevant_info': relevant_info
        }

        return jsonify(response)

    return render_template('index.html', initial_notification=initial_notification)

@app.route('/refresh', methods=['POST'])
def refresh_notifications():
    # Execute the scrape_main.py script and retrieve the latest notification data
    notification = get_notification_data()

    # Return the notification data as JSON
    return jsonify(notification)

if __name__ == '__main__':
    app.run(debug=True)
