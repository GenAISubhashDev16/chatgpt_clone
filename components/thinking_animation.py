
from typing import Any

import streamlit as st


# Available progress stages
THINKING_STAGES = {
    "preparing": {
        "label": "Preparing your request...",
        "message": "Checking your conversation context.",
    },
    "generating": {
        "label": "Generating response...",
        "message": "The AI is preparing a response.",
    },
    "finishing": {
        "label": "Finishing response...",
        "message": "Almost done. Finalizing the response.",
    },
}


def start_thinking_animation() -> Any:
    """
    Start the Streamlit thinking/progress indicator.

    Returns:
        The Streamlit status container so other functions can update it.
    """
    status = st.status(
        THINKING_STAGES["preparing"]["label"],
        expanded=True,
        state="running",
    )

    status.write(THINKING_STAGES["preparing"]["message"])

    return status


def update_thinking_animation(status: Any, stage: str) -> None:
    """
    Update the progress indicator to another stage.

    Args:
        status: The status container returned by start_thinking_animation().
        stage: One of preparing, generating, or finishing.
    """
    if stage not in THINKING_STAGES:
        valid_stages = ", ".join(THINKING_STAGES.keys())
        raise ValueError(
            f"Invalid thinking stage: {stage}. "
            f"Choose one of: {valid_stages}"
        )

    stage_info = THINKING_STAGES[stage]

    status.update(
        label=stage_info["label"],
        state="running",
        expanded=True,
    )

    status.write(stage_info["message"])


def complete_thinking_animation(status: Any) -> None:
    """
    Mark the progress indicator as completed.
    """
    status.update(
        label="Response ready",
        state="complete",
        expanded=False,
    )


def fail_thinking_animation(status: Any) -> None:
    """
    Mark the progress indicator as failed.
    """
    status.update(
        label="Unable to generate response",
        state="error",
        expanded=True,
    )
