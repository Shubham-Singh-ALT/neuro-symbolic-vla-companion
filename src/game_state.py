from pydantic import BaseModel, Field
from typing import List, Optional

class GameObject(BaseModel):
    label: str
    confidence: float
    box: List[float]  # [x1, y1, x2, y2]

class GameState(BaseModel):
    timestamp: float
    player_health_estimated: int = Field(default=100, ge=0, le=100)
    detected_objects: List[GameObject] = []
    threat_level: str = "Low"
    recommended_action: Optional[str] = None

    def evaluate_threat(self):
        # Simple symbolic rule evaluation
        enemy_count = sum(1 for obj in self.detected_objects if obj.label in ['person', 'enemy'])
        if enemy_count >= 3 or self.player_health_estimated < 25:
            self.threat_level = "Critical"
        elif enemy_count > 0:
            self.threat_level = "Moderate"
        else:
            self.threat_level = "Low"