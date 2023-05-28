#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QLCDNumber>
#include <QTimer>
#include <QSlider>
#include <QLabel>
#include <QString>
#include "elevator.h"
#include "pcb.h"
#include "scheduler.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    //调度器
    Scheduler sch;
    //每个楼层的按钮
    QPushButton *fbtn[20][2];
    //每个电梯内部的按钮
    QPushButton *ebtn[5][20];
    //报警器
    QPushButton *alarm[5];
    //运行状态标签
    QLabel *label[5];
    //滑动条
    QSlider *sld[5];
    //每个滑动条底部的数码显示器
    QLCDNumber *lcd[5];
    //更新界面
    void updateMainwindow();
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

//没有信号
signals:
//槽函数
public slots:
    //点击电梯内部按钮
    void in_floor_button_clicked(int ele_id,int floor);
    //点击电梯外部按钮
    void out_floor_button_clicked(int floor,int dir);
    //点击报警按钮
    void alarm_button_clicked(int ele_id);
    void run();

};
#endif // MAINWINDOW_H
