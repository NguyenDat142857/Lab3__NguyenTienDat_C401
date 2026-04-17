# Individual Report: Lab 3 - Chatbot vs ReAct Agent

* **Student Name**: Nguyen Tien Dat
* **Student ID**: [2A202600218]
* **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

During this lab, I contributed to the development and improvement of the ReAct Agent system by implementing tools, refining prompts, and debugging execution flows.

### Modules Implemented

* `src/tools/search_tool.py`
* `src/tools/calculator.py`
* `src/agent/react_loop.py`

---

### Code Highlights

Example: Simple calculator tool

```python
def calculator(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b
```

Example: ReAct loop logic (simplified)

```python
while not done:
    thought = llm.generate(context)
    action = parse_action(thought)
    observation = call_tool(action)
    context += observation
```

---

### Documentation

The system follows the ReAct (Reasoning + Acting) loop:

1. The LLM generates a **Thought**
2. The system parses the **Action**
3. A tool is executed
4. The result (**Observation**) is fed back into the LLM

My contribution focused on:

* Ensuring tools return correct formats
* Improving parsing logic to avoid crashes
* Making the loop stable with stopping conditions

---

## II. Debugging Case Study (10 Points)

### Problem Description

During testing, the agent entered an infinite loop:

```
Thought: I need to search for more info
Action: search(None)
```

This repeated multiple times without producing a final answer.

---

### Log Source

Example log:

```
[2026-04-03 10:32:11]
Thought: Need more info
Action: search(None)
Observation: Error - invalid input
```

---

### Diagnosis

The issue was caused by:

* Missing argument validation
* Weak prompt instructions
* The model defaulted to calling tools even when inputs were invalid

---

### Solution

* Added validation rule in prompt:
  "Do not call a tool if arguments are missing or invalid"

* Improved parser:

  * Reject `None` inputs
  * Return fallback response

* Added loop limit:

  ```python
  if step > 5:
      break
  ```

Result:

* Infinite loop issue resolved
* System stability improved significantly

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

### 1. Reasoning

The `Thought` block significantly improves reasoning:

* Chatbot → Direct answer (often wrong)
* Agent → Step-by-step reasoning

This allows the agent to:

* Break down complex problems
* Decide when to use tools

---

### 2. Reliability

Cases where Agent performs worse:

* Simple questions (overhead too high)
* Poorly defined tools → wrong outputs
* Bad prompt → incorrect tool usage

---

### 3. Observation

Observations play a critical role:

* Provide real-world feedback
* Allow correction of mistakes
* Guide next reasoning step

Without observation, the system becomes a normal chatbot again.

---

## IV. Future Improvements (5 Points)

### Scalability

* Use async tool execution
* Queue-based architecture

---

### Safety

* Add Supervisor LLM
* Validate all tool outputs
* Prevent prompt injection

---

### Performance

* Use Vector Database (FAISS, Pinecone)
* Reduce token usage via caching
* Optimize prompt length

---

## Conclusion

The ReAct Agent provides a significant improvement over traditional chatbots in handling complex and multi-step tasks. However, it requires careful design in prompt engineering, tool integration, and system control to achieve production-level performance.

---

> [!NOTE]
> File name: REPORT_NguyenTienDat.md
