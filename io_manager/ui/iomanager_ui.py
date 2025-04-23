from PySide6.QtWidgets import QMainWindow, QCheckBox, QVBoxLayout
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QGroupBox
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from event.io_event_handler import select_directory, toggle_edit_mode, save_table_to_csv
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
        file_path_label = QLabel("File path:")
        self.file_path_le = QLineEdit()
        self.file_path_le.setPlaceholderText("Input your shot path")
        shot_select_btn = QPushButton("Select")
        shot_load_btn = QPushButton("Load")

        self.table = QTableWidget()

        self.excel_label = QLabel("Ready to load")
        excel_save_btn = QPushButton("Save")
        self.excel_edit_btn = QPushButton("Enable Edit")

        # Event Handle
        shot_select_btn.clicked.connect(
            lambda: select_directory(self.file_path_le)
        )
        shot_load_btn.clicked.connect(self.on_load_clicked)
        self.excel_edit_btn.clicked.connect(self.on_edit_clicked)
        excel_save_btn.clicked.connect(self.on_save_clicked)
        

        # Layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        shot_select_container = QHBoxLayout()
        bottom_layout = QHBoxLayout()
        excel_group = QGroupBox("Excel")
        excel_btn_layout = QHBoxLayout()

        shot_select_container.addWidget(file_path_label)
        shot_select_container.addWidget(self.file_path_le)
        shot_select_container.addWidget(shot_select_btn)
        shot_select_container.addWidget(shot_load_btn)

        excel_btn_layout.addWidget(excel_save_btn)
        excel_btn_layout.addWidget(self.excel_edit_btn)
        excel_group.setLayout(excel_btn_layout)
        bottom_layout.addWidget(self.excel_label)
        bottom_layout.addWidget(excel_group)

        main_layout.addLayout(shot_select_container)
        main_layout.addWidget(self.table)
        main_layout.addLayout(bottom_layout)

        central_widget.setLayout(main_layout)

    def on_load_clicked(self):
        csv_path = export_metadata(self.file_path_le.text())
        if csv_path:
            self.update_table(csv_path)
            self.excel_label.setText(csv_path)

    def on_edit_clicked(self):
        self.edit_mode = toggle_edit_mode(self.table, self.edit_mode)
        if self.edit_mode:
            self.excel_edit_btn.setText("Disable Edit")
        else:
            self.excel_edit_btn.setText("Enable Edit")

    def on_save_clicked(self):
        csv_path = self.excel_label.text()
        save_table_to_csv(self.table, csv_path, parent=self)
    
    def update_table(self, csv_path):
        self.edit_mode = False
        df = pd.read_csv(csv_path)
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns) + 1)
        header_list = ["check"] + df.columns.tolist()
        self.table.setHorizontalHeaderLabels(header_list)

        for row_idx, row_data in df.iterrows():
            checkbox = QCheckBox()
            self.table.setCellWidget(row_idx, 0, checkbox)

            for col_idx, header in enumerate(df.columns):
                value = row_data[header]

                # NaN 처리
                if pd.isna(value):
                    value = ""

                # 썸네일 처리
                if header == "thumbnail" and isinstance(value, str) and os.path.exists(value):
                    self.set_thumbnail_cell(row_idx, col_idx + 1, value)
                    item = QTableWidgetItem(value)
                    self.table.setItem(row_idx, col_idx + 1, item)
                else:
                    item = QTableWidgetItem(str(value))
                    self.table.setItem(row_idx, col_idx + 1, item)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

    def set_thumbnail_cell(self, row, col, img_path):
        label = QLabel()
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            label.setPixmap(pixmap.scaledToHeight(200, Qt.SmoothTransformation))
            label.setAlignment(Qt.AlignLeft)
            self.table.setCellWidget(row, col, label)
            self.table.setRowHeight(row, 200)