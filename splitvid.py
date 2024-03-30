import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QGraphicsView
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from gui import Ui_MainWindow  # Import the generated UI class
import os
import pickle
import subprocess
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget
import geopandas as gpd
       
            
class YourApplication(QMainWindow, Ui_MainWindow):
    def __init__(self, data = None):
        super().__init__()
        self.setupUi(self)  # Set up the UI from the generated code
        ## Setup the button clicks\
        self.selected_geojson_path = None
        self.selected_video_path = None
        self.init_ui()
        self.scrollLayout = QVBoxLayout()  # Create a QVBoxLayout to hold all the widgets
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)  # Set the QVBoxLayout as the layout for the scroll area

       
        
        
        
    def init_ui(self):
        """Initialize all of the buttons and other elements"""
        self.readMatchButton.setEnabled(False)
        self.calcGeomButton.setEnabled(False)
        self.splitFilesButton.setEnabled(False)
        self.readGeojsonButton.clicked.connect(self.select_folder)
        self.readVidsButton.clicked.connect(self.select_folder_2)
        self.readMatchButton.clicked.connect(self.read_match_files)
        
    
    def read_match_files(self):
        ###Check if video path and geojson path has been selected
        ### Loop through the geojson folder location and create_details_tables based on it
        ###Populate the scrollArea
        if self.selected_geojson_path and self.selected_video_path:
            for serialnumber, filename in enumerate(os.listdir(self.selected_geojson_path)):
                if filename.endswith('.geojson'):
                    file_path = os.path.join(self.selected_geojson_path, filename)
                    length= self.get_length_in_meters(file_path)
                    self.create_details_table(str(serialnumber+1), str(file_path), str(length.round(2)))
        else:
            self.show_message_box('Unable to Process data', "Make sure the geojson folder path and the video folder path are selected first")
        
        
    def get_length_in_meters(self, filepath):
        gdf= gpd.read_file(filepath)
        if not gdf.empty and ('LineString' in gdf.geom_type.unique() or 'MultiLineString' in gdf.geom_type.unique()):
            # Set CRS to WGS84 if not already set
            if gdf.crs is None:
                gdf.crs = 'epsg:4326'  # WGS84

            # Reproject CRS to EPSG 32361
            gdf = gdf.to_crs(epsg=32631)

            # Calculate the length of all LineString and MultiLineString geometries and sum them up
            total_length = gdf.geometry.length.sum()

            return total_length

        
        
    
    ## Def functions
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            self.selectGeojsonLineEdit.setText(folder_path)
            self.selected_geojson_path = folder_path
            
            if self.selected_video_path and self.selected_geojson_path:
                self.readMatchButton.setEnabled(True)

            
    def select_folder_2(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            self.readVidsLineEdit.setText(folder_path)
            self.selected_video_path = folder_path
            
            if self.selected_video_path and self.selected_geojson_path:
                self.readMatchButton.setEnabled(True)
                
    def get_video_length(self, video_path):
        ## Function to get the video length... TAIWOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        pass
                
    def create_details_table(self, sn, filepath, length):
        # Create main layout
        main_layout = QHBoxLayout()

        # Create Col_1 with numbers
        col_1_layout = QVBoxLayout()
        label_col_1 = QLabel(str(sn))
        label_col_1.setFixedWidth(100)
        col_1_layout.addWidget(label_col_1)
        # Add your numbers widgets here
        main_layout.addLayout(col_1_layout)

        # Create Col_2 with four rows
        col_2_layout = QVBoxLayout()
        # Row 1
        row_1_layout = QVBoxLayout()
        row_1_layout.addWidget(QLabel(f"Geojson Filename: \t {filepath}"))
        col_2_layout.addLayout(row_1_layout)
        # Row 2
        row_2_layout = QHBoxLayout()
        row_2_layout.addWidget(QLabel("Vid Path: path_to_file"))
        row_2_layout.addWidget(QLabel("Vid Length: 30:50"))
        col_2_layout.addLayout(row_2_layout)
        # Row 3
        row_3_layout = QVBoxLayout()
        row_3_layout.addWidget(QLabel("Output File Dir: \t path_to_folder"))
        col_2_layout.addLayout(row_3_layout)
        # Row 4
        row_4_layout = QHBoxLayout()
        row_4_layout.addWidget(QLabel(f"{length}m"))
        row_4_layout.addWidget(QLabel("vvcol_2"))
        row_4_layout.addWidget(QLabel("vvcol_3"))
        col_2_layout.addLayout(row_4_layout)

        main_layout.addLayout(col_2_layout)

        # Create Col_3 for map
        col_3_layout = QVBoxLayout()
        col_3_layout.addWidget(QLabel("Col_3: Map Display"))
        # Add your map widget here
        main_layout.addLayout(col_3_layout)

        # Create a widget to contain the main layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        
        main_widget.setStyleSheet("border: 1px solid rgb(0, 85, 255)")
        scroll_area_width = self.scrollArea.width()
        
        main_widget.setFixedSize(scroll_area_width-20, 250)  # Set your desired width and height

        # Set the alignment of scrollLayout to top
        self.scrollLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Set the main widget as the widget for the scroll area
        self.scrollLayout.addWidget(main_widget)

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
        
def main():
    app = QApplication(sys.argv)
    window = YourApplication()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()