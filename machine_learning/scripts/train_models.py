import os
import joblib
import logging
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from evaluate_model import evaluate
from data_prep import prepare_corpus
from sklearn.metrics import classification_report, confusion_matrix


# =============================
# Setup logging
# =============================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================
# Config paths
# =============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'balanced_reviews.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# =============================
# Load data
# =============================
logger.info("📥 Loading dataset...")
dataset = pd.read_csv(DATA_PATH)
dataset = dataset.dropna(subset=["clean_summary"])
dataset["clean_summary"] = dataset["clean_summary"].astype(str)
dataset = dataset.reset_index(drop=True)
logger.info(f"✅ Dataset size: {len(dataset):,} samples")

# =============================
# Prepare corpus
# =============================
logger.info("🔍 Preparing corpus...")
corpus = prepare_corpus(dataset, "clean_summary")
labels = dataset["label"].values[:len(corpus)]

# =============================
# Vectorize
# =============================
logger.info("🧹 Vectorizing with TF-IDF...")
vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(corpus)
y = labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
logger.info(f"✅ Train samples: {X_train.shape[0]:,}, Test samples: {X_test.shape[0]:,}")

# =============================
# Define models
# =============================
logger.info("🔧 Setting up models...")
models = {
    "Logistic Regression": LogisticRegression(
        class_weight='balanced', max_iter=1000
    ),
    "Linear SVM": CalibratedClassifierCV(
        LinearSVC(class_weight='balanced', max_iter=1000)
    )
}

# =============================
# Train & evaluate
# =============================
results = []
trained_models = {}

try:
    for name, model in models.items():
        logger.info(f"🚀 Training {name}...")
        model.fit(X_train, y_train)
        logger.info(f"✅ {name} trained successfully!")

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

except KeyboardInterrupt:
    logger.warning("🛑 Training interrupted by user!")
    exit()

# =============================
# Results & Save best
# =============================
df_results = pd.DataFrame(results).sort_values(by='F1', ascending=False)
logger.info("\n=== Model Results ===\n%s", df_results)

best_model_name = df_results.iloc[0]['Model']
best_model = trained_models[best_model_name]
logger.info(f"🏆 Best Model: {best_model_name}")

joblib.dump(best_model, os.path.join(MODEL_DIR, 'best_model.pkl'))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, 'vectorizer.pkl'))

logger.info(f"✅ Best Model saved to: {os.path.join(MODEL_DIR, 'best_model.pkl')}")
logger.info(f"✅ Vectorizer saved to: {os.path.join(MODEL_DIR, 'vectorizer.pkl')}")


# =============================
# CM & Classification Report
# =============================

y_test_pred = best_model.predict(X_test)
logger.info("\n=== Classification Report ===\n%s",
            classification_report(y_test, y_test_pred, target_names=["Negative", "Positive"], zero_division=0))

cm = confusion_matrix(y_test, y_test_pred)
logger.info(f"Confusion Matrix:\n{cm}")

plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Negative", "Positive"],
            yticklabels=["Negative", "Positive"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title(f"Confusion Matrix ({best_model_name})")
plt.tight_layout()
plt.show()