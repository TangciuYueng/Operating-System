from time import sleep
import sys
from functools import partial
import random
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QTimer, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# 是否继续程序
GOON = True
# 电梯数量
NUM_OF_ELEVATOR = 5 
# 楼层数量
NUM_OF_FLOOR = 20
# 总体任务阈值
Q = 1.25
# 门操作时间，以毫秒为单位
DOOR_OPERATION_TIME = 4000

# 锁
outer_task_mutex = QMutex()

# 窗口大小
WIDTH, HEIGHT = 1280, 720

# 初始楼层
INIT_FLOOR = 0

# status of elevator
FREE = 0
RUNNINGUP = 1
RUNNINGDOWN = 2
OPENING = 3
CLOSING = 4
BROKEN = 5
OPEN = 6
PREOPEN = 7
PRECLOSE = 8
# status of pcb
WAITING = 9
RUNNING = 10
FINISHED = 11
# 外部任务队列
outer_task = []

'''
外部任务
self.start_floor: 任务发出楼层
self.status: 任务状态
self.direction: 任务请求方向
'''
class PCB():
    def __init__(self, start, stat, dire):
        self.start_floor = start
        self.status = stat
        self.direction = dire
    
'''
电梯
self.id: 电梯编号
self.status: 电梯状态
self.des: 该电梯目标
self.inner_target: 该电梯内部目标
'''
class Elevator(QThread):
    def __init__(self, id):
        super(Elevator, self).__init__()
        self.id = id
        self.status = FREE
        self.des = set()
        self.inner_target = set()

    # 电梯移动
    def move(self):
        # 电梯坏了不管了
        if self.status == BROKEN:
            # 电梯内还有人
            if len(self.des) != 0:
                self.elev_err()
            return
        # 电梯开门中，开门，关门中不移动
        if self.status in (OPEN, OPENING, CLOSING, PREOPEN, PRECLOSE):
            return
        
        # 没目标置为空闲状态
        if len(self.des) == 0:
            self.status = FREE

        # 电梯移动
        if self.status == RUNNINGDOWN:
            if cur_floor[self.id] != 0:
                cur_floor[self.id] -= 1
            # 到1楼不能再往下了
            else:
                self.status = FREE
        elif self.status == RUNNINGUP:
            if cur_floor[self.id] != NUM_OF_FLOOR:
                cur_floor[self.id] += 1
            # 到最高楼不能再往上了
            else:
                self.status = FREE 
    
    # 电梯故障处理
    def elev_err(self):
        # 重新分配外部的任务，内部的人出不来
        for task in outer_task:
            # 外部任务在本电梯的目标中就设置为等待状态
            if task.start_floor in self.des:
                task.status = WAITING
        
        self.des = set()
        self.inner_target = set()
    # 设置故障状态
    def set_err(self):
        self.status = BROKEN
        self.elev_err()

    # 状态改变
    def status_check(self):
        # 故障了就不管了
        if self.status == BROKEN:
            return
        # 开关门状态
        if self.status in (OPEN, OPENING, CLOSING, PREOPEN, PRECLOSE):
            return
        # 到达楼层
        if len(self.des) != 0:
            for floor in self.des:
                if floor == cur_floor[self.id]:
                    # 开关门
                    self.status = PREOPEN
                    self.des.discard(floor)
                    self.inner_target.discard(floor)
                    # break
                    # 交给开关门操作变化状态最后为free
                    return
        # 没有任务
        if len(self.des) == 0:
            self.status == FREE
        # 有任务
        else:
            if min(self.des) > cur_floor[self.id]:
                self.status = RUNNINGUP
            elif max(self.des) < cur_floor[self.id]:
                self.status = RUNNINGDOWN
            # 要上要下去近的
            else:
                if abs(max(self.des) - cur_floor[self.id]) < abs(min(self.des) - cur_floor[self.id]):
                    self.status = RUNNINGUP
                else:
                    self.status = RUNNINGDOWN
    # 外部任务完成确认
    def outer_task_check(self):
        for task in outer_task:
            if cur_floor[self.id] == task.start_floor:
                task.status = FINISHED

    # 线程运行
    def run(self):
        while True:
            self.status_check()
            self.move()
            self.outer_task_check()
            sleep(1)

