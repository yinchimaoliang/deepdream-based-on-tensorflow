import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import my_deepdream

dream = my_deepdream.my_deep_dream()
class FirstWindow(QWidget):

    close_signal = pyqtSignal()
    def on_layer_box_Clicked(self,t):
        dream.set_layer(self.layer_index[t.currentIndex()])
        # print(self.layer_index[t.currentIndex()])
    def __init__(self, parent=None):
        self.layer_index = ['mixed3a_pool_reduce','mixed3b_pool_reduce','mixed4a_pool_reduce','mixed4b_pool_reduce','mixed4c_pool_reduce',
        'mixed4d_pool_reduce','mixed4e_pool_reduce','mixed5a_pool_reduce','mixed5b_pool_reduce']
        # super这个用法是调用父类的构造函数
        # parent=None表示默认没有父Widget，如果指定父亲Widget，则调用之
        super(FirstWindow, self).__init__(parent)
        self.layer_box = QComboBox(self)
        self.layer_box.addItems(self.layer_index)
        # self.resize(100, 100)
        self.layer_box.setGeometry(0,200,200,30)
        self.layer_box.currentIndexChanged.connect(lambda :self.on_layer_box_Clicked(self.layer_box))
        self.btn = QToolButton(self)
        self.btn.setText("开始转换")
        self.btn.setGeometry(0, 300, 100, 30)
        self.__btn_Load = QPushButton("选择图片")
        self.__btn_Load.setParent(self)
        self.__btn_Load.setGeometry(0, 0, 100, 30)
        self.__btn_Load.clicked.connect(self.on_btn_Load_Clicked)
        self.__spinBox_iterNum_text = QLabel(self)
        self.__spinBox_iterNum_text.setText("迭代次数")
        self.__spinBox_iterNum_text.setGeometry(0,70,70,30)
        self.__spinBox_iterNum = QSpinBox(self)
        self.__spinBox_iterNum.setGeometry(0,100,100,30)
        self.__spinBox_iterNum.setRange(50,400)
        self.__spinBox_iterNum.setSingleStep(10)
        self.__spinBox_iterNum.valueChanged.connect(lambda :self.on_iterNum_Clicked(self.__spinBox_iterNum))
        self.setGeometry(300, 300, 200, 400)

    def on_iterNum_Clicked(self,t):
        print(t.value())
        dream.set_iter_num(t.value())


    def on_btn_Load_Clicked(self):
        self.absolute_path = QFileDialog.getOpenFileName(self, 'Open file', '.', "jpg files (*.jpg)")
        dream.get_image(self.absolute_path[0])
        print(self.absolute_path[0])



    def closeEvent(self, event):
        self.close_signal.emit()
        self.close()


class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)


    def handle_click(self):
        dream.deep_dream()
        self.pix = QPixmap("output/output1.jpg")
        self.lb1 = QLabel(self)
        self.lb1.setGeometry(100, 0, 400, 400)
        self.setStyleSheet("background: black")
        self.lb1.setPixmap(self.pix)
        if not self.isVisible():
            self.show()

    def handle_close(self):
        self.close()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = FirstWindow()
    s = SecondWindow()
    ex.btn.clicked.connect(s.handle_click)
    # ex.btn.clicked.connect(ex.hide)
    ex.close_signal.connect(ex.close)
    ex.show()
    sys.exit(App.exec_())