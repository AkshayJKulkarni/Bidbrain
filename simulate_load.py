import asyncio
import time
import httpx
import random
from typing import List

async def send_bid_request(client: httpx.AsyncClient, request_id: int) -> float:
    start_time = time.time()
    
    payload = {
        "ad_id": f"ad_{request_id}",
        "advertiser_id": f"adv_{request_id % 10}",
        "user_profile": {
            "age": random.randint(18, 65),
            "region": random.choice(["US", "UK", "CA", "DE"]),
            "interests": random.sample(["tech", "sports", "fashion", "food", "travel"], k=random.randint(1, 3))
        },
        "bid_floor": round(random.uniform(0.1, 2.0), 2)
    }
    
    response = await client.post("http://localhost:8000/bid", json=payload)
    response.raise_for_status()
    
    return time.time() - start_time

async def run_load_test(num_requests: int = 1000):
    print(f"Starting load test with {num_requests} requests...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        start_time = time.time()
        
        tasks = [send_bid_request(client, i) for i in range(num_requests)]
        response_times = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
    
    # Calculate metrics
    avg_response_time = sum(response_times) / len(response_times)
    requests_per_second = num_requests / total_time
    
    print(f"\n--- Load Test Results ---")
    print(f"Total requests: {num_requests}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average response time: {avg_response_time:.3f}s")
    print(f"Requests per second: {requests_per_second:.2f}")
    print(f"Min response time: {min(response_times):.3f}s")
    print(f"Max response time: {max(response_times):.3f}s")

if __name__ == "__main__":
    asyncio.run(run_load_test(1000))