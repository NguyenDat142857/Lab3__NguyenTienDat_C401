import os
import re
from typing import List, Dict, Any
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger


class ReActAgent:
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        tool_descriptions = "\n".join(
            [f"- {t['name']}: {t['description']}" for t in self.tools]
        )

        return f"""
You are an intelligent ReAct Agent.

You have access to the following tools:
{tool_descriptions}

STRICT RULES:
- Always think step-by-step
- If information is missing → use a tool
- NEVER call a tool with missing arguments
- If you know the answer → output Final Answer

FORMAT:

Thought: your reasoning
Action: tool_name(arguments)
Observation: result of tool

Repeat if needed.

Final Answer: your final response
"""

    def run(self, user_input: str) -> str:
        logger.log_event("AGENT_START", {
            "input": user_input,
            "model": self.llm.model_name
        })

        context = user_input
        steps = 0

        while steps < self.max_steps:
            # 1. Gọi LLM
            result = self.llm.generate(
                context,
                system_prompt=self.get_system_prompt()
            )

            logger.log_event("LLM_OUTPUT", {"step": steps, "output": result})

            # 2. Check FINAL ANSWER
            if "Final Answer:" in result:
                final_answer = result.split("Final Answer:")[-1].strip()
                logger.log_event("FINAL_ANSWER", {"answer": final_answer})
                return final_answer

            # 3. Parse ACTION
            action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", result)

            if action_match:
                tool_name = action_match.group(1)
                args = action_match.group(2)

                logger.log_event("TOOL_CALL", {
                    "tool": tool_name,
                    "args": args
                })

                # 4. Gọi tool
                observation = self._execute_tool(tool_name, args)

                logger.log_event("TOOL_RESULT", {
                    "result": observation
                })

                # 5. Update context (VERY IMPORTANT)
                context += f"\n{result}\nObservation: {observation}\n"

            else:
                # Nếu không có action → dừng
                logger.log_event("NO_ACTION", {"output": result})
                return result

            steps += 1

        logger.log_event("MAX_STEPS_REACHED", {"steps": steps})
        return "Sorry, I could not complete the task within the step limit."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        for tool in self.tools:
            if tool["name"] == tool_name:
                try:
                    # Parse args đơn giản dạng: a=1,b=2
                    kwargs = {}
                    if args.strip():
                        for pair in args.split(","):
                            key, value = pair.split("=")
                            kwargs[key.strip()] = eval(value.strip())

                    return str(tool["function"](**kwargs))

                except Exception as e:
                    return f"Tool execution error: {str(e)}"

        return f"Tool {tool_name} not found."