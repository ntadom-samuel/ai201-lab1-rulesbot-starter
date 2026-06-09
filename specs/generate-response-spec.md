# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter          | Type         | Description                                                                             |
| ------------------ | ------------ | --------------------------------------------------------------------------------------- |
| `query`            | `str`        | The user's original question                                                            |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:

- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

_Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours._

---

### Context formatting

_How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?_

```

Label each chunk with its game and use a clear delimiter. Distance scores are noise for the LLM — leave them out:


[Game: Catan]
<chunk text>

---

[Game: Monopoly]
<chunk text>

This lets the model cite which game each rule came from without you having to re-engineer the prompt.
```

---

### System prompt — grounding instruction

_Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function._

```
You are a board game rules assistant. Answer ONLY using the rule text provided below. Do NOT use your general knowledge about board games. If the answer is not in the provided context, say so clearly — do not guess.

```

---

### System prompt — citation instruction

_Write the exact instruction you will use to tell the model to identify which game its answer comes from._

```
When answering, always state which game the rule comes from, e.g. "According to [Game Name]'s rules, ..." If the context includes rules from multiple games, specify which game each part of your answer comes from.

```

---

### Fallback behavior

_What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message._

```
I couldn't find a confident answer to that in the loaded rules. The context I retrieved doesn't seem relevant enough to answer reliably. Try rephrasing, or consult the official rulebook directly.

```

---

### Handling low-relevance chunks

_`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?_

```
Filter above 0.7: cleaner context, but if all chunks are filtered, return the fallback message instead of calling the LLM at all — saves a Groq API call on junk queries
```

---

### Message structure

_Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?_

```
system: grounding instruction + citation instruction
user:   "Context:\n{formatted chunks}\n\nQuestion: {query}"

```

---

## Implementation Notes

_Fill this in after implementing and testing._

**Test query and response:**

```
Query: [your test query]
Response: [abbreviated response]
Correctly grounded? [yes / no]
Cited the right game? [yes / no]
```

**One thing you changed from your original spec after seeing the actual output:**

```
[your answer here]
```
