# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter   | Type  | Description                                                                |
| ----------- | ----- | -------------------------------------------------------------------------- |
| `query`     | `str` | The user's natural language question                                       |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key          | Type    | Description                                                   |
| ------------ | ------- | ------------------------------------------------------------- |
| `"text"`     | `str`   | The chunk text                                                |
| `"game"`     | `str`   | The game name this chunk came from                            |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

_Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours._

---

### Query approach

_Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?_

```
Approach (_collection.query() arguments)

You pass query_texts=[query] (a list, even for one query), n_results=n_results, and include=["documents", "metadatas", "distances"].

The include list controls what ChromaDB returns — you need all three to build your output dicts.

ChromaDB embeds the query string automatically using the same _ef you set on the collection.
```

---

### Return structure

_Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?_

```
The three include fields map directly to your output keys:

"text" ← results["documents"][0][i]
"game" ← results["metadatas"][0][i]["game"]
"distance" ← results["distances"][0][i]

```

---

### Handling the nested result structure

_`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists._

```
_collection.query() always returns results as a list-of-lists — one inner list per query string you passed.

Since you pass a single query (query_texts=[query]), index [0] gives you the flat list for that query.

The nesting exists so the same API works for batch queries.
```

---

### Relevance threshold

_Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?_

```
Two options: filter by distance (e.g. drop anything above 0.7) or return all n_results unconditionally.

Filter: cleaner context for the LLM, but you might return zero results for obscure questions

No filter: simpler, predictable count, but the LLM gets noise for off-topic queries
```

---

### Edge cases

_How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?_

```
(a) Empty collection: already handled — the existing if _collection.count() == 0: return [] guard covers this.

(b) Poor match: ChromaDB returns the closest chunks it has regardless of quality.
The distances will be high (close to 1.0) but results still come back. Without a threshold filter, these get passed to the LLM.

(c) Multiple games: ChromaDB returns globally nearest neighbors — results can come from any game, ranked purely by distance.
Your output naturally includes the "game" field so the generator can distinguish them.
```

---

## Implementation Notes

_Fill this in after implementing, before moving to Milestone 3._

**Test query and top result returned:**

```
Query: [your test query]
Top result game: [game name]
Distance score: [score]
Does it make sense? [yes / no / explain]
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
