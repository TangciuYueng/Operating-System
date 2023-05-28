#include <QTimer>
#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    //控件初始化
    //电梯1
    ebtn[0][0]=ui->pushButton101;
    ebtn[0][1]=ui->pushButton102;
    ebtn[0][2]=ui->pushButton103;
    ebtn[0][3]=ui->pushButton104;
    ebtn[0][4]=ui->pushButton105;
    ebtn[0][5]=ui->pushButton106;
    ebtn[0][6]=ui->pushButton107;
    ebtn[0][7]=ui->pushButton108;
    ebtn[0][8]=ui->pushButton109;
    ebtn[0][9]=ui->pushButton110;
    ebtn[0][10]=ui->pushButton111;
    ebtn[0][11]=ui->pushButton112;
    ebtn[0][12]=ui->pushButton113;
    ebtn[0][13]=ui->pushButton114;
    ebtn[0][14]=ui->pushButton115;
    ebtn[0][15]=ui->pushButton116;
    ebtn[0][16]=ui->pushButton117;
    ebtn[0][17]=ui->pushButton118;
    ebtn[0][18]=ui->pushButton119;
    ebtn[0][19]=ui->pushButton120;
    //电梯2
    ebtn[1][0]=ui->pushButton201;
    ebtn[1][1]=ui->pushButton202;
    ebtn[1][2]=ui->pushButton203;
    ebtn[1][3]=ui->pushButton204;
    ebtn[1][4]=ui->pushButton205;
    ebtn[1][5]=ui->pushButton206;
    ebtn[1][6]=ui->pushButton207;
    ebtn[1][7]=ui->pushButton208;
    ebtn[1][8]=ui->pushButton209;
    ebtn[1][9]=ui->pushButton210;
    ebtn[1][10]=ui->pushButton211;
    ebtn[1][11]=ui->pushButton212;
    ebtn[1][12]=ui->pushButton213;
    ebtn[1][13]=ui->pushButton214;
    ebtn[1][14]=ui->pushButton215;
    ebtn[1][15]=ui->pushButton216;
    ebtn[1][16]=ui->pushButton217;
    ebtn[1][17]=ui->pushButton218;
    ebtn[1][18]=ui->pushButton219;
    ebtn[1][19]=ui->pushButton220;
    //电梯3
    ebtn[2][0]=ui->pushButton301;
    ebtn[2][1]=ui->pushButton302;
    ebtn[2][2]=ui->pushButton303;
    ebtn[2][3]=ui->pushButton304;
    ebtn[2][4]=ui->pushButton305;
    ebtn[2][5]=ui->pushButton306;
    ebtn[2][6]=ui->pushButton307;
    ebtn[2][7]=ui->pushButton308;
    ebtn[2][8]=ui->pushButton309;
    ebtn[2][9]=ui->pushButton310;
    ebtn[2][10]=ui->pushButton311;
    ebtn[2][11]=ui->pushButton312;
    ebtn[2][12]=ui->pushButton313;
    ebtn[2][13]=ui->pushButton314;
    ebtn[2][14]=ui->pushButton315;
    ebtn[2][15]=ui->pushButton316;
    ebtn[2][16]=ui->pushButton317;
    ebtn[2][17]=ui->pushButton318;
    ebtn[2][18]=ui->pushButton319;
    ebtn[2][19]=ui->pushButton320;
    //电梯4
    ebtn[3][0]=ui->pushButton401;
    ebtn[3][1]=ui->pushButton402;
    ebtn[3][2]=ui->pushButton403;
    ebtn[3][3]=ui->pushButton404;
    ebtn[3][4]=ui->pushButton405;
    ebtn[3][5]=ui->pushButton406;
    ebtn[3][6]=ui->pushButton407;
    ebtn[3][7]=ui->pushButton408;
    ebtn[3][8]=ui->pushButton409;
    ebtn[3][9]=ui->pushButton410;
    ebtn[3][10]=ui->pushButton411;
    ebtn[3][11]=ui->pushButton412;
    ebtn[3][12]=ui->pushButton413;
    ebtn[3][13]=ui->pushButton414;
    ebtn[3][14]=ui->pushButton415;
    ebtn[3][15]=ui->pushButton416;
    ebtn[3][16]=ui->pushButton417;
    ebtn[3][17]=ui->pushButton418;
    ebtn[3][18]=ui->pushButton419;
    ebtn[3][19]=ui->pushButton420;
    //电梯5
    ebtn[4][0]=ui->pushButton501;
    ebtn[4][1]=ui->pushButton502;
    ebtn[4][2]=ui->pushButton503;
    ebtn[4][3]=ui->pushButton504;
    ebtn[4][4]=ui->pushButton505;
    ebtn[4][5]=ui->pushButton506;
    ebtn[4][6]=ui->pushButton507;
    ebtn[4][7]=ui->pushButton508;
    ebtn[4][8]=ui->pushButton509;
    ebtn[4][9]=ui->pushButton510;
    ebtn[4][10]=ui->pushButton511;
    ebtn[4][11]=ui->pushButton512;
    ebtn[4][12]=ui->pushButton513;
    ebtn[4][13]=ui->pushButton514;
    ebtn[4][14]=ui->pushButton515;
    ebtn[4][15]=ui->pushButton516;
    ebtn[4][16]=ui->pushButton517;
    ebtn[4][17]=ui->pushButton518;
    ebtn[4][18]=ui->pushButton519;
    ebtn[4][19]=ui->pushButton520;
    //电梯滑块
    sld[0]=ui->verticalSlider_1;
    sld[1]=ui->verticalSlider_2;
    sld[2]=ui->verticalSlider_3;
    sld[3]=ui->verticalSlider_4;
    sld[4]=ui->verticalSlider_5;
    //电梯楼层显示
    lcd[0]=ui->lcdNumber_1;
    lcd[1]=ui->lcdNumber_2;
    lcd[2]=ui->lcdNumber_3;
    lcd[3]=ui->lcdNumber_4;
    lcd[4]=ui->lcdNumber_5;
    //外部楼层按键
    fbtn[0][0]=ui->pushButton1u;
    fbtn[1][0]=ui->pushButton2u;
    fbtn[1][1]=ui->pushButton2d;
    fbtn[2][0]=ui->pushButton3u;
    fbtn[2][1]=ui->pushButton3d;
    fbtn[3][0]=ui->pushButton4u;
    fbtn[3][1]=ui->pushButton4d;
    fbtn[4][0]=ui->pushButton5u;
    fbtn[4][1]=ui->pushButton5d;
    fbtn[5][0]=ui->pushButton6u;
    fbtn[5][1]=ui->pushButton6d;
    fbtn[6][0]=ui->pushButton7u;
    fbtn[6][1]=ui->pushButton7d;
    fbtn[7][0]=ui->pushButton8u;
    fbtn[7][1]=ui->pushButton8d;
    fbtn[8][0]=ui->pushButton9u;
    fbtn[8][1]=ui->pushButton9d;
    fbtn[9][0]=ui->pushButton10u;
    fbtn[9][1]=ui->pushButton10d;
    fbtn[10][0]=ui->pushButton11u;
    fbtn[10][1]=ui->pushButton11d;
    fbtn[11][0]=ui->pushButton12u;
    fbtn[11][1]=ui->pushButton12d;
    fbtn[12][0]=ui->pushButton13u;
    fbtn[12][1]=ui->pushButton13d;
    fbtn[13][0]=ui->pushButton14u;
    fbtn[13][1]=ui->pushButton14d;
    fbtn[14][0]=ui->pushButton15u;
    fbtn[14][1]=ui->pushButton15d;
    fbtn[15][0]=ui->pushButton16u;
    fbtn[15][1]=ui->pushButton16d;
    fbtn[16][0]=ui->pushButton17u;
    fbtn[16][1]=ui->pushButton17d;
    fbtn[17][0]=ui->pushButton18u;
    fbtn[17][1]=ui->pushButton18d;
    fbtn[18][0]=ui->pushButton19u;
    fbtn[18][1]=ui->pushButton19d;
    fbtn[19][1]=ui->pushButton20d;
    //报警器
    alarm[0]=ui->alarm1;
    alarm[1]=ui->alarm2;
    alarm[2]=ui->alarm3;
    alarm[3]=ui->alarm4;
    alarm[4]=ui->alarm5;
    //运行状态显示器
    label[0]=ui->l1;
    label[1]=ui->l2;
    label[2]=ui->l3;
    label[3]=ui->l4;
    label[4]=ui->l5;
    for(int i=0;i<5;i++)
    {
        label[i]->setStyleSheet("QLabel{""font:bold 20px;""color:blue;""}");
        alarm[i]->setStyleSheet("QPushButton{"
                                       "background-color:red;"//背景色）
                                       "border-style:outset;"                  //边框样式（inset/outset）
                                       "border-width:4px;"                     //边框宽度像素
                                       "border-radius:10px;"                   //边框圆角半径像素
                                       "border-color:rgba(255,255,255,30);"    //边框颜色
                                       "font:bold 15px;"                       //字体，字体大小
                                       "color:white;"                //字体颜色
                                       "padding:6px;"                          //填衬
                                       "}"
                    );
    }
    //连接按钮事件和槽函数
    for(int i=0;i<5;i++)
    {
        for(int j=0;j<20;j++)
        {
            connect(ebtn[i][j],&QPushButton::clicked,this,[=](){in_floor_button_clicked(i,j+1);});
        }
    }
    for(int i=0;i<20;i++)
    {
        if(i==0)
        {
            connect(fbtn[i][0],&QPushButton::clicked,this,[=](){out_floor_button_clicked(i+1,1);});
        }
        else if(i==19)
        {
            connect(fbtn[i][1],&QPushButton::clicked,this,[=](){out_floor_button_clicked(i+1,-1);});
        }
        else
        {
            connect(fbtn[i][0],&QPushButton::clicked,this,[=](){out_floor_button_clicked(i+1,1);});
            connect(fbtn[i][1],&QPushButton::clicked,this,[=](){out_floor_button_clicked(i+1,-1);});
        }
    }
    for(int i=0;i<5;i++)
    {
        connect(alarm[i],&QPushButton::clicked,this,[=](){alarm_button_clicked(i);});
    }
    //连接槽函数和时间函数
    QTimer *timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(run()));
    timer->start(1000);
}

