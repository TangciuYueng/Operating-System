#include "mymemory.h"

MyMemory::MyMemory()
{
    for(int i=0;i<10;i++)
    {
        memo[i]="##########";
    }
    nearesttime = -1;
    entertime=-1;
    pageid=-1;
}

string MyMemory::getinstru(int tar)
{
    return memo[tar];
}

int MyMemory::getnearesttime()
{
    return this->nearesttime;
}

int MyMemory::getentertime()
{
    return this->entertime;
}

int MyMemory::getpageid()
{
    return this->pageid;
}

void MyMemory::modifymemo(string tar[10])
{
    for(int i=0;i<10;i++)
    {
        memo[i]=tar[i];
    }
}

void MyMemory::updatenearesttime(int time)
{
    this->nearesttime=time;
}

void MyMemory::updateentertime(int time)
{
    this->entertime=time;
}

void MyMemory::modifypageid(int tar)
{
    this->pageid=tar;
}
