# GitHub Copilot Reference Guide

> **Version Note:** This guide reflects GitHub Copilot features as of late 2025. For the latest updates, refer to the [official VS Code Copilot documentation](https://code.visualstudio.com/docs/copilot/overview).

This reference guide provides a comprehensive overview of GitHub Copilot's features, commands, and capabilities in Visual Studio Code. Use it as a quick-reference companion during your development workflow.

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Inline Suggestions](#2-inline-suggestions)
3. [Chat Interface](#3-chat-interface)
4. [Chat Modes](#4-chat-modes)
5. [Context Management](#5-context-management)
6. [Tools and Extensions](#6-tools-and-extensions)
7. [Customization](#7-customization)
8. [Keyboard Shortcuts](#8-keyboard-shortcuts)
9. [Settings Reference](#9-settings-reference)

---

## 1. Getting Started

### Installation

1. Install the **GitHub Copilot** extension from the VS Code Marketplace
2. Sign in with your GitHub account
3. Copilot icon appears in the status bar when active

### Subscription Tiers

| Tier | Features |
| --- | --- |
| **Copilot Free** | Limited monthly inline suggestions and chat interactions |
| **Copilot Pro** | Unlimited suggestions, premium models, advanced features |
| **Copilot Business/Enterprise** | Organization management, policy controls, audit logs |

### Verify Setup

- Hover over the Copilot icon in the status bar
- Check for "GitHub Copilot" in the Extensions view
- Test with a simple code completion in any file

---

## 2. Inline Suggestions

Copilot provides two types of inline code suggestions:

### Ghost Text Suggestions

Dimmed text appears at your cursor as you type, predicting what you might write next.

**Actions:**
- `Tab` — Accept the suggestion
- `Esc` — Dismiss the suggestion
- `Alt + ]` — View next suggestion
- `Alt + [` — View previous suggestion
- `Alt + \` — Trigger suggestion manually

### Next Edit Suggestions (NES)

Copilot predicts not just *what* you'll type, but *where* your next edit will be.

**How it works:**
- Analyzes your recent edits
- Suggests the location and content of your next change
- Particularly useful for repetitive refactoring tasks

**Actions:**
- `Tab` — Accept and jump to the suggested edit location
- Continue typing to ignore

---

## 3. Chat Interface

Access Copilot Chat through multiple entry points:

| Entry Point | Shortcut (Mac) | Shortcut (Win/Linux) | Use Case |
| --- | --- | --- | --- |
| **Chat View** | `⌃⌘I` | `Ctrl+Alt+I` | Extended conversations, complex tasks |
| **Inline Chat** | `⌘I` | `Ctrl+I` | Quick edits in the editor |
| **Quick Chat** | `⇧⌘I` | `Ctrl+Shift+I` | Fast questions without leaving context |
| **Terminal Chat** | Right-click in terminal | Right-click in terminal | Command-line help |

### Chat View Features

- **History** — Access previous conversations via the clock icon
- **New Chat** — Start fresh with `⌘N` / `Ctrl+N`
- **Checkpoints** — Save and restore conversation states
- **Export** — Save conversations for documentation

---

## 4. Chat Modes

Copilot offers three primary interaction modes, each optimized for different tasks:

### Ask Mode

**Purpose:** Get answers, explanations, and guidance without modifying code.

**Best for:**
- Understanding code behavior
- Learning new concepts
- Exploring implementation options
- Getting documentation

**Example prompts:**
```
Explain how authentication works in #codebase
What's the difference between async/await and promises?
How should I structure a REST API for user management?
```

### Edit Mode

**Purpose:** Make targeted changes to specific files or selections.

**Best for:**
- Refactoring existing code
- Adding features to specific files
- Bug fixes with known locations
- Code transformations

**Behavior:**
- Shows proposed changes as diffs
- You review and accept/reject each change
- Changes apply to explicitly referenced files

**Example prompts:**
```
Refactor this function to use async/await
Add input validation to the user registration form
Convert this class to use TypeScript interfaces
```

### Agent Mode

**Purpose:** Autonomous problem-solving across your entire workspace.

**Best for:**
- Complex, multi-file changes
- Tasks requiring exploration
- When you don't know where changes are needed
- End-to-end feature implementation

**Behavior:**
- Autonomously explores your codebase
- Runs terminal commands (with approval)
- Creates, modifies, and deletes files
- Iterates until the task is complete

**Example prompts:**
```
Add a dark mode toggle to the application
Fix all TypeScript errors in the project
Create a new API endpoint for user preferences with tests
```

### Mode Selection Quick Reference

| Scenario | Recommended Mode |
| --- | --- |
| "What does this code do?" | Ask |
| "Refactor this specific function" | Edit |
| "Add a new feature across the app" | Agent |
| "Fix the bug in line 42" | Edit / Inline Chat |
| "Why is this test failing?" | Ask |
| "Set up authentication for the project" | Agent |

---

## 5. Context Management

### Automatic Context

Copilot automatically includes:
- **Active file** — The file currently open in the editor
- **Selection** — Any highlighted code
- **Open tabs** — Recently viewed files (weighted by relevance)
- **Workspace structure** — Project layout awareness

### #-Mentions (Explicit Context)

Type `#` followed by a context reference to explicitly include information:

| Mention | Description | Example |
| --- | --- | --- |
| `#file` | Reference a specific file | `Explain #auth.py` |
| `#folder` | Include an entire directory | `What's in #src/components` |
| `#codebase` | Search entire workspace | `Where is logging configured? #codebase` |
| `#selection` | Current editor selection | `Optimize #selection` |
| `#editor` | Visible editor content | `What's wrong with #editor` |
| `#problems` | VS Code Problems panel | `Fix the issues in #problems` |
| `#terminalLastCommand` | Last terminal command output | `Why did #terminalLastCommand fail?` |
| `#terminalSelection` | Selected terminal text | `Explain #terminalSelection` |
| `#changes` | Uncommitted git changes | `Review #changes` |
| `#testFailure` | Recent test failures | `Fix #testFailure` |

### Tool References

Reference tools directly with `#`:

| Tool | Purpose | Example |
| --- | --- | --- |
| `#fetch` | Retrieve web content | `#fetch https://api.example.com/docs` |
| `#githubRepo` | Reference GitHub repository | `#githubRepo owner/repo` |
| `#usages` | Find symbol usages | `#usages myFunction` |

### Workspace Indexing

For large codebases, enable workspace indexing for better `#codebase` searches:

1. **Remote Index** — If hosted on GitHub, builds index in the cloud
2. **Local Index** — Stored on your machine for private repositories

Check indexing status in the Copilot status menu.

---

## 6. Tools and Extensions

### Built-in Tools

Copilot can use various tools autonomously in Agent mode:

| Tool | Capability |
| --- | --- |
| **File Operations** | Create, read, edit, delete files |
| **Terminal** | Run shell commands |
| **Search** | Find files, symbols, and text |
| **Git** | Stage, commit, view diffs |
| **Problems** | Access diagnostics |
| **Testing** | Run and analyze tests |

### MCP (Model Context Protocol) Servers

Extend Copilot's capabilities with MCP servers:

**Configuration Location:** `.vscode/mcp.json` or user settings

**Example Configuration:**
```json
{
  "servers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["path/to/server.js"]
    }
  }
}
```

**Common MCP Use Cases:**
- Database queries
- API integrations
- Custom tooling
- External service access

### Tool Approval

For security, certain tools require approval before execution:
- **Allow** — Run once
- **Allow for Session** — Trust for current session
- **Allow for Workspace** — Trust in this project
- **Skip** — Decline the tool invocation

---

## 7. Customization

### Custom Instructions

Define project-wide coding standards and preferences.

**Location:** `.github/copilot-instructions.md`

**Example:**
```markdown
# Project Coding Standards

## Style
- Use TypeScript strict mode
- Prefer functional components in React
- Use async/await over raw promises

## Conventions
- Use camelCase for variables and functions
- Use PascalCase for classes and types
- Prefix private members with underscore

## Error Handling
- Always use try/catch for async operations
- Log errors with contextual information
```

### Prompt Files

Create reusable prompt templates for common tasks.

**Location:** `.github/prompts/`

**Structure:**
```markdown
---
name: "create-component"
description: "Generate a React component with tests"
---

Create a new React functional component with:
- TypeScript types
- Unit tests using Jest
- Storybook story
- CSS module for styling
```

**Usage:** Type `/` in chat to access prompt files.

### Custom Agents

Define specialized AI personas for specific tasks.

**Location:** `.github/agents/`

**Example Agent (`Code Reviewer.md`):**
```markdown
---
name: "Code Reviewer"
description: "Analyzes code for quality and best practices"
tools: []
---

You are a senior code reviewer focused on:
- Code quality and maintainability
- Security vulnerabilities
- Performance issues
- Best practice adherence

Provide constructive feedback without making changes.
```

### Language Model Selection

Choose different models for different tasks:

**Access:** Click the model name in Chat view

**Model Types:**
- **Fast models** — Quick responses, simpler tasks
- **Advanced models** — Complex reasoning, detailed analysis
- **Auto** — VS Code selects optimal model

---

## 8. Keyboard Shortcuts

### Essential Shortcuts (macOS)

| Action | Shortcut |
| --- | --- |
| Open Chat View | `⌃⌘I` |
| Inline Chat | `⌘I` |
| Quick Chat | `⇧⌘I` |
| Accept Suggestion | `Tab` |
| Dismiss Suggestion | `Esc` |
| Next Suggestion | `⌥]` |
| Previous Suggestion | `⌥[` |
| Trigger Suggestion | `⌥\` |
| New Chat | `⌘N` (in Chat view) |
| Accept All Edits | `⌘Enter` (in Edit mode) |

### Essential Shortcuts (Windows/Linux)

| Action | Shortcut |
| --- | --- |
| Open Chat View | `Ctrl+Alt+I` |
| Inline Chat | `Ctrl+I` |
| Quick Chat | `Ctrl+Shift+I` |
| Accept Suggestion | `Tab` |
| Dismiss Suggestion | `Esc` |
| Next Suggestion | `Alt+]` |
| Previous Suggestion | `Alt+[` |
| Trigger Suggestion | `Alt+\` |
| New Chat | `Ctrl+N` (in Chat view) |
| Accept All Edits | `Ctrl+Enter` (in Edit mode) |

---

## 9. Settings Reference

### Key Settings

Access via `Settings > Extensions > GitHub Copilot` or `settings.json`:

```json
{
  // Enable/disable Copilot
  "github.copilot.enable": {
    "*": true,
    "markdown": false,
    "plaintext": false
  },
  
  // Inline suggestions
  "github.copilot.inlineSuggest.enable": true,
  
  // Next Edit Suggestions
  "github.copilot.nextEditSuggestions.enable": true,
  
  // Auto-completions in comments
  "github.copilot.inlineSuggest.enableCodeActions": true,
  
  // Chat settings
  "chat.editor.fontSize": 14,
  "chat.editor.wordWrap": "on"
}
```

### Per-Language Configuration

Disable Copilot for specific languages:

```json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": false,
    "markdown": false,
    "json": false
  }
}
```

### Workspace-Specific Settings

Create `.vscode/settings.json` for project-specific configuration:

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    "Use Python 3.11+ features",
    "Follow PEP 8 style guidelines",
    "Include type hints for all functions"
  ]
}
```

---

## Quick Reference Card

### Starting Points
- **Need help understanding code?** → Ask mode + `#codebase`
- **Making targeted changes?** → Edit mode + `#file`
- **Building new features?** → Agent mode
- **Quick inline fix?** → `⌘I` / `Ctrl+I`

### Context Essentials
- `#file:path` — Include specific file
- `#codebase` — Search whole project
- `#problems` — Reference VS Code errors
- `#selection` — Current selection

### Customization Files
- `.github/copilot-instructions.md` — Project guidelines
- `.github/prompts/*.prompt.md` — Reusable prompts
- `.github/agents/*.md` — Custom AI personas
- `.vscode/mcp.json` — MCP server configuration

---

## Additional Resources

- [VS Code Copilot Documentation](https://code.visualstudio.com/docs/copilot/overview)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Copilot Cheat Sheet](https://code.visualstudio.com/docs/copilot/reference/copilot-cheat-sheet)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
