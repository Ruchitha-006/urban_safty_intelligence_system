from pathlib import Path

import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

VECTORIZER_PATH = MODEL_DIR / "fir_vectorizer.pkl"
MODEL_PATH = MODEL_DIR / "fir_model.pkl"


TRAINING_TEXT = [
    "mobile phone stolen from shop",
    "wallet stolen near bus stand",
    "thief stole cash",
    "chain snatching reported",
    "house burglary at night",
    "attempted robbery with weapon",
    "person attacked with knife",
    "physical assault reported",
    "fight and injury",
    "fraudulent bank transaction",
    "online scam money transfer",
    "cyber fraud complaint",
    "vehicle accident on road",
    "traffic collision",
    "road accident injury",
]

TRAINING_LABELS = [
    "Theft",
    "Theft",
    "Theft",
    "Theft",
    "Burglary",
    "Robbery",
    "Assault",
    "Assault",
    "Assault",
    "Fraud",
    "Cyber Crime",
    "Cyber Crime",
    "Traffic Accident",
    "Traffic Accident",
    "Traffic Accident",
]


def train_model():

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        lowercase=True,
    )

    features = vectorizer.fit_transform(
        TRAINING_TEXT
    )

    classifier = LogisticRegression(
        max_iter=1000
    )

    classifier.fit(
        features,
        TRAINING_LABELS
    )

    joblib.dump(
        vectorizer,
        VECTORIZER_PATH
    )

    joblib.dump(
        classifier,
        MODEL_PATH
    )

    return vectorizer, classifier


def load_model():

    if (
        VECTORIZER_PATH.exists()
        and MODEL_PATH.exists()
    ):

        vectorizer = joblib.load(
            VECTORIZER_PATH
        )

        classifier = joblib.load(
            MODEL_PATH
        )

        return vectorizer, classifier

    return train_model()


def classify_fir(text: str) -> dict:

    vectorizer, classifier = load_model()

    features = vectorizer.transform(
        [text]
    )

    prediction = classifier.predict(
        features
    )[0]

    probabilities = (
        classifier.predict_proba(
            features
        )[0]
    )

    confidence = float(
        max(probabilities)
    )

    return {
        "crime_type": prediction,
        "confidence": round(
            confidence * 100,
            2,
        ),
    }