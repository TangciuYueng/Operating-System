# from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from re import sub
import sys
import os
# app = QApplication([])
# tree = QTreeWidget()
# tree.setColumnCount(1)
# tree.setHeaderLabels(['Name'])

# root = QTreeWidgetItem(tree, ['Root'])
# for i in range(10):
#     QTreeWidgetItem(root, ['Child %d' % (i + 3)])
# tree.show()
# sys.exit(app.exec_())

# exitAct.triggered.connect(qApp.quit)
import datetime
'''
对表格视图不会整行处理，遂give up
'''

class Index:
    max_length = 100
    def __init__(self):
        self.index = []
        

    def addIndex(self, data: int):
        if len(self.index) >= max_length:
            return False
        self.index.append(data)
        return True

    def isFull(self):
        return len(index) > max_length

class IndexTable:
    def __init__(self):
        self.primaryIndex = Index()
        self.secondaryIndex = None
        self.thirdIndex = None

    def addIndex(data: int):
        if not self.primaryIndex.isFull():
            self.primaryIndex.addIndex(data)
            if self.primaryIndex.isFull():
                self.secondaryIndex = Index()
        elif not self.secondaryIndex.isFull():
            self.secondaryIndex.addIndex(data)
            if self.secondaryIndex.isFull():
                self.thirdIndex = Index()
        elif not thirdIndex.isFull():
            thirdIndex.addIndex(data)
        else:
            return False
        return True

    def readTable(self):
        res = self.primaryIndex.index
        if (not self.secondaryIndex) and self.primaryIndex.isFull():
            res += self.secondaryIndex.index
        if (not self.thirdIndex) and self.secondaryIndex.isFull():
            res += self.thirdIndex.index

        return res

class Block:
    max_length = 16
    def __init__(self):
        self.info = ''
        self.length = 0
        

    def setInfo(self, new_info):
        self.length = max_length if len(new_info) > max_length else len(new_info)
        self.info = new_info

class BasicFCB:
    def __init__(self, item, father_path):
        self.name = item.fileName
        self.size = '0'
        self.type = item.fileType
        self.file_id = item.fileId
        self.path = father_path + '\\' + self.name
        self.modifiedTime = datetime.datetime.now()
        self.indexTable = IndexTable()

class SymFCB:
    cnt = 0
    def __init__(self, fileName = '', fileType = 'folder'):
        self.fileName = fileName
        self.fileType = fileType
        self.fileId = SymFCB.cnt
        SymFCB.cnt += 1
        self.father = None
        self.children = []
    
    def addSon(self, newItem):
        self.children.append(newItem)
        newItem.father = self
        # if not self.son:
        #     self.son = newItem
        #     newItem.father = self
        # else:
        #     temp = self.son
        #     while temp.next:
        #         temp = temp.next
        #     temp.next = newItem
        #     newItem.pre = temp
    # 移除自己
    # def remove(self):
    #     if not self.pre:
    #         self.father.son = self.next
    #     else:
    #         self.pre.next = self.next
    #         self.next.pre = self.pre

class Catalog:
    def __init__(self):
        self.rootFCB = SymFCB()
    
class Pair:
    def __init__(self, sf = None, bf = None):
        self.symFCB = sf
        self.basicFCB = bf

class Manager:
    Capacity = int(1e6)
    def __init__(self):
        self.blocks = [None] * Manager.Capacity
        self.bitMap = [True] * Manager.Capacity
        self.bit_idx = 0

    def getBlock(self, i):
        return self.blocks[i].info

    def withdraw(self, *idxList):
        for idx in idxList:
            bitMap[idx] = True

    def allocBlock(self, data):
        self.bit_idx %= Capacity
        pointer = self.bit_idx
        while True:
            if self.bitMap[pointer]:
                self.blocks[pointer] = Block()
                self.blocks[pointer].setInfo(data)
                self.bit_idx = pointer + 1
                return pointer
            else:
                pointer = (pointer + 1) % Capacity
            
            if pointer == self.bit_idx:
                break
        return -1

    def writeData(self, data):
        table = IndexTable()
        while len(data) > IndexTable.max_length:
            table.addIndex(self.allocBlock(data[: IndexTable.max_length]))
            data = data[IndexTable.max_length: ]
        table.addIndex(self.allocBlock(data))
        return table

table_header = ['name', 'modifiedTime', 'type', 'size']
# 窗口大小
WIDTH, HEIGHT = 1280, 720
# 左边大小
WIDTH1 = 250
# 字体
font = 'Microsoft Yahei'
# 表格中字体大小
table_font_size = 14
# 文本字体大小
text_font_size = 12
# 粗体
font_weight_bold = 75

