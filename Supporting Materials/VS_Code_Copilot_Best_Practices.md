# VS Code GitHub Copilot Best Practices

> **Version Note:** This guide reflects GitHub Copilot features as of late 2025. For the latest updates, refer to the [official VS Code Copilot documentation](https://code.visualstudio.com/docs/copilot/overview).

This guide provides practical strategies for getting the most out of GitHub Copilot in VS Code. It covers context management, prompt engineering, mode selection, session management, and quality optimization.

---

## Table of Contents

1. [Context Management](#1-context-management)
2. [Effective Prompting](#2-effective-prompting)
3. [Mode Selection](#3-mode-selection)
4. [Session Hygiene](#4-session-hygiene)
5. [Model Selection](#5-model-selection)
6. [Quality Optimization](#6-quality-optimization)
7. [Speed Optimization](#7-speed-optimization)
8. [Common Pitfalls](#8-common-pitfalls)
9. [Decision Trees](#9-decision-trees)

---

## 1. Context Management

### The Golden Rule

**More relevant context = better results. Less irrelevant context = faster, more focused results.**

### When to Use #codebase vs #file

| Use `#codebase` when... | Use `#file` when... |
| --- | --- |
| You don't know where code lives | You know the exact file |
| Searching for patterns across project | Making targeted changes |
| Understanding project architecture | Focusing on specific implementation |
| Finding all usages of a concept | Avoiding noise from unrelated files |

**Example:**
```
# Broad search — use #codebase
Where is authentication implemented? #codebase

# Targeted work — use #file
Add input validation to #auth_controller.py
```

### Context Hierarchy (Most to Least Specific)

1. **#selection** — Exact code you're focused on
2. **#editor** — Visible code in current file
3. **#file** — Specific file(s) by name
4. **#folder** — Directory contents
5. **#codebase** — Entire workspace search

**Best Practice:** Start specific, broaden only if needed.

### Effective #-Mention Patterns

**Pattern 1: Anchored Context**
```
Explain the error handling in #utils/errors.py and how it's used in #api/handlers.py
```

**Pattern 2: Comparative Analysis**
```
Compare the implementation patterns in #service_a.py vs #service_b.py
```

**Pattern 3: Contextual Generation**
```
Create a new endpoint similar to the ones in #routes/users.py
```

### Context Quality Tips

1. **Close irrelevant tabs** — Open tabs influence suggestions
2. **Use workspace folders wisely** — Multi-root workspaces dilute context
3. **Enable workspace indexing** — Essential for `#codebase` effectiveness
4. **Reference recent files** — Recently edited files get more weight

---

## 2. Effective Prompting

### The CLEAR Framework

| Element | Description | Example |
| --- | --- | --- |
| **C**ontext | What's the situation? | "In this Flask API..." |
| **L**anguage/Tech | What stack? | "...using Python 3.11 and SQLAlchemy..." |
| **E**xpectation | What format/style? | "...following our existing patterns..." |
| **A**ction | What should happen? | "...add a new endpoint for user preferences..." |
| **R**estrictions | What to avoid? | "...without modifying the database schema" |

**Complete Example:**
```
In this Flask API using Python 3.11 and SQLAlchemy, following the patterns 
in #routes/users.py, add a new endpoint for user preferences that supports 
GET and PATCH methods, without modifying the existing database schema.
```

### Prompt Structures That Work

**For Code Generation:**
```
Create a [thing] that:
- Does X
- Handles Y edge case
- Returns Z format
```

**For Debugging:**
```
This code is [doing X] but should [do Y].
Error message: [paste error]
Relevant code: #file
```

**For Refactoring:**
```
Refactor #file to:
- [Change 1]
- [Change 2]
While preserving [constraint]
```

**For Explanation:**
```
Explain how [concept/function] works in #codebase, focusing on [specific aspect]
```

### Anti-Patterns to Avoid

| Don't | Do Instead |
| --- | --- |
| "Fix the bug" | "Fix the null pointer error on line 42 when input is empty" |
| "Make it better" | "Refactor to reduce cyclomatic complexity and add error handling" |
| "Write some tests" | "Write pytest unit tests covering the happy path and edge cases for #module.py" |
| "Clean this up" | "Extract the database logic into a separate repository class" |

### Iterative Refinement

When results aren't right:

1. **Add constraints:** "Also ensure thread safety"
2. **Provide examples:** "Similar to how #existing_code.py handles this"
3. **Narrow scope:** "Focus only on the validate_input function"
4. **Clarify format:** "Return as a Python dataclass, not a dictionary"

---

## 3. Mode Selection

### Quick Decision Guide

```
Do you need to modify code?
├── No → Ask Mode
│         Best for: Learning, exploration, understanding
│
└── Yes → Do you know exactly what files to change?
          ├── Yes → Edit Mode
          │         Best for: Targeted refactoring, specific fixes
          │
          └── No → Agent Mode
                    Best for: Complex features, multi-file changes
```

### Mode Characteristics

| Aspect | Ask | Edit | Agent |
| --- | --- | --- | --- |
| **Modifies files** | Never | Referenced only | Any file |
| **Runs commands** | Never | Never | With approval |
| **Explores codebase** | On request | Limited | Autonomously |
| **Speed** | Fast | Medium | Variable |
| **Control** | Full | High | Supervisory |
| **Risk** | None | Low | Medium |

### Ask Mode Best Practices

**Ideal for:**
- Understanding unfamiliar code
- Exploring implementation options before committing
- Learning new concepts in context
- Getting documentation and explanations

**Tips:**
- Use `#codebase` liberally for exploration
- Ask follow-up questions to drill down
- Request multiple approaches before choosing

**Example workflow:**
```
1. "How does authentication work in #codebase?"
2. "What are the security implications of this approach?"
3. "What would be needed to add OAuth support?"
4. [Switch to Edit/Agent mode for implementation]
```

### Edit Mode Best Practices

**Ideal for:**
- Refactoring specific functions or classes
- Adding features to known locations
- Bug fixes with identified root cause
- Code transformations (e.g., style changes)

**Tips:**
- Always reference specific files with `#file`
- Review diffs carefully before accepting
- Use for one logical change at a time
- Combine with inline chat for small edits

**Example workflow:**
```
1. "Add type hints to all functions in #user_service.py"
2. [Review diff]
3. "Now add corresponding unit tests in #test_user_service.py"
```

### Agent Mode Best Practices

**Ideal for:**
- End-to-end feature implementation
- Tasks requiring exploration
- Multi-file coordinated changes
- Setting up new components or modules

**Tips:**
- Give clear, complete task descriptions
- Review tool invocations before approving
- Use checkpoints for complex tasks
- Let the agent finish before intervening

**Example workflow:**
```
"Add a caching layer for the user service:
- Use Redis for cache backend
- Cache user lookups for 5 minutes
- Add cache invalidation on user updates
- Include configuration for cache settings
- Add appropriate tests"
```

### Inline Chat: The Fourth Option

**When to use:**
- Quick, single-location edits
- Explaining selected code
- Generating code at cursor position
- Small refactorings

**Shortcut:** `⌘I` (Mac) / `Ctrl+I` (Windows/Linux)

**Best for:** Changes that don't require conversation history.

---

## 4. Session Hygiene

### When to Start a New Session

| Start New Session | Continue Existing Session |
| --- | --- |
| Switching to unrelated task | Follow-up on previous response |
| Context becoming cluttered | Iterating on same feature |
| Getting confused or off-track responses | Building on established context |
| Starting fresh exploration | Debugging conversation itself |

### Session Management Tips

1. **Use descriptive first messages** — Sets context for entire session
2. **One topic per session** — Mixing topics degrades quality
3. **Check history periodically** — Access via clock icon
4. **Export important sessions** — Document decisions and rationale

### Checkpoints

Checkpoints save your workspace state during a session, allowing you to:
- Experiment with different approaches
- Roll back if changes go wrong
- Compare before/after states

**When to create checkpoints:**
- Before major refactoring
- When exploring multiple solutions
- Before agent mode tasks

**Important:** Checkpoints are session-scoped, not version control. Use Git for permanent history.

### Context Refresh Strategies

When a session becomes sluggish or confused:

1. **Re-anchor with files:** Start message with `#file` references
2. **Summarize state:** "We've added X and Y. Now we need Z."
3. **Clear irrelevant context:** Close unrelated files/tabs
4. **Start fresh:** Sometimes a new session is faster

---

## 5. Model Selection

### Model Categories

| Category | Characteristics | Best For |
| --- | --- | --- |
| **Fast** | Low latency, lower cost | Simple completions, quick questions, formatting |
| **Advanced** | Better reasoning, more thorough | Architecture, debugging, complex logic |
| **Auto** | Dynamically selected | When unsure; balances speed and quality |

### Task-to-Model Mapping

| Task | Recommended Model |
| --- | --- |
| Code completion | Fast |
| Simple questions | Fast |
| Code formatting | Fast |
| Bug fixes (simple) | Fast |
| Architecture design | Advanced |
| Security analysis | Advanced |
| Complex debugging | Advanced |
| API design | Advanced |
| General development | Auto |

### Model Selection Strategy

```
Is this a quick, bounded task?
├── Yes → Fast model
│         Examples: "Add a docstring", "Format this JSON", "What's the syntax for X?"
│
└── No → Does it require deep reasoning?
         ├── Yes → Advanced model
         │         Examples: "Design a caching strategy", "Find the security flaw", "Architect this system"
         │
         └── Unsure → Auto
                      Let VS Code optimize based on context
```

### Premium Request Considerations

Some models consume premium requests at higher rates. For Copilot Pro/Business:
- Monitor usage in GitHub settings
- Use fast models for routine tasks
- Reserve advanced models for complex problems

---

## 6. Quality Optimization

### Code Quality Settings

Configure Copilot to match your standards:

**Via `.github/copilot-instructions.md`:**
```markdown
# Code Quality Standards

- All functions must have type hints
- Use Google-style docstrings
- Maximum function length: 50 lines
- Prefer composition over inheritance
- Always handle errors explicitly
```

**Via VS Code settings:**
```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    "Use Python 3.11+ features",
    "Follow PEP 8 strictly",
    "Include comprehensive error handling"
  ]
}
```

### Review Strategies

**For Edit Mode:**
1. Read the full diff before accepting
2. Check edge cases in generated code
3. Verify error handling is appropriate
4. Ensure tests cover new code

**For Agent Mode:**
1. Review each file change individually
2. Run tests after accepting changes
3. Check for unintended modifications
4. Verify no sensitive data exposed

### Validation Checklist

After accepting Copilot-generated code:

- [ ] Code compiles/runs without errors
- [ ] Existing tests still pass
- [ ] New functionality has tests
- [ ] No security vulnerabilities introduced
- [ ] Follows project conventions
- [ ] Documentation updated if needed

---

## 7. Speed Optimization

### Reduce Latency

1. **Use specific context** — `#file` faster than `#codebase`
2. **Choose fast models** — When quality permits
3. **Keep prompts focused** — Shorter = faster
4. **Close unused tabs** — Less context to process

### Efficient Workflows

**Batch Related Changes:**
```
# Instead of 3 separate requests:
Add type hints, docstrings, and error handling to #user_service.py
```

**Use Inline Chat for Small Edits:**
- Faster than opening full chat
- No context switch
- Immediate visual feedback

**Leverage Next Edit Suggestions (NES):**
- Make one change, let Copilot suggest the rest
- Especially powerful for repetitive refactoring

### Keyboard-First Workflow

| Action | Shortcut (Mac) | Shortcut (Win/Linux) |
| --- | --- | --- |
| Inline Chat | `⌘I` | `Ctrl+I` |
| Quick Chat | `⇧⌘I` | `Ctrl+Shift+I` |
| Accept Suggestion | `Tab` | `Tab` |
| Next Suggestion | `⌥]` | `Alt+]` |
| Trigger Suggestion | `⌥\` | `Alt+\` |

---

## 8. Common Pitfalls

### Pitfall 1: Over-Trusting Generated Code

**Problem:** Accepting code without review.

**Solution:**
- Always read generated code
- Run tests before committing
- Check edge cases manually
- Review security implications

### Pitfall 2: Context Overload

**Problem:** Including too much irrelevant context.

**Solution:**
- Be specific with #-mentions
- Close unrelated files
- Use `#selection` for focused edits
- Start new sessions for new topics

### Pitfall 3: Vague Prompts

**Problem:** "Make it better" or "Fix the bug."

**Solution:**
- Describe specific desired outcome
- Include constraints and requirements
- Provide examples when helpful
- State what should NOT change

### Pitfall 4: Wrong Mode Selection

**Problem:** Using Agent mode for simple edits (slow) or Ask mode when changes needed (requires re-doing work).

**Solution:**
- Refer to mode decision tree
- Match mode to task complexity
- Switch modes as needs evolve

### Pitfall 5: Ignoring Custom Instructions

**Problem:** Re-explaining standards in every prompt.

**Solution:**
- Set up `.github/copilot-instructions.md`
- Create prompt files for common tasks
- Use custom agents for specialized roles

### Pitfall 6: Session Context Decay

**Problem:** Quality degrades in long sessions.

**Solution:**
- Start new sessions for new topics
- Re-anchor context periodically
- Use checkpoints before major changes
- Keep sessions focused

---

## 9. Decision Trees

### What Mode Should I Use?

```
┌─────────────────────────────────────────────────────────────────┐
│                  WHAT DO YOU NEED?                               │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Understanding    Targeted Edit    Complex Task
              │               │               │
              ▼               ▼               ▼
         ASK MODE        EDIT MODE      AGENT MODE
              │               │               │
              ▼               ▼               ▼
    • Explanations     • Refactoring    • Multi-file changes
    • Exploration      • Bug fixes      • New features
    • Learning         • Additions      • Unknown scope
    • Documentation    • Known files    • Autonomous work
```

### What Context Should I Include?

```
┌─────────────────────────────────────────────────────────────────┐
│              HOW SPECIFIC IS YOUR TASK?                          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   Very Specific        Somewhat Specific        Exploratory
        │                     │                     │
        ▼                     ▼                     ▼
   #selection              #file               #codebase
   #editor              #folder                    │
        │                     │                     │
        ▼                     ▼                     ▼
 "Fix this loop"     "Refactor this       "How does auth
                      service"             work here?"
```

### What Model Should I Use?

```
┌─────────────────────────────────────────────────────────────────┐
│                  TASK COMPLEXITY                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
     Simple              Medium               Complex
        │                     │                     │
        ▼                     ▼                     ▼
   Fast Model           Auto Model         Advanced Model
        │                     │                     │
        ▼                     ▼                     ▼
 • Completions        • General dev       • Architecture
 • Formatting         • Feature work      • Security review
 • Quick Q&A          • Bug fixes         • Complex debug
```

---

## Quick Reference Summary

### The 5 Rules of Effective Copilot Use

1. **Right Mode** — Ask for learning, Edit for changes, Agent for features
2. **Right Context** — Specific files beat broad searches
3. **Right Model** — Fast for simple, Advanced for complex
4. **Right Prompt** — Clear, specific, constrained
5. **Right Session** — Fresh for new topics, continued for iterations

### Daily Workflow Pattern

```
Morning: Review code with Ask mode + #codebase
↓
Planning: Discuss approaches in Ask mode
↓
Implementation: Agent mode for features, Edit for refinements
↓
Review: Ask mode for explanations, Edit for fixes
↓
End of day: Commit, close sessions, clear context
```

---

## Additional Resources

- [GitHub Copilot Reference Guide](GitHub_Copilot_Reference_Guide.md) — Commands and features
- [Lab 0: GitHub Copilot Practice](../Labs/Day_01_Planning_and_Requirements/D0_Lab0_GitHub_Copilot_Practice.md) — Hands-on exercises
- [VS Code Copilot Documentation](https://code.visualstudio.com/docs/copilot/overview) — Official docs
- [Prompt Engineering Guide](https://code.visualstudio.com/docs/copilot/prompt-engineering) — Advanced prompting
