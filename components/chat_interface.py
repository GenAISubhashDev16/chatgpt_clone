
import streamlit as st

from services.chat_service import (
    get_conversation,
    stream_message,
)

from components.thinking_animation import (
    start_thinking_animation,
    update_thinking_animation,
    complete_thinking_animation,
    fail_thinking_animation,
)


def render_welcome_screen() -> None:
    """
    Display the welcome screen when no conversation is selected.
    """
    st.title("AI Chat Assistant")

    st.markdown(
        """
        ### How can I help you today?

        Ask me anything. I can help with:

        - Python and programming
        - Generative AI and RAG
        - Learning and interview preparation
        - Technical problem solving
        - General questions
        """
    )


def render_chat_history(chat_id: str) -> None:
    """
    Display all previously saved messages for a conversation.
    """
    conversation = get_conversation(chat_id)

    messages = conversation["messages"]

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role not in ("user", "assistant"):
            continue

        with st.chat_message(role):
            st.markdown(content)


def handle_user_message(chat_id: str, user_input: str) -> None:
    """
    Process a user message and display the streamed AI response.
    """
    # Display the user's message immediately.
    with st.chat_message("user"):
        st.markdown(user_input)

    status = start_thinking_animation()

    try:
        # Update progress before requesting the AI response.
        update_thinking_animation(status, "generating")

        # Stream the response so the user sees it as it is generated.
        with st.chat_message("assistant"):
            st.write_stream(
                stream_message(chat_id, user_input)
            )

        # Mark the final stage and complete the progress indicator.
        update_thinking_animation(status, "finishing")
        complete_thinking_animation(status)

    except Exception as error:
        fail_thinking_animation(status)

        st.error(
            f"Unable to generate a response: {error}"
        )

    # Reload the page to display the newly saved messages.
    st.rerun()


def render_chat_interface(chat_id: str | None) -> None:
    """
    Render the main chat interface.

    Args:
        chat_id: The ID of the currently selected conversation.
    """
    if not chat_id:
        render_welcome_screen()
        return

    try:
        # Load and display the existing conversation.
        conversation = get_conversation(chat_id)

        chat = conversation["chat"]

        st.title(chat.get("title") or "AI Chat Assistant")

        render_chat_history(chat_id)

    except ValueError:
        st.error("Conversation not found. Please select another chat.")
        return

    except Exception as error:
        st.error(f"Unable to load conversation: {error}")
        return

    # Chat input stays at the bottom of the conversation.
    user_input = st.chat_input(
        "Message AI Chat Assistant..."
    )

    if user_input and user_input.strip():
        handle_user_message(
            chat_id=chat_id,
            user_input=user_input.strip(),
        )
