
import streamlit as st

from services.chat_service import (
    create_new_chat,
    get_recent_chats,
)


def render_sidebar() -> str | None:
    """
    Render the ChatGPT-style sidebar.

    Returns:
        The ID of the currently active chat, or None.
    """

    # Initialize the active chat ID in Streamlit session state.
    if "active_chat_id" not in st.session_state:
        st.session_state["active_chat_id"] = None

    sidebar = st.sidebar

    # Sidebar heading
    sidebar.title("AI Chat Assistant")

    # Create a new conversation.
    if sidebar.button(
        "＋ New Chat",
        key="new_chat_button",
        use_container_width=True,
        type="primary",
    ):
        new_chat_id = create_new_chat()

        st.session_state["active_chat_id"] = new_chat_id

        # Refresh the application to display the new conversation.
        st.rerun()

        return new_chat_id

    sidebar.divider()

    # Conversation history heading
    sidebar.subheader("Chat History")

    # Load saved conversations from SQLite.
    chats = get_recent_chats()

    if not chats:
        sidebar.caption("No conversations yet. Start a new chat!")
        return st.session_state["active_chat_id"]

    # Display each saved conversation.
    for chat in chats:
        chat_id = chat["id"]
        chat_title = chat.get("title") or "New Chat"

        is_active = (
            st.session_state["active_chat_id"] == chat_id
        )

        button_type = "primary" if is_active else "secondary"

        if sidebar.button(
            chat_title,
            key=f"chat_{chat_id}",
            use_container_width=True,
            type=button_type,
        ):
            st.session_state["active_chat_id"] = chat_id

            # Refresh the application to load the selected conversation.
            st.rerun()

            return chat_id

    return st.session_state["active_chat_id"]
