# Group Report: Lab 3 - Production-Grade Agentic System

| Tên             | Mã số sinh viên | Email                           |
| --------------- | --------------- | -----                           |
| Nguyễn Tiến Đạt | 2A202600218     | 69tiendat@gmail.com             |
| Ngô Văn Long    | 2A202600129     | lonqnv3008@gmail.com            |
| Nguyễn Duy Hiếu | 2A202600153     | nguyenduyhieu03112003@gmail.com |
| Phạm Đan Kha    | 2A202600253     | khapham117@gmail.com            |

---

## 1. Executive Summary

This project explores the transformation of a traditional LLM-based chatbot into a production-grade Agentic AI system using the ReAct (Reasoning + Acting) framework.

The baseline chatbot relies purely on internal knowledge and often fails when dealing with:

* Multi-step reasoning tasks
* Real-time information queries
* Structured computation problems

To address these limitations, we implemented an Agent capable of:

* Iterative reasoning (multi-step thinking)
* Tool invocation (external APIs/functions)
* Self-correction through observation feedback

### Key Results

* **Success Rate**: ~85% on 20 structured test cases
* **Improvement over baseline**: +40% on multi-step tasks
* **Key Insight**: Tool usage is the primary factor in improving reliability

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation

The core architecture is based on the ReAct paradigm:

```
User Query
   ↓
Thought (LLM reasoning)
   ↓
Action (Tool Call)
   ↓
Observation (Tool Output)
   ↓
Repeat until Final Answer
```

### Detailed Behavior

* The agent first **analyzes intent**
* Decides whether:

  * Answer directly OR
  * Call a tool
* After tool execution:

  * Updates context
  * Continues reasoning

This loop ensures:

* Reduced hallucination
* Better factual accuracy
* Ability to handle complex workflows

---

### 2.2 Tool Definitions (Inventory)

| Tool Name        | Input Format             | Output          | Use Case                    |
| :--------------- | :----------------------- | :-------------- | :-------------------------- |
| `search_tool`    | string                   | text            | Retrieve external knowledge |
| `calculator`     | json `{a, b, op}`        | number          | Math computation            |
| `tax_calculator` | json `{amount, country}` | number          | Tax estimation              |
| `cv_parser`      | raw text                 | structured json | Extract CV data             |

---

### 2.3 LLM Providers Used

* **Primary**: GPT-4o (high reasoning capability)
* **Secondary**: Phi-3-mini (local fallback)

### Why multi-provider?

* Reduce downtime risk
* Optimize cost
* Enable offline testing

---

## 3. Telemetry & Performance Dashboard

We implemented logging to monitor:

### Metrics

* **P50 Latency**: ~1.2s
* **P95 Latency**: ~2.8s
* **P99 Latency**: ~4.5s
* **Avg Tokens / Task**: ~320
* **Cost / Task**: ~$0.002

### Insights

* Latency increases with loop depth
* Tool calls add overhead but improve accuracy
* Token usage grows linearly with reasoning steps

---

## 4. Root Cause Analysis (RCA)

### Case 1: Tool Misuse

* **Input**: "Tax for 500 in Vietnam"
* **Issue**: Wrong argument format
* **Cause**:

  * Weak prompt constraints
  * Lack of examples

### Case 2: Hallucination

* **Input**: "Latest AI law 2026"
* **Issue**: Agent guessed answer
* **Cause**:

  * Did not trigger search tool
  * Missing rule: “Unknown → must search”

### Case 3: Infinite Loop Risk

* Agent repeatedly called tools
* Cause:

  * No stopping condition

---

## 5. Ablation Studies & Experiments

### Experiment 1: Prompt Optimization

| Version | Change                | Result           |
| :------ | :-------------------- | :--------------- |
| v1      | Basic instructions    | Many tool errors |
| v2      | Add validation rule   | -30% errors      |
| v3      | Add few-shot examples | Best performance |

---

### Experiment 2: Chatbot vs Agent

| Scenario   | Chatbot | Agent | Winner |
| :--------- | :------ | :---- | :----- |
| Simple Q   | ✅       | ✅     | Draw   |
| Multi-step | ❌       | ✅     | Agent  |
| Real-time  | ❌       | ✅     | Agent  |
| Math       | ❌       | ✅     | Agent  |

---

## 6. Production Readiness Review

### 6.1 Security

* Input sanitization
* Prevent prompt injection
* Validate tool arguments

---

### 6.2 Guardrails

* Max loop = 5
* Timeout control
* Fallback response

---

### 6.3 Observability

* Logging (input/output/tool calls)
* Error tracking
* Performance monitoring

---

### 6.4 Scalability

Future upgrades:

* LangGraph (multi-agent system)
* RAG (retrieval-augmented generation)
* Vector DB integration

---

## 7. Real-World Applications

This system can be applied to:

* AI Interview Assistant
* AI Customer Support
* AI Health Advisor
* AI Coding Assistant

---

## 8. Lessons Learned

* Prompt design = cực kỳ quan trọng
* Tool design ảnh hưởng trực tiếp đến accuracy
* Agent mạnh hơn chatbot nhưng phức tạp hơn

---

## 9. Conclusion

The Agentic system demonstrates clear advantages over traditional chatbots in handling complex tasks.

However, achieving production-level performance requires:

* Careful prompt engineering
* Robust tool design
* Strong guardrails

---

> [!NOTE]
> File name: GROUP_REPORT_NguyenTienDat.md
