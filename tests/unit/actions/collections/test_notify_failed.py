"""Test the notify_failed method in collections action."""

from unittest.mock import MagicMock  # pylint: disable=preferred-module
from unittest.mock import patch  # pylint: disable=preferred-module

from ansible_navigator.actions.collections import Action


def test_notify_failed_in_stdout_mode() -> None:
    """Test that notify_failed doesn't crash in stdout mode when _interaction is not set.

    This tests the fix for the AttributeError that occurred when trying to access
    _interaction.ui.show_form() in stdout mode.
    """
    # Create minimal args mock with mode set to stdout
    args = MagicMock()
    args.mode = "stdout"
    action = Action(args=args)

    # Ensure _interaction is not set (not in stdout mode)
    assert not hasattr(action, "_interaction")

    # Expected AttributesError
    with patch.object(action._logger, "error") as mock_logger:
        action.notify_failed()

        assert mock_logger.call_count > 0
        logged_messages = [call[0][0] for call in mock_logger.call_args_list]
        assert any("Something went really wrong" in msg for msg in logged_messages)
        assert any("log file" in msg for msg in logged_messages)


def test_notify_failed_in_interactive_mode() -> None:
    """Test that notify_failed works correctly in interactive mode with _interaction set."""
    args = MagicMock()
    args.mode = "interactive"
    action = Action(args=args)

    mock_interaction = MagicMock()
    mock_ui = MagicMock()
    mock_interaction.ui = mock_ui
    action._interaction = mock_interaction

    action.notify_failed()

    # Verify that show_form was called
    mock_ui.show_form.assert_called_once()
