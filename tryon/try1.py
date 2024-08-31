import pyvista as pv
import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QColorDialog,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QDialog,
)
from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint, QTimer


class DrawingCanvas(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 400)  # Set the size of the canvas
        self.setWindowTitle("Draw on Shirt")
        self.image = QPixmap(self.size())  # Create a blank image
        self.image.fill(Qt.white)  # Fill the canvas with white
        self.last_point = QPoint()  # To track the last point of drawing
        self.drawing = False  # To track whether the user is drawing

        self.parent = parent

    def paintEvent(self, event):
        # Method for painting
        canvas_painter = QPainter(self)
        canvas_painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        # When the mouse button is pressed, start drawing
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.drawing = True

    def mouseMoveEvent(self, event):
        # When the mouse moves, draw lines if drawing is True
        if self.drawing:
            painter = QPainter(self.image)
            pen = QPen(Qt.black, 5, Qt.SolidLine)  # Black pen with 5px width
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

            # Real-time update of drawing on the 3D model
            self.update_texture()

    def mouseReleaseEvent(self, event):
        # Stop drawing when the mouse button is released
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def update_texture(self):
        # Save the current drawing as a temporary image file
        drawing_path = "Resources3d/3d_shirt/real_time_drawing.png"
        self.image.save(drawing_path)

        # Load the saved drawing as a texture in PyVista
        if self.parent is not None:
            texture = pv.read_texture(drawing_path)
            self.parent.update_texture(texture)

    def save_drawing(self, file_path):
        # Save the current drawing as an image
        self.image.save(file_path)


class ShirtCustomizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screenshot_count = 1  # Counter for screenshot filenames
        self.initUI()

    def initUI(self):
        self.setWindowTitle("3D Shirt Customizer")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        # Color selection button
        self.color_btn = QPushButton("Select Shirt Color", self)
        self.color_btn.clicked.connect(self.select_color)
        self.layout.addWidget(self.color_btn)

        # Drawing button
        self.draw_btn = QPushButton("Draw on Shirt", self)
        self.draw_btn.clicked.connect(self.draw_on_shirt)
        self.layout.addWidget(self.draw_btn)

        # Image overlay button
        self.img_btn = QPushButton("Overlay Image", self)
        self.img_btn.clicked.connect(self.overlay_image)
        self.layout.addWidget(self.img_btn)

        # Screenshot button
        self.screenshot_btn = QPushButton("Take Screenshot", self)
        self.screenshot_btn.clicked.connect(self.take_screenshot)
        self.layout.addWidget(self.screenshot_btn)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            # Convert the QColor to RGB values and scale from 0-255 to 0-1
            r = color.red() / 255.0
            g = color.green() / 255.0
            b = color.blue() / 255.0
            selected_color = (r, g, b)

            # Set the selected color to the 3D model in PyVista
            mesh_actor.GetProperty().SetColor(selected_color)
            plotter.render()

    def draw_on_shirt(self):
        # Open the drawing canvas and allow drawing in a separate dialog
        self.canvas = DrawingCanvas(self)
        self.canvas.setModal(False)  # Non-blocking dialog box
        self.canvas.show()

        # Real-time update with QTimer to avoid blocking
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.canvas.update_texture)
        self.timer.start(100)  # Update every 100 ms for smoother real-time updates

    def update_texture(self, texture):
        # Update the texture on the 3D shirt model
        mesh_actor.SetTexture(texture)
        plotter.render()

    def overlay_image(self):
        # Load an image file and map it onto the shirt
        image_path = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)"
        )[0]
        if image_path:
            # Load the texture from the image
            texture = pv.read_texture(image_path)

            # Ensure texture coordinates are applied correctly
            if (
                shirt_model.point_data.active_texture_coordinates is None
                or shirt_model.point_data.active_texture_coordinates.size == 0
            ):
                shirt_model.texture_map_to_plane(inplace=True)

            # Apply the texture to the shirt mesh
            mesh_actor.SetTexture(texture)
            plotter.render()

    def take_screenshot(self):
        # Directory to store screenshots
        screenshot_dir = "Resources3d/3d_shirt/"
        os.makedirs(screenshot_dir, exist_ok=True)  # Ensure directory exists

        # Create the file path using the screenshot count
        screenshot_path = os.path.join(screenshot_dir, f"{self.screenshot_count}.png")

        # Increment the screenshot count for the next image
        self.screenshot_count += 1

        # Take a screenshot with a transparent background
        plotter.screenshot(screenshot_path, transparent_background=True)

        print(f"Screenshot saved to {screenshot_path}")


# PyVista plotter setup
shirt_model = pv.read(
    "Resources3d/Shirts/3dshirt.obj"
)  # Path to your 3D shirt model file
plotter = pv.Plotter(window_size=[1280, 720])
mesh_actor = plotter.add_mesh(shirt_model, color="lightblue", opacity=1)

# Set plotter background to transparent (it will be transparent in the screenshot)
plotter.set_background(
    "white"
)  # For viewing in the window, but saved with transparent background


def main_loop():
    app = QApplication(sys.argv)
    customizer = ShirtCustomizer()
    customizer.show()
    plotter.show(auto_close=False)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main_loop()
