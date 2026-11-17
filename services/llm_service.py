
from functools import lru_cache
from typing import Iterator, Sequence

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    validate_groq_config
)


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    """
    Initialize and return the Groq chat model.

    The lru_cache decorator ensures that the model
    configuration is reused instead of recreated
    on every request.

    Returns:
        ChatGroq: Configured Groq chat model.
    """

    # Validate API key before initializing the model
    validate_groq_config()

    llm = ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.7,
        max_retries=2,
        timeout=60
    )

    return llm


def generate_response(
    messages: Sequence[BaseMessage]
) -> str:
    """
    Generate a complete response from Groq.

    Args:
        messages: Structured LangChain messages.

    Returns:
        str: Generated AI response.
    """

    if not messages:
        raise ValueError("Messages cannot be empty.")

    try:
        llm = get_llm()

        # Send messages to the Groq model
        response = llm.invoke(messages)

        return extract_text(response.content)

    except Exception as error:
        raise RuntimeError(
            f"Failed to generate AI response: {error}"
        ) from error


def stream_response(
    messages: Sequence[BaseMessage]
) -> Iterator[str]:
    """
    Stream the Groq response piece by piece.

    Args:
        messages: Structured LangChain messages.

    Yields:
        str: Individual text chunks from the AI.
    """

    if not messages:
        raise ValueError("Messages cannot be empty.")

    try:
        llm = get_llm()

        # Stream response chunks from Groq
        for chunk in llm.stream(messages):

            text_chunk = extract_text(chunk.content)

            if text_chunk:
                yield text_chunk

    except Exception as error:
        raise RuntimeError(
            f"Failed to stream AI response: {error}"
        ) from error


def extract_text(content) -> str:
    """
    Extract readable text from LangChain message content.

    Some models return plain strings, while others
    may return structured content blocks.
    """

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for block in content:

            if isinstance(block, str):
                text_parts.append(block)

            elif isinstance(block, dict):
                if block.get("type") == "text":
                    text_parts.append(
                        block.get("text", "")
                    )

        return "".join(text_parts)

    return ""
