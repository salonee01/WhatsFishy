import random
import sys
import time
import getMail

from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (
	QApplication,
	QLabel,
	QMainWindow,
	QPushButton,
	QVBoxLayout,
	QWidget,
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class Worker(QObject):
	finished = pyqtSignal()
	progress = pyqtSignal(int)

	def run(self):
		getMail.getEmails()
		self.finished.emit()

class Window(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi()

	def setupUi(self):
		self.setWindowTitle("What\'s Fishy?")
		self.resize(250, 150)
		self.centralWidget = QWidget()
		self.setCentralWidget(self.centralWidget)
		# Create and connect widgets
		self.label = QLabel("Remove the phishing emails and stay safe!")
		self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.countBtn = QPushButton("De-phish!")
		self.countBtn.clicked.connect(self.runTasks)
		# Set the layout
		layout = QVBoxLayout()
		layout.addWidget(self.label)
		layout.addWidget(self.countBtn)
		self.centralWidget.setLayout(layout)

	def runTasks(self):
		self.thread = QThread()
		self.worker = Worker()
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		self.thread.start()
		self.countBtn.setEnabled(False)
		self.label.setText('Your inbox is being cleaned...')
		self.thread.finished.connect(
			lambda: self.countBtn.setEnabled(True)
		)
		self.thread.finished.connect(
			lambda: self.label.setText("Your inbox is free of phishng mails!")
		)



if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	window.show()
	sys.exit(app.exec())
	p = multiprocessing.Process(target=Worker.run)
	p.start()
	p.join(300)
	if p.is_alive():
		p.terminate()
		p.join()