#include "viraddress.h"

VirAddress::VirAddress()
{
    pageContentID = 0;
    pageTableID2 = 0;
    pageTableID3 = 0;
    pageOffsets = 0;
}

int VirAddress::getpageContentID()
{
    return this->pageContentID;
}

int VirAddress::getpageTableID2()
{
    return this->pageTableID2;
}

int VirAddress::getpageTableID3()
{
    return this->pageTableID3;
}

int VirAddress::getpageOffsets()
{
    return this->pageOffsets;
}

void VirAddress::modifypageContentID(int tar)
{
    this->pageContentID=tar;
}

void VirAddress::modifypageTableID2(int tar)
{
    this->pageTableID2=tar;
}

void VirAddress::modifypageTableID3(int tar)
{
    this->pageTableID3=tar;
}

void VirAddress::modifypageOffsets(int tar)
{
    this->pageOffsets=tar;
}
