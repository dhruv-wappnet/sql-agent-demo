import asyncio
import os
from agent import agent
from agents import Runner

prompts = [
    "List all employees working in the Logistics department.",
    "Show all inventory items that have less than 20 units in stock.",
    "Show me the names of employees who last updated any inventory item.",
    "Which technicians performed maintenance in the last 7 days? List their names and the vehicle plates.",
    "List all employees whose RFID tag was used in either an inventory update or a vehicle maintenance operation.",
    "Show employees who updated inventory items AND also performed vehicle maintenance."
]

async def run_evaluation():
    print("Starting Evaluation...\n")
    # Initialize Runner with the agent
    # Note: Depending on the SDK version, Runner might need specific initialization
    # If Runner isn't the right entry point, we might need to look at how run_demo_loop is implemented
    # But usually Runner(agent).run(input) is the pattern.
    
    # Creating a new runner for each turn or reusing? 
    # Reusing preserves history, which might be good or bad. 
    # The prompts seem independent. Let's try independent runs to ensure no context pollution, 
    # although "Show me..." implies context is okay. 
    # But for strict evaluation of specific queries, independent is often cleaner.
    # However, Runner usually maintains state.
    
    for i, prompt in enumerate(prompts, 1):
        print(f"--- Level {1 if i<=2 else 2 if i<=4 else 3} Prompt {i} ---")
        print(f"Query: {prompt}")
        
        # We'll create a fresh runner for each query to ensure independence
        runner = Runner()
        
        try:
            result = await runner.run(starting_agent=agent,input=prompt)
            print("\nResponse:")
            print(result.final_output)
        except Exception as e:
            print(f"Error running prompt: {e}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY is not set. Evaluation might fail.")
    asyncio.run(run_evaluation())
