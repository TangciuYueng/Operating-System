#ifndef PAGETABLE_H
#define PAGETABLE_H

//中断位、访问位、修改位在本题中没用
class PageTable
{
private:
    int pageID;
    int interrupt;
    int mainMemoryID;
    int diskMemoryID;
    bool visited;
    bool modify;
public:
    PageTable();
    int getpageID();
    int getinterrupt();
    int getmainMemoryID();
    int getdiskMemoryID();
    bool getvisited();
    bool getmodify();
    void modifypageID(int tar);
    void modifyinterrupt(int tar);
    void modifymainMemoryID(int tar);
    void modifydiskMemoryID(int tar);
    void modifyvisited(int tar);
    void modifymodify(int tar);
};

#endif // PAGETABLE_H
