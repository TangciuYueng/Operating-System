from time import sleep
from random import random
from math import ceil, floor
import sys

from PyQt5.QtCore import QThread, QSize, Qt, QTime, QEventLoop, QMutex, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 指令总数
INSTRUCTION_NUM = 320
# 每页指令数
INSTRUCTION_PER_PAGE = 10
# 内存页数
PAGE_NUM = 4
# 最大时间间隔
MAX_INTERVAL = 1000
# 是否继续程序
GOON = True

# 左侧宽度
WIDTH1 = 1000
# 左下侧高度
HEIGHT2 = 380
# LCD高度
LCD_HEIGHT = 100

# 缺页数量
missing_page_num = 0
# 当前步数
cur_step = 0
# 上一个指令编号
previous_ins_id = None
# 是否一直执行
begin_loop = False
# 指令执行间隔
interval = 500
# 置换算法
selected = 'LRU'
# 指令执行完成
finished = False
# 输出信息
output = {
    'step': None,
    'ins_num': None,
    'missing': None,
    'swap in': None,
    'swap out': None
}
# 字体
font = 'Microsoft Yahei'
# 表格中字体大小
table_font_size = 14
# 文本字体大小
text_font_size = 12
# 粗体
font_weight_bold = 75

# 记录页相关信息
class Page:
    def __init__(self, pid = -1, es = None, rs = None):
        self.page_id = pid
        self.enter_step = es
        self.recent_used_step = rs

# 内存中页表信息记录
pages = []
# 一行显示页的数量
PAGE_NUM_PER_ROW = 4
# 窗口大小
WIDTH, HEIGHT = 1350, 850
# 页面初始显示
INIT_NUM = -1
# 输入内容表头
table_head = ['step', 'ins_num', 'missing', 'swap in', 'swap out']
# 下拉框内容
select_algorithm = ['LRU', 'FIFO']

'''
程序开始的数据输入框
输入指令总数、内存页数以及每页指令数
'''
class myDialog(QDialog):
    def __init__(self):
        super(myDialog, self).__init__()
        self.setStyleSheet(
            'QPushButton{border-radius: 10px; border: 2px solid black; background-color: lightskyblue}'
            'QPushButton:pressed{padding-left:5px; padding-top:5px}'
            'QPushButton:hover{background-color: lightskyblue}'
            'QLabel{font-weight: bold;}'
            'QLineEdit{font-weight: bold}'
            '#dialogWindow{background-color: lightblue}'
        )
        # 标题
        self.setWindowTitle('内存管理')
        # 名字
        self.setObjectName('dialogWindow')
        # 整体网格布局
        grid = QGridLayout()
        # 输入标签
        self.total_ins_num_text = QLabel('指令总数', self)
        self.page_num_text = QLabel('内存页数', self)
        self.ins_per_page_num_text = QLabel('每页指令数', self)
        # 输入框
        self.total_ins_num_input = QLineEdit('320', self)
        self.page_num_input = QLineEdit('4', self)
        self.ins_per_page_num_input = QLineEdit('10', self)
        # 输入限制
        self.total_ins_num_input.setValidator(QIntValidator(bottom = 1, top = 10000))
        self.page_num_input.setValidator(QIntValidator(bottom = 1, top = 100))
        self.ins_per_page_num_input.setValidator(QIntValidator(bottom = 1, top = 100))
        # 字体显示
        for comp in self.findChildren((QLineEdit, QLabel)):
            comp.setFont(QFont(font, 16))
        # 全选
        self.total_ins_num_input.selectAll()
        self.page_num_input.selectAll()
        self.ins_per_page_num_input.selectAll()
        # 确认按钮
        self.btn = QPushButton('OK', self)
        self.btn.clicked.connect(self.btn_clicked)
        self.btn.setFont(QFont(font, 10, font_weight_bold))
        self.btn.setMinimumHeight(40)

        # 在界面中放置组件
        # 放置文本
        grid.addWidget(self.total_ins_num_text, 0, 0)
        grid.addWidget(self.page_num_text, 1, 0)
        grid.addWidget(self.ins_per_page_num_text, 2, 0)
        # 放置输入框
        grid.addWidget(self.total_ins_num_input, 0, 1)
        grid.addWidget(self.page_num_input, 1, 1)
        grid.addWidget(self.ins_per_page_num_input, 2, 1)
        # 放置按钮
        grid.addWidget(self.btn, 3, 0, 1, 2)

        # 放置布局
        self.setLayout(grid)

    # 按下确认按钮
    def btn_clicked(self):
        global INSTRUCTION_NUM, INSTRUCTION_PER_PAGE, PAGE_NUM
        # 获得输入内容
        total_ins_num_str = self.total_ins_num_input.text()
        page_num_str = self.page_num_input.text()
        ins_per_page_num_str = self.ins_per_page_num_input.text()
        # 检查是否非空
        if total_ins_num_str == '' or page_num_str == '' or ins_per_page_num_str == '':
            return
        total_ins_num = int(total_ins_num_str)
        ins_per_page_num = int(ins_per_page_num_str)
        page_num = int(page_num_str)
        # 限制一定范围
        if total_ins_num <= 0 or total_ins_num > 99999  \
            or page_num <= 0 or page_num > 999 \
            or ins_per_page_num <= 0 or ins_per_page_num > 999 \
            or ins_per_page_num > total_ins_num:
            return

        # 修改数量
        INSTRUCTION_NUM = total_ins_num
        INSTRUCTION_PER_PAGE = ins_per_page_num
        PAGE_NUM = page_num
        # 隐藏窗口
        self.hide()
    # 点击关闭
    def closeEvent(self, e):
        print('you click to exit the program')
        global GOON
        GOON = False

