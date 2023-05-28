from random import random
from math import ceil, floor
from time import sleep

INSTRUCTION_NUM = 320
INSTRUCTION_PER_PAGE = 10
PAGE_NUM = 4

begin_loop = False
missing_page_num = 0
cur_step = 0
previous_ins_id = None

loop = True

class Page:
    def __init__(self, pid = -1, es = None, rs = None):
        self.page_id = pid
        self.enter_step = es
        self.recent_used_step = rs

pages = [None] * PAGE_NUM

for i in range(PAGE_NUM):
    pages[i] = Page()

def get_next_ins():
    global previous_ins_id
    res = -1
    # 不是第一条
    if previous_ins_id:
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
    print('next idx is %d' % ans)
    return ans

def swap(page_id, algorithm='FIFO'):
    print('将page: %d 换入' % page_id)
    if algorithm == 'FIFO':
        # 找到最先进来的
        min_step = INSTRUCTION_NUM
        target_page = None
        for page in pages:
            if page.enter_step < min_step:
                min_step = page.enter_step
                target_page = page
        pages[pages.index(target_page)] = Page(page_id, cur_step, cur_step)
    else:
        pass

def jump_next(next_ins_id):
    global cur_step, missing_page_num
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
        print('内存中找到 %d, 不用换' % page_id)
        pass
    else:
        missing_page_num += 1
        # 检查内存中是否还可以调入页面
        get_in = False
        for idx, page in enumerate(pages):
            if page.page_id == -1:
                print('有空位')
                pages[idx] = Page(page_id, cur_step, cur_step)
                
                get_in = True
                break
        # 没有空位，需要swap
        if not get_in:
            swap(page_id)

def move_one_step():
    global cur_step, loop
    if cur_step >= INSTRUCTION_NUM:
        print('执行完成')
        loop = False
        return
    
    print('cur step: %d' % cur_step)
    jump_next(get_next_ins())
    cur_step += 1

while loop:
    move_one_step()
    output = [page.page_id for page in pages]
    print('cur step: ', cur_step)
    print('内存页表', output)
    print('缺页率', missing_page_num / cur_step)
    sleep(0.02)