import pandas as pd
import os
import joblib

from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from data_prep import prepare_corpus
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'balanced_reviews.csv')

# Load data
dataset = pd.read_csv(DATA_PATH)
dataset = dataset.dropna(subset=["clean_summary"])
dataset["clean_summary"] = dataset["clean_summary"].astype(str)

# Reset indexes to avoid KeyError
dataset = dataset.reset_index(drop=True)

corpus = prepare_corpus(dataset, "clean_summary")
labels = dataset["label"].values[:len(corpus)]  # Asegura alineación

# Vectorize (sparse input)
vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(corpus)

y = labels

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Define models
# Only models compatible with sparse input:
models = {
    "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000),
    "SVM": SVC(kernel='linear', class_weight='balanced', probability=True),
}

# Train & evaluate
results = []
trained_models = {}

for name, model in models.items():
    print(f"Trainning {name}...")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    results.append({
        "Model": name,
        "Accuracy": acc,
        "F1": f1,
        "Precision": precision,
        "Recall": recall
    })
    trained_models[name] = model


# Results DataFrame
df_results = pd.DataFrame(results).sort_values(by='F1', ascending=False)
print("\n=== Model Results ===")
print(df_results)


# Save best model and vectorizer
best_model_name = df_results.iloc[0]['Model']
best_model = trained_models[best_model_name]

print(f"Best Model: {best_model_name}")


# Create models folder if it doesn't exist
MODEL_DIR = os.path.join('machine_learning', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Save the best model and the vectorizer
joblib.dump(best_model, os.path.join(MODEL_DIR, 'best_model.pkl'))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'vectorizer.pkl'))

print(f"\n✅ Best Model: {os.path.join(MODEL_DIR, 'best_model.pkl')}")
print(f"✅ Vectorizer saved in: {os.path.join(MODEL_DIR, 'vectorizer.pkl')}")