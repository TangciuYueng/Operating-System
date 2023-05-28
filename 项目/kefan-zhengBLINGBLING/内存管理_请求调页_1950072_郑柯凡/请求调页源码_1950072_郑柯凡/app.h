#ifndef APP_H
#define APP_H
#include<iostream>
#include<mymemory.h>
#include<pagetable.h>
#include<viraddress.h>
#include<string.h>
using namespace std;

//三级页表
class app
{
private:
    VirAddress viraddtable[320];
    MyMemory mainmemory[4];
    MyMemory disk[32];
    //页目录（即一级页表）
    int pagecontent[4];
    //二级页表
    int pagetable_2[4][4];
    //三级页表，存储页表结构
    PageTable pagetable_3[4][4][2];
    //已经执行的指令数目
    int allnum;
    //当前内存页号、指令编号及指令
    int curmainpageid;
    int curinstruid;
    string curinstru;
    //记录缺页号
    int misspageid;
    //记录总缺页数目
    int missnum;
    //算法选择
    int algorithm;
public:
    app();
    //初始化
    void init();
    //搜索物理地址（in参数为1，返回对应内存地址的正数,不在内存中返回0；in参数为0，返回对应磁盘地址）
    int searchPhyaddress(VirAddress src,int in);
    //替换算法
    int replace(VirAddress vir);
    //程序运行（搜索指令）
    bool runapp(int instru);
    //获取内存
    MyMemory getmainmemory(int tar);
    //获取缺页状态
    int getmisspageid();
    int getallnum();
    int getmissnum();
    int getcurinstruid();
    int getcurmainpageid();
    string getcurinstru();    
    void modifyalgorithm(int tar);
};

#endif // APP_H
