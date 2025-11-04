# BidBrain — AI-Powered Bidding Engine

A high-performance real-time ad bidding system that combines machine learning with async processing to optimize bid decisions at scale.

## Tech Stack
- **FastAPI** - Async web framework for high-throughput API endpoints
- **Python** - Core language with asyncio for concurrent processing
- **scikit-learn** - Linear regression models for CTR prediction and bid optimization
- **asyncio** - Concurrent request handling for 1000+ requests/second

## Highlights
- **High Performance**: Handles 1000+ simulated bid requests per second
- **ML-Powered**: Uses trained models to predict CTR and optimize bid amounts
- **Scalable Architecture**: Designed for async performance and horizontal scaling
- **Real Value Creation**: Demonstrates Moloco's value "Create Real Value" by blending ML intelligence with real-time engineering excellence

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

## API Endpoints

### POST /bid - Process Bid Request
```bash
curl -X POST "http://localhost:8000/bid" \
  -H "Content-Type: application/json" \
  -d '{
    "ad_id": "ad_001",
    "advertiser_id": "adv_001", 
    "user_profile": {
      "age": 28,
      "region": "US",
      "interests": ["tech", "shopping"]
    },
    "bid_floor": 1.5
  }'
```

### POST /train - Retrain ML Model
```bash
curl -X POST "http://localhost:8000/train"
```

### GET /stats - View Performance Metrics
```bash
curl "http://localhost:8000/stats"
```

## Load Testing

```bash
# Run 1000 concurrent requests
python simulate_load.py
```