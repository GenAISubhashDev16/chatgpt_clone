
import uuid
from datetime import datetime, timezone

from database.db import get_db_connection


def get_current_timestamp():
    """
    Return the current UTC timestamp in ISO format.
    """
    return datetime.now(timezone.utc).isoformat()


def create_chat(title="New Chat"):
    """
    Create a new conversation.

    Args:
        title: Conversation title.

    Returns:
        str: Unique chat ID.
    """
    chat_id = str(uuid.uuid4())
    timestamp = get_current_timestamp()

    with get_db_connection() as connection:

        connection.execute(
            """
            INSERT INTO chats (
                id,
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (chat_id, title, timestamp, timestamp)
        )

    return chat_id


def get_all_chats():
    """
    Retrieve all conversations.

    Most recently updated conversations appear first.
    """
    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            SELECT id, title, created_at, updated_at
            FROM chats
            ORDER BY updated_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]


def get_chat_by_id(chat_id):
    """
    Retrieve one conversation using its unique ID.
    """
    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            SELECT *
            FROM chats
            WHERE id = ?
            """,
            (chat_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None


def update_chat_title(chat_id, title):
    """
    Update the conversation title.
    """
    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            UPDATE chats
            SET title = ?, updated_at = ?
            WHERE id = ?
            """,
            (title, get_current_timestamp(), chat_id)
        )

        return cursor.rowcount > 0


def update_chat_timestamp(chat_id):
    """
    Update the last activity timestamp of a conversation.
    """
    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            UPDATE chats
            SET updated_at = ?
            WHERE id = ?
            """,
            (get_current_timestamp(), chat_id)
        )

        return cursor.rowcount > 0


def save_message(chat_id, role, content):
    """
    Save a message inside an existing conversation.

    Args:
        chat_id: Unique conversation ID.
        role: user, assistant, or system.
        content: Message text.

    Returns:
        int: Newly created message ID.
    """
    if role not in ("user", "assistant", "system"):
        raise ValueError("Invalid message role.")

    if not content or not content.strip():
        raise ValueError("Message content cannot be empty.")

    timestamp = get_current_timestamp()

    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO messages (
                chat_id,
                role,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (chat_id, role, content, timestamp)
        )

        message_id = cursor.lastrowid

        # Update conversation activity
        connection.execute(
            """
            UPDATE chats
            SET updated_at = ?
            WHERE id = ?
            """,
            (timestamp, chat_id)
        )

        return message_id


def get_messages(chat_id):
    """
    Retrieve all messages for a conversation.

    Messages are returned in chronological order.
    """
    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            SELECT id, chat_id, role, content, created_at
            FROM messages
            WHERE chat_id = ?
            ORDER BY id ASC
            """,
            (chat_id,)
        )

        return [dict(row) for row in cursor.fetchall()]


def delete_chat(chat_id):
    """
    Delete a conversation.

    Its messages are automatically deleted through
    the ON DELETE CASCADE foreign key constraint.
    """
    with get_db_connection() as connection:

        cursor = connection.execute(
            """
            DELETE FROM chats
            WHERE id = ?
            """,
            (chat_id,)
        )

        return cursor.rowcount > 0
