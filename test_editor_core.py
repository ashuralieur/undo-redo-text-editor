import unittest

from editor_core import TwoStackEditor


class TwoStackEditorTests(unittest.TestCase):
    def test_edit_undo_and_redo(self):
        editor = TwoStackEditor("A")
        self.assertTrue(editor.edit("AB"))
        self.assertTrue(editor.edit("ABC"))
        self.assertTrue(editor.undo())
        self.assertEqual(editor.current_text, "AB")
        self.assertTrue(editor.redo())
        self.assertEqual(editor.current_text, "ABC")

    def test_new_edit_clears_redo_history(self):
        editor = TwoStackEditor("A")
        editor.edit("AB")
        editor.undo()
        editor.edit("AX")
        self.assertFalse(editor.redo())

    def test_undo_empty_history(self):
        editor = TwoStackEditor()
        self.assertFalse(editor.undo())
        self.assertFalse(editor.redo())


if __name__ == "__main__":
    unittest.main()
