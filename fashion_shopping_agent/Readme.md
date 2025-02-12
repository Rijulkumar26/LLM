# Virtual Shopping Assistant (ATC-Based Approach)

## Comparison of Papers

| Approach            | Agent Design                                              | Reasoning Steps                                              | Tool Use                                    | Real-world Applicability                                      |
|---------------------|-----------------------------------------------------------|-------------------------------------------------------------|---------------------------------------------|---------------------------------------------------------------|
| **ReAct**          | Generates reasoning traces (thoughts) interleaved with actions. | Uses chain-of-thought reasoning to track and update plans.  | Interacts with APIs for real-time information retrieval. | Suitable for question answering, fact verification, and navigation. |
| **Automatic Tool Chain (ATC)** | Programmatically chains tools, learns tool dependencies from documentation. | Generates a sequence of tool calls, caches results, and tracks errors. | Uses black-box probing for tool discovery. | Suitable for tasks requiring long-term planning and complex tool dependencies. |
| **Language Agent Tree Search (LATS)** | Expands ReAct with Monte Carlo Tree Search (MCTS) for planning. | Uses search algorithms to optimize action selection. | Uses APIs for retrieving external information. | Useful for web navigation, programming, and autonomous reasoning. |
| **Toolformer**     | Self-supervised learning for tool usage with minimal demonstrations. | Predicts which tools to use and when, incorporating API results into token prediction. | Uses a variety of APIs, including search engines and calculators. | Ideal for zero-shot tasks where predefined tool use is unknown. |
| **ReST-meets-React** | Refines ReAct-style agents with iterative training and web search. | Iteratively trains on past responses using reinforcement learning. | Uses web search and self-verification mechanisms. | Designed for answering complex, open-ended questions. |


## Comparative Conceptual Map

### **Evaluation of Methods for Virtual Shopping Assistant**

| Method       | Strengths | Weaknesses |
|-------------|-----------|------------|
| **Automatic Tool Chain (ATC)** | Best for complex tool integration, automated tool discovery, and error tracking | More complex to implement initially |
| **ReAct** | Interleaves reasoning and acting, useful for interacting with APIs | Less efficient in managing complex sequential tool use |
| **LATS** | Enhances decision-making via search algorithms | Focuses more on general problem-solving than specific tool orchestration |
| **Toolformer** | Learns tool usage in a self-supervised way | Not optimized for managing interdependent tools |
| **ReST-meets-React** | Improves existing methods via AI feedback and self-improvement | Not a standalone solution for architecture design |

## **Short Written Analysis (Results & Performance of Methods)**

Given the requirements of a virtual shopping assistant—including search aggregation, shipping estimation, discount checking, price comparison, and return policy verification—**ATC emerges as the best candidate** due to its ability to programmatically chain tools, adapt to new APIs, and ensure reliability through attributable reflection mechanisms.

While **ReAct** and **Toolformer** offer valuable features, they do not handle complex, multi-step dependencies as efficiently as ATC. **LATS** can enhance planning, but it does not directly support tool execution, making it less suitable. **ReST-meets-React** improve existing approaches but do not constitute a core framework.

## **Design Decisions (Agent Architecture & Tool Selection)**

### Agent Design (ATC Approach)

#### Tool Integration
The ATC framework enables seamless orchestration of tools via programmatic chaining. The LLM (GPT-2) dynamically decides which tools to call based on the user's query and executes them in the correct sequence.

##### Automated Discovery
- The system uses the LLM to interpret the user's query and determine the appropriate tools to use.  
- This allows the system to adapt to different types of queries without hardcoding specific tool calls.  

##### Error Tracking
- The system incorporates basic error handling by checking for valid responses from tools.  
- Example: Ensuring `search_products` returns valid results before calling other tools.  
- If a tool fails or returns no data, the system provides a meaningful error message to the user.  

---

#### Tool Selection
The assistant interacts with the following tools:

##### **Product Search Tool (`search_products`)**
- **Purpose:** Searches for products based on user queries, filtering by name, size, price, or stock availability.  
- **Input:** User query (e.g., `"Floral Skirt"`).  
- **Output:** List of matching products with details (name, price, size, stock availability, etc.).  

##### **Shipping Time Estimator (`estimate_shipping`)**
- **Purpose:** Estimates shipping costs and delivery time based on the user's location.  
- **Input:** User's location (e.g., `"Bangalore"`).  
- **Output:** Shipping details (estimated days, cost, feasibility).  

##### **Discount / Promo Checker (`check_discount`)**
- **Purpose:** Validates and applies promo codes to eligible products.  
- **Input:** User query and promo code (e.g., `"SAVE10"`).  
- **Output:** Discount details (discount applied, final price, or error message).  

##### **Competitor Price Comparison (`compare_prices`)**
- **Purpose:** Compares prices of a product across different stores (Amazon, eBay, Walmart).  
- **Input:** User query (e.g., `"Floral Skirt"`).  
- **Output:** Price comparison across stores.  

##### **Return Policy Checker (`get_return_policy`)**
- **Purpose:** Retrieves return policies for e-commerce stores.  
- **Input:** User query (e.g., `"Floral Skirt"`).  
- **Output:** Return policy details.  

---

#### Tool Execution Workflow

##### **1. User Query Processing**
- The user enters a query (e.g., `"Find a Floral Skirt and compare prices"`).  
- The LLM analyzes the query and determines which tools to call.  

##### **2. Tool Chain Generation**
- The LLM generates a sequence of tools to execute (e.g., `search_products → compare_prices`).  

##### **3. Tool Execution**
The system calls the tools in the specified order:
1. **`search_products`**: Finds the product.  
2. **`compare_prices`**: Compares prices across stores.  
3. **`check_discount`**: Applies promo codes (if provided).  
4. **`estimate_shipping`**: Calculates shipping costs.  
5. **`get_return_policy`**: Retrieves return policies.  

##### **4. Response Aggregation**
- The system aggregates the results from the tools into a structured JSON response.  

##### **5. Final Output**
- The system displays the final response to the user in a user-friendly format.  

## **Challenges & Improvements**

### **Challenges Faced**
1. **API Rate Limits**: Some services have restrictive API limits, requiring caching and batching requests.
2. **Inconsistent Data Formats**: Different e-commerce platforms structure data differently.
3. **Latency Issues**: Chaining multiple tools may introduce latency.

### **Potential Improvements**
1. **Hybrid Approach**: Combining ATC with LATS for improved decision-making.
2. **Parallel Execution**: Running non-dependent tool calls in parallel to reduce latency.
3. **Fine-Tuned LLM**: Using a domain-specific LLM for better API response interpretation.

## **Open Questions & References**

### **Open Questions**
- How can ATC be further optimized for real-time applications?
- Can integrating reinforcement learning improve the assistant’s efficiency?
- What are the best fallback mechanisms when APIs fail?

### **References**
1. Schick, T., et al. "Toolformer: Language Models Can Teach Themselves to Use Tools." arXiv preprint (2023).
2. Yao, S., et al. "ReAct: Synergizing Reasoning and Acting in Language Models." arXiv preprint (2022).
3. Xie, S., et al. "LATS: Learning to Act and Think Step by Step with Search." arXiv preprint (2023).
4. Zhou, C., et al. "ATC: Automatic Tool Chain for Multi-Step Reasoning." arXiv preprint (2024).
5. Renat Aksitov,et al."REST MEETS REACT: SELF-IMPROVEMENT FOR MULTI-STEP REASONING LLM AGENT"arXiv preprint (2023).
