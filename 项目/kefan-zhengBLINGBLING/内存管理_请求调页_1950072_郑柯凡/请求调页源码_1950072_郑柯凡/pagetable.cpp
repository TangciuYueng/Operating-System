#include "pagetable.h"

PageTable::PageTable()
{
    pageID = 0;
    interrupt = 0;
    mainMemoryID = -1;
    diskMemoryID = 0;
    visited = false;
    modify = false;
}

int PageTable::getpageID()
{
    return this->pageID;
}

int PageTable::getinterrupt()
{
    return this->interrupt;
}

int PageTable::getmainMemoryID()
{
    return this->mainMemoryID;
}

int PageTable::getdiskMemoryID()
{
    return this->diskMemoryID;
}

bool PageTable::getvisited()
{
    return this->visited;
}

bool PageTable::getmodify()
{
    return this->modify;
}

void PageTable::modifypageID(int tar)
{
    this->pageID=tar;
}

void PageTable::modifyinterrupt(int tar)
{
    this->interrupt=tar;
}

void PageTable::modifymainMemoryID(int tar)
{
    this->mainMemoryID=tar;
}

void PageTable::modifydiskMemoryID(int tar)
{
    this->diskMemoryID=tar;
}

void PageTable::modifyvisited(int tar)
{
    this->visited=tar;
}

void PageTable::modifymodify(int tar)
{
    this->modify=tar;
}
