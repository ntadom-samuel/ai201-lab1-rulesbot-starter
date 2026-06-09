from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    relevant_chunks = [c for c in retrieved_chunks if c["distance"] <= 0.7]
    if not relevant_chunks:
        return (
            "I couldn't find a confident answer to that in the loaded rules. "
            "The context I retrieved doesn't seem relevant enough to answer reliably. "
            "Try rephrasing, or consult the official rulebook directly."
        )

    context_parts = []
    for chunk in relevant_chunks:
        context_parts.append(f"[Game: {chunk['game']}]\n{chunk['text']}")
    context_block = "\n\n---\n\n".join(context_parts)

    system_message = (
        "You are a board game rules assistant. Answer ONLY using the rule text provided below. "
        "Do NOT use your general knowledge about board games. If the answer is not in the provided context, "
        "say so clearly — do not guess.\n\n"
        "When answering, always state which game the rule comes from, e.g. "
        "\"According to [Game Name]'s rules, ...\" If the context includes rules from multiple games, "
        "specify which game each part of your answer comes from."
    )

    user_message = f"Context:\n{context_block}\n\nQuestion: {query}"

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content
