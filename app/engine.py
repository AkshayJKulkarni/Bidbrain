import asyncio
import random
from typing import List
from app.models import AdRequest, AdResponse, Bid
from app.ml_model import BidPredictor

class BidEngine:
    def __init__(self):
        self.predictor = BidPredictor()
        self.bid_logs = []
    
    async def process_request(self, request: AdRequest) -> AdResponse:
        predicted_ctr, optimal_bid = self.predictor.predict(request.user_profile, request.bid_floor)
        final_bid = request.bid_floor * (1 + predicted_ctr)
        win_probability = min(final_bid / (request.bid_floor * 2), 1.0)
        
        # Simulate win/loss outcome
        outcome = "win" if random.random() < win_probability else "loss"
        
        # Log bid result
        bid_log = Bid(
            advertiser_id=request.advertiser_id,
            bid_amount=final_bid,
            outcome=outcome
        )
        self.bid_logs.append(bid_log)
        
        return AdResponse(
            ad_id=request.ad_id,
            final_bid=final_bid,
            predicted_ctr=predicted_ctr,
            win_probability=win_probability
        )
    
    async def batch_process(self, requests: List[AdRequest]) -> List[AdResponse]:
        tasks = [self.process_request(request) for request in requests]
        return await asyncio.gather(*tasks)

engine = BidEngine()