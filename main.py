from PyQt5.QtWidgets import QMessageBox, QFileDialog, QLineEdit,  QVBoxLayout, QSlider, QHBoxLayout, QLabel, QWidget, QApplication, QPushButton
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QRect
import os
import time


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
        self.current_image_index = -1
        # For file extensions of an image
        self.file_extension = ""


        # Widgets
        # Main v layout
        self.main_layout = QVBoxLayout()
        # Save, open etc buttons
        self.btn_main_layout = QHBoxLayout()
        # Sliders
        self.sliders_layout = QHBoxLayout()
        # Image layout
        self.image_layout = QHBoxLayout()

        # Buttons
        # Open btn
        self.open_btn = QPushButton("Open image")
        # connect open btn to opem_image fucntion
        self.open_btn.clicked.connect(self.open_image)
        self.open_btn.setObjectName("open_button")
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

        # Save button
        self.save_btn  = QPushButton("Save")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setObjectName("save_button")

        # Change to gray button
        self.gray_change = QPushButton("Gray")
        self.gray_change.clicked.connect(self.change_to_gray)
        # Image is not opened
        self.gray_change.setEnabled(False)

        # Blur button
        self.blur_change = QPushButton("Blur")
        self.blur_change.clicked.connect(self.blur_image)
        # Image is not opened
        self.blur_change.setEnabled(False)

        # Resolution increase button
        self.resolution_btn = QPushButton("Quality")
        self.resolution_btn.clicked.connect(self.higher_resolution)
        self.resolution_btn.setEnabled(False)

        # Flip horizontally
        self.flip_h = QPushButton("FlipH")
        self.flip_h.clicked.connect(self.flip_horizontal)
        self.flip_h.setEnabled(False)

        # Flip vertically
        self.flip_v = QPushButton("FlipV")
        self.flip_v.clicked.connect(self.flip_vertical)
        self.flip_v.setEnabled(False)

        # Resize an image button
        self.resize_button = QPushButton("Resize")
        self.resize_button.clicked.connect(self.resize_image)
        self.resize_button.setEnabled(False)

        # Crop image button
        self.crop_button = QPushButton("Crop")
        self.crop_button.clicked.connect(self.crop_image)
        self.crop_button.setEnabled(False)

        # Change weight and height text
        self.weight_size_label = QLabel("Weight")
        self.weight_size_label.setVisible(False)
        self.weight_size = QLineEdit()
        self.weight_size.setVisible(False)
        self.height_size_label = QLabel("Height")
        self.height_size_label.setVisible(False)
        self.height_size = QLineEdit()
        self.height_size.setVisible(False)
        self.resize_btn_in_function = QPushButton("Resize")
        self.resize_btn_in_function.setVisible(False)
        # When done clicked make other buttons enabled
        self.resize_done_btn = QPushButton("Done")
        self.resize_done_btn.setVisible(False)
        self.resize_done_btn.clicked.connect(self.resize_done)

        # Buttons for back and next images in images list
        self.previous_image = QPushButton("Previous")
        self.previous_image.clicked.connect(self.show_previous_image)
        self.previous_image.setEnabled(False)
        self.next_image = QPushButton("Next")
        self.next_image.clicked.connect(self.show_next_image)
        self.next_image.setEnabled(False)

        # Put widgets into btn layout
        self.btn_main_layout.addWidget(self.open_btn, alignment=Qt.AlignTop)
        self.btn_main_layout.addWidget(self.save_btn)
        self.btn_main_layout.addWidget(self.gray_change)
        self.btn_main_layout.addWidget(self.blur_change)
        self.btn_main_layout.addWidget(self.resolution_btn)
        self.btn_main_layout.addWidget(self.flip_h)
        self.btn_main_layout.addWidget(self.flip_v)
        self.btn_main_layout.addWidget(self.resize_button)
        self.btn_main_layout.addWidget(self.crop_button)
        self.btn_main_layout.addWidget(self.previous_image)
        self.btn_main_layout.addWidget(self.next_image)
        self.btn_main_layout.setAlignment(Qt.AlignLeft)

        # for resize button
        self.sliders_layout.addWidget(self.weight_size_label)
        self.sliders_layout.addWidget(self.weight_size)
        self.sliders_layout.addWidget(self.height_size_label)
        self.sliders_layout.addWidget(self.height_size)
        self.sliders_layout.addWidget(self.resize_btn_in_function)
        self.sliders_layout.addWidget(self.resize_done_btn)

        # Selecting to crop
        self.selecting_crop = False
        self.selecting_area_crop = None

        # Image show
        self.image_field = QLabel()

        # Add image into image layout
        self.image_layout.addWidget(self.image_field)

        # Show all layout
        self.main_layout.addLayout(self.btn_main_layout, 20)
        self.main_layout.addLayout(self.sliders_layout, 10)
        self.main_layout.addLayout(self.image_layout, 70)
        self.setLayout(self.main_layout)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.selecting_crop = True
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.selecting_crop:
            self.end_pos = event.pos()
            self.selecting_area_crop = QRect(self.start_pos, self.end_pos)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.selecting_crop = False


    def paintEvent(self, event):
        painter = QPainter(self)
        if self.selecting_area_crop:
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.setOpacity(0.4)
            painter.setBrush(Qt.gray)
            painter.drawRect(self.selecting_area_crop)

    def make_all_btns_true(self):
        # Makes all buttons editable true
        self.gray_change.setEnabled(True)
        self.blur_change.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.resolution_btn.setEnabled(True)
        self.flip_h.setEnabled(True)
        self.flip_v.setEnabled(True)
        self.resize_button.setEnabled(True)
        self.crop_button.setEnabled(True)

    def make_all_btns_false(self):
        # Makes all buttons editable false
        self.gray_change.setEnabled(False)
        self.blur_change.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.resolution_btn.setEnabled(False)
        self.flip_h.setEnabled(False)
        self.flip_v.setEnabled(False)
        self.resize_button.setEnabled(False)
        self.crop_button.setEnabled(False)

    def make_resize_label_btn_visible(self):
        """Show the resize buttons and labels"""
        self.weight_size_label.setVisible(True)
        self.weight_size.setVisible(True)
        self.height_size_label.setVisible(True)
        self.height_size.setVisible(True)
        self.resize_btn_in_function.setVisible(True)
        self.resize_done_btn.setVisible(True)

    def make_resize_label_btn_not_visible(self):
        """Hide the resize buttons and labels"""
        self.weight_size_label.setVisible(False)
        self.weight_size.setVisible(False)
        self.height_size_label.setVisible(False)
        self.height_size.setVisible(False)
        self.resize_btn_in_function.setVisible(False)
        self.resize_done_btn.setVisible(False)



    def open_image(self):
        """For opening images"""
        try:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            if filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                # Save file like image
                image = Image.open(filename)
                # create folder images for saving them there
                #os.mkdir("images")
                # Find extensions, save extension for the image for all changes
                self.file_extension = os.path.splitext(filename)[1]
                # New name
                new_filename = f"images/org{self.file_extension}"
                # Save in images folder, (*occupies some space)
                image.save(new_filename)
                # Add into images list for return back
                self.images.append(new_filename)
                # Show image
                self.load_image(new_filename)
                # When image is selected, you can change it
                self.make_all_btns_true()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open a file: {str(e)}")

    def save_image(self):
        """Save the image"""
        try:
            pixmap = QPixmap(self.images[self.current_image_index])
            if not pixmap.isNull():
                filename, _ = QFileDialog.getSaveFileName(self, "Open Image", f"my_image{self.file_extension}", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
                if filename:
                    pixmap.save(filename)
                    QMessageBox.information(self, "Success", "Image was saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open a file: {str(e)}")


    def load_image(self, new_filename):
        """Load an edited image on the screen"""
        pixmap = QPixmap(new_filename)
        print(self.images)
        # Scale to ration of the screen
        self.image_field.setPixmap(pixmap.scaled(self.image_field.size(), aspectRatioMode=True))
        # Align center
        self.image_field.setAlignment(Qt.AlignCenter)
        self.image_field.adjustSize()

        # (!!!!!!!!!!!!!!!! Change because can be a problem with index)
        print("Length images", len(self.images))
        # Only if we have not last image
        if self.current_image_index < -1:
            self.next_image.setEnabled(True)
        else:
            self.next_image.setEnabled(False)
        # If we have more length than 1 item in the list and not overwhelm the list itself
        if len(self.images) > 1 and abs(self.current_image_index) <= len(self.images) - 1:
            self.previous_image.setEnabled(True)
        else:
            self.previous_image.setEnabled(False)
        # save memory
        self.clear_images()
        print("Index", self.current_image_index)

    def crop_image(self):
        try:
            if self.selecting_area_crop:
                image = Image.open(self.images[self.current_image_index])
                # Click make others button disabled!!!!!!!!!!!!!!!!!
                image_cropped = image.crop((self.start_pos.x()*2, self.start_pos.y()*2, self.end_pos.x()*2, self.end_pos.y()*2))
                print((self.start_pos.x()//2, self.start_pos.y()//2, self.end_pos.x()//2, self.end_pos.y()//2))

                new_filename = f"images/crop{self.file_extension}"
                image_cropped.save(new_filename)
                # Add into images list for return back
                # Add during changes only one element resize
                if len(self.images) > 1:
                    self.images[-1] = new_filename
                else:
                    self.images.append(new_filename)

                # Set current index = -1, the last editing
                self.current_image_index = -1
                # Show image
                self.load_image(new_filename)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def resize_image(self):
        try:
            self.image_resized = Image.open(self.images[self.current_image_index])
            # Clicked resize main btn
            self.make_resize_label_btn_visible()
            # Make main buttons disabled
            self.make_all_btns_false()

            self.weight_size.setText(str(self.image_resized.width))
            self.height_size.setText(str(self.image_resized.height))
            self.resize_btn_in_function.clicked.connect(self.save_resized_image)


        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def resize_done(self):
        # When you're done resize the image click done and hide the labels and btn and show main buttons
        self.make_all_btns_true()
        self.make_resize_label_btn_not_visible()

    def save_resized_image(self):
        """Mini resize button's function"""
        new_width = int(self.weight_size.text())
        new_height = int(self.height_size.text())

        # Resize the image
        new_image = self.image_resized.resize((new_width, new_height))
        # New name
        new_filename = f"images/resize{self.file_extension}"
        new_image.save(new_filename)
        # Add into images list for return back
        # Add during changes only one element resize
        self.images[-1] = new_filename
        # Set current index = -1, the last editing
        self.current_image_index = -1
        # Show image
        self.load_image(new_filename)

    def clear_images(self):
        """Clear self.images in order to save memory, if the length more or equal to 20 (!!!!!!!!!Find better solution)"""
        if len(self.images) >= 20:
            print("Clear memory")
            self.images.pop(0)


    def show_previous_image(self):
        """-1 means show -2, -3 in the list"""
        self.current_image_index -= 1
        self.load_image(self.images[self.current_image_index])


    def show_next_image(self):
        """1 means show 0, 1 in the list"""
        self.current_image_index += 1
        self.load_image(self.images[self.current_image_index])

    def higher_resolution(self):
        """Increase the image resolution(quality)"""
        try:
            image = Image.open(self.images[self.current_image_index])
            width, height = image.size
            if width < 2000 and height < 2000:
                new_width = width * 2
                new_height = height * 2
                print(new_width, new_height)
                new_image = image.resize((new_width, new_height), Image.LANCZOS)
                # New name
                new_filename = f"images/resol{self.file_extension}"
                new_image.save(new_filename)
                # Add into images list for return back
                self.images.append(new_filename)
                # Set current index = -1, the last editing
                self.current_image_index = -1
                # Show image
                self.load_image(new_filename)
                self.resolution_btn.setEnabled(True)
            else:
                self.resolution_btn.setEnabled(False)
                QMessageBox.warning(self, "Warning", "The resolution is already high!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def change_to_gray(self):
        """Change image into gray color"""
        try:
            # Change into an image pillow
            image = Image.open(self.images[self.current_image_index])
            # Change the image
            gray_image = image.convert("L")
            # New name
            new_filename = f"images/gray{self.file_extension}"
            # Save the image
            gray_image.save(new_filename)
            # Add into images list for return back
            self.images.append(new_filename)
            # Set current index = -1, the last editing
            self.current_image_index = -1
            # Show image
            self.load_image(new_filename)
            # Disable the button
            #self.gray_change.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def blur_image(self):
        """Blur image"""
        try:
            # Change into an image pillow
            image = Image.open(self.images[self.current_image_index])
            # Change the image
            gray_image = image.filter(ImageFilter.BLUR)
            # New name
            new_filename = f"images/blur{self.file_extension}"
            # Save the image
            gray_image.save(new_filename)
            # Add into images list for return back
            self.images.append(new_filename)
            # Set current index = -1, the last editing
            self.current_image_index = -1
            # Show image
            self.load_image(new_filename)
            # disable the button
            self.blur_change.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def flip_horizontal(self):
        try:
            # Open last image
            image = Image.open(self.images[self.current_image_index])
            flip_image = image.transpose(Image.FLIP_LEFT_RIGHT)
            # New name
            new_filename = f"images/fliph{self.file_extension}"
            # Save the image
            flip_image.save(new_filename)
            # Add into images list for return back
            self.images.append(new_filename)
            # Set current index = -1, the last editing
            self.current_image_index = -1
            # Show image
            self.load_image(new_filename)
            # disable the button
            #self.flip_h.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def flip_vertical(self):
        try:
            # Open last image
            image = Image.open(self.images[self.current_image_index])
            flip_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            # New name
            new_filename = f"images/flipv{self.file_extension}"
            # Save the image
            flip_image.save(new_filename)
            # Add into images list for return back
            self.images.append(new_filename)
            # Set current index = -1, the last editing
            self.current_image_index = -1
            # Show image
            self.load_image(new_filename)
            # disable the button
            # self.flip_h.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")



if __name__ == "__main__":
    app = QApplication([])
    main = ImageEditor()
    main.show()
    app.exec_()

