from PyQt5.QtWidgets import QMessageBox, QFileDialog,  QVBoxLayout, QHBoxLayout, QLabel, QWidget, QApplication, QPushButton
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

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
        # Current image to change
        self.current_image = ""


        # Widgets
        # Main v layout
        self.main_layout = QVBoxLayout()
        # Save, open etc buttons
        self.btn_main_layout = QHBoxLayout()
        # Image layout
        self.image_layout = QHBoxLayout()

        # Buttons
        # Open btn
        self.open_btn = QPushButton("Open image")
        # connect open btn to opem_image fucntion
        self.open_btn.clicked.connect(self.open_image)
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

        # Image show
        self.image_field = QLabel()

        # Add image into image layout
        self.image_layout.addWidget(self.image_field)

        # Show all layout
        self.main_layout.addLayout(self.btn_main_layout, 20)
        self.main_layout.addLayout(self.image_layout, 80)
        self.setLayout(self.main_layout)

    def open_image(self):
        """For opening images"""
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            if filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                # Save file like image
                image = Image.open(filename)
                # Find extensions
                file_extension = os.path.splitext(filename)[1]
                # New name
                new_filename = f"images/org{file_extension}"
                # Save in images folder, (*occupies some space)
                image.save(new_filename)
                # Show image
                self.load_image(new_filename)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open a file: {e}")

    def load_image(self, new_filename):
        """Load an edited image on the screen"""
        pixmap = QPixmap(new_filename)
        # Add into images list for return back
        self.images.append(new_filename)
        print(self.images)
        # Scale to ration of the screen
        self.image_field.setPixmap(pixmap.scaled(self.image_field.size(), aspectRatioMode=True))
        # Align center
        self.image_field.setAlignment(Qt.AlignCenter)
        self.image_field.adjustSize()


if __name__ == "__main__":
    app = QApplication([])
    main = ImageEditor()
    main.show()
    app.exec_()
