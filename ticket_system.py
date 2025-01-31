from collections import defaultdict
from typing import List, Dict, Tuple

class TicketSystem:
    def __init__(self):
        # Store ratings per agent in a dictionary {agent_id: [ratings]}
        self.agent_ratings = defaultdict(list)

    def add_rating(self, agent_id: str, rating: int):
        """Add a rating for a specific agent, ensuring it stays within 1-5."""
        if 1 <= rating <= 5:
            self.agent_ratings[agent_id].append(rating)
        else:
            raise ValueError("Rating must be between 1 and 5")
        
    def calculate_average_ratings(self) -> Dict[str, float]:
        """Calculate the average rating for each agent."""
        return {
            agent: round(sum(ratings) / len(ratings), 2) if ratings else 0
            for agent, ratings in self.agent_ratings.items()
        }
    
    def get_highest_lowest_rating(self) -> Dict[str, Tuple[int, int]]:
        """Retrieve the highest and lowest rating per agent."""
        return {
            agent: (max(ratings), min(ratings)) if ratings else (None, None)
            for agent, ratings in self.agent_ratings.items()
        }