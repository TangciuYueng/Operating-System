#include "app.h"
#include <QDebug>

app::app()
{
    for(int i=0;i<4;i++)
    {
        pagecontent[i]=0;
        for(int j=0;j<4;j++)
        {
            pagetable_2[i][j]=0;
        }
    }
    allnum=0;
    curinstruid=-1;
    curinstru="##########";
    curmainpageid=-1;
    misspageid=-1;
    missnum=0;
    algorithm=0;
}

void app::init()
{
    for(int i=0;i<320;i++)
    {
        viraddtable[i].modifypageContentID((i/10)%4);
        viraddtable[i].modifypageTableID2(((i/10)%16)/4);
        viraddtable[i].modifypageTableID3(((i/10)%32)/16);
        viraddtable[i].modifypageOffsets(i%10);
    }
    for(int i=0;i<4;i++)
    {
        string tmpmemo[10];
        for(int j=0;j<10;j++)
        {
            tmpmemo[j]="##########";
        }
        mainmemory[i].modifymemo(tmpmemo);
        mainmemory[i].updateentertime(-1);
        mainmemory[i].updatenearesttime(-1);
        mainmemory[i].modifypageid(-1);
    }
    for(int i=0;i<32;i++)
    {
        string tmpmemo[10];
        for(int j=0;j<10;j++)
        {
            tmpmemo[j]="我是第"+to_string(i*10+j)+"条指令";
        }
        disk[i].modifymemo(tmpmemo);
    }    
    for(int i=0;i<4;i++)
    {
        pagecontent[i]=i;
        for(int j=0;j<4;j++)
        {
            pagetable_2[i][j]=j;
            for(int k=0;k<2;k++)
            {
                pagetable_3[i][j][k].modifypageID(16*k+4*j+i);
                pagetable_3[i][j][k].modifyinterrupt(0);
                pagetable_3[i][j][k].modifymainMemoryID(-1);
                pagetable_3[i][j][k].modifydiskMemoryID(16*k+4*j+i);//页号
                pagetable_3[i][j][k].modifyvisited(0);
                pagetable_3[i][j][k].modifymodify(0);
            }
        }
    }
    allnum=0;
    curinstruid=-1;
    curinstru="##########";
    curmainpageid=-1;
    misspageid=-1;
    missnum=0;
    algorithm=0;
}

int app::searchPhyaddress(VirAddress src,int in)
{
    int i=src.getpageContentID();
    int j=src.getpageTableID2();
    int k=src.getpageTableID3();
    if(in==1)
    {
        return this->pagetable_3[i][j][k].getmainMemoryID();
    }
    else if(in==0)
    {
        return this->pagetable_3[i][j][k].getdiskMemoryID();
    }
    return 0;
}

int app::replace(VirAddress vir)
{
    //找到目标在磁盘中的地址（页号）
    int diskadd=searchPhyaddress(vir,0);
    //找到替换的目标(根据LRU或FIFO)
    int replace=0;
    //LRU
    if(algorithm==0)
    {
        for(int i=1;i<4;i++)
        {
            if(mainmemory[i].getnearesttime()<mainmemory[replace].getnearesttime())
            {
                replace=i;
            }
        }
    }
    //FIFO
    else if(algorithm==1)
    {
        for(int i=1;i<4;i++)
        {
            if(mainmemory[i].getentertime()<mainmemory[replace].getentertime())
            {
                replace=i;
            }
        }
    }
    //修改旧页面的页表信息
    int prepageid=mainmemory[replace].getpageid();
    int o=prepageid%4;
    int p=(prepageid%16)/4;
    int q=(prepageid%32)/16;
    pagetable_3[o][p][q].modifymainMemoryID(-1);
    //交换并更新内存信息
    string tmp[10];
    for(int i=0;i<10;i++)
    {
        tmp[i]=disk[diskadd].getinstru(i);
    }
    mainmemory[replace].modifymemo(tmp);
    mainmemory[replace].modifypageid(diskadd);
    return replace;
}

bool app::runapp(int instru)
{
    if(allnum<320&&instru<320)
    {
        int i=viraddtable[instru].getpageContentID();
        int j=viraddtable[instru].getpageTableID2();
        int k=viraddtable[instru].getpageTableID3();
        curinstruid=instru;
        misspageid=-1;
        int mainmemoadd=searchPhyaddress(viraddtable[instru],1);
        //不在内存中,先替换再输出指令
        if(mainmemoadd==-1)
        {
            //缺页数目加1
            missnum++;
            //页交换
            curmainpageid=replace(viraddtable[instru]);
            curinstru=mainmemory[curmainpageid].getinstru(viraddtable[instru].getpageOffsets());
            mainmemory[curmainpageid].updatenearesttime(allnum);
            mainmemory[curmainpageid].updateentertime(allnum);
            misspageid=curmainpageid;
            //修改页表信息
            pagetable_3[i][j][k].modifymainMemoryID(curmainpageid);
        }
        //在内存中，找到其位置输出
        else if(mainmemoadd!=-1)
        {
            //内存页地址就是mainmemoadd
            curmainpageid=mainmemoadd;
            mainmemory[curmainpageid].updatenearesttime(allnum);
            //指令
            curinstru=mainmemory[mainmemoadd].getinstru(viraddtable[instru].getpageOffsets());
        }
        allnum++;
        return 1;
    }
    else
    {
        return 0;
    }
}

MyMemory app::getmainmemory(int tar)
{
    return this->mainmemory[tar];
}

int app::getmisspageid()
{
    return this->misspageid;
}

int app::getcurmainpageid()
{
    return this->curmainpageid;
}

int app::getcurinstruid()
{
    return this->curinstruid;
}

int app::getmissnum()
{
    return this->missnum;
}

int app::getallnum()
{
    return this->allnum;
}

string app::getcurinstru()
{
    return this->curinstru;
}

void app::modifyalgorithm(int tar)
{
    this->algorithm=tar;
}
