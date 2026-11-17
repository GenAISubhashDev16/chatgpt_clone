
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)


# Define the default behaviour of our AI assistant
SYSTEM_PROMPT = """
You are a helpful, intelligent and professional AI assistant.

Your responsibilities:

1. Answer questions clearly and accurately.
2. Explain technical concepts step by step.
3. Provide practical examples whenever useful.
4. When writing code, use clean and readable programming practices.
5. Explain important parts of the code.
6. Help users debug errors by identifying the root cause.
7. If you are unsure about an answer, be honest.
8. Never invent facts or pretend to have performed actions.
9. Use proper Markdown formatting for readable answers.
10. Maintain context from the previous conversation.

Communication style:

- Be friendly and professional.
- Prefer simple English.
- Use headings and bullet points when appropriate.
- Avoid unnecessary repetition.
- Give detailed explanations when the user requests them.

You are currently operating as a general-purpose AI assistant.
"""


def get_chat_prompt():
    """
    Create and return the LangChain chat prompt template.

    The template contains:
    - System instructions.
    - Previous conversation messages.
    - Current user message.

    Returns:
        ChatPromptTemplate: Structured chat prompt.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),

            # Insert previous conversation messages
            MessagesPlaceholder(
                variable_name="chat_history"
            ),

            # Insert the latest user question
            ("human", "{user_input}")
        ]
    )

    return prompt


def format_chat_prompt(user_input, chat_history=None):
    """
    Format the chat prompt using user input and history.

    Args:
        user_input (str): Latest user question.
        chat_history (list): Previous conversation messages.

    Returns:
        list: Formatted LangChain messages.
    """

    if chat_history is None:
        chat_history = []

    prompt = get_chat_prompt()

    formatted_messages = prompt.format_messages(
        chat_history=chat_history,
        user_input=user_input
    )

    return formatted_messages
