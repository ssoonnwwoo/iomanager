from PySide6.QtWidgets import QFileDialog, QTableWidget, QMessageBox
import os
import pandas as pd

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

def toggle_edit_mode(table, edit_mode):
    if edit_mode:
        table.setEditTriggers(QTableWidget.NoEditTriggers)
    else:
        table.setEditTriggers(QTableWidget.AllEditTriggers)
    return not edit_mode

def save_table_to_csv(table, csv_path, parent=None):
    if not os.path.exists(csv_path):
        QMessageBox.warning(parent, "Save Failed", f"CSV path is not valid\nPlease check csv path on left")
        return False

    row_count = table.rowCount()
    col_count = table.columnCount()

    headers = []
    data = []
    for i in range(1, col_count):
        headers.append(table.horizontalHeaderItem(i).text())

    for row in range(row_count):
        row_data = {}
        for col in range(1, col_count):
            item = table.item(row, col)
            row_data[headers[col - 1]] = item.text() if item else ""
        data.append(row_data)

    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)

    QMessageBox.information(parent, "Save Complete", f"Saved to:\n{csv_path}")
    print(f"[SAVE] Table saved to {csv_path}")
    return True