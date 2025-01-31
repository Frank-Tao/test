# tests/test_ticket_system.py
import pytest
from ticket_system import TicketSystem  

@pytest.fixture
def initialized_ticket_system():
    # Create an instance of TicketSystem
    ticket_system = TicketSystem()

    # Add initial ratings for testing
    ticket_system.add_rating("agent1", 5)
    ticket_system.add_rating("agent1", 4)
    ticket_system.add_rating("agent2", 3)
    ticket_system.add_rating("agent2", 2)
    ticket_system.add_rating("agent3", 1)

    return ticket_system

def test_add_rating(initialized_ticket_system):
    # Test adding a valid rating
    initialized_ticket_system.add_rating("agent1", 3)
    assert initialized_ticket_system.agent_ratings["agent1"] == [5, 4, 3]

    # Test adding an invalid rating (should raise ValueError)
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        initialized_ticket_system.add_rating("agent1", 6)

def test_calculate_average_ratings(initialized_ticket_system):
    # Test calculating average ratings
    averages = initialized_ticket_system.calculate_average_ratings()
    assert averages == {
        "agent1": 4.5,  # (5 + 4) / 2 = 4.5
        "agent2": 2.5,  # (3 + 2) / 2 = 2.5
        "agent3": 1.0,  # (1) / 1 = 1.0
    }

def test_get_highest_lowest_rating(initialized_ticket_system):
    # Test getting highest and lowest ratings
    highest_lowest = initialized_ticket_system.get_highest_lowest_rating()
    assert highest_lowest == {
        "agent1": (5, 4),  # Highest: 5, Lowest: 4
        "agent2": (3, 2),  # Highest: 3, Lowest: 2
        "agent3": (1, 1),  # Highest: 1, Lowest: 1
    }

def test_empty_ratings():
    # Create a new TicketSystem instance with no ratings
    ticket_system = TicketSystem()

    # Test calculate_average_ratings with no ratings
    averages = ticket_system.calculate_average_ratings()
    assert averages == {}  # No agents, so empty dict

    # Test get_highest_lowest_rating with no ratings
    highest_lowest = ticket_system.get_highest_lowest_rating()
    assert highest_lowest == {}  # No agents, so empty dict