class myDialog(QDialog):
    def __init__(self):
        super(myDialog, self).__init__()
        self.setStyleSheet(
            'QPushButton{font-weight: bold; border-radius: 5px; border: 2px solid black}'
            'QLabel{font-weight: bold;}'
            'QPushButton:hover{background-color: rgb(150, 150, 150)}'
            'QPushButton:pressed{padding-left:3px; padding-top:3px}'
            'QLineEdit{font-weight: bold}'
        )
        # 标题
        self.setWindowTitle('电梯调度！')
        # 整体网格布局
        grid = QGridLayout()
        # 输入标签
        self.elev_num_text = QLabel('电梯数量', self)
        self.floor_num_text = QLabel('楼层数量', self)
        # 输入框
        self.elev_num_input = QLineEdit('5', self)
        self.floor_num_input = QLineEdit('20', self)
        # 输入限制
        self.elev_num_input.setValidator(QIntValidator(bottom = 0, top = 100))
        self.elev_num_input.setMaxLength(3)
        self.floor_num_input.setValidator(QIntValidator(bottom = 0, top = 500))
        self.floor_num_input.setMaxLength(3)
        # 字体显示
        self.elev_num_text.setFont(QFont("Arial", 16))
        self.floor_num_text.setFont(QFont("Arial", 16))
        self.elev_num_input.setFont(QFont("Arial", 16))
        self.floor_num_input.setFont(QFont("Arial", 16))
        # 全选
        self.elev_num_input.selectAll()
        self.floor_num_input.selectAll()
        # 确认按钮
        self.btn = QPushButton('OK', self)
        self.btn.clicked.connect(self.btn_clicked)
        self.btn.setFont(QFont("Arial", 10))


        grid.addWidget(self.elev_num_text, 0, 0)
        grid.addWidget(self.floor_num_text, 1, 0)

        grid.addWidget(self.elev_num_input, 0, 1)
        grid.addWidget(self.floor_num_input, 1, 1)

        grid.addWidget(self.btn, 2, 0, 1, 2)

        self.setLayout(grid)
        # 设置标志位是否结束程序
        self.exitProgram = True

    def btn_clicked(self):
        global NUM_OF_ELEVATOR
        global NUM_OF_FLOOR
        elev_num_str = self.elev_num_input.text()
        floor_num_str = self.floor_num_input.text()
        if elev_num_str == '' or floor_num_str == '':
            return
        # 修改数量
        NUM_OF_ELEVATOR = int(self.elev_num_input.text())
        NUM_OF_FLOOR = int(self.floor_num_input.text())
        # 隐藏窗口
        self.hide()
    # 点击关闭
    def closeEvent(self, e):
        print('you click to exit the program')
        global GOON
        GOON = False

