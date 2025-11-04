from typing import List, Dict
from app.models import Bid
import asyncio

class MockDatabase:
    def __init__(self):
        self.ads = [
            Bid(ad_id="ad_1", advertiser_id="adv_1", bid_amount=2.5, target_audience="tech", category="software"),
            Bid(ad_id="ad_2", advertiser_id="adv_2", bid_amount=1.8, target_audience="general", category="retail"),
            Bid(ad_id="ad_3", advertiser_id="adv_3", bid_amount=3.2, target_audience="premium", category="luxury"),
            Bid(ad_id="ad_4", advertiser_id="adv_4", bid_amount=1.2, target_audience="budget", category="discount"),
        ]
        self.bid_history = []
    
    async def get_available_ads(self) -> List[Bid]:
        await asyncio.sleep(0.001)  # Simulate DB latency
        return self.ads
    
    async def store_bid_result(self, result: Dict):
        await asyncio.sleep(0.001)
        self.bid_history.append(result)

db = MockDatabase()