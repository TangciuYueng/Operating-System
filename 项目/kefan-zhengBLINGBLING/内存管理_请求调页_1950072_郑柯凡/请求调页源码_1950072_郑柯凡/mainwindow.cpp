#include "mainwindow.h"
#include "ui_mainwindow.h"

//发生替换的内存块有浅红色背景
//通过逻辑地址寻找虚拟地址（若在内存中，返回其内存中的物理地址；若不在内存中，先进行替换再显示替换的内存地址）
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //操作部分
    singlestep=ui->pushButton_2;
    run=ui->pushButton;
    run20=ui->pushButton_4;
    reset=ui->pushButton_3;
    LRU=ui->radioButton;
    FIFO=ui->radioButton_2;
    //内存显示部分
    mainmemory[0]=ui->lcdNumber;
    mainmemory[1]=ui->lcdNumber_2;
    mainmemory[2]=ui->lcdNumber_3;
    mainmemory[3]=ui->lcdNumber_4;
    pagestate[0]=ui->labelsta0;
    pagestate[1]=ui->labelsta1;
    pagestate[2]=ui->labelsta2;
    pagestate[3]=ui->labelsta3;
    nearvistime[0]=ui->nearvis0;
    nearvistime[1]=ui->nearvis1;
    nearvistime[2]=ui->nearvis2;
    nearvistime[3]=ui->nearvis3;
    entertime[0]=ui->entertime0;
    entertime[1]=ui->entertime1;
    entertime[2]=ui->entertime2;
    entertime[3]=ui->entertime3;
    //指令显示部分
    instruid=ui->lcdNumber_5;
    instru=ui->label_4;
    history=ui->textEdit;
    missprob=ui->label_6;
    missnum=ui->label;
    bar=ui->progressBar;
    delayslider=ui->horizontalSlider;
    delaytime=ui->label_14;
    allinstru=ui->label_15;
    //修改控件样式
    for(int i=0;i<4;i++)
    {
        nearvistime[i]->setStyleSheet("border:0.5px solid black;");
        entertime[i]->setStyleSheet("border:0.5px solid black;");
    }
    //初始化
    myApp.init();
    //连接槽函数和函数
    connect(run,&QPushButton::clicked,this,[=](){onpushButton_clicked();});
    connect(run20,&QPushButton::clicked,this,[=](){onpushButton_4_clicked();});
    connect(singlestep,&QPushButton::clicked,this,[=](){onpushButton_2_clicked();});
    connect(reset,&QPushButton::clicked,this,[=](){onpushButton_3_clicked();});
    connect(LRU,&QRadioButton::clicked,this,[=](){onradioButton_clicked();});
    connect(FIFO,&QRadioButton::clicked,this,[=](){onradioButton_2_clicked();});    
    connect(delayslider, SIGNAL(valueChanged(int)), this, SLOT(onhorizontalSlider_valueChanged(int)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::updateinterface()
{
    //更新进度条
    bar->setValue(myApp.getallnum());
    //更新内存块
    for(int i=0;i<4;i++)
    {
        mainmemory[i]->display(myApp.getmainmemory(i).getpageid());
    }
    //更新页状态
    if(myApp.getmisspageid()==-1)
    {
        for(int i=0;i<4;i++)
        {
            mainmemory[i]->setStyleSheet("QLCDNumber{""background:rgb(113,220,232);""}");
            pagestate[i]->setText("正常");
            pagestate[i]->setStyleSheet("QLabel{""font:bold 20px;""color:blue;""}");
        }
    }
    else if(myApp.getmisspageid()!=-1)
    {
        for(int i=0;i<4;i++)
        {
            mainmemory[i]->setStyleSheet("QLCDNumber{""background:rgb(113,220,232);""}");
            pagestate[i]->setText("正常");
            pagestate[i]->setStyleSheet("QLabel{""font:bold 20px;""color:blue;""}");
        }
        pagestate[myApp.getmisspageid()]->setText("缺页调入");
        pagestate[myApp.getmisspageid()]->setStyleSheet("QLabel{""font:bold 20px;""color:red;""}");
        mainmemory[myApp.getcurmainpageid()]->setStyleSheet("QLCDNumber{""background:rgb(238,100,123);""}");
    }
    //更新最近访问时间和调入时间
    for(int i=0;i<4;i++)
    {
        nearvistime[i]->setText(to_string(myApp.getmainmemory(i).getnearesttime()).data());
        entertime[i]->setText(to_string(myApp.getmainmemory(i).getentertime()).data());
    }
    //更新当前指令号和指令
    instruid->display(myApp.getcurinstruid());
    instru->setText(myApp.getcurinstru().data());
    //更新历史记录
    string sta=(myApp.getmisspageid()==-1)?"正常":"缺页";
    string tmp=to_string(myApp.getallnum())+"   "+myApp.getcurinstru()+"    "+sta;
    history->append(tmp.data());
    //更新缺页率
    string tmpstr;
    if(myApp.getallnum()==0)
    {
        tmpstr="0";
    }
    else
    {
        tmpstr=to_string(double(myApp.getmissnum())/myApp.getallnum()*100);
    }
    missprob->setText(("缺页率:"+tmpstr+"%").data());
    missnum->setText(("缺页数:"+to_string(myApp.getmissnum())).data());
    allinstru->setText(("执行数:"+to_string(myApp.getallnum())).data());
    //延时
    delay(delayslider->value());
}

void MainWindow::runandupdateUI(int instru)
{
    myApp.runapp(instru);
    updateinterface();
}

void MainWindow::onpushButton_clicked()
{
    if(myApp.getallnum()>=320)
    {
        QMessageBox::about(this,"提示","程序已执行完毕，请重置");
    }
    else
    {
        //随机地址顺序执行
        srand((unsigned)time(NULL));
        int start=rand()%320;
        runandupdateUI(start);
        runandupdateUI(start+1);
        while(myApp.getallnum()<320)
        {
            //前地址顺序执行
            int addr=rand()%start;
            runandupdateUI(addr);
            runandupdateUI(addr+1);
            //后地址顺序执行
            addr=rand()%(320-myApp.getcurinstruid())+myApp.getcurinstruid();
            start=addr;
            runandupdateUI(addr);
            runandupdateUI(addr+1);
        }
        QMessageBox::about(this,"提示","程序已执行完毕，请重置");
    }
}

void MainWindow::onpushButton_2_clicked()
{
    if(myApp.getallnum()>=320)
    {
        QMessageBox::about(this,"提示","程序已执行完毕，请重置");
    }
    else
    {
        srand((unsigned)time(NULL));
        myApp.runapp(rand()%320);
        updateinterface();
    }
}

void MainWindow::onpushButton_4_clicked()
{
    if(myApp.getallnum()>=320)
    {
        QMessageBox::about(this,"提示","程序已执行完毕，请重置");
    }
    else
    {
        //随机地址顺序执行
        srand((unsigned)time(NULL));
        int random=rand()%320;
        myApp.runapp(random);
        updateinterface();
        myApp.runapp(random+1);
        updateinterface();
        for(int i=0;i<9;i++)
        {
            //前地址顺序执行
            int addr=rand()%random;
            myApp.runapp(addr);
            updateinterface();
            myApp.runapp(addr+1);
            updateinterface();
            //后地址顺序执行
            addr=rand()%(320-myApp.getcurinstruid())+myApp.getcurinstruid();
            random=addr;
            myApp.runapp(addr);
            updateinterface();
            myApp.runapp(addr+1);
            updateinterface();
        }
    }
}

void MainWindow::onpushButton_3_clicked()
{
    myApp.init();
    updateinterface();
    history->clear();
}

void MainWindow::onradioButton_clicked()
{
    myApp.modifyalgorithm(0);
}

void MainWindow::onradioButton_2_clicked()
{
    myApp.modifyalgorithm(1);
}
// aaaa
void MainWindow::delay(int msec)//延时函数
{
    QTime dieTime = QTime::currentTime().addMSecs(msec);
    while( QTime::currentTime() < dieTime )
    QCoreApplication::processEvents(QEventLoop::AllEvents, 100);
}

void MainWindow::onhorizontalSlider_valueChanged(int value)
{
    delaytime->setText((to_string(value)+"ms").data());
}


