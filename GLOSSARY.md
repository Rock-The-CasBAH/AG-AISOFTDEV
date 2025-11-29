# Glossary

This glossary defines key terms used throughout the AI-Driven Software Engineering Program. Terms are organized alphabetically within categories.

---

## AI & Machine Learning Terms

### Agent
An AI system that can perceive its environment, make decisions, and take actions autonomously to achieve specific goals. Unlike simple chatbots, agents can use tools, maintain state, and reason through multi-step problems.

### Chain-of-Thought (CoT)
A prompting technique that encourages the LLM to break down complex reasoning into intermediate steps, improving accuracy on multi-step problems. Often triggered by phrases like "think step by step."

### Context Window
The maximum amount of text (measured in tokens) that an LLM can process in a single request. Larger context windows allow for more information to be included in prompts but may increase latency and cost.

### Embedding
A numerical vector representation of text that captures semantic meaning. Similar texts have similar embeddings, enabling semantic search and comparison.

### Few-Shot Learning
A technique where examples are provided in the prompt to guide the model's behavior and output format. Contrasts with zero-shot (no examples) and fine-tuning (training on many examples).

### Fine-Tuning
The process of further training a pre-trained model on a specific dataset to specialize it for particular tasks or domains.

### Hallucination
When an LLM generates information that is factually incorrect, fabricated, or not grounded in the provided context. RAG systems help reduce hallucinations by grounding responses in retrieved documents.

### In-Context Learning (ICL)
The ability of LLMs to learn patterns from examples provided within the prompt, without updating model weights. This includes few-shot and zero-shot prompting.

### Large Language Model (LLM)
A neural network trained on vast amounts of text data that can understand and generate human-like text. Examples include GPT-4, Claude, and Gemini.

### Model Context Protocol (MCP)
A standardized protocol for structuring complex prompts and agent interactions. MCP provides clear separation between instructions, context, and requests, making agent behavior more predictable and reliable.

### Multi-Agent System
An architecture where multiple specialized AI agents collaborate to solve complex problems. Each agent has specific capabilities, and an orchestrator coordinates their interactions.

### Prompt Engineering
The practice of designing and optimizing input prompts to elicit desired outputs from LLMs. Effective prompt engineering considers structure, context, examples, and constraints.

### RAG (Retrieval-Augmented Generation)
A technique that combines information retrieval with LLM generation. The system retrieves relevant documents from a knowledge base and provides them as context to the LLM, enabling accurate answers about specific domains.

### ReAct (Reason + Act)
An agent framework where the model alternates between reasoning about the current state and taking actions. The cycle of Thought → Action → Observation enables multi-step problem solving.

### Red Teaming
The practice of adversarially testing AI systems by attempting to make them produce harmful, incorrect, or unintended outputs. Used to identify vulnerabilities before deployment.

### Structured Output
LLM outputs that follow a specific format (JSON, XML, etc.) that can be programmatically parsed. Modern APIs support schema-based structured outputs for reliable data extraction.

### Temperature
A parameter controlling the randomness of LLM outputs. Lower temperatures (0.0-0.3) produce more deterministic, focused responses; higher temperatures (0.7-1.0) increase creativity and variability.

### Token
The basic unit of text processing for LLMs. A token roughly corresponds to 3-4 characters or about 0.75 words in English. Tokens are used for both input (prompt) and output (completion).

### Tool Calling (Function Calling)
The ability of an LLM to generate structured calls to external functions or APIs. The model decides when to use a tool, generates the required parameters, and incorporates the results into its response.

### Vector Store (Vector Database)
A database optimized for storing and searching embedding vectors. Used in RAG systems to find documents semantically similar to a query. Examples include FAISS, Pinecone, and Weaviate.

---

## Software Engineering Terms

### ADR (Architectural Decision Record)
A document that captures an important architectural decision along with its context and consequences. ADRs help teams understand why certain technical choices were made.

