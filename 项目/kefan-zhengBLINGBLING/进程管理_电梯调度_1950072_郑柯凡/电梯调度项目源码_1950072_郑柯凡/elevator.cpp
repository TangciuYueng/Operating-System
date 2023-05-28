#include "elevator.h"

void Elevator::updateflag()
{
    flag=0;
    for(int i=0;i<20;i++)
    {
        if(in[i]!=0||out[i]!=0)
        {
            flag=1;
        }
    }
}

void Elevator::updatein(int x)
{
    in[x-1]=1;
}

void Elevator::updateout(int x)
{
    out[x-1]=1;
}

void Elevator::updatedirection(int x)
{
    direction=x;
}

void Elevator::updateend()
{
    //向上
    if(direction==1)
    {
        for(int i=0;i<20;i++)
        {
            if(in[i]!=0||out[i]!=0)
            {
                end=i+1;
            }
        }
    }
    //向下
    else if(direction==-1)
    {
        for(int i=19;i>=0;i--)
        {
            if(in[i]!=0||out[i]!=0)
            {
                end=i+1;
            }
        }
    }
    //停留，没有终点
    else if(direction==0)
    {
        end=0;
    }
}

//电梯运行（处理线程）
bool Elevator::run()
{
    //电梯处于运行态
    if(getflag()==1)
    {
        updateend();
        if(nowfloor<=20 && nowfloor>=1)
        {
            //未到达终点
            if(nowfloor!=end)
            {
                //处理中间楼层
                if(in[nowfloor-1]==1||out[nowfloor-1]==1)
                {
                    if(in[nowfloor-1]==1)
                    {
                        in[nowfloor-1]=0;
                    }
                    if(out[nowfloor-1]==1)
                    {
                        out[nowfloor-1]=0;
                    }
                    return 1;
                }
                return 0;
            }
            //到达终点
            else if(nowfloor==end)
            {
                //处理中间楼层
                int tag=0;
                if(in[nowfloor-1]==1||out[nowfloor-1]==1)
                {
                    if(in[nowfloor-1]==1)
                    {
                        in[nowfloor-1]=0;
                    }
                    if(out[nowfloor-1]==1)
                    {
                        out[nowfloor-1]=0;
                    }
                    tag=1;
                }
                //查看是否还有反方向的任务
                updateflag();
                //没有其他任务
                if(getflag()==0)
                {
                    //更新方向为0（停留）
                    updatedirection(0);
                }
                //还有反方向的任务
                else if(getflag()!=0)
                {
                    updatedirection(-getdirection());
                }
                if(tag==1)
                {
                    return 1;
                }
                return 0;
            }
        }
    }
    //电梯处于空闲状态
    else if(getflag()==0)
    {
        //查看有无任务
        int upnum=0;
        int downnum=0;
        for(int j=0;j<20;j++)
        {
            if(in[j]!=0&&j+1!=getnowfloor())
            {
                if(j+1<getnowfloor())
                {
                    downnum++;
                }
                else
                {
                    upnum++;
                }
            }
        }
        //楼上任务数和楼下任务数不等
        if(upnum!=downnum)
        {
            int dir=(upnum>downnum)?1:-1;
            updatedirection(dir);
            updateend();
            updateflag();
        }
        //楼下任务数和楼上任务数相等
        else
        {
            //任务默认向上
            if(upnum!=0)
            {
                updatedirection(1);
                updateend();
                updateflag();
            }
            else
            {
                if(in[nowfloor-1]==1||out[nowfloor-1]==1)
                {
                    if(in[nowfloor-1]==1)
                    {
                        in[nowfloor-1]=0;
                    }
                    if(out[nowfloor-1]==1)
                    {
                        out[nowfloor-1]=0;
                    }
                    return 1;
                }
            }
        }
        return 0;
    }
    else if(getflag()==2||getflag()==3||getflag()==4||getflag()==5||getflag()==6)
    {
        return 1;
    }
    return 0;
}

