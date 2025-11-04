import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, Tuple
from app.models import UserProfile

class BidPredictor:
    def __init__(self):
        self.ctr_model = LinearRegression()
        self.bid_model = LinearRegression()
        self.train()
    
    def train(self):
        # Generate synthetic data: [age, region_score, interest_count, bid_floor]
        np.random.seed(42)
        n_samples = 1000
        
        ages = np.random.randint(18, 65, n_samples)
        region_scores = np.random.choice([0.8, 0.6, 0.4], n_samples)
        interest_counts = np.random.randint(1, 6, n_samples)
        bid_floors = np.random.uniform(0.1, 2.0, n_samples)
        
        X = np.column_stack([ages, region_scores, interest_counts, bid_floors])
        
        # CTR: higher for younger users, premium regions, more interests
        ctr_y = (0.01 + (65 - ages) * 0.0005 + region_scores * 0.02 + 
                interest_counts * 0.003 + np.random.normal(0, 0.005, n_samples))
        ctr_y = np.clip(ctr_y, 0.001, 0.1)
        
        # Bid adjustment: based on CTR and competition
        bid_y = bid_floors * (1 + ctr_y * 10 + np.random.normal(0, 0.1, n_samples))
        
        self.ctr_model.fit(X, ctr_y)
        self.bid_model.fit(X, bid_y)
    
    def predict(self, user_profile: UserProfile, bid_floor: float) -> Tuple[float, float]:
        region_score = 0.8 if user_profile.region in ["US", "UK"] else 0.6
        features = np.array([[user_profile.age, region_score, len(user_profile.interests), bid_floor]])
        
        # Add randomization for online learning simulation
        noise = np.random.normal(0, 0.01)
        predicted_ctr = max(0.001, self.ctr_model.predict(features)[0] + noise)
        optimal_bid = max(bid_floor, self.bid_model.predict(features)[0] + noise)
        
        return predicted_ctr, optimal_bid