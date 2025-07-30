from langgraph.graph import StateGraph
from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class State(TypedDict):
    messages: list
    user_input: str
    response: str

def process_input(state: State):
    # Initialize the LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # Get the user input
    user_message = state["user_input"]
    
    # Create conversation history
    conversation = state["messages"] + [{"role": "user", "content": user_message}]
    
    # Get response from LLM
    response = llm.invoke([{"role": msg["role"], "content": msg["content"]} for msg in conversation])
    
    # Update state
    new_state = state.copy()
    new_state["response"] = response.content
    new_state["messages"] = conversation + [{"role": "assistant", "content": response.content}]
    
    return new_state

# Create the graph
workflow = StateGraph(State)
workflow.add_node("process", process_input)
workflow.set_entry_point("process")
workflow.set_finish_point("process")

app = workflow.compile()

if __name__ == "__main__":
    print("LangGraph QA bot Started!")
    print("Type quit to exit\n")

    # Initialize conversation state
    state = {
        "messages": [],
        "user_input": "",
        "response": ""
    }

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # update the state with user input
        state["user_input"] = user_input

        # Process through langgraph
        result = app.invoke(state)

        # Print bot response
        print(f"Bot: {result['response']}\n")

        # Update state for next iteration
        state = result