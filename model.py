import os
import pickle
import random
import string
from typing import List
import numpy as np
from sklearn.linear_model import LogisticRegression
from feature_extractor import extract_url_features

FEATURE_DIM = 16

class PhishModel:
    def __init__(self, model_path="phishguard_model.pkl"):
        self.model_path = model_path
        self.model = None

    def ensure_trained(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            self.train_and_save()

    def train_and_save(self, n_samples: int = 2000, random_seed: int = 42):
        random.seed(random_seed)
        np.random.seed(random_seed)

        X, y = self._generate_synthetic_dataset(n_samples)
        clf = LogisticRegression(max_iter=200)
        clf.fit(X, y)

        with open(self.model_path, "wb") as f:
            pickle.dump(clf, f)
        self.model = clf

    def predict_proba(self, X: List[List[float]]):
        if self.model is None:
            self.ensure_trained()
        # Return probability of class 1 (phishing)
        return self.model.predict_proba(np.array(X))[:, 1]

    # ---------- Synthetic data generator (heuristic) ----------
    def _generate_synthetic_dataset(self, n=2000):
        legit_domains = [
            "example.com","wikipedia.org","openai.com","github.com","google.com",
            "microsoft.com","amazon.com","apple.com","cloudflare.com","reddit.com",
            "bbc.co.uk","mit.edu","yahoo.com","stackexchange.com","khanacademy.org"
        ]
        phishing_tokens = [
            "login","secure","verify","account","update","confirm","wallet",
            "free","bonus","prize","gift","urgent","support","helpdesk","signin"
        ]
        sus_tlds = ["zip","xyz","top","gq","country","kim","men","loan","lol","ml","cf","tk"]

        X, y = [], []

        def rnd_path():
            parts = ["".join(random.choices(string.ascii_lowercase, k=random.randint(3,10))) for _ in range(random.randint(1,4))]
            return "/" + "/".join(parts)

        # Legit samples
        for _ in range(n//2):
            dom = random.choice(legit_domains)
            scheme = random.choice(["https","https","https","http"])
            path = rnd_path() if random.random() < 0.5 else "/"
            url = f"{scheme}://{dom}{path}"
            if random.random() < 0.3:
                url += f"?q={' '.join(random.choice(['news','docs','about','product']) for _ in range(2))}"
            X.append(extract_url_features(url))
            y.append(0)

        # Phishing-like samples
        for _ in range(n//2):
            token = random.choice(phishing_tokens)
            base = "".join(random.choices(string.ascii_lowercase, k=random.randint(5,10)))
            tld = random.choice(sus_tlds)
            sub = "".join(random.choices(string.ascii_lowercase, k=random.randint(3,6)))
            scheme = random.choice(["http","http","https"])
            # Use multiple subdomains and hyphens
            url = f"{scheme}://{sub}-{token}.{base}.{tld}/{token}/index.html"
            # Add query noise
            if random.random() < 0.8:
                url += f"?id={random.randint(1000,9999)}&secure=true&login={random.randint(1,2)}"
            # Occasionally use IP host
            if random.random() < 0.15:
                ip = ".".join(str(random.randint(1,255)) for _ in range(4))
                url = f"{scheme}://{ip}/{token}/update?acc={random.randint(100,999)}"
            X.append(extract_url_features(url))
            y.append(1)

        return np.array(X), np.array(y)
