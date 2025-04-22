from PySide6.QtWidgets import QFileDialog
import os

def select_directory(line_edit_widget):
    show_dir = os.path.join(os.path.expanduser("~"), "show")
    dir_path = QFileDialog.getExistingDirectory(
        None, # 부모위젯 x
        "Select scan data folder",
        show_dir, 
        QFileDialog.ShowDirsOnly
    )
    if dir_path:
        line_edit_widget.setText(dir_path)



