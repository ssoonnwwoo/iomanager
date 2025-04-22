from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from event.io_event_handler import select_directory
from tools.export_metadata import export_metadata

import os
import pandas as pd

class IOManagerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IO Manager Prototype")

        # Widgets
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        shot_select_container = QHBoxLayout()
        file_path_label = QLabel("File path:")
        self.file_path_le = QLineEdit()
        self.file_path_le.setPlaceholderText("Input your shot path")
        shot_select_btn = QPushButton("Select")
        shot_load_btn = QPushButton("Load")

        self.table = QTableWidget()

        # Event Handle
        shot_select_btn.clicked.connect(
            lambda: select_directory(self.file_path_le)
        )
        shot_load_btn.clicked.connect(self.on_load_clicked)

        # Layout
        shot_select_container.addWidget(file_path_label)
        shot_select_container.addWidget(self.file_path_le)
        shot_select_container.addWidget(shot_select_btn)
        shot_select_container.addWidget(shot_load_btn)

        main_layout.addLayout(shot_select_container)
        main_layout.addWidget(self.table)

        central_widget.setLayout(main_layout)

    def on_load_clicked(self):
        csv_path = export_metadata(self.file_path_le.text())
        if csv_path:
            self.update_table(csv_path)
    
    def update_table(self, csv_path):
        df = pd.read_csv(csv_path)

        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())

        for row_idx, row_data in df.iterrows():
            for col_idx, header in enumerate(df.columns):
                value = row_data[header]

                # NaN 처리
                if pd.isna(value):
                    value = ""

                # 썸네일 처리
                if header == "thumbnail" and isinstance(value, str) and os.path.exists(value):
                    self._set_thumbnail_cell(row_idx, col_idx, value)
                else:
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_idx, col_idx, item)

    def _set_thumbnail_cell(self, row, col, img_path):
        label = QLabel()
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            label.setPixmap(pixmap.scaledToHeight(200, Qt.SmoothTransformation))
            label.setAlignment(Qt.AlignLeft)
            self.table.setCellWidget(row, col, label)
            self.table.setRowHeight(row, 200)