import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.ecc import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = 'http://127.0.0.1:5000/api/ecc/generate_keys'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)    
                msg.setText(data['message'])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_sign(self):
        url = 'http://127.0.0.1:5000/api/ecc/sign'
        payload = {
            'message': self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setText(data['signature'])

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText('Signed successfully')
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        message = self.ui.txt_info.toPlainText().strip()
        signature = self.ui.txt_sign.toPlainText().strip()

        if not message or not signature:
            QMessageBox.warning(self, "Warning", "Missing message or signature")
            return

        payload = {
            "message": message,
            "signature": signature
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('isVerified'):
                    QMessageBox.information(self, "Result", "Verified Successfully")
                else:
                    QMessageBox.warning(self, "Result", "Verified Fail")
            else:
                QMessageBox.critical(self, "Error", f"API Error {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
