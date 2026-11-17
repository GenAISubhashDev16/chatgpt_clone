
import streamlit as st

from config.settings import APP_NAME, APP_VERSION
from database.db import create_tables

from components.sidebar import render_sidebar
from components.chat_interface import render_chat_interface


def initialize_application() -> None:
    """
    Initialize the database and application session state.
    """

    # Create database tables if they do not exist.
    create_tables()

    # Initialize the active conversation.
    if "active_chat_id" not in st.session_state:
        st.session_state["active_chat_id"] = None


def configure_page() -> None:
    """
    Configure Streamlit page settings.
    """

    st.set_page_config(
        page_title=APP_NAME,
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def main() -> None:
    """
    Main application entry point.
    """

    # Configure the page before rendering other Streamlit elements.
    configure_page()

    # Initialize database and session state.
    initialize_application()

    # Render the sidebar and get the selected conversation ID.
    active_chat_id = render_sidebar()

    # Render the main chat interface.
    render_chat_interface(active_chat_id)

    # Application footer.
    st.sidebar.divider()

    st.sidebar.caption(
        f"{APP_NAME} v{APP_VERSION}"
    )


if __name__ == "__main__":
    main()
