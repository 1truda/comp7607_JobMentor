# AI Agent Proposal for Assisting Students with Job Search

---

## Objective

The goal of this AI agent is to assist students in job search preparation and streamline the associated processes, including quality tests, interview practice, scheduling, and coding interview preparation. The system aims to enhance efficiency and learning outcomes by utilizing AI-driven techniques in areas such as question-answering, interview simulation, automated scheduling, and coding problem-solving.

---

## Data Sets

1. **Quality Test Questions**:
   - **Sources**: Quality test platforms such as [NowCoder](https://www.nowcoder.com/exam/intelligent?type=vip) and [GKZenti](https://www.gkzenti.cn/paper/1723610466312).
   - **Content**: Various types of questions, including math reasoning, context reasoning, and office skills assessments.

2. **Email Scheduling Data**:
   - **Collected From**: Students’ email accounts for personalized scheduling and management.
   - **Purpose**: To learn patterns in communication and time management.

3. **Quora Question Pairs**:
   - **Usage**: Model semantic similarity in interview preparation scenarios. Data will be cleaned and augmented to emphasize job-related topics.

4. **Coding Interview Questions**:
   - **Scope**: Over 3,300 coding problems and solutions, covering data structures, algorithms, and various programming concepts in Python.

5. **Customer-Service Conversations**:
   - **Source**: JD.com dataset containing 10,000 anonymized sessions, simulating interview dialogues.
   - **Additional Data**: Frequently asked interview questions and responses for prompt engineering and interview simulation.

---

## Methodology

1. **Quality Test Assistance**:
   - **QA Agent**: Trains on datasets to answer various quality test questions correctly. Uses OCR to extract text from screenshots and automated browser interaction to complete online tests.

2. **Scheduling System**:
   - **Email Parsing & To-Do Lists**: Utilizes LLMs to extract and summarize email content, recognize time-related information, and create optimized schedules. Automates confirmations, reminders, and generates to-do lists.
   - **Techniques**: Few-shot learning and parameterized prompts for accurate information extraction, combined with a MySQL database for managing scheduling data.

3. **Interview Preparation**:
   - **Semantic Search & Recommendation**: Uses BM25, BERT embeddings, and fine-tuned SBERT for question similarity. DPR enhances retrieval for complex queries. User feedback loops improve the recommendation system.
   - **RAG System**: Combines information retrieval with generative models to simulate interviews. Retrieves relevant content and provides tailored feedback. LangChain integrates the modules for dynamic Q&A.

4. **Coding Interview Agent**:
   - **QA Agent**: Powered by Llama-3.1 and OS-Copilot, generates accurate Python solutions to coding problems. Provides interactive assistance, teaching techniques, and enhances coding skills.

5. **Simulated Interview System**:
   - **Interactive Simulation**: Implements Retrieval-Augmented Generation (RAG) for realistic interview scenarios. Uses LangChain for integration, feedback generation, and managing conversation flow.

---

## Technical Framework

1. **AI Models & Frameworks**:
   - **Llama-3.1**: Core NLP model for natural language understanding and Python code generation.
   - **OS-Copilot**: Enhances coding assistance and automates solution suggestions.
   - **BM25 & BERT**: Baseline and semantic similarity search for interview preparation.
   - **RAG & LangChain**: Combine retrieval and generative models for an interactive interview experience.

2. **APIs & Databases**:
   - **Outlook API**: Automates email management and scheduling tasks.
   - **MySQL**: Securely stores and manages user scheduling data.
   - **APIs for Browser Automation**: Executes tasks like test completion.

3. **Integration & Automation**:
   - **LangChain**: Manages context, tracks user interactions, and integrates tools and models for a cohesive interview and learning experience.
   - **Scripts & Automation**: Facilitates interaction with external systems (e.g., email, scheduling platforms, test websites).

---

## References
1. [Retrieval-Augmented Generation for Large Language Models: A Survey Gao et al., 2023.](https://arxiv.org/html/2312.10997v5)
2. [Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions, ACL 2023](https://arxiv.org/html/2212.10509)
3. [Retrieval Augmented Thoughts Elicit Context-Aware Reasoning in Large Language Models](https://arxiv.org/html/2403.05313v1)
4. [OS-COPILOT: TOWARDS GENERALIST COMPUTER AGENTS WITH SELF-IMPROVEMENT](https://arxiv.org/pdf/2402.07456.pdf)
5. [OS-pilot](https://github.com/OS-Copilot/OS-Copilot)
6. [ChatTTS](https://github.com/xianyu110/ChatTTS)