'''
后台线程每隔interval时间执行一步
从而完成连续执行的效果
'''
class conStepWorker(QThread):
    # ui需要更新的信号
    ui_changed = pyqtSignal()
    # 执行完成修改按钮文字
    btn_start = pyqtSignal()

    def __init__(self):
        super(conStepWorker, self).__init__()
        
    # 重写线程运行函数 
    def run(self):
        global cur_step, begin_loop, finished
        # 原来在连续，现在不连续
        if begin_loop:
            begin_loop = False
            return
        # 原来不连续，现在连续
        begin_loop = True
        # 还没执行完就继续
        while begin_loop and cur_step < INSTRUCTION_NUM:
            # 执行一步
            move_one_step()
            # 更新UI界面信号发出
            self.ui_changed.emit()
            # 指令执行时间间隔
            sleep(interval / 1000)
        # 执行完成
        if cur_step >= INSTRUCTION_NUM:
            finished = True
        begin_loop = False
        # 执行完成回复按钮文字信号发出
        self.btn_start.emit()



class myWin(QWidget):
    def __init__(self):
        super(myWin, self).__init__()
        # 定时更新UI界面
        self.setup_UI()

        # 连续执行后台线程
        self.t = conStepWorker()
        self.t.ui_changed.connect(self.update)
        self.t.btn_start.connect(lambda: self.findChild(QPushButton, 'btn_continuous').setText('开始连续执行'))

    # 设置UI 
    def setup_UI(self):
        # 样式表
        self.setStyleSheet(
            'QLabel{font-weight: bold}' 
            '#mainWindow{background-color: skyblue}'
            'QScrollArea{background-color: white}'
            'QPushButton:hover{background-color: lightskyblue}'
            'QPushButton{border-radius: 10px; border: 2px solid black; background-color: lightblue}'
            'QPushButton:pressed{padding-left:5px; padding-top:5px}'
        )
        # 标题
        self.setWindowTitle('内存管理——分页机制')
        # 窗口名字
        self.setObjectName('mainWindow')
        # 窗口大小
        self.resize(WIDTH, HEIGHT)
        # 网格整体布局
        gridLayout = QGridLayout()

        # 内存页面区域
        scrollArea_show_page = QScrollArea()
        grid = QGridLayout()
        for i in range(PAGE_NUM):
            # 第i个物理页面标签
            label = QLabel('Page %d' % i)
            label.setFont(QFont(font, text_font_size))
            # 在物理页面中显示装入页面
            lcd = QLCDNumber()
            lcd.display('--')
            lcd.setDigitCount(len(str(ceil(INSTRUCTION_NUM / INSTRUCTION_PER_PAGE))))
            lcd.setSegmentStyle(QLCDNumber.Flat)
            lcd.setObjectName('page%d' % i)
            lcd.setMinimumSize(WIDTH1 // 5, LCD_HEIGHT)
            lcd.setStyleSheet('QLCDNumber{background-color: black; color: red; border-radius: 10px}')
            # 最近访问于第i步
            label1 = QLabel('最近访问: %d' % INIT_NUM)
            label1.setFont(QFont(font, text_font_size))
            label1.setObjectName('lru%d' % i)
            # 于第j步进入内存
            label2 = QLabel('何时进入: %d' % INIT_NUM)
            label2.setFont(QFont(font, text_font_size))
            label2.setObjectName('fifo%d' % i)
            # 布局一个page及其相关信息占PAGE_NUM_PER_ROW行
            grid.addWidget(label, i // PAGE_NUM_PER_ROW * PAGE_NUM_PER_ROW, i % PAGE_NUM_PER_ROW)
            grid.addWidget(lcd, i // PAGE_NUM_PER_ROW  * PAGE_NUM_PER_ROW + 1, i % PAGE_NUM_PER_ROW)
            grid.addWidget(label1, i // PAGE_NUM_PER_ROW  * PAGE_NUM_PER_ROW + 2, i % PAGE_NUM_PER_ROW)
            grid.addWidget(label2, i // PAGE_NUM_PER_ROW  * PAGE_NUM_PER_ROW + 3, i % PAGE_NUM_PER_ROW)
        # grid加入scroll区域
        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: white')
        scroll_w.setLayout(grid)
        scrollArea_show_page.setWidget(scroll_w)

        # # 输出信息区域
        table = QTableWidget()
        table.setObjectName('table')
        # 设置列数
        table.setColumnCount(len(table_head))
        table.setHorizontalHeaderLabels(table_head)
        table.horizontalHeader().setFont(QFont(font, table_font_size, font_weight_bold))
        # 列宽自动分配
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 行高自动分配
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 颜色交替
        table.setAlternatingRowColors(True)
        table.setStyleSheet("alternate-background-color: lightblue; background-color: white;")
        # 不可编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不可选中
        table.setSelectionMode(QAbstractItemView.NoSelection)
        # 最小尺寸
        table.setMinimumSize(WIDTH1, HEIGHT2)
        # 隐藏行数
        table.verticalHeader().setVisible(False)

        # 右侧布局
        scrollArea_op = QScrollArea()
        grid = QGridLayout()
        # 当前需要调入指令编号，页号
        cur_ins_text = QLabel('当前指令编号: ')
        cur_ins_text.setFont(QFont(font, text_font_size))
        cur_ins = QLCDNumber()
        cur_ins.display('--')
        cur_ins.setObjectName('cur_ins')
        cur_ins.setStyleSheet('QLCDNumber{background-color: black; color: red; border-radius: 10px}')
        cur_ins.setMinimumSize(WIDTH1 // 5, LCD_HEIGHT)
        cur_ins.setSegmentStyle(QLCDNumber.Flat)
        grid.addWidget(cur_ins_text)
        grid.addWidget(cur_ins)
        # 作业指令总数
        total_ins_text = QLabel('作业指令总数: %d' % INSTRUCTION_NUM)
        total_ins_text.setFont(QFont(font, text_font_size))
        grid.addWidget(total_ins_text)
        # 每页存放指令数
        ins_per_page_text = QLabel('每页存放指令数: %d' % INSTRUCTION_PER_PAGE)
        ins_per_page_text.setFont(QFont(font, text_font_size))
        grid.addWidget(ins_per_page_text)
        # 内存页数
        memory_page_num_text = QLabel('内存页数: %d' % PAGE_NUM)
        memory_page_num_text.setFont(QFont(font, text_font_size))
        grid.addWidget(memory_page_num_text)
        # 页面置换算法，下拉框
        algorithm_text = QLabel('页面置换算法: ')
        algorithm_text.setFont(QFont(font, text_font_size))
        grid.addWidget(algorithm_text)
        cb = QComboBox()
        cb.setObjectName('select')
        cb.addItems(select_algorithm)
        cb.currentTextChanged.connect(self.selected_change)
        cb.setFont(QFont(font, text_font_size))
        grid.addWidget(cb)
        # 执行进度
        pgb_text = QLabel('执行进度: ')
        pgb_text.setFont(QFont(font, text_font_size))
        grid.addWidget(pgb_text)
        pgb = QProgressBar()
        pgb.setObjectName('pgb')
        pgb.setRange(0, 100)
        pgb.setValue(0)
        pgb.setFont(QFont(font, text_font_size))
        # 设置进度条样式
        pgb.setStyleSheet(
            'QProgressBar { border: 2px solid grey; border-radius: 5px; background-color: #FFFFFF; text-align: center;}'
            'QProgressBar::chunk{background:QLinearGradient(x1:0,y1:0,x2:2,y2:0,stop:0 powderblue,stop:1  blue); }')
        grid.addWidget(pgb)
        # 缺页数
        missing_page_num_text = QLabel('缺页数: 0')
        missing_page_num_text.setFont(QFont(font, text_font_size))
        missing_page_num_text.setObjectName('missing')
        grid.addWidget(missing_page_num_text)
        # 当前执行页数
        cur_step_text = QLabel('当前执行步数: -1')
        cur_step_text.setFont(QFont(font, text_font_size))
        cur_step_text.setObjectName('cur_step')
        grid.addWidget(cur_step_text)
        # 缺页率
        missing_rate_text = QLabel('缺页率: 0')
        missing_rate_text.setFont(QFont(font, text_font_size))
        missing_rate_text.setObjectName('missing_rate')
        grid.addWidget(missing_rate_text)
        # 每隔多少秒执行一次指令
        interval_text = QLabel('指令执行间隔: %dms' % interval)
        interval_text.setFont(QFont(font, text_font_size))
        interval_text.setObjectName('interval')
        grid.addWidget(interval_text)
        slider = QSlider(Qt.Horizontal)
        slider.setSliderPosition(interval)
        slider.setObjectName('slider')
        slider.setRange(10, MAX_INTERVAL)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.valueChanged.connect(self.change_interval)
        grid.addWidget(slider)

        # 操作按钮 单步执行 (开始/结束)连续运行 重置
        btn_single = QPushButton('单步执行')
        btn_single.clicked.connect(self.single_step_clicked)
        
        btn_continuous = QPushButton('开始连续执行')
        # btn_continuous.clicked.connect(continuous_step)
        btn_continuous.clicked.connect(self.con_step_clicked)
        btn_continuous.setObjectName('btn_continuous')

        btn_reset = QPushButton('重置')
        btn_reset.clicked.connect(self.reset_clicked)
        # btn_reset.clicked.connect(self.table_clear)

        grid.addWidget(btn_single)
        grid.addWidget(btn_continuous)
        grid.addWidget(btn_reset)

        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: white')
        scroll_w.setMinimumWidth(300)
        scroll_w.setLayout(grid)
        scrollArea_op.setWidget(scroll_w)

        # 总体网格布局中加入各个区域
        gridLayout.addWidget(scrollArea_show_page, 0, 0, 2, 1)
        gridLayout.addWidget(table, 2, 0, 3, 1)
        gridLayout.addWidget(scrollArea_op, 0, 1, 5, 1)

        self.setLayout(gridLayout)
        # 所有按钮按下都更新
        btns = self.findChildren(QPushButton)
        for btn in btns:
            btn.clicked.connect(self.update)
            btn.setFont(QFont(font, text_font_size))
            btn.setStyleSheet(
                'QPushButton{border-radius: 10px; border: 2px solid black; background-color: lightblue}'
                'QPushButton:pressed{padding-left:5px; padding-top:5px}'
                'QPushButton:hover{background-color: lightskyblue}')
        # 更新界面后再判断是否已经完成
        btn_single.clicked.connect(self.finish_ins)
        btn_continuous.clicked.connect(self.finish_ins)

        # 首先刷新一次界面
        self.update()

    # 重置按钮按下
    def reset_clicked(self):
        global begin_loop
        # 在连续执行点击该按钮无效
        if begin_loop:
            QMessageBox.warning(self, '警告', '正在连续执行不能进行该操作')
            return
        reset()
        self.table_clear()

    # 单步执行
    def single_step_clicked(self):
        global begin_loop
        # 在连续执行点击该按钮无效
        if begin_loop:
            QMessageBox.warning(self, '警告', '正在连续执行不能进行该操作')
            return
        # 执行一步函数
        move_one_step()

    # 连续执行
    def con_step_clicked(self):
        global begin_loop
        btn = self.findChild(QPushButton, 'btn_continuous')

        # 线程已经在运行，结束线程
        if self.t.isRunning():
            btn.setText('开始连续执行')
            # 使线程中运行函数跳出循环
            begin_loop = False
            return

        # 更改按钮文字
        btn.setText('结束连续执行')
        # 开始线程
        self.t.start()
    
    # 执行指令时间间隔
    def change_interval(self, val):
        global interval
        interval = val
        # 更新指令执行时间间隔显示文本
        interval_text = self.findChild(QLabel, 'interval')
        interval_text.setText('指令执行间隔: %dms' % interval)

    # 下拉框选择变化selected变量
    def selected_change(self, algorithm_text):
        global selected
        selected = algorithm_text

    # 清除table中数据
    def table_clear(self):
        table = self.findChild(QTableWidget)
        row = table.rowCount()
        for r in range(0, row)[::-1]:
            table.removeRow(r)
        # print('current table row: %d' % table.rowCount())
    
    # 执行完成消息提示
    def finish_ins(self):
        global finished
        if finished:
            QMessageBox.about(self, '温馨提示', '指令已执行完成，请重置')

    # 连续执行过程中点击其他按钮，消息提示
    def con_other_btn(self):
        global begin_loop
        if begin_loop:
            QMessageBox.warning(self, '警告', '当前正在连续执行，不可执行此操作')

    # 更新UI界面
    def update(self):
        # 更新内存页面显示
        for idx, page in enumerate(pages):
            lcd = self.findChild(QLCDNumber, 'page%d' % idx)
            lru_text = self.findChild(QLabel, 'lru%d' % idx)
            fifo_text = self.findChild(QLabel, 'fifo%d' % idx)
            if page.page_id == -1:
                lcd.display('--')
                lru_text.setText('最近访问: %d' % INIT_NUM)
                fifo_text.setText('何时进入: %d' % INIT_NUM)
                continue
            lcd.display(page.page_id)
            lru_text.setText('最近访问: %d' % page.recent_used_step)
            fifo_text.setText('何时进入: %d' % page.enter_step)
        # 更新当前指令编号显示
        lcd = self.findChild(QLCDNumber, 'cur_ins')
        if previous_ins_id is not None:
            lcd.display(previous_ins_id)
        else:
            lcd.display('--')
        # 更新执行步数
        cur_step_text = self.findChild(QLabel, 'cur_step')
        cur_step_text.setText('当前执行步数: %d' % (cur_step - 1))
        # 更新缺页数量
        missing_page_num_text = self.findChild(QLabel, 'missing')
        missing_page_num_text.setText('缺页数: %d' % missing_page_num)
        # 更新缺页率
        missing_rate_text = self.findChild(QLabel, 'missing_rate')
        if cur_step:
            missing_rate_text.setText('缺页率: {:.2f}'.format(missing_page_num / cur_step))
        else:
            missing_rate_text.setText('缺页率: 0')
        # 更新进度条
        pgb = self.findChild(QProgressBar, 'pgb')
        pgb.setValue(cur_step * 100 // INSTRUCTION_NUM)
        # 更新指令执行时间间隔显示文本
        interval_text = self.findChild(QLabel, 'interval')
        interval_text.setText('指令执行间隔: %dms' % interval)
        # 更新滑动条位置
        slider = self.findChild(QSlider, 'slider')
        slider.setSliderPosition(interval)
        # 更新输出表格，output有信息才输出
        if output['ins_num']:
            table = self.findChild(QTableWidget, 'table')
            row = table.rowCount()
            table.setRowCount(row + 1)
            print(output)
            for idx, pro in enumerate(table_head):
                item = QTableWidgetItem(str(output[pro]))
                item.setFont(QFont(font, table_font_size))
                table.setItem(row, idx, item)
                output[pro] = None
               
    

# 随机生成下一条指令的编号
def get_next_ins():
    global previous_ins_id
    res = -1
    # 不是第一条
    if previous_ins_id is not None:
        random_num = random()
        if random_num < 0.5:
            if previous_ins_id + 1 < INSTRUCTION_NUM:
                ans = previous_ins_id + 1
            else:
                ans = floor(random() * INSTRUCTION_NUM)
        elif 0.5 <= random_num <= 0.75:
            ans = floor(random() * previous_ins_id)
        else:
            ans = floor(random() * (INSTRUCTION_NUM - previous_ins_id)) + previous_ins_id
    else:
        ans = floor(random() * INSTRUCTION_NUM)

    # 更新上一条指令记录
    previous_ins_id = ans
    output['ins_num'] = ans
    print('next idx is %d' % ans)
    return ans

# 将页交换
def swap(page_id, algorithm=selected):
    global output
    print('将page: %d 换入' % page_id)
    # 找到最先进来的或最近未使用的
    min_step = INSTRUCTION_NUM
    target_page = None
    for page in pages:
        if page.enter_step < min_step:
            min_step = page.enter_step if algorithm == 'FIFO' else page.recent_used_step
            target_page = page
    pages[pages.index(target_page)] = Page(page_id, cur_step, cur_step)
    output['swap in'] = page_id
    output['swap out'] = target_page.page_id
    print('将page: %d 换出' % target_page.page_id)

def jump_next(next_ins_id):
    global cur_step, missing_page_num, output
    output['step'] = cur_step
    found = False
    page_id = floor(next_ins_id / INSTRUCTION_PER_PAGE)

    # 检查是否已经在内存中的页表
    for page in pages:
        if page.page_id == page_id:
            # 找到了更新最近使用时间
            page.recent_used_step = cur_step
            found = True
            break
    if found:
        output['missing'] = False
        print('内存中找到 %d, 不用换' % page_id)
    else:
        output['missing'] = True
        missing_page_num += 1
        # 检查内存中是否还可以调入页面
        get_in = False
        for idx, page in enumerate(pages):
            if page.page_id == -1:
                print('有空位')
                pages[idx] = Page(page_id, cur_step, cur_step)
                output['swap in'] = page_id
                get_in = True
                break
        # 没有空位，需要swap
        if not get_in:
            swap(page_id)

# 单步执行函数
def move_one_step():
    global cur_step, begin_loop, finished
    if cur_step >= INSTRUCTION_NUM:
        print('执行完成')
        finished = True
        begin_loop = False
        return
    
    print('cur step: %d' % cur_step)
    jump_next(get_next_ins())
    cur_step += 1



# 重置参数
def reset():
    global missing_page_num, cur_step, previous_ins_id, begin_loop, interval, pages, finished
    # 缺页数量
    missing_page_num = 0
    # 当前步数
    cur_step = 0
    # 上一个指令编号
    previous_ins_id = None
    # 是否一直执行
    begin_loop = False
    # 执行完成标记
    finished = False
    # 指令执行间隔
    interval = 500
    # 内存中的页
    pages = []
    for i in range(PAGE_NUM):
        pages.append(Page())

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 消息窗口设置参数
    dialog = myDialog()
    dialog.exec_()
    if GOON: 
        # 在内存中的页
        for i in range(PAGE_NUM):
            pages.append(Page())

        # 主界面
        w = myWin()
        w.show()
        sys.exit(app.exec_())
    else:
        print('程序结束')