# 文件排序
def compare_items(file_name1, file_name2, col):
    text1 = file_name1.text(col)
    text2 = file_name2.text(col)

    label1 = sub('\d', '', text1)
    label2 = sub('\d', '', text2)

    # 先比较字母
    if label1 != label2:
        return label1 < label2

    # 相同了再比较后面数字，注意可能没有数字
    num1 = sub('\D', '', text1)
    num2 = sub('\D', '', text2)
    # 转换为整型
    num1 = 0 if num1 == '' else int(num1)
    num2 = 0 if num2 == '' else int(num2)
    return num1 < num2


class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, item_list, parent=None):
        super(TreeWidgetItem, self).__init__(parent, item_list) 

    def __lt__(self, other):
        text1 = self.text(0)
        text2 = other.text(0)
        # 去掉数字以及括号
        label1 = sub('\d|\(|\)', '', text1)
        label2 = sub('\d|\(|\)', '', text2)

        # 先比较字母
        if label1 != label2:
            return label1 > label2

        # 相同了再比较后面数字，注意可能没有数字
        num1 = sub('\D', '', text1)
        num2 = sub('\D', '', text2)
        # 转换为整型
        num1 = 0 if num1 == '' else int(num1)
        num2 = 0 if num2 == '' else int(num2)
        return num1 > num2

class TableWidgetItem(QTableWidgetItem):
    def __init__(self, item):
        super(TableWidgetItem, self).__init__(item)

    def __lt__(self, other):
        text1 = self.text()
        text2 = other.text()
        text1 = self.data(Qt.UserRole)
        text2 = other.data(Qt.UserRole)
        print(text1, text2)
        # 去掉数字以及括号
        label1 = sub('\d|\(|\)', '', text1)
        label2 = sub('\d|\(|\)', '', text2)

        # 先比较字母
        if label1 != label2:
            return label1 < label2

        # 相同了再比较后面数字，注意可能没有数字
        num1 = sub('\D', '', text1)
        num2 = sub('\D', '', text2)
        # 转换为整型
        num1 = 0 if num1 == '' else int(num1)
        num2 = 0 if num2 == '' else int(num2)
        return num1 < num2

