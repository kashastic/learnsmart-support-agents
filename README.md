# LearnSmart Support Agents  
AI-powered multi-agent customer support system for an EdTech company  

## What is this project?
This project simulates a **customer support system** for a fictional edtech startup called **LearnSmart**, which sells online courses.  

Instead of a simple chatbot, the system uses **multiple AI agents working together** to:  
- Categorize (triage) incoming support tickets  
- Draft responses using company FAQs, policies, and course catalog (via RAG)  
- Take business actions like issuing refunds or resending password links  
- Supervise responses for safety and escalate if needed  
- Generate business insights such as top issues and resolution rates  

It’s designed as a **portfolio project** to show how agentic AI workflows can be applied in real business settings.  

## System Design

**Agents in the workflow:**
1. **Triage Agent** – decides the ticket category (billing, access, technical, certificates, general)  
2. **Solution Agent** – retrieves knowledge and drafts a response  
3. **Supervisor Agent** – checks if the reply is safe and correct, escalates if unsure  
4. **Action Agent** – simulates taking action (refund, unlock, log resolution)  
5. **Insight Agent** – aggregates logs into business intelligence reports  

**Workflow diagram (simplified):**

```mermaid
flowchart LR
    A[Ticket] --> B[Triage Agent]
    B --> C[Solution Agent]
    C --> D[Supervisor Agent]
    D -->|Approve| E[Action Agent]
    D -->|Escalate| F[Human Support]
    E --> G[CRM Log]