void MainWindow::updateMainwindow()
{
    //更新电梯状态
    for(int i=0;i<5;i++)
    {
        if(sch.schedule[i].getflag()==0)
        {
            label[i]->setText("空闲");
            label[i]->setStyleSheet("QLabel{""font:bold 20px;""color:blue;""}");
        }
        else if(sch.schedule[i].getflag()==1)
        {
            label[i]->setText("运行");
            label[i]->setStyleSheet("QLabel{""font:bold 20px;""color:blue;""}");
        }
        else if(sch.schedule[i].getflag()==2||
                sch.schedule[i].getflag()==3)
        {
            label[i]->setText("开门");
            label[i]->setStyleSheet("QLabel{""font:bold 20px;""color:red;""}");
        }
        else if(sch.schedule[i].getflag()==4||
                sch.schedule[i].getflag()==5||
                sch.schedule[i].getflag()==6)
        {
            label[i]->setText("关门");
            label[i]->setStyleSheet("QLabel{""font:bold 20px;""color:red;""}");
        }
        else if(sch.schedule[i].getflag()==10)
        {
            label[i]->setText("维修");
            label[i]->setStyleSheet("QLabel{""font:bold 20px;""color:red;""}");
        }
    }
    //更新滑动条和数码显示屏
    for(int i=0;i<5;i++)
    {
        sld[i]->setValue(sch.schedule[i].getnowfloor());
        lcd[i]->display(sch.schedule[i].getnowfloor());
    }
}

