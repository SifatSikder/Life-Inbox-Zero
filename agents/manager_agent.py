import json
import os
import google.generativeai as genai

class ManagerAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.system_prompt = """
        You are the Manager Agent for "Life Inbox Zero".
        Style: Minimalist, Clear, Direct, No fluff.
        Responsibilities:
        1. Understand user intent.
        2. Create a clear step-by-step plan.
        3. Stream each step as it executes.
        4. Delegate to sub-agents.
        5. Provide a final concise summary.
        """

    def run(self, user_input, context=None):
        # In a real ADK, this would interact with the runtime to call other agents.
        # Here we simulate the planning and delegation.
        
        plan = self.create_plan(user_input)
        yield f"Plan:\n{plan}"
        
        # Simulation of execution
        steps = plan.split('\n')
        for step in steps:
            if step.strip():
                yield f"Executing: {step}"
                # logic to call other agents would go here
                # e.g., result = ingestion_agent.run(...)
                yield f"✓ Completed: {step}"
        
        yield "Done. Your life inbox is organized."

    def create_plan(self, user_input):
        prompt = f"{self.system_prompt}\nUser Input: {user_input}\nCreate a step-by-step plan."
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    # For testing
    agent = ManagerAgent()
    for update in agent.run("Organize my life"):
        print(update)