class myWin(QWidget):
    def __init__(self):
        super(myWin, self).__init__()
        # 定时更新UI界面
        self.timer = QTimer()
        self.setup_UI()

    def setup_UI(self):
        # 样式表
        self.setStyleSheet(
            'QPushButton{border-radius: 10px; border: 2px solid black}'
            'QPushButton:pressed{padding-left:5px; padding-top:5px}'
            'QLCDNumber{background-color: black; color: red; border-radius: 10px}'
            'QLabel{font-weight: bold;}'
            '#mainWindow{background-color: #fded7e}'
            'QScrollArea{background-color: #cee58d}'
        )
        # 标题
        self.setWindowTitle('电梯调度模拟')
        # 窗口名字
        self.setObjectName('mainWindow')
        # 窗口大小
        self.resize(WIDTH, HEIGHT)
        # 网格整体布局
        gridLayout = QGridLayout()

        # 滚动区域中放LCD
        scrollArea_lcd = QScrollArea()
        grid = QGridLayout()
        for i in range(NUM_OF_ELEVATOR):
            # 文本标记哪个电梯
            label = QLabel('Elevator: %d' % i)
            label.setFont(QFont("Microsoft YaHei", 12))
            # 电梯数字显示
            lcd = QLCDNumber(INIT_FLOOR + 1)
            lcd.setDigitCount(len(str(NUM_OF_FLOOR)))
            lcd.setSegmentStyle(QLCDNumber.Flat)
            lcd.setObjectName('elev%d' % i)
            lcd.setMinimumSize(150, 75)
            

            grid.addWidget(label, i // 5 * 2, i % 5)
            grid.addWidget(lcd, i // 5 * 2 + 1, i % 5)
        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: #cee58d')
        scroll_w.setLayout(grid)
        scrollArea_lcd.setWidget(scroll_w)

        # 电梯门
        scrollArea_door = QScrollArea()
        grid = QGridLayout()
        for i in range(NUM_OF_ELEVATOR):
            # 文本标记哪个电梯
            label = QLabel('Elevator: %d' % i)
            label.setFont(QFont("Microsoft YaHei", 12))
            # 电梯door_back显示
            door_back = QLabel()
            door_back.setMinimumSize(150, 75)
            door_back.setStyleSheet('background-color: #6C6C6C;  border: 2px solid black')

            door = QLabel()
            door.setObjectName('%d' % i)
            door.setStyleSheet('background-color: #d0d0d0;  border: 2px solid black;')

            grid.addWidget(label, i // 5 * 2, i % 5)
            grid.addWidget(door_back, i // 5 * 2 + 1, i % 5)
            grid.addWidget(door, i // 5 * 2 + 1, i % 5)
        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: #cee58d')
        scroll_w.setLayout(grid)
        scrollArea_door.setWidget(scroll_w)

        # 电梯选择按钮
        scrollArea_radioButton = QScrollArea()
        grid = QGridLayout()
        for i in range(NUM_OF_ELEVATOR):
            radio = QRadioButton('Elevator: %d' % i)
            radio.setFont(QFont("Microsoft YaHei", 14))
            radio.setObjectName('elev%d' % i)
            grid.addWidget(radio, i // 5, i % 5)
            # 初始为第0个电梯被选中
            if i == 0:
                radio.setChecked(True)
        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: #cee58d')
        scroll_w.setLayout(grid)
        scrollArea_radioButton.setWidget(scroll_w)

        # 电梯内按钮
        scrollArea_btn = QScrollArea()
        grid = QGridLayout()
        # 楼层按钮
        for i in range(NUM_OF_FLOOR):
            btn = QPushButton('%d' % (i + 1))
            btn.setObjectName('%d' % i)
            btn.setFont(QFont("Microsoft YaHei", 14))
            btn.setStyleSheet('background-color: #E1E1E1;')
            btn.setMinimumSize(20, 50)
            btn.clicked.connect(partial(self.floor_btn_clicked, i))
            grid.addWidget(btn, i // 5, i % 5)
        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: #cee58d')
        scroll_w.setLayout(grid)
        scrollArea_btn.setWidget(scroll_w)

        # 开关门按钮 故障按钮 自动产生任务
        scrollArea_btn_feature = QScrollArea()
        grid = QGridLayout()
        # 控件
        btn_open = QPushButton('Open')
        btn_close = QPushButton('Close')
        btn_broken = QPushButton('Broken')
        task_text = QLabel('Random tasks')
        task_num_input = QLineEdit('0')
        btn_task_generate = QPushButton('Generate')
        # 名字
        btn_open.setObjectName('open')
        btn_close.setObjectName('close')
        btn_broken.setObjectName('broken')
        task_num_input.setObjectName('task_num_input')
        btn_task_generate.setObjectName('generate')
        # 大小
        btn_broken.setMinimumSize(120, 40)
        btn_task_generate.setMinimumSize(100, 40)
        # 初始颜色
        btn_open.setStyleSheet('QPushButton{background-color: lightblue}'
            'QPushButton:hover{background-color: lightsteelblue}'
            )
        btn_close.setStyleSheet('QPushButton{background-color: lightblue}'
            'QPushButton:hover{background-color: lightsteelblue}'
            )
        btn_broken.setStyleSheet('QPushButton{background-color: pink}'
            'QPushButton:hover{background-color: hotpink}')
        btn_task_generate.setStyleSheet('QPushButton:hover{background-color: rgb(150, 150, 150)}')
        # 设置字体
        font_size = 10
        btn_open.setFont(QFont("Microsoft YaHei", font_size))
        btn_close.setFont(QFont("Microsoft YaHei", font_size))
        btn_broken.setFont(QFont("Microsoft YaHei", font_size))
        task_text.setFont(QFont("Microsoft YaHei", font_size))
        task_num_input.setFont(QFont("Microsoft YaHei", font_size))
        btn_task_generate.setFont(QFont("Microsoft YaHei", font_size))
        # 输入限制
        task_num_input.setValidator(QIntValidator(bottom = 0, top = (NUM_OF_ELEVATOR * NUM_OF_FLOOR + 2 * (NUM_OF_FLOOR - 1)) // Q))
        # 绑定槽函数
        btn_open.clicked.connect(self.open_animate)
        btn_close.clicked.connect(self.close_animate)
        btn_broken.clicked.connect(self.broken_btn_clicked)
        btn_task_generate.clicked.connect(self.generate_task)
        # 控件大小
        task_num_input.setMaximumWidth(120)
        # 将控件加入网格布局
        grid.addWidget(btn_open, 0, 0)
        grid.addWidget(btn_close, 0, 1)
        grid.addWidget(btn_broken, 1, 0, 1, 2)
        grid.addWidget(task_text, 2, 0, 1, 2)
        grid.addWidget(task_num_input, 3, 0, 1, 1)
        grid.addWidget(btn_task_generate, 3, 1, 1, 1)

        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: #cee58d')
        scroll_w.setLayout(grid)
        scrollArea_btn_feature.setWidget(scroll_w)

        # 电梯外按钮
        scrollArea_outer_btn = QScrollArea()
        grid = QGridLayout()
        for i in range(NUM_OF_FLOOR):
            label = QLabel('%d' % (i + 1))
            btn_up = QPushButton('UP')
            btn_down = QPushButton('DOWN')

            btn_up.setFixedSize(100, 40)
            btn_down.setFixedSize(100, 40)

            btn_up.setObjectName('up%d' % i)
            btn_down.setObjectName('down%d' % i)

            btn_up.setStyleSheet('background-color: #E1E1E1;')
            btn_down.setStyleSheet('background-color: #E1E1E1;')

            btn_up.clicked.connect(partial(self.outer_btn_request, i, RUNNINGUP))
            btn_down.clicked.connect(partial(self.outer_btn_request, i, RUNNINGDOWN))

            label.setFont(QFont("Microsoft YaHei", 10))
            btn_up.setFont(QFont("Microsoft YaHei", 10))
            btn_down.setFont(QFont("Microsoft YaHei", 10))

            grid.addWidget(label, i, 0)
            grid.addWidget(btn_up, i, 1)
            grid.addWidget(btn_down, i, 2)

        scroll_w = QWidget()
        scroll_w.setStyleSheet('background-color: #cee58d')
        scroll_w.setLayout(grid)
        scrollArea_outer_btn.setWidget(scroll_w)

        # 网格布局
        gridLayout.addWidget(scrollArea_lcd, 0, 0, 1, 2)
        gridLayout.addWidget(scrollArea_door, 1, 0, 1, 2)
        gridLayout.addWidget(scrollArea_radioButton, 2, 0, 1, 2)
        gridLayout.addWidget(scrollArea_btn, 3, 0, 1, 1)
        gridLayout.addWidget(scrollArea_btn_feature, 3, 1, 1, 1)
        gridLayout.addWidget(scrollArea_outer_btn, 0, 3, 4, 1)

        self.setLayout(gridLayout)

        # 每隔30ms更新
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def floor_btn_clicked(self, target_floor):
        # 检查是哪个电梯，那个radio被选中了
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                ObjName = radio.objectName()
                elev_id = int(ObjName[4:])
                # 电梯坏了电梯内按钮禁用
                if elevs[elev_id].status != BROKEN:
                    elevs[elev_id].des.add(target_floor)
                    elevs[elev_id].inner_target.add(target_floor)
                    print(ObjName, '添加目标楼层', target_floor)
                    break
                else:
                    # 电梯坏了还想点击内部按钮发出警告
                    QMessageBox.warning(self, '警告', '%s 已经故障' % ObjName)
    
    def broken_btn_clicked(self):
        # 检查是哪个电梯，那个radio被选中了
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                ObjName = radio.objectName()
                elevs[int(ObjName[4:])].status = BROKEN
                # 将LCD显示故障变化
                lcd = self.findChild(QLCDNumber, 'elev%d' % int(ObjName[4:]))
                lcd.display('--')
                print(ObjName, '故障!')
                break
        if self.check_all_broken():
            QMessageBox.warning(self, '电梯故障', '所有电梯均故障!')
         
    def outer_btn_request(self, start_floor, direction):
        # 电梯都故障不加入等待队列
        if self.check_all_broken():
            QMessageBox.warning(self, '电梯故障', '所有电梯均故障!无法调度!')
            return

        # 没有状态的外部任务用于比较是否已经在其中
        temp_task = [(t.start_floor, t.direction) for t in outer_task]
        # 防止重复布置任务
        outer_task_mutex.lock()
        if (start_floor, direction) not in temp_task:
            pcb = PCB(start_floor, WAITING, direction)
            outer_task.append(pcb)
            print(start_floor, '发出', '上行' if direction == RUNNINGUP else '下行')
        outer_task_mutex.unlock()

    # 随机产生任务
    def generate_task(self):
        # 电梯都故障不完成任务
        if self.check_all_broken():
            QMessageBox.warning(self, '电梯故障', '所有电梯均故障!无法生成任务!')
            return

        # 找到输入框内容
        num_str = self.findChild(QLineEdit, 'task_num_input').text()
        if num_str == '':
            return
        # 要求产生任务数量
        num = int(num_str)
        # 检查是否适合实际
        # 还有多少电梯
        cur_elev_num = 0
        for elev in elevs:
            if elev.status != BROKEN:
                cur_elev_num += 1
        # 最多多少个任务，加个阈值
        max_task_num = (cur_elev_num * NUM_OF_FLOOR + 2 * (NUM_OF_FLOOR - 1)) // Q
        # 输入任务太多了
        if num > max_task_num:
            QMessageBox.warning(self, '电梯任务生成警告', '任务过多，请输入不超过%d个的任务' % max_task_num)
            return

        print('随机产生%d个任务' % num)
        # 按照比例分配
        global outer_task
        # 外部任务数量
        outer_task_num = num * 2 * (NUM_OF_FLOOR - 1) // (cur_elev_num * NUM_OF_FLOOR + 2 * (NUM_OF_FLOOR - 1))
        # 分两批次产生外部任务 batch1上 其他下
        outer_task_num_batch_one = outer_task_num // 2
        outer_task_generate = random.sample(range(NUM_OF_FLOOR), outer_task_num_batch_one)
        pcb_list = [PCB(t, WAITING, RUNNINGUP) for t in outer_task_generate]
        # 加入外部任务1
        outer_task.extend(pcb_list)
        # 下行批次
        outer_task_generate = random.sample(range(NUM_OF_FLOOR), outer_task_num - outer_task_num_batch_one)
        pcb_list = [PCB(t, WAITING, RUNNINGDOWN) for t in outer_task_generate]
        # 加入外部任务2
        outer_task.extend(pcb_list)
        outer_task = list(set(outer_task))
        
        # 电梯内部任务生成
        num -= outer_task_num
        # 每个剩下每部电梯
        part_num = num // cur_elev_num
        for elev in elevs:
            # 不管故障电梯分配
            if elev.status == BROKEN:
                continue
            generate_num = part_num
            if part_num <= num < 2 * part_num:
                generate_num = num
            
            inner_task_generate = set(random.sample(range(NUM_OF_FLOOR), generate_num))
            elev.des =  elev.des.union(inner_task_generate)
            elev.inner_target = elev.inner_target.union(inner_task_generate)
            
            num -= part_num
    
    # 更新LCD
    def update_lcd(self):
        # 更新LCD显示电梯楼层
        for i in range(NUM_OF_ELEVATOR):
            lcd = self.findChild(QLCDNumber, 'elev%d' % i)
            lcd.setStyleSheet('background-color: black; color: red; border-radius: 10px')
            # 坏掉不更新
            if elevs[i].status == BROKEN:
                continue
            lcd.display(cur_floor[i] + 1)
    
    # 外部任务调度
    def outer_task_deal(self):
        outer_task_mutex.lock()
        global outer_task
        # 分配任务
        for task in outer_task:
            # 只关注在等待的任务
            if task.status == FINISHED or task.status == RUNNING:
                continue
            # 初始距离为楼层数
            dis = [NUM_OF_FLOOR] * NUM_OF_ELEVATOR
            for i, elev in enumerate(elevs):
                if elev.status == BROKEN:
                    continue
                # 下行顺路
                if elev.status == task.direction and elev.status == RUNNINGDOWN and cur_floor[i] >= task.start_floor:
                    dis[i] = cur_floor[i] - task.start_floor
                # 上行顺路
                elif elev.status == task.direction and elev.status == RUNNINGUP and cur_floor[i] <= task.start_floor:
                    dis[i] = task.start_floor - cur_floor[i]
                # 静止
                elif elev.status == FREE:
                    dis[i] = abs(task.start_floor - cur_floor[i])
                # 刚好在那层，处于开关门状态
                elif elev.status in (PREOPEN, PRECLOSE, OPENING, OPEN, CLOSING) and cur_floor[i] == task.start_floor:
                    dis[i] = 0

            # 选择距离最近的
            idx = dis.index(min(dis))
            elevs[idx].des.add(task.start_floor)
            print('将 %d 请求分配给电梯%d' % (task.start_floor, idx))
            task.status = RUNNING
        # 过滤掉已经完成的
        outer_task = [t for t in outer_task if t.status != FINISHED]
        outer_task_mutex.unlock()

    # 检查所有电梯是否都故障
    def check_all_broken(self):
        # 检查是否所有电梯都故障
        for elev in elevs:
            # 至少有一部电梯没故障就不管
            if elev.status != BROKEN:
                return False
        # 返回True表示都坏了
        return True

    # 更新按钮颜色
    def update_btn(self):
        # 检查是哪个电梯，那个radio被选中了
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                ObjName = radio.objectName()
                elev_id = int(ObjName[4:])
                # 电梯坏了电梯内按钮禁用
                if elevs[elev_id].status != BROKEN:
                    # 将电梯按钮在目标数组中变色，不在的白色
                    for i in range(NUM_OF_FLOOR):
                        btn = self.findChild(QPushButton, '%d' % i)
                        if i in elevs[elev_id].inner_target:
                            btn.setStyleSheet('background-color: yellow')
                        else:
                            btn.setStyleSheet('QPushButton{background-color: #E1E1E1}'
                                'QPushButton:hover{background-color: rgb(150, 150, 150)}')
                    break
        # 外部楼层还没完成的变色
        outer_target_floor_up = [t.start_floor for t in outer_task if t.status != FINISHED and t.direction == RUNNINGUP]
        outer_target_floor_down = [t.start_floor for t in outer_task if t.status != FINISHED and t.direction == RUNNINGDOWN]
        # 外部的按钮
        for i in range(NUM_OF_FLOOR):
            # 上行请求
            if i in outer_target_floor_up:
                btn1 = self.findChild(QPushButton, 'up%d' % i)
                btn1.setStyleSheet('background-color: yellow')
            # 下行请求
            elif i in outer_target_floor_down:
                btn2 = self.findChild(QPushButton, 'down%d' % i)
                btn2.setStyleSheet('background-color: yellow')
            # 没有请求
            else:
                btn1 = self.findChild(QPushButton, 'up%d' % i)
                btn2 = self.findChild(QPushButton, 'down%d' % i)
                btn1.setStyleSheet('QPushButton{background-color: #E1E1E1}'
                                'QPushButton:hover{background-color: rgb(150, 150, 150)}')
                btn2.setStyleSheet('QPushButton{background-color: #E1E1E1}'
                                'QPushButton:hover{background-color: rgb(150, 150, 150)}')
        # 故障按钮
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                ObjName = radio.objectName()
                elev_id = int(ObjName[4:])
                btn = self.findChild(QPushButton, 'broken')
                if elevs[elev_id].status == BROKEN:
                    btn.setStyleSheet('QPushButton{background-color: red}'
            )
                else:
                    btn.setStyleSheet('QPushButton{background-color: pink}'
            'QPushButton:hover{background-color: hotpink}'
            )
                break

        # 随机生成输入按钮
        lineInput = self.findChild(QLineEdit, 'task_num_input')
        lineInput.setStyleSheet('background-color: white')
        btn = self.findChild(QPushButton, 'generate')
        btn.setStyleSheet('QPushButton{background-color: #E1E1E1}'
                'QPushButton:hover{background-color: rgb(150, 150, 150)}')
      
    # 更新界面
    def update(self):
        self.update_lcd()
        self.outer_task_deal()
        self.update_btn()
        self.check_open_close_door()

    # 将电梯设为关门空闲状态
    def set_elev_free(self, elev_id):
        elevs[elev_id].status = FREE
    # 将电梯设为开门状态
    def set_elev_open(self, elev_id):
        elevs[elev_id].status = OPEN

    # 检查是否需要开关门动画
    def check_open_close_door(self):
        for i in range(NUM_OF_ELEVATOR):
            self.elev_open_close_opening(i)

    # 电梯到达楼层开关门函数
    def elev_open_close_opening(self, elev_id):
        if elevs[elev_id].status == PREOPEN:
            door = self.findChild(QLabel, '%d' % elev_id)
                    
            animation = QPropertyAnimation(door, b'geometry', self)
            animation.setDuration(DOOR_OPERATION_TIME)
            animation.setStartValue(door.geometry())
            animation.setEndValue(QRect(door.geometry().x(), door.geometry().y(), 10, 75))
            animation.start()
            elevs[elev_id].status = OPENING
            print('电梯%d 开门于%d层' % (elev_id, cur_floor[elev_id]))
            animation.finished.connect(partial(self.elev_open_close_closing, elev_id))
        elif elevs[elev_id].status == PRECLOSE:
            door = self.findChild(QLabel, '%d' % elev_id)
                    
            animation = QPropertyAnimation(door, b'geometry', self)
            animation.setDuration(DOOR_OPERATION_TIME)
            animation.setStartValue(door.geometry())
            animation.setEndValue(QRect(door.geometry().x(), door.geometry().y(), 150, 75))
            animation.start()
            elevs[elev_id].status = CLOSING
            print('电梯%d 关门于%d层' % (elev_id, cur_floor[elev_id]))
            # 完成时再将电梯设置为空闲状态
            animation.finished.connect(partial(self.elev_open_close_closing, elev_id)) 
    # 开门后的关门
    def elev_open_close_closing(self, elev_id):
        elevs[elev_id].status = OPEN
        elevs[elev_id].status == PRECLOSE
        door = self.findChild(QLabel, '%d' % elev_id)
                
        animation = QPropertyAnimation(door, b'geometry', self)
        animation.setDuration(DOOR_OPERATION_TIME)
        animation.setStartValue(door.geometry())
        animation.setEndValue(QRect(door.geometry().x(), door.geometry().y(), 150, 75))
        animation.start()
        elevs[elev_id].status = CLOSING
        print('电梯%d 关门于%d层' % (elev_id, cur_floor[elev_id]))
        # 完成时再将电梯设置为空闲状态
        animation.finished.connect(partial(self.set_elev_free, elev_id)) 


    # 开门动画
    def open_animate(self):
        # 检查是哪个电梯，那个radio被选中了
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                ObjName = radio.objectName()
                elev_id = int(ObjName[4:])
                # 电梯坏了电梯内按钮禁用
                if elevs[elev_id].status == FREE:
                    door = self.findChild(QLabel, '%d' % elev_id)
                    
                    animation = QPropertyAnimation(door, b'geometry', self)
                    animation.setDuration(DOOR_OPERATION_TIME)
                    animation.setStartValue(door.geometry())
                    animation.setEndValue(QRect(door.geometry().x(), door.geometry().y(), 10, 75))
                    animation.start()
                    elevs[elev_id].status = OPENING
                    print('电梯%d 开门于%d层' % (elev_id, cur_floor[elev_id]))
                    animation.finished.connect(partial(self.set_elev_open, elev_id))
                elif elevs[elev_id].status == BROKEN:
                    # 电梯坏了还想点击内部按钮发出警告
                    QMessageBox.warning(self, '警告', '%s 已经故障' % ObjName)

    # 关门动画
    def close_animate(self):
        # 检查是哪个电梯，那个radio被选中了
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                ObjName = radio.objectName()
                elev_id = int(ObjName[4:])
                # 电梯坏了电梯内按钮禁用
                if elevs[elev_id].status == OPEN:
                    door = self.findChild(QLabel, '%d' % elev_id)
                    
                    animation = QPropertyAnimation(door, b'geometry', self)
                    animation.setDuration(DOOR_OPERATION_TIME)
                    animation.setStartValue(door.geometry())
                    animation.setEndValue(QRect(door.geometry().x(), door.geometry().y(), 150, 75))
                    animation.start()
                    elevs[elev_id].status = CLOSING
                    print('电梯%d 开门于%d层' % (elev_id, cur_floor[elev_id]))
                    # 完成时再将电梯设置为空闲状态
                    animation.finished.connect(partial(self.set_elev_free, elev_id)) 
                elif elevs[elev_id].status == BROKEN:
                    # 电梯坏了还想点击内部按钮发出警告
                    QMessageBox.warning(self, '警告', '%s 已经故障' % ObjName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 首先弹出消息窗口
    dialog = myDialog()
    dialog.exec_()
    # 判断是否继续
    if GOON == True:
        # 打印电梯楼层数量
        print('elevator num: ', NUM_OF_ELEVATOR)
        print('floor num: ', NUM_OF_FLOOR)
        # 电梯当前楼层
        cur_floor = [INIT_FLOOR] * NUM_OF_ELEVATOR
        # 然后生成主界面
        w = myWin()
        # 生成电梯进程
        elevs = [None] * NUM_OF_ELEVATOR
        for i in range(NUM_OF_ELEVATOR):
            elevs[i] = Elevator(i)
            elevs[i].start()

        w.show()
        sys.exit(app.exec_())
    else:
        print('程序结束')