#!/usr/bin/env python3
"""
Example script demonstrating how to use the AgentFactory with config loading.
"""

from src.agents import AgentFactory, agent_factory

def main():
    """Demonstrate loading agents from config file."""
    
    # Create a factory instance (or use the global one)
    factory = AgentFactory()
    
    print("Available agent types:", factory.list_agent_types())
    
    try:
        # Load agents from the config file
        loaded_agents = factory.load_agents_from_config()
        
        print(f"\nLoaded {len(loaded_agents)} agents:")
        for name, agent in loaded_agents.items():
            print(f"- {name}: {agent.description}")
        
        # List all agents in the factory
        print(f"\nAll agents in factory: {factory.list_agents()}")
        
        # Get info about a specific agent
        if loaded_agents:
            first_agent_name = list(loaded_agents.keys())[0]
            agent_info = factory.get_agent_info(first_agent_name)
            print(f"\nInfo for '{first_agent_name}':")
            for key, value in agent_info.items():
                print(f"  {key}: {value}")
        
        # Example: Get a response from an agent
        if "question_generator_agent" in loaded_agents:
            agent = loaded_agents["question_generator_agent"]
            print(f"\nTesting agent '{agent.name}':")
            try:
                response = agent.get_response("Generate a question about Python programming")
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error getting response: {e}")
        
    except Exception as e:
        print(f"Error loading agents from config: {e}")

if __name__ == "__main__":
    main()
