from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime

class UserProfile(BaseModel):
    age: int = Field(default=25, ge=13, le=100)
    region: str = Field(default="US")
    interests: List[str] = Field(default=["tech", "shopping"])

class AdRequest(BaseModel):
    ad_id: str = Field(default="ad_001")
    advertiser_id: str = Field(default="adv_001")
    user_profile: UserProfile = Field(default_factory=UserProfile)
    bid_floor: float = Field(default=0.5, ge=0.0)

class AdResponse(BaseModel):
    ad_id: str
    final_bid: float = Field(ge=0.0)
    predicted_ctr: float = Field(ge=0.0, le=1.0)
    win_probability: float = Field(ge=0.0, le=1.0)

class Bid(BaseModel):
    advertiser_id: str
    bid_amount: float = Field(ge=0.0)
    timestamp: datetime = Field(default_factory=datetime.now)
    outcome: Literal["win", "loss"] = Field(default="loss")