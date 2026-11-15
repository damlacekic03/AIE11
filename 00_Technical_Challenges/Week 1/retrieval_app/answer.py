"""Stage 5: turn retrieved chunks into an answer.

YOUR CODE GOES HERE. The prompt is yours to write — it is the cheapest thing
in the pipeline to change and often the most effective.
"""

from .index import Hit, client

CHAT_MODEL = "gpt-4.1-mini"
RAG_SYSTEM_PROMPT = """You are a personal movie-notes assistant that answers only from the user's film ratings and notes.
Answer the user's question using ONLY the provided context chunks.

Rules:
1. Cite the source chunk ID in brackets (e.g., [0]) for every claim you make.
2. If the provided context does not contain enough information to answer the question, reply exactly with: "I don't know based on the provided context."
3. Do NOT use outside knowledge, guess, or extrapolate from loosely related chunks.
"""

def build_messages(question: str, hits: list[Hit]) -> list[dict]:
    """Assemble the messages list sent to the chat model.

    Args:
        question: the user's question.
        hits: what search() returned. May be empty.

    Returns:
        A list of {"role": ..., "content": ...} dicts — a system message
        setting the rules, and a user message carrying the context and the
        question.

    Three things your prompt has to decide, and they are real decisions:
      1. How do you label each chunk in the context so the model can refer to
         it? (hit.chunk_id exists for this.)
      2. What should it do when the context does not contain the answer? Say
         so explicitly, or it will answer from the nearest chunk regardless.
      3. What happens when `hits` is empty? Write that branch deliberately.

    Hint: Session 2's RAG_SYSTEM_TEMPLATE is a good starting point, and a
    better one once you have read Step 3's failures and edited it.
    """
    if not question or not question.strip():
        raise ValueError("question cannot be empty.")
    if not hits:
        user_content = (
            "Context:\n"
            "[No relevant context was found in the corpus.]\n\n"
            f"Question: {question.strip()}"
        )
        return [
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
    formatted_chunks = []
    for hit in hits:
        formatted_chunks.append(f"[{hit.chunk_id}]\n{hit.text.strip()}")

    context_block = "\n\n---\n\n".join(formatted_chunks)

    user_content = (
        f"Context:\n{context_block}\n\n"
        f"Question: {question.strip()}"
    )

    return [
        {"role": "system", "content": RAG_SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]

def answer(question: str, hits: list[Hit]) -> str:
    """Call the chat model and return its reply as a string.

    Hint: `client().chat.completions.create(model=CHAT_MODEL, messages=...)`,
    then dig out `.choices[0].message.content`. Look up what `temperature`
    does to your results when you run the same question twice.
    """
    messages = build_messages(question, hits)
    response = client().chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("Model returned an empty response (content is None).")

    return content.strip()