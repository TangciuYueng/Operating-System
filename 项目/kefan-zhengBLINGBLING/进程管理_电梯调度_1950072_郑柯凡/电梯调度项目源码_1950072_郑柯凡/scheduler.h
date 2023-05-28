#ifndef SCHEDULER_H
#define SCHEDULER_H
#include "pcb.h"
#include "elevator.h"

//调度器
class Scheduler
{
public:
    Elevator schedule[5];
    queue<PCB>all;
    Scheduler(){};
    ~Scheduler(){};
    //对现有进程进行分配(每隔0.3调用一次)
    void dispatch();
    //外部按键亮，创建一个进程
    void createPCB(int floor,int direction);
};

#endif // SCHEDULER_H

