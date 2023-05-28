#ifndef PCB_H
#define PCB_H

//进程控制块
//每次在电梯外按键表示创建一个进程
class PCB
{
private:
    int start;
    int direction;
    //进程状态，用于分配资源时使用
    bool status;
public:
    PCB();
    PCB(int x,int d)
    {
        start=x;
        direction=d;
        status=0;
    }
    ~PCB(){};
    //返回楼层
    int getstart(){return this->start;}
    //返回方向
    int getdirection(){return this->direction;}
    //返回状态
    bool getstatus(){return this->status;}
    //修改状态
    void changestatus(){this->status=1;}
};

#endif // PCB_H