### API (Application Programming Interface)
A set of protocols and tools for building software applications. In this course, we primarily work with REST APIs for web services and LLM provider APIs.

### CRUD Operations
The four basic operations of persistent storage: Create, Read, Update, and Delete. Forms the foundation of most database-backed applications.

### CI/CD (Continuous Integration/Continuous Deployment)
Automated practices where code changes are frequently integrated (CI) and automatically deployed to production (CD). Typically implemented with tools like GitHub Actions or GitLab CI.

### Docker
A platform for developing, shipping, and running applications in containers. Containers package an application with its dependencies, ensuring consistent behavior across environments.

### Endpoint
A specific URL in an API that performs a particular function. For example, `GET /users/` might return a list of users, while `POST /users/` creates a new user.

### FastAPI
A modern, high-performance Python web framework for building APIs. Known for automatic documentation, type hints support, and async capabilities.

### Fixture (pytest)
A function that provides test data or performs setup/teardown operations. Fixtures help create isolated, repeatable test environments.

### Gherkin
A structured language for writing acceptance criteria using Given/When/Then syntax. Makes test scenarios readable by both technical and non-technical stakeholders.

### Integration Test
A test that verifies multiple components work together correctly. Contrasts with unit tests, which test individual functions in isolation.

### Middleware
Software that sits between the application and other components (database, external services). In FastAPI, middleware can handle cross-cutting concerns like CORS, authentication, and logging.

### ORM (Object-Relational Mapping)
A technique for converting data between incompatible type systems (object-oriented code and relational databases). SQLAlchemy is a popular Python ORM.

### PRD (Product Requirements Document)
A document that defines the purpose, features, and functionality of a product. Serves as the foundation for design and development decisions.

### Pydantic
A Python library for data validation using type annotations. Used extensively in FastAPI for request/response validation and in LLM applications for structured output parsing.

### Refactoring
The process of restructuring existing code without changing its external behavior. Improves code readability, maintainability, and performance.

### Schema
The structure of a database, defining tables, columns, relationships, and constraints. In APIs, schemas define the expected format of requests and responses.

### SQLAlchemy
A Python SQL toolkit and ORM that provides a full suite of database interaction patterns. Used in this course for database models and queries.

### SQLite
A lightweight, file-based relational database. Ideal for development and small applications; used throughout this course for its simplicity.

### Unit Test
A test that verifies a single function or method works correctly in isolation. Unit tests should be fast, independent, and cover edge cases.

### User Story
A short, informal description of a feature from the perspective of an end user. Format: "As a [persona], I want [goal] so that [benefit]."

---

## Framework-Specific Terms

### LangChain
A framework for developing applications powered by LLMs. Provides abstractions for chains, agents, memory, and tool integration.

### LangGraph
A library built on LangChain for creating stateful, multi-agent applications as directed graphs. Nodes represent processing steps; edges define the flow.

### AutoGen
Microsoft's framework for building multi-agent conversational systems. Agents can have different roles and collaborate through structured conversations.

### CrewAI
A framework for orchestrating role-playing AI agents. Agents have specific roles, goals, and backstories, working together on complex tasks.

### Streamlit
A Python library for creating interactive web applications quickly. Popular for building data science dashboards and AI demos.

### Tavily
A search API optimized for AI agents. Provides structured, relevant search results designed for LLM consumption.

---

## Course-Specific Terms

### Artifact
A file or document generated during the course (user stories, schemas, code, etc.). Artifacts are saved to the `artifacts/` directory and build upon each other across days.

### Challenge (in Labs)
A hands-on exercise within a lab. Challenges progress from Foundational to Intermediate to Advanced, building skills incrementally.

### Self-Paced (SP) Practice
Optional exercises that reinforce the day's concepts with a different problem domain. Located in files named `D*_SP_*.ipynb`.

### Solution
Reference implementations provided in the `Solutions/` directory. Students should attempt labs independently before consulting solutions.

---

*This glossary is a living document. Terms may be added as the curriculum evolves.*
