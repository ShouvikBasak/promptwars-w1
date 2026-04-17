# AI Contract: Gemini Assistant Behavior

This document serves as the strict operational contract for the Gemini AI reasoning module powering StadiumFlow. Adhering to these bounds guarantees cost protection, output testability, consistent user safety, and strict alignment with the demo MVP constraints. 

## 1. Input Bounds

The reasoning module operates as a stateless processor. It accepts solely the explicit context injected by the Cloud Run backend for a single query.

**Permitted Inputs:**
- **User Context:** Information defining the attendee's explicitly chosen location (e.g., "North Gate") and the list of physically nearby Points of Interest (POIs).
- **Aggregated Crowd Data:** Quantitative context mapped to the POIs, primarily `currentWaitMinutes` and `confidenceScore`.
- **Accessibility Preferences (Optional):** Specific capability tags to filter recommendations safely (e.g., mapping a "family_restroom" preference against the POI's `accessibilityFeatures` array).

## 2. Output Bounds

To prevent unparseable results and cognitive overload in the frontend, the generated output from the model must conform identically to these deterministic bounds:

**Structural Constraints:**
- **JSON Only:** The model's response must strictly consist of native JSON. Any markdown blocks, conversational prefixes (e.g., "Sure, here are your recommendations"), or plain-text appendages are explicitly forbidden.
- **Fixed Schema:** Responses will conform to a highly predictable JSON object interface, strictly returning a single array of items.
- **Maximum Options:** The model is capped at generating a maximum of **3 recommendation options**. 
- **Plain Language:** The explanation field for each recommendation must be succinct and use simple, plain language designed for a high-stress, noisy physical environment.

## 3. Strict Behavioral Rules

The system restricts the AI from drifting creatively, enforcing "smart assistant" logic rather than "generative conversationalist" workflows.

- **No Hallucinated Facts:** The assistant will not generate non-existent POIs, invent wait times, or hallucinate physical constraints not explicitly provided in the payload.
- **No External Knowledge Assumptions:** The assistant is explicitly sandboxed; it must not use generalized physical stadium knowledge or domain reasoning that conflicts with the passed JSON parameters.
- **Length Constraint (Max 120 Tokens):** The output verbosity is strictly limited. The prompt and generation configurations must limit overall output to a maximum of **120 tokens** to ensure rapid completion speeds and protect API margins.
- **Low Confidence Transparency:** If the provided contextual data contains a low `confidenceScore` for any evaluated POI, the AI must natively evaluate this and explicitly state the uncertainty in the recommendation's plain-language justification, maintaining the crucial 'human-in-the-loop' trust model.
