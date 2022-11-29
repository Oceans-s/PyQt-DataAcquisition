# PyQt-DataAcquisition

## Installation

To install:
```
pip install opencv-python
pip install more_itertools
pip install selenium
pip install pool
pip install pyqt5
pip install pyqt5-tools
```

## Getting Started

It takes only several lines of code to create a simple demo.

```python
class MyWidget(QWidget):

    def __init__(self, parent=None):
        super(MyWidget, self).__init__()
        self.ui = uic.loadUi("./MyUI.ui")

if __name__ == '__main__':

    myapp = QApplication(sys.argv)
    myWidget = MyWidget()
    myWidget.ui.show()
    sys.exit(myapp.exec_())
```
