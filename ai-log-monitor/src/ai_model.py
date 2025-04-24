from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

class LogAnomalyDetector:
    def __init__(self, contamination=0.05, random_state=42):
        self.vectorizer = TfidfVectorizer()
        self.model = IsolationForest(contamination=contamination, random_state=random_state)
        self.trained = False

    def fit(self, log_messages):
        """
        Train the anomaly detection model using a list of log messages.
        """
        X = self.vectorizer.fit_transform(log_messages)
        self.model.fit(X)
        self.trained = True

    def predict(self, log_messages):
        """
        Predict whether each log message is normal or an anomaly.
        Returns: predictions (-1 for anomaly, 1 for normal), and scores
        """
        if not self.trained:
            raise RuntimeError("Model is not trained yet. Call fit() first.")

        X = self.vectorizer.transform(log_messages)
        predictions = self.model.predict(X)
        scores = self.model.decision_function(X)
        return predictions, scores
