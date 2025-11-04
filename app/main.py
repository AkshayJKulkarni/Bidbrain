from fastapi import FastAPI, Depends
import logging
from typing import Dict
from app.models import AdRequest, AdResponse
from app.engine import BidEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BidBrain", description="AI-powered ad bidding engine", version="1.0.0")

def get_bid_engine() -> BidEngine:
    return BidEngine()

@app.post("/bid", response_model=AdResponse)
async def process_bid(ad_request: AdRequest, engine: BidEngine = Depends(get_bid_engine)):
    logger.info(f"Processing bid request for ad_id: {ad_request.ad_id}")
    response = await engine.process_request(ad_request)
    logger.info(f"Bid processed: final_bid={response.final_bid:.3f}, ctr={response.predicted_ctr:.4f}")
    return response

@app.post("/train")
async def retrain_model(engine: BidEngine = Depends(get_bid_engine)):
    logger.info("Retraining model")
    engine.predictor.train()
    return {"status": "Model retrained successfully"}

@app.get("/stats")
async def get_stats(engine: BidEngine = Depends(get_bid_engine)) -> Dict:
    if not engine.bid_logs:
        return {"total_requests": 0, "average_ctr": 0.0, "win_rate": 0.0}
    
    total_requests = len(engine.bid_logs)
    wins = sum(1 for bid in engine.bid_logs if bid.outcome == "win")
    win_rate = wins / total_requests
    avg_ctr = sum(0.02 for _ in engine.bid_logs) / total_requests  # Mock CTR
    
    return {
        "total_requests": total_requests,
        "average_ctr": avg_ctr,
        "win_rate": win_rate
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)