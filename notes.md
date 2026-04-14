# Physical Event Experience

## Problem Statement

Design a solution that improves the physical event experience for attendees at large-scale sporting venues. The system should address challenges such as crowd movement, waiting times, and real-time coordination, while ensuring a seamless and enjoyable experience.

Your submission consists of two parts:
    Technical: Codebase (GitHub Repo) + Live Preview (Cloud Run URL).
    Narrative: A LinkedIn post of your build to share with the community.

$5 - [PromptWars: W1, Pan India, India - 2026]
Your credit will allow you to use Google Cloud, Gemini API and Firebase.

## Instructions

1. Before You Begin

Make sure the following prerequisites are completed:

    Google Antigravity is downloaded and set up on your system
    Git is installed and configured
    You have an active GitHub account
    You are able to create and manage public repositories

2. Important Rules

    You have a maximum of 2 submission attempts for the Warm Up Round
    You have a maximum of 4 submission attempts (For Actual Challenge Round)
    The repository size must be less than 1 MB
    The GitHub repository must be public
    The repository should contain only one branch
    Failure to follow these rules may result in your submission not being evaluated

3. Challenge Expectations

Your solution should demonstrate:

    Ability to build a smart, dynamic assistant
    Logical decision making based on user context
    Effective use of Google Services
    Practical and real-world usability
    Clean and maintainable code

Participants must choose one of the provided challenge verticals and design their solution around that persona and logic.
4. How to Work on Your Project

    Create a new repository on GitHub
    Ensure the repository is set to public
    Open Google Antigravity
    Clone your repository inside Antigravity
    Build your solution through prompting and coding
    Regularly commit and push your progress
    Keep all work within a single branch

5. What to Submit

Note: For detail guide on how to submit. Please refer to the document
Link

Your submission must include:

    A public GitHub repository link
    Complete project code inside the repository
    A README explaining:
        Your chosen vertical
        Approach and logic
        How the solution works
        Any assumptions made

6. Evaluation Focus Areas

Submissions will be reviewed on:

    Code Quality – structure, readability, maintainability
    Security – safe and responsible implementation
    Efficiency – optimal use of resources
    Testing – validation of functionality
    Accessibility – inclusive and usable design
    Google Services – meaningful integration of Google Services

## IDEATION: Prompt to brainstorm ideas

Initial prompt to Copilot for ideation

I am participating in the Google PromptWars Hackathon, and I need to design a solution that improves the physical event experience for attendees at large-scale sporting venues. The system should address challenges such as crowd movement, waiting times, and real-time coordination, while ensuring a seamless and enjoyable experience. I have $5 credit to use Google Cloud, Gemini API, and Firebase for my project. Can you help me brainstorm some ideas on how to approach this problem?

As a judging criteria, my solution will be evaluated on code quality, security, efficiency, testing, accessibility, and the use of Google services. I want to make sure that my solution is not only innovative but also practical and user-friendly.

The submission will consist of two parts: a technical component, which includes a codebase hosted on GitHub and a live preview hosted on Cloud Run, and a narrative component, which is a LinkedIn post sharing my build with the community.

I have to use Google Antigravity to create the solution.

Can you help me brainstorm some ideas on how to approach this problem and design a solution that meets the criteria mentioned above? Also, what are similar existing websites that perform similar functions, and how can I differentiate my solution from them?

## Planning phase - laying the foundations

Based on the above, have done the following:

- Created a git repo "promptwars-w1" which is private now and will make public once my project is ready for submission
- Cloned the git repo locally and opened using Antigravity
- Created the README.md

What are now the best practices to build the project using Antigravity. Before I actually start building the project I would go step by step setting up the best practices and follow accordingly so that the foundations are strong and the code base meets all the criteria for AI to evaluate the following parameters:
    Code Quality – structure, readability, maintainability
    Security – safe and responsible implementation
    Efficiency – optimal use of resources
    Testing – validation of functionality
    Accessibility – inclusive and usable design
    Google Services – meaningful integration of Google Services

Recommendations:
Think of this as “how a senior engineer would use Antigravity intentionally”, not vibe‑coding.

### Create RULES

### Create ARTIFACTS

Make Antigravity “auditable” in your repo (this is a differentiator)

Add a /prompts folder and commit:

- SPEC.md (problem → constraints → MVP scope → non-goals)
- PROMPT_STRATEGY.md (your prompting rules, safety constraints, how you used artifacts)
- ARCHITECTURE.md (diagram + data model)
- WALKTHROUGH.md (screenshots, how to run, test evidence)

This mirrors what strong PromptWars repos often do (public examples show prompt strategy + architecture docs as first-class artifacts).

They are control surfaces for Antigravity. In Antigravity terms: these are Artifacts the agent can reason against instead of improvising.

/ARCHITECTURE.md
/ASSUMPTIONS.md
/SECURITY.md
/ACCESSIBILITY.md
/TESTING.md

#### ARCHITECTURE.md (10–15 lines only)

Purpose: prevent architectural sprawl.
Include:

Frontend: static web UI (no framework escalation)
Backend: Cloud Run API
Data: Firestore (collections listed, no joins)
AI: Gemini via backend only
No background jobs, no streaming, no sensors

This file is your “do not exceed” guardrail.

#### ASSUMPTIONS.md

Purpose: stop overengineering and judge confusion.
Include:

Wait times are approximate
Human confirmation > automation
No camera or sensor data
MVP demo scale only

Judges like explicit assumptions.

#### SECURITY.md

Purpose: show intentional responsibility.
Include:

Auth required for writes
Role separation (attendee vs staff)
No PII
API keys server‑side only

This directly maps to Security scoring.

#### ACCESSIBILITY.md

Purpose: bake inclusion into design.
Include:

Keyboard navigation required
No color‑only signals
Plain‑language responses
Reduced motion preference respected

This prevents UI regressions later.

#### TESTING.md

Purpose: avoid “no tests” penalty.
Include:

Unit tests for aggregation logic
Validation tests for API inputs
Manual accessibility checklist

Even minimal tests score well if intentional.

## References

- [Arena AI: The Official AI Ranking & LLM Leaderboard](https://arena.ai/)
- [OpenRouter - Unified interface for LLMs](https://openrouter.ai/)
- [cursor.directory - Rules](https://cursor.directory/plugins?q=rules) (for setting up project rules in Antigravity and other coding assistants)

## Evaluation Focus

|Focus Area|How this design helps|
|----------|---------------------|
|Code quality|Clear separation: attendee vs ops logic|
|Security|Justifiable role separation (even if simple)|
|Efficiency|Human-in-loop avoids heavy ML / sensors|
|Testing|Easy to unit-test decision logic|
|Accessibility|Ops UI can be keyboard-only|
|Google servicesFirebase Auth + Firestore + Gemini|