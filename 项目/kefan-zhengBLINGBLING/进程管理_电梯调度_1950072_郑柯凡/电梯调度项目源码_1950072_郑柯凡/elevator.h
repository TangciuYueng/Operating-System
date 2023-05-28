#ifndef ELEVATOR_H
#define ELEVATOR_H
#include<iostream>
#include<queue>
#include<string.h>
using namespace std;

//电梯对象
//先调度器分配资源，再更新终点，再运行
class Elevator
{
public:
    //进程状态(0代表空闲，1表示运行,2，3表示开门，4,5,6表示关门，7代表维修)
    int flag;
    //内部按键
    int in[20];
    //外部按键
    int out[20];
    //当前方向的终点
    int end;
    //当前楼层
    int nowfloor;
    //运行方向(1代表向上，-1代表向下，0代表停留)
    int direction;
    Elevator()
    {
        flag=0;
        direction=0;
        end=0;
        nowfloor=1;
        memset(in,0,sizeof(in));
        memset(out,0,sizeof(out));
    };
    ~Elevator(){};
    //返回电梯状态
    int getflag(){return this->flag;}
    //返回电梯运行方向
    int getdirection(){return this->direction;}
    //返回当前楼层
    int getnowfloor(){return this->nowfloor;}
    //更新电梯工作状态
    void updateflag();
    //更新电梯进程
    void updatein(int x);
    void updateout(int x);
    void updatedirection(int x);
    void updateend();
    //电梯运行（处理线程）(每隔1秒调用一次)
    bool run();
};


#endif 
