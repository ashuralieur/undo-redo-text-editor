"""Two-stack history engine used by the Undo/Redo Text Editor."""


class TwoStackEditor:
    """Stores previous states in undo_stack and reversed states in redo_stack."""

    def __init__(self, initial_text: str = ""):
        self.current_text = initial_text
        self.undo_stack: list[str] = []
        self.redo_stack: list[str] = []

    def edit(self, new_text: str) -> bool:
        """Apply one edit. Returns False when the text did not actually change."""
        if new_text == self.current_text:
            return False
        self.undo_stack.append(self.current_text)
        self.current_text = new_text
        self.redo_stack.clear()
        return True

    def undo(self) -> bool:
        """Restore the most recent prior state, if one exists."""
        if not self.undo_stack:
            return False
        self.redo_stack.append(self.current_text)
        self.current_text = self.undo_stack.pop()
        return True

    def redo(self) -> bool:
        """Reapply the most recently undone state, if one exists."""
        if not self.redo_stack:
            return False
        self.undo_stack.append(self.current_text)
        self.current_text = self.redo_stack.pop()
        return True

    def clear_history(self) -> None:
        self.undo_stack.clear()
        self.redo_stack.clear()
