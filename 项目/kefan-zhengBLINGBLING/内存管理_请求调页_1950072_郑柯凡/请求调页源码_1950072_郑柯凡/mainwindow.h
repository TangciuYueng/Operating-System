#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QTimer>
#include <QMainWindow>
#include <QPushButton>
#include <QProgressBar>
#include <QLabel>
#include <QLCDNumber>
#include <QRadioButton>
#include <QTextEdit>
#include <QMessageBox>
#include <QSlider>
#include <QTime>
#include <ctime>
#include <app.h>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT
private:
    app myApp;
    //操作部分按钮
    QPushButton *singlestep;
    QPushButton *run;
    QPushButton *run20;
    QPushButton *reset;
    QRadioButton *LRU;
    QRadioButton *FIFO;
    //内存显示部分
    QLCDNumber *mainmemory[4];
    QLabel *pagestate[4];
    QLabel *nearvistime[4];
    QLabel *entertime[4];
    //指令显示部分
    QLCDNumber *instruid;
    QLabel *instru;
    QLabel *allinstru;
    QLabel *missprob;
    QLabel *missnum;
    QTextEdit *history;
    QProgressBar *bar;
    QSlider *delayslider;
    QLabel *delaytime;

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
    //更新界面
    void updateinterface();
    void runandupdateUI(int instru);
    void delay(int mesc);

private slots:
    void onpushButton_clicked();
    void onpushButton_2_clicked();
    void onradioButton_clicked();
    void onradioButton_2_clicked();
    void onpushButton_3_clicked();
    void onhorizontalSlider_valueChanged(int value);
    void onpushButton_4_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
