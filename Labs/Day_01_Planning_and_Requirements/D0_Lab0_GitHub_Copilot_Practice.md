# Lab 0: GitHub Copilot Practice

## Overview

* **Synopsis:** This pre-lab introduces you to GitHub Copilot, your AI pair programmer throughout this course. You will explore inline suggestions, chat modes, context management, and customization features that will accelerate your development workflow.
* **Core Question:** How can we configure and leverage GitHub Copilot to maximize productivity while maintaining code quality?
* **Time Required:** 45-60 minutes
* **Prerequisites:** VS Code installed, GitHub account with Copilot access (Free tier is sufficient)

> **Version Note:** This lab reflects GitHub Copilot features as of late 2025. Features evolve rapidly—refer to the [official documentation](https://code.visualstudio.com/docs/copilot/overview) for the latest updates.

---

## Learning Objectives

By the end of this lab, you will be able to:

1. Verify your GitHub Copilot installation and understand subscription tiers
2. Use inline suggestions effectively (ghost text and Next Edit Suggestions)
3. Navigate between Ask, Edit, and Agent chat modes appropriately
4. Manage context with #-mentions for precise AI assistance
5. Create custom instructions, prompt files, and agents for your projects
6. Configure MCP servers to extend Copilot's capabilities

---

## Part 1: Setup Verification (5 minutes)

### Exercise 1.1: Confirm Installation

1. Open VS Code
2. Look for the Copilot icon in the **status bar** (bottom right)
3. If missing, install from Extensions (`⇧⌘X` / `Ctrl+Shift+X`):
   - Search for "GitHub Copilot"
   - Install both **GitHub Copilot** and **GitHub Copilot Chat**

### Exercise 1.2: Sign In and Verify

1. Click the Copilot icon in the status bar
2. If prompted, sign in with your GitHub account
3. Verify status shows "GitHub Copilot" (not "Sign in required")

**Checkpoint:** Open any `.py` file and start typing. You should see ghost text suggestions appear.

### Exercise 1.3: Explore the Chat View

1. Open Chat View: `⌃⌘I` (Mac) or `Ctrl+Alt+I` (Windows/Linux)
2. Notice the mode selector at the top (Ask/Edit/Agent)
3. Notice the model selector (click to see available models)
4. Type a simple question: `What is a Python list comprehension?`

---

## Part 2: Inline Suggestions (10 minutes)

### Exercise 2.1: Ghost Text Completions

Create a new file called `copilot_practice.py` and type the following, pausing after each line to observe suggestions:

```python
# Exercise 2.1: Ghost text practice

# Function to calculate the factorial of a number
def factorial(
```

**Tasks:**
1. Wait for Copilot to suggest the function body
2. Press `Tab` to accept, or `Esc` to dismiss
3. Try `Alt+]` / `Alt+[` to cycle through alternative suggestions

### Exercise 2.2: Comment-Driven Development

Type a comment describing what you want, then let Copilot generate the code:

```python
# Function that takes a list of numbers and returns only the even ones
```

Press `Enter` and wait for Copilot to suggest the function.

### Exercise 2.3: Next Edit Suggestions (NES)

NES predicts where you'll edit next. Try this refactoring exercise:

```python
# Exercise 2.3: NES practice
def greet(name):
    return "Hello, " + name

def farewell(name):
    return "Goodbye, " + name

def welcome(name):
    return "Welcome, " + name
```

1. Change the first function to use f-strings: `return f"Hello, {name}"`
2. Watch for NES to suggest the same change in subsequent functions
3. Press `Tab` to accept and jump to the next suggested edit

**Reflection:** How might NES improve your refactoring workflow?

---

## Part 3: Chat Modes (15 minutes)

### Exercise 3.1: Ask Mode — Understanding Code

Switch to **Ask** mode in the Chat view.

**Task 1:** Ask about the codebase
```
What testing frameworks are used in this #codebase?
```

**Task 2:** Ask a conceptual question
```
Explain the difference between @staticmethod and @classmethod in Python
```

**Task 3:** Explore implementation options
```
What are three different ways to implement a cache in Python?
```

**Key Insight:** Ask mode never modifies files—it's safe for exploration.

### Exercise 3.2: Edit Mode — Targeted Changes

Switch to **Edit** mode.

**Task 1:** Add to your practice file:
```
Add comprehensive docstrings to all functions in #copilot_practice.py
```

**Task 2:** Review the proposed changes:
- Examine the diff view
- Accept individual changes or all at once
- Notice how only the referenced file is modified

**Task 3:** Try a refactoring request:
```
Refactor the greet, farewell, and welcome functions to use a single generic function with a message parameter
```

### Exercise 3.3: Agent Mode — Autonomous Problem Solving

Switch to **Agent** mode.

> ⚠️ **Note:** Agent mode can run terminal commands and modify multiple files. Review actions before approving.

**Task 1:** Simple exploration task
```
List all Python files in this project and summarize their purpose
```

**Task 2:** Multi-step task (observe the agent's approach)
```
Create a new file called string_utils.py with three helper functions for string manipulation, including unit tests
```

Watch how the agent:
- Plans its approach
- Creates files
- May run commands (with your approval)
- Iterates if needed

### Exercise 3.4: Inline Chat — Quick Edits

1. Select a block of code in your editor
2. Press `⌘I` (Mac) or `Ctrl+I` (Windows/Linux)
3. Type: `Add error handling for invalid input`
4. Review and accept the changes

**When to use:** Quick, localized edits without opening the full chat panel.

---

## Part 4: Context Management (10 minutes)

### Exercise 4.1: File References with #-Mentions

In the Chat view, practice these context patterns:

**Single file:**
```
Explain the main function in #copilot_practice.py
```

**Multiple files:**
```
How do #copilot_practice.py and #string_utils.py relate to each other?
```

**Folders:**
```
What's the structure of the #Labs folder?
```

### Exercise 4.2: Codebase-Wide Searches

Use `#codebase` for broad searches:

```
Where is error handling implemented in #codebase?
```

```
Find all functions that make HTTP requests #codebase
```

**Pro tip:** `#codebase` works best when your workspace is indexed. Check indexing status via the Copilot status menu.

### Exercise 4.3: Problem and Terminal Context

**Reference VS Code problems:**
```
Fix the issues shown in #problems
```

**Reference terminal output:**
```
Why did #terminalLastCommand fail?
```

### Exercise 4.4: Source Control Context

**Review uncommitted changes:**
```
Review my #changes and suggest improvements
```

**Understand test failures:**
```
Help me fix #testFailure
```

---

## Part 5: Customization (15 minutes)

### Exercise 5.1: Create Custom Instructions

Custom instructions tell Copilot about your project's coding standards.

1. Create the folder structure (if it doesn't exist):
   ```bash
   mkdir -p .github
   ```

2. Create `.github/copilot-instructions.md`:

```markdown
# Project Coding Standards

## Python Style
- Follow PEP 8 guidelines
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters

## Documentation
- All public functions must have docstrings (Google style)
- Include usage examples in docstrings for complex functions

## Error Handling
- Use specific exception types, not bare except
- Log errors with contextual information
- Provide helpful error messages for users

## Testing
- Write unit tests for all public functions
- Use pytest as the testing framework
- Aim for >80% code coverage
```

3. Test the instructions:
   - Open a new chat session
   - Ask: `Generate a function to read a JSON file`
   - Verify the output follows your specified standards

### Exercise 5.2: Create a Prompt File

Prompt files are reusable templates for common tasks.

1. Create the prompts folder:
   ```bash
   mkdir -p .github/prompts
   ```

2. Create `.github/prompts/create-utility.prompt.md`:

```markdown
---
name: "create-utility"
description: "Generate a Python utility function with tests"
---

Create a Python utility function with the following requirements:

1. **Function Implementation**
   - Include comprehensive type hints
   - Add a Google-style docstring with examples
   - Handle edge cases gracefully

2. **Unit Tests**
   - Create a corresponding test file in the tests/ directory
   - Include tests for normal cases, edge cases, and error conditions
   - Use pytest fixtures where appropriate

3. **Documentation**
   - Add the function to any relevant module docstrings

The function should: {{description}}
```

3. Use the prompt:
   - In chat, type `/` to see available prompts
   - Select `create-utility`
   - Fill in: `parse a date string in multiple formats and return a datetime object`

### Exercise 5.3: Create a Custom Agent

Custom agents define specialized AI personas.

1. Create the agents folder:
   ```bash
   mkdir -p .github/agents
   ```

2. Create `.github/agents/Code Reviewer.md`:

```markdown
---
name: "Code Reviewer"
description: "Reviews code for quality, security, and best practices"
tools: []
---

You are a senior code reviewer with expertise in Python development. Your role is to analyze code and provide constructive feedback.

## Focus Areas
1. **Code Quality**
   - Readability and maintainability
   - Appropriate naming conventions
   - Function/class design

2. **Security**
   - Input validation
   - Injection vulnerabilities
   - Secure handling of sensitive data

3. **Performance**
   - Algorithmic efficiency
   - Memory usage
   - Unnecessary computations

4. **Best Practices**
   - DRY (Don't Repeat Yourself)
   - SOLID principles where applicable
   - Appropriate error handling

## Response Format
- List issues by severity (Critical, Major, Minor, Suggestion)
- Provide specific line references
- Include code examples for suggested fixes
- Acknowledge well-written code

**Important:** Do not make changes to code. Only provide analysis and recommendations.
```

3. Use the agent:
   - In chat, select the "Code Reviewer" agent from the mode dropdown
   - Ask: `Review #copilot_practice.py`

### Exercise 5.4: Configure an MCP Server (Advanced)

MCP (Model Context Protocol) servers extend Copilot with custom tools.

1. Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "example-server": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "your_mcp_server"],
      "env": {
        "EXAMPLE_VAR": "value"
      }
    }
  }
}
```

**Common MCP Use Cases:**
- Database query tools
- API integration helpers
- Custom documentation fetchers
- Project-specific utilities

> **Note:** MCP servers require implementing the Model Context Protocol. See [modelcontextprotocol.io](https://modelcontextprotocol.io) for specifications.

---

## Part 6: Model Selection (5 minutes)

### Exercise 6.1: Explore Available Models

1. In the Chat view, click the model name (e.g., "GPT-4o")
2. Review available models:
   - **Fast models** — Lower latency, good for simple tasks
   - **Advanced models** — Better reasoning, complex tasks
   - **Auto** — VS Code selects based on context

### Exercise 6.2: Match Model to Task

Try the same prompt with different models:

```
Design a caching strategy for a web application with high read traffic
```

**Observe:**
- Response quality differences
- Latency differences
- When "Auto" switches models

**Guideline:**
- Use fast models for: code completion, simple questions, formatting
- Use advanced models for: architecture design, complex debugging, security analysis

---

## ✅ Summary Checklist

Before proceeding to Day 1 labs, confirm you can:

- [ ] See ghost text suggestions while typing
- [ ] Accept/reject/cycle through inline suggestions
- [ ] Open and use the Chat view
- [ ] Switch between Ask, Edit, and Agent modes
- [ ] Use #-mentions to add context (#file, #codebase, #problems)
- [ ] Create and test custom instructions
- [ ] Create and use a prompt file
- [ ] Create and use a custom agent
- [ ] Select appropriate language models

---

## 🔍 Troubleshooting

| Issue | Solution |
| --- | --- |
| No inline suggestions | Check Copilot status bar icon; ensure signed in |
| Chat not responding | Check internet connection; try a different model |
| #codebase returns poor results | Wait for workspace indexing to complete |
| Custom instructions not applied | Ensure file is in `.github/copilot-instructions.md` |
| Prompt file not appearing | Check file extension is `.prompt.md` |
| Agent not showing | Verify file is in `.github/agents/` with correct frontmatter |

---

## 🚀 Next Steps

With Copilot configured and practiced, you're ready for:

1. **Lab 1:** Use Copilot to generate requirements and user stories
2. **Lab 2:** Let Copilot help create a Product Requirements Document
3. **Throughout the course:** Apply these Copilot skills to accelerate every phase of development

---

## Additional Resources

- [GitHub Copilot Reference Guide](../../Supporting%20Materials/GitHub_Copilot_Reference_Guide.md) — Quick reference for commands and features
- [VS Code Copilot Best Practices](../../Supporting%20Materials/VS_Code_Copilot_Best_Practices.md) — Optimization strategies
- [Official VS Code Copilot Docs](https://code.visualstudio.com/docs/copilot/overview) — Comprehensive documentation
- [Copilot Chat Prompt Examples](https://code.visualstudio.com/docs/copilot/chat/prompt-examples) — Curated prompt patterns
