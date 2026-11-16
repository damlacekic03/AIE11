"""Stage 1 and 2: load the source text, and split it into chunks.

YOUR CODE GOES HERE. Both functions below raise NotImplementedError.
You saw working versions of both in Session 2's `aimakerspace/text_utils.py`:
read it, understand it, then write your own. Copying it verbatim is allowed;
not being able to explain it is not.

Neither function knows or cares what your corpus is about. That is the point:
swap the .txt in data/ and nothing in this file should need to change.
"""

from pathlib import Path


def load_corpus(path: Path) -> str:
    """Read a .txt file and return its entire contents as one string.

    Args:
        path: the .txt file to read, whichever corpus the app was pointed at.

    Returns:
        The whole file as a single string.

    Hint: this is three lines. `open()`, or `Path.read_text()`. Mind the
    encoding: read it as utf-8, and your own corpus may need you to mean it.
    """
    if path.suffix.lower() != ".txt":
        raise ValueError(f"Corpus file {path} is not a .txt file.")
    if not path.is_file():
         raise FileNotFoundError(f"No such file: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
         raise ValueError(f"Corpus file is empty: {path}")
    return text    

def split_corpus(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """Split one long string into a list of overlapping chunks.

    Args:
        text: the whole corpus, from load_corpus().
        chunk_size: how many characters in each chunk.
        chunk_overlap: how many characters each chunk repeats from the last one.

    Returns:
        A list of strings.

    Your check, for any corpus: a loop stepping by (chunk_size - chunk_overlap)
    over N characters produces ceil(N / (chunk_size - chunk_overlap)) chunks.
    The app prints both numbers, so you can verify the count without being told
    the answer. The shipped guide is 16,206 characters, which is 21 chunks on
    the defaults above.

    Hint: a range() that steps by (chunk_size - chunk_overlap), slicing as it
    goes. Why does the step subtract the overlap rather than add it?
    """
    """if not text or not text.strip():
         return []
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= text_length:
            break

        start += chunk_size - chunk_overlap

    return chunks"""
    if not text or not text.strip():
        return []

    chunks = []
    current = []

    for line in text.splitlines():
        stripped = line.lstrip()

        if stripped.startswith(("## ", "### ")):
            if current:
                chunk_text = "\n".join(current).strip()
                if chunk_text:
                    chunks.append(chunk_text)
            current = [line]
        else:
            current.append(line)

    if current:
        chunk_text = "\n".join(current).strip()
        if chunk_text:
            chunks.append(chunk_text)

    return chunks