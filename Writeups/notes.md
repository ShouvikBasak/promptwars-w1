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

### Create CONSTRAINTS

Make Antigravity “auditable” in your repo (this is a differentiator)

They are control surfaces for Antigravity. In Antigravity terms: these are Artifacts the agent can reason against instead of improvising.

/SPECS.md
/ARCHITECTURE.md
/ASSUMPTIONS.md
/SECURITY.md
/ACCESSIBILITY.md
/TESTING.md

## Evaluation Focus

|Focus Area|How this design helps|
|----------|---------------------|
|Code quality|Clear separation: attendee vs ops logic|
|Security|Justifiable role separation (even if simple)|
|Efficiency|Human-in-loop avoids heavy ML / sensors|
|Testing|Easy to unit-test decision logic|
|Accessibility|Ops UI can be keyboard-only|
|Google servicesFirebase Auth + Firestore + Gemini|


## Phase 1 — Scope Lock & Planning (NO CODE)

Goal: Freeze scope and architecture so the agent cannot drift later.

### Prompt 1.1 — Scope Alignment & Risk Check

You are acting as a senior software architect reviewing an AI‑assisted hackathon project.

Read the following files carefully:
- README.md
- ARCHITECTURE.md
- ASSUMPTIONS.md
- ACCESSIBILITY.md
- SECURITY.md
- TESTING.md
- SPEC.md

Your task:
1. Verify that the scope is cohesive and realistic for a demo‑ready MVP.
2. Identify any scope ambiguity or over‑engineering risk.
3. Propose clarifications ONLY if strictly necessary.

Constraints:
- Do NOT generate any code.
- Do NOT suggest new features.
- Keep the response concise (max 20 bullet points).

Output:
Create a markdown artifact named IMPLEMENTATION_SCOPE_REVIEW.md.

#### Actions following the findings from the review:
Update files to include clarifications and reduce ambiguitys. Ask the Agent again to review and provide a findings in v2 of the file.

### Prompt 1.2 — Implementation Plan (Controlled)

Based strictly on:
- README.md
- ARCHITECTURE.md
- ASSUMPTIONS.md
- ACCESSIBILITY.md
- SECURITY.md
- TESTING.md
- SPEC.md
- Implementation_Scope_Review_v2.md

Create a high‑level implementation plan.

Rules:
- Maximum 12 steps.
- Each step must map directly to content in README.md.
- No step may introduce a new capability not already described.
- Absolutely no code generation.

Output:
Create a markdown artifact named IMPLEMENTATION_PLAN.md.




