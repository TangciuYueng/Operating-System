#include "scheduler.h"

void Scheduler::createPCB(int floor,int direction)
{
    //按键的楼层和运行方向
    PCB pcb=PCB(floor,direction);
    all.push(pcb);
}

void Scheduler::dispatch()
{
    int num=all.size();
    while(num>0)
    {
        //遍历就绪队列，根据方向为每个进程分配电梯
        PCB pcb=all.front();
        all.pop();
        //遍历运行的电梯，查看是否可以加入
        //思路（先查看能否加入同方向运行态的电梯，若无再查看有无空闲电梯，若还无，则返回队列等待下次分配）
        for(int i=0;i<5;i++)
        {
            //处于运行态的电梯
            if(schedule[i].getflag()==1)
            {
                //方向都为上
                if(schedule[i].getdirection()==1&&pcb.getdirection()==1)
                {
                    //楼层未错过
                    if(schedule[i].getnowfloor()<=pcb.getstart())
                    {
                        schedule[i].updateout(pcb.getstart());
                        pcb.changestatus();
                        break;
                    }
                }
                //方向都为下
                else if(schedule[i].getdirection()==-1&&pcb.getdirection()==-1)
                {
                    //楼层未错过
                    if(schedule[i].getnowfloor()>=pcb.getstart())
                    {
                        schedule[i].updateout(pcb.getstart());
                        pcb.changestatus();
                        break;
                    }
                }
            }
        }
        //优先考虑离得最近的空闲的电梯
        int nearestele=-1;int maxn=30;
        for(int i=0;i<5;i++)
        {
            //已被分配
            if(pcb.getstatus()==1)
            {
                break;
            }
            if(schedule[i].getflag()==0)
            {
                int dis=abs(schedule[i].getnowfloor()-pcb.getstart());
                if(dis<maxn)
                {
                    maxn=dis;
                    nearestele=i;
                }
            }
        }
        //有符合条件的电梯
        if(nearestele!=-1)
        {
            //计算电梯接人运行方向
            schedule[nearestele].updateout(pcb.getstart());
            //同一层无需移动
            if(schedule[nearestele].getnowfloor()-pcb.getstart()==0)
            {
               pcb.changestatus();
               break;
            }
            int dir=(schedule[nearestele].getnowfloor()-pcb.getstart()<0)?1:-1;
            schedule[nearestele].updatedirection(dir);
            schedule[nearestele].updateflag();
            pcb.changestatus();
        }
        if(pcb.getstatus()==0)
        {
            all.push(pcb);
        }
        num--;
    }
};