void MainWindow::in_floor_button_clicked(int ele_id,int floor)
{
    sch.schedule[ele_id].updatein(floor);
    ebtn[ele_id][floor-1]->setStyleSheet("background-color: rgb(250, 0, 0)");
}

void MainWindow::out_floor_button_clicked(int floor,int dir)
{
    sch.createPCB(floor,dir);
    int ud=(dir==1)?0:1;
    fbtn[floor-1][ud]->setStyleSheet("background-color: rgb(250, 0, 0)");
}

void MainWindow::alarm_button_clicked(int ele_id)
{
    sld[ele_id]->setStyleSheet("background-color: rgb(250, 0, 0)");
    sch.schedule[ele_id].flag=10;
}

void MainWindow::run()
{
    //给现有pcb分配电梯资源
    sch.dispatch();
    //5部电梯运行，函数外部看是并行处理
    for(int i=0;i<5;i++)
    {
        //查看是否是任务楼层
        if(sch.schedule[i].run()==1)
        {
            if(sch.schedule[i].getflag()==0||sch.schedule[i].getflag()==1)
            {
                sch.schedule[i].flag=2;
            }
            else if(sch.schedule[i].getflag()==2||
                    sch.schedule[i].getflag()==3||
                    sch.schedule[i].getflag()==4||
                    sch.schedule[i].getflag()==5)
            {
                sch.schedule[i].flag+=1;
            }
            else if(sch.schedule[i].getflag()==6)
            {
                sch.schedule[i].updateflag();
            }
            lcd[i]->setPalette(Qt::red);
            //消除相应任务的红色高亮按钮
            ebtn[i][sch.schedule[i].getnowfloor()-1]->setStyleSheet("background-color: rgb(225,225,225)");
            if(sch.schedule[i].getdirection()==0)
            {
                if(sch.schedule[i].getnowfloor()==1)
                {
                    fbtn[sch.schedule[i].getnowfloor()-1][0]->setStyleSheet("background-color: rgb(225,225,225)");
                }
                else if(sch.schedule[i].getnowfloor()==20)
                {
                    fbtn[sch.schedule[i].getnowfloor()-1][1]->setStyleSheet("background-color: rgb(225,225,225)");
                }
                else
                {
                    fbtn[sch.schedule[i].getnowfloor()-1][0]->setStyleSheet("background-color: rgb(225,225,225)");
                    fbtn[sch.schedule[i].getnowfloor()-1][1]->setStyleSheet("background-color: rgb(225,225,225)");
                }
            }
            else
            {
                int dirbtn=(sch.schedule[i].getdirection()==1)?0:1;
                fbtn[sch.schedule[i].getnowfloor()-1][dirbtn]->setStyleSheet("background-color: rgb(225,225,225)");
            }
        }
        else
        {
            lcd[i]->setPalette(Qt::blue);
        }
    }    
    updateMainwindow();
    //沿着当前方向前进一层
    for(int i=0;i<5;i++)
    {
        if(sch.schedule[i].getflag()<2)
        {
            sch.schedule[i].nowfloor+=sch.schedule[i].getdirection();
        }
    }
}



MainWindow::~MainWindow()
{
    delete ui;
}



