import unittest
from main import ImageEditor
from PyQt5.QtWidgets import QApplication, QListWidget, QPushButton
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import sys


app = QApplication(sys.argv)


class TestImageEditor(unittest.TestCase):
    def setUp(self):
        self.ImageEditor = ImageEditor()


    def test_save_button(self):
        self.save_button = self.ImageEditor.findChild(QPushButton, "save_button")
        # Check disable when open the app
        self.assertFalse(self.save_button.isEnabled())
        # When clicked and choosen an image
        self.open_button = self.ImageEditor.findChild(QPushButton, "open_button")
        QTest.mouseClick(self.open_button, Qt.LeftButton)
        self.assertTrue(self.save_button.isEnabled())
        # Check save
        QTest.mouseClick(self.save_button, Qt.LeftButton)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)