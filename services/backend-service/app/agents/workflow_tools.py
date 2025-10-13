"""
Workflow tools that wrap graph-based workflows for use as tools in the orchestrator.
"""

from strands import tool
from strands.multiagent import GraphBuilder
from .specialized_agents import (
    behavioral_question_generator, 
    behavioral_question_evaluator,
    technical_question_generator, 
    technical_question_evaluator
)

@tool
def behavioral_workflow(user_input: str) -> str:
    """
    Execute the complete behavioral interview workflow using a graph-based approach.
    This tool coordinates the behavioral question generation and evaluation process.

    Args:
        user_input: The user's input or response to process through the behavioral workflow

    Returns:
        A comprehensive result from the behavioral interview workflow
    """
    try:
        # Build the behavioral workflow graph
        builder = GraphBuilder()
        
        # Add nodes using agent factories
        builder.add_node(behavioral_question_generator, "behavioral_question")
        builder.add_node(behavioral_question_evaluator, "behavioral_evaluation")
        
        # Add edges (dependencies)
        builder.add_edge("behavioral_question", "behavioral_evaluation")
        
        # Set entry point
        builder.set_entry_point("behavioral_question")
        
        # Configure execution limits for safety
        builder.set_execution_timeout(600)  # 10 minute timeout
        
        # Build and execute the graph
        graph = builder.build()
        result = graph(user_input)
        
        # Format the result for the orchestrator
        if hasattr(result, 'status') and hasattr(result, 'execution_order'):
            return f"Behavioral Workflow Complete\nStatus: {result.status}\nExecution Order: {[node.node_id for node in result.execution_order]}\nResult: {str(result)}"
        else:
            return f"Behavioral Workflow Result: {str(result)}"
            
    except Exception as e:
        return f"Error in behavioral workflow: {str(e)}"

@tool
def technical_workflow(user_input: str) -> str:
    """
    Execute the complete technical interview workflow using a graph-based approach.
    This tool coordinates the technical question generation and evaluation process.

    Args:
        user_input: The user's input or response to process through the technical workflow

    Returns:
        A comprehensive result from the technical interview workflow
    """
    try:
        # Build the technical workflow graph
        builder = GraphBuilder()
        
        # Add nodes using agent factories
        builder.add_node(technical_question_generator, "technical_question")
        builder.add_node(technical_question_evaluator, "technical_evaluation")
        
        # Add edges (dependencies)
        builder.add_edge("technical_question", "technical_evaluation")
        
        # Set entry point
        builder.set_entry_point("technical_question")
        
        # Configure execution limits for safety
        builder.set_execution_timeout(600)  # 10 minute timeout
        
        # Build and execute the graph
        graph = builder.build()
        result = graph(user_input)
        
        # Format the result for the orchestrator
        if hasattr(result, 'status') and hasattr(result, 'execution_order'):
            return f"Technical Workflow Complete\nStatus: {result.status}\nExecution Order: {[node.node_id for node in result.execution_order]}\nResult: {str(result)}"
        else:
            return f"Technical Workflow Result: {str(result)}"
            
    except Exception as e:
        return f"Error in technical workflow: {str(e)}"
