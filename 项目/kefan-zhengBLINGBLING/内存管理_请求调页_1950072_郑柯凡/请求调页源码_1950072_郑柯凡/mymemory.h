#ifndef MEMORY_H
#define MEMORY_H
#include<iostream>
using namespace std;

class MyMemory
{
private:
    string memo[10];
    //最近使用的时钟周期
    int nearesttime;
    //被调入时的时钟周期
    int entertime;
    //页号
    int pageid;
public:
    MyMemory();    
    int getpageid();
    int getentertime();
    int getnearesttime();
    string getinstru(int tar);
    void modifymemo(string tar[10]);
    void updatenearesttime(int time);
    void updateentertime(int time);
    void modifypageid(int tar);
};

#endif // MEMORY_H
