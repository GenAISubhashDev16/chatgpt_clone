
from typing import Iterator

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    BaseMessage
)

from database.chat_repository import (
    create_chat,
    get_all_chats,
    get_chat_by_id,
    update_chat_title,
    save_message,
    get_messages,
    delete_chat
)

from services.prompt_service import format_chat_prompt

from services.llm_service import (
    generate_response,
    stream_response
)


# Maximum number of previous messages sent to the LLM
MAX_HISTORY_MESSAGES = 20


def create_new_chat(title: str = "New Chat") -> str:
    """
    Create a new conversation.

    Args:
        title: Initial conversation title.

    Returns:
        str: Unique conversation ID.
    """
    return create_chat(title)


def get_recent_chats() -> list[dict]:
    """
    Retrieve all conversations, ordered by recent activity.
    """
    return get_all_chats()


def get_conversation(chat_id: str) -> dict:
    """
    Retrieve a conversation and all its messages.

    Args:
        chat_id: Unique conversation ID.

    Returns:
        dict: Chat details and message history.

    Raises:
        ValueError: If the conversation does not exist.
    """
    chat = get_chat_by_id(chat_id)

    if chat is None:
        raise ValueError("Conversation not found.")

    messages = get_messages(chat_id)

    return {
        "chat": chat,
        "messages": messages
    }


def convert_to_langchain_messages(
    history: list[dict]
) -> list[BaseMessage]:
    """
    Convert database messages into LangChain messages.

    Args:
        history: Messages retrieved from SQLite.

    Returns:
        list: LangChain HumanMessage and AIMessage objects.
    """
    langchain_messages = []

    for message in history:

        role = message["role"]
        content = message["content"]

        if role == "user":
            langchain_messages.append(
                HumanMessage(content=content)
            )

        elif role == "assistant":
            langchain_messages.append(
                AIMessage(content=content)
            )

        # System messages are not included in conversation history.
        # The system instructions come from prompt_service.py.

    return langchain_messages


def generate_chat_title(user_input: str) -> str:
    """
    Generate a simple conversation title from the first question.

    This does not require an additional LLM API request.
    """
    title = " ".join(user_input.strip().split())

    if len(title) > 40:
        title = title[:37].rstrip() + "..."

    return title or "New Chat"


def prepare_messages(
    chat_id: str,
    user_input: str
) -> list[BaseMessage]:
    """
    Prepare the prompt using previous conversation history.

    The latest user question is added separately to the prompt.
    """

    if not user_input or not user_input.strip():
        raise ValueError("Please enter a valid message.")

    # Retrieve existing conversation history
    history = get_messages(chat_id)

    # Convert database records into LangChain messages
    history = convert_to_langchain_messages(history)

    # Keep only the latest messages to control token usage
    history = history[-MAX_HISTORY_MESSAGES:]

    # Build structured prompt
    messages = format_chat_prompt(
        user_input=user_input.strip(),
        chat_history=history
    )

    return messages


def send_message(
    chat_id: str,
    user_input: str
) -> str:
    """
    Process a user message and return the complete AI response.

    Workflow:
    1. Validate the conversation.
    2. Prepare previous conversation context.
    3. Save the user message.
    4. Generate an AI response.
    5. Save the assistant response.
    """

    chat = get_chat_by_id(chat_id)

    if chat is None:
        raise ValueError("Conversation not found.")

    # Prepare context before saving the new user message
    messages = prepare_messages(chat_id, user_input)

    # Save the user's message
    save_message(
        chat_id=chat_id,
        role="user",
        content=user_input.strip()
    )

    # Set the conversation title from the first question
    if chat["title"] == "New Chat":
        update_chat_title(
            chat_id,
            generate_chat_title(user_input)
        )

    # Generate the AI response
    response = generate_response(messages)

    if not response.strip():
        raise RuntimeError("The AI returned an empty response.")

    # Save the assistant response
    save_message(
        chat_id=chat_id,
        role="assistant",
        content=response
    )

    return response


def stream_message(
    chat_id: str,
    user_input: str
) -> Iterator[str]:
    """
    Process a user message and stream the AI response.

    The completed assistant response is saved after
    the stream finishes successfully.
    """

    chat = get_chat_by_id(chat_id)

    if chat is None:
        raise ValueError("Conversation not found.")

    # Prepare conversation context
    messages = prepare_messages(chat_id, user_input)

    # Save the user's message
    save_message(
        chat_id=chat_id,
        role="user",
        content=user_input.strip()
    )

    # Generate a title from the first question
    if chat["title"] == "New Chat":
        update_chat_title(
            chat_id,
            generate_chat_title(user_input)
        )

    # Collect streamed chunks for database storage
    complete_response = []

    # Stream chunks from the LLM service
    for chunk in stream_response(messages):

        if chunk:
            complete_response.append(chunk)
            yield chunk

    # Save only after the complete stream succeeds
    final_response = "".join(complete_response)

    if not final_response.strip():
        raise RuntimeError("The AI returned an empty response.")

    save_message(
        chat_id=chat_id,
        role="assistant",
        content=final_response
    )


def rename_chat(chat_id: str, new_title: str) -> bool:
    """
    Rename an existing conversation.
    """

    if not new_title or not new_title.strip():
        raise ValueError("Chat title cannot be empty.")

    if get_chat_by_id(chat_id) is None:
        raise ValueError("Conversation not found.")

    return update_chat_title(
        chat_id,
        new_title.strip()
    )


def remove_chat(chat_id: str) -> bool:
    """
    Delete a conversation and its associated messages.
    """

    return delete_chat(chat_id)
