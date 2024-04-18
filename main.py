from PyQt5.QtWidgets import QMessageBox, QFileDialog,  QVBoxLayout, QHBoxLayout, QLabel, QWidget, QApplication, QPushButton
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageEditor(QWidget):
    """Program for editing images"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 800, 800)

        self.initUI()

    def initUI(self):
        """Main widgets and styles"""
        # Original image save
        self.original_image = ""
        # all images links to previous image
        self.images = []


        # Widgets
        # Main v layout
        self.main_layout = QVBoxLayout()
        # Save, open etc buttons
        self.btn_main_layout = QHBoxLayout()
        # Image layout
        self.image_layout = QHBoxLayout()

        # Buttons
        self.open_btn = QPushButton("Open image")
        self.open_btn.style()
        self.open_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #007bff;" 
            "   color: #ffffff;"  
            "   padding: 10px 20px;"  
            "   margin: 0;"  
            "   border: 2px solid #007bff;" 
            "   border-radius: 5px;" 
            "   font-family: Arial;"          
            "   font-size: 20px;"            
            "   font-weight: bold;"           
            "}"
            "QPushButton:hover {"
            "   background-color: #0056b3;"  
            "   border: 2px solid #0056b3;" 
            "}"
        )

        # Put widgets into btn layout
        self.btn_main_layout.addWidget(self.open_btn, alignment=Qt.AlignTop)
        self.btn_main_layout.setAlignment(Qt.AlignLeft)

        # Show all layout
        self.main_layout.addLayout(self.btn_main_layout)
        self.main_layout.addLayout(self.image_layout)
        self.setLayout(self.main_layout)


if __name__ == "__main__":
    app = QApplication([])
    main = ImageEditor()
    main.show()
    app.exec_()
