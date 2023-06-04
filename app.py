from flask import Flask, render_template, request, redirect
import json
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve user input from the HTML form
        text = request.form['user_input']
        words = word_tokenize(text)
        tagged_words = pos_tag(words)

        user_keywords = []
        for word, tag in tagged_words:
            if tag.startswith('NN') or tag.startswith('JJ') or tag.startswith('PR'):
                user_keywords.append(word)

        user_query_vectorized = vectorizer.transform([" ".join(user_keywords)])

        predicted_label = clf.predict(user_query_vectorized)[0]
        print(predicted_label)
        relevant_info = "Relevant information not found"
        for item in data:
            if item['query_type'] == predicted_label:
                relevant_info = item['relevant_information']
                break

        return render_template('index.html', relevant_info=relevant_info,predicted_label=predicted_label)    

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