class myWin(QWidget):
    def __init__(self):
        super(myWin, self).__init__()
        self.catalog = Catalog()
        self.cur_symfcb = self.catalog.rootFCB
        self.folder_stack = [self.cur_symfcb]
        self.pair_table = {}
        self.manager = Manager()
        self.cur_path = os.path.realpath(__file__)
        self.list_table = {}
        self.root_node = None

        self.set_UI()
        self.init_tree()

    def set_UI(self):
        self.setStyleSheet(
            'QMenuBar{font-size: 20px}'
            'QMenu{font-size: 20px}'
            'QAction{font-size: 20px;}'
        )
        self.setWindowTitle('file management')
        self.setObjectName('myWin')
        self.resize(WIDTH, HEIGHT)

        grid = QGridLayout()

        menu = QMenuBar()
        # 三个menu
        file_menu = menu.addMenu('file')
        option_menu = menu.addMenu('options')
        about_menu = menu.addMenu('about')
        # 第一个menu中
        save_file_act = QAction('save file message&(S)', self)
        save_file_act.setShortcut('Ctrl+S')
        load_file_act = QAction('load exist message&(L)', self)
        load_file_act.setShortcut('Ctrl+L')
        file_menu.addActions([save_file_act, load_file_act])

        # 第二个menu中
        open_act = QAction('open&(O)', self)
        open_act.setShortcut('Ctrl+O')
        
        # 第二个menu中的new
        new_menu = option_menu.addMenu('new')
        new_txt = QAction('new txt&(T)', self)
        new_txt.setShortcut('Ctrl+T')
        new_txt.triggered.connect(self.new_txt_clicked)
        new_folder = QAction('new folder&(F)', self)
        new_folder.setShortcut('Ctrl+F')
        new_folder.triggered.connect(self.new_folder_clicked)
        new_menu.addActions([new_txt, new_folder])

        # 第三个menu
        delete_act = QAction('delete&(D)', self)
        delete_act.setShortcut('Ctrl+D')
        rename_act = QAction('rename&(R)', self)
        rename_act.setShortcut('Ctrl+R')
        format_act = QAction('format&(M)', self)
        format_act.setShortcut('Ctrl+M')

        option_menu.addActions([delete_act, rename_act, format_act, open_act])

        # 工具栏
        tool = QToolBar('tool')
        back_act = QAction('<-', self)
        back_act.setFont(QFont(font, text_font_size, font_weight_bold))
        forward_act = QAction('->', self)
        forward_act.setFont(QFont(font, text_font_size, font_weight_bold))

        address = QLineEdit('root\\')
        address.setReadOnly(True)
        address.setFont(QFont(font, text_font_size, font_weight_bold))
        tool.addActions([back_act, forward_act])
        tool.addWidget(address)

        # 左边树形结构
        tree = QTreeWidget()
        tree.setObjectName('tree')
        tree.setColumnCount(1)
        tree.setHeaderLabels(['Name'])
        tree.setSortingEnabled(True)
        # 自定义排序方法
        # tree.sortItems.connect(lambda column, order: treeWidget.sortItems(column, order, compare_items))
        # tree.setFont(QFont(font, table_font_size, font_weight_bold))
        tree.setMaximumWidth(WIDTH1)
        # 右边文件列表
        table = QTableWidget()
        table.setObjectName('table')
        table.setColumnCount(len(table_header))
        table.setHorizontalHeaderLabels(table_header)
        # 选中整行
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        # 隐藏行数
        table.verticalHeader().setVisible(False)
        # 不可编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置字体
        table.horizontalHeader().setFont(QFont(font, table_font_size, font_weight_bold))
        # 列宽自动分配
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 行高自动分配
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 排序
        table.setSortingEnabled(True)
        table.sortItems(0, Qt.AscendingOrder)
        
        grid.addWidget(menu, 0, 0, 1, 2)
        grid.addWidget(tool, 1, 0, 1, 2)
        grid.addWidget(tree, 2, 0)
        grid.addWidget(table, 2, 1)
        self.setLayout(grid)

    # 构建文件号 -> SymFCB 和 BasicFCB的映射
    def map(self, item, file):
        self.pair_table[item.fileId] = Pair(item, file)

    # 检查是否重名
    def check_name(self, file_name, ext=''):
        # cur_symfcb_son = self.cur_symfcb.son
        cnt = 0
        for child in self.cur_symfcb.children:
            name_arr = child.fileName.split('(')
            if name_arr[0] != child.fileName and name_arr[0] == file_name \
               or child.fileName == file_name + ext:
               cnt += 1
        if cnt > 0:
            file_name += '(' + str(cnt) + ')'
        return file_name + ext 

    # 点击新建文件
    def new_txt_clicked(self):
        file_name = self.check_name('New text', '.txt')
        new_fcb = SymFCB(file_name, 'txt')
        self.cur_symfcb.addSon(new_fcb)

        father = None
        if self.cur_symfcb in self.pair_table:
            father = self.pair_table[self.cur_symfcb.fileId].basicFCB
        father_path = 'root' if father == None else father.path
        new_file = BasicFCB(new_fcb, father_path)
        self.map(new_fcb, new_file)
        # 更新界面
        self.update_view()

    # 点击新建文件夹
    def new_folder_clicked(self):
        file_name = self.check_name('New folder')
        new_fcb = SymFCB(file_name, 'folder')
        self.cur_symfcb.addSon(new_fcb)

        father = None
        if self.cur_symfcb in self.pair_table:
            father = self.pair_table[self.cur_symfcb.fileId].basicFCB
        father_path = 'root' if father == None else father.path
        new_file = BasicFCB(new_fcb, father_path)
        self.map(new_fcb, new_file)
        # 更新界面
        self.update_view()

    # 更新视图
    def update_view(self):
        self.update_tree()
        self.update_table()

    # 初始化左侧树形
    def init_tree(self):
        tree = self.findChild(QTreeWidget, 'tree')
        root = TreeWidgetItem(['Root'], tree)
        tree.expandAll()

    # 更新左侧树形
    def update_tree(self):
        tree = self.findChild(QTreeWidget,'tree')
        tree.clear()
        tree.addTopLevelItem(self.create_tree(self.catalog.rootFCB))
        tree.expandAll()
    
    # 构建树形结构
    def create_tree(self, root):
        qtree_item = TreeWidgetItem([root.fileName if root.fileId else 'root'])
        for child in root.children:
            child_qtree_item = self.create_tree(child)
            qtree_item.addChild(child_qtree_item)
        return qtree_item

    # 更新表格
    def update_table(self):
        table = self.findChild(QTableWidget)
        table.clearContents()
        table.setRowCount(0)
        
        for row, child in enumerate(self.cur_symfcb.children):
            basic_fcb = self.pair_table[child.fileId].basicFCB

            row = table.rowCount()
            table.setRowCount(row + 1)
            item_name = TableWidgetItem(basic_fcb.name)
            item_time = TableWidgetItem(str(basic_fcb.modifiedTime))
            item_type = TableWidgetItem(basic_fcb.type)
            item_size = TableWidgetItem(basic_fcb.size)
            
            items = [item_name, item_time, item_type, item_size]

            for col, item in enumerate(items):
                table.setItem(row, col, item)



                    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWin()
    w.show()
    sys.exit(app.exec_())