## 进程同步
### 临界区问题
- 临界资源(互斥资源)：系统中某些资源一次只允许一个进程使用
- 临界区(互斥区): 进程中设计到临界资源的**程序段**(critical section)
- **使用原则**考点
  - 有空让进
  - 无空等待
  - 多中择一
  - 有限等待
  - 让权等待
    - 处于等待状态的进程应该放弃占用CPU，以便让其他进程有机会得到CPU的使用权，让CPU充分忙起来
    - 以下软件硬件方法都不能做到，共同缺点，因此才会交给OS完成
- 软件方法
  - 基本思路：在进入区检查和设置标志，如果已经有进程在临界区，则在进入区通过循环检查进行等待，在退出区修改标志
  - 总的缺点
    - 忙等待
    - 实现过于复杂
  - 算法1: 单标志位法
    - 公用整形变量turn，如`turn == i`时$P_i$可以进入
    - $P_i$的代码段
    ```c
    while (turn != i);
        critical section
    turn = j;
        remainder section
    ```
    - 缺点 
      - 若不是自己的标志就空循环、忙等待
      - 任务序列为：$P_i, P_i, P_j$第二个就不行了，$P_i, P_j$强制轮流进入临界区，易造成资源利用不充分
  - 算法2: 先检查后修改的双标志位法，很有意义但错误的
    - 标志数组flag[]描述进程是否在临界区内
    - $P_i$的代码段
    ```c
    while (flag[j]);    //<a>
    flag[i] = true;     //<b>
        critical section
    flag[i] = false;
        remainder section
    ```
    - 优点：改进了强制交替进入
    - 缺点：当确定$P_i.<a>$执行完成准备进入$P_i.<b>$时，发生*调度*，这时候发现$P_j.<a>$也可以即将进入$P_j.<b>$，有可能两个进程同时进入临界区
  - 算法3: 先修改后检查的双标志位，同样是调度问题，可能都进不了临界区
    - $P_i$的代码段
    ```c
    flag[i] = true;     //<a>
    while (flag[j]);    //<b>
        critical section
    flag[i] = false;
        remainder section
    ```
  - 算法4: 先修改后检查，后修改者等待
    - 在算法3的基础上结合算法1，正确的
    - $P_i$的代码段
    ```c
    flag[i] = true; turn = j
    while (flag[j] && turn == j);
        critical section
    flag[i] = false;
        remainder section
    ```
    - 这样子就算**后**调度到$P_j.<a>$，也会将`turn = i;`，保证调度回$P_i.<b>$时候知道虽然`flag[j] = true`，但并不是真的进去了，保证算法3两个都进不去的时候有一个可以进去
  - 硬件方法
    - 在硬件层面添加一个指令(原子性分不开)
    - 优点
      - 任意数目进程
      - 简单
      - 支持进程中存在多个临界区
    - 缺点
      - 不能让权等待
      - 存在“饥饿现象”
      - 可能死锁
    - Test-and-Set指令
        ```c
        // 返回lock的值并一直赋给它true
        // 直到别的进程将`lock = false`
        boolean TS(boolean *lock) {
            boolean old;
            old = *lock;
            *lock = true;
            return old;
        }
        ```
      - $P_i$的代码段
        ```c
        while (TS(&lock));
            critical section
        lock = false;
            remainder section
        ```
    - Swap指令
        ```c
        void SWAP(int* a, int* b) {
            int temp = *a;
            *a = *b;
            *b = temp;
        }
        ```
      - $P_i$的代码段
        ```c
        // 每个临界资源设置一个公共布尔变量lock = false;
        // 每个进程设置一个私有布尔变量key
        key = true;
        do {
            SWAP(&lock, key);
        } while (key);
            critical section
        lock = false
        ```
    - 开关中断指令
      - 进入临界区前执行“关中断”指令
      - 离开临界区后执行“开中断”指令
### 进程同步机制
- 同步机制：OS从进程管理者角度来处理进程间**同步&互斥**问题的机制
- 利用信号量(区分不是信号)和P/V两个系统调用处理
- 现在还有更高的封装：管程...
- 信号量(一个P/V处理的数据结构)
    - 表示一类资源有多少个可用(S > 0)or有多少进程在等着用(S < 0)
    ```c
    struct semaphore {
        int value;
        pointer_PCV queue;
    }
    ```
    - 信号量只能通过初始化和P/V原语来访问
    - 访问信号量的进程，不受进程调度的打断
- P/B机制
  - 先运算or先判断都可以，取等号的问题
  - 此时注意S变化之前的值
  - P原语: 申请资源
    - 运算: S = S - 1
    - 判断:   $
                \begin{cases}
                \text{有资源，调用P(S)的进程继续运行 \quad S >= 0} \\
                \text{没资源，进程阻塞，插入等待信号量S的阻塞队列 \quad S < 0} \\
                \end{cases}
              $
      - 由此实现让权等待
  - V原语: 释放资源
    - 运算: S = S + 1
    - 判断:   $
                \begin{cases}
                \text{调用P(S)的进程继续运行 \quad S > 0} \\
                \text{有等待信号量S的进程，从等待信号量S的阻塞队列中选**头一个**进入就绪队列，然后继续运行 \quad S <= 0} \\
                \end{cases}
              $
  - 优缺点
    - 简单，表达能力强
    - 不够安全，使用不当会出现死锁
    - 遇到复杂同步互斥问题时实现复杂
  - P/V操作必须成对出现
    - 互斥->同一进程，mutex初始值设置为正数
      ```cpp
      P(mutex);
        critical section;
      V(mutex);
        remainder section;
      ```
    - 同步->不同进程，mutex初始值设置为0，**V下先P上后**
      ```cpp
      //想要section1完成才能到section2
      //万一先调度到PROCESS2了，就会进入阻塞队列，等到PROCESS1的V完成了，才会进入就绪队列
      // PROCESS1
      section1;
      V(mutex);

      // PROCESS2
      P(mutex);
      section2;
      ```
      
    - 对于不同信号量，两个P/V操作顺序
- 问题分析
  - 哪个资源要协作
  - 哪些进程要协作
  - 进程之间的关系
- 经典问题
  - 生产者-消费者问题
    - 问题描述
      - 若干进程共享有限缓冲区交换数据，缓冲区N个
      - 任何时刻只能有一个进程进行操作
    - 分析
      - 任何一个进程对缓冲区互斥
      - 满的时候消费者先生产者后，同步
      - 空的时候生产者先消费者后，同步
    - 信号量确定
      - full: 使用了多少个缓冲区，初值0，给Producer去增加，Consumer去减少，从而控制0个空闲缓冲区了，Producer先
      - empty: 缓冲区空的数目，初值为N,给Producer去减少，Consumer去增加，从而控制没有空闲缓冲区了，Consumer先
      - mutex访问缓冲区的的互斥
      ```cpp
      // Producer
      P(empty);
      P(mutex);
        add buffer;
      V(mutex);
      V(full);
      // Consumer
      P(full);
      P(mutex);
        remove buffer;
      V(mutex);
      V(empty);
      ```
  - 问题描述
    - 共享一组数据区
    - 多个读者可以同时读
    - 读写互斥
    - 写者之间互斥
  - 分类
    - 第一类: 读者优先，只要有人在读，等待有读有写，让读的先进来，只有没人要读了，写才进来(可能导致写者饥饿)，读旧数据
    - 第二类: 写者优先，只要有人在读，等待有读有写，当前读完，写的先进来，再让要读的进来，读新数据
  - 确定
    - 临界资源readcount: 记录当前多少个读者，初始值为0
    - metex: 读者之间互斥修改readcount，初始值为0
    - w: 读写互斥，初始值为1
    ```cpp
    // reader
    while (true) {
      // 读者互斥访问readcount，增加读者
      P(mutex);
        readcount++;
        // 第一个读者进来才判断是否能读
        // 只要有人在读，剩下进来的读者都能读
        if (readcount == 1)
          P(w);// 不给写者进来，但读者能有就进来
      V(mutex);
      READ();
      // 读完了，减少读者
      P(mutex);
        readconnt--;
        // 没有读者了才释放资源，让写者有机会进入
        if (readcount == 0)
          V(w);// 最后的读者出去了，写者才有机会进来
      V(mutex);
    }

    // writer
    while (true) {
      P(w);
      WRITE();
      V(w);
    }
    ```
  - 第二类读写问题
    ```cpp
    // 加入z信号量保证R信号量的原子性操作，从而使得读写都来了写先进来
    reader:
    P(z);
    P(R);// 写进程进来，新的读只能等
    P(readerCountMutext);
    readerCount++;
    if (readerCount == 1)
      P(RorW);
    V(readerCountMutex);
    V(R);// 以便后续读进程不被阻断
    V(z);

    read();

    P(readerCountMutext);
    readerCount--;
    if (readerCount == 0)
      V(RorW);
    V(readerCountMutex);


    writer:
    P(writerCountMutex);
    writerCount++;
    if (writerCount == 1)
      P(R);// 在这里阻断读进程
    V(writerCountMutex);

    P(RorW);
    write();
    V(RorW);

    P(writerCountMutex);
    writerCount--;
    if (writerCount == 0)
      V(R);// 没有写了才让读进来
    V(writerCountMutex);
    ```
    ```cpp
    // A给B送信，C给D送信，只有一个信箱，一次只能放一封信
    // src: 信箱的互斥，初始值为1
    // s1: B等待A的信才能收，同步
    // s2: D等待B的信才能收，同步
    
    // A
    P(src);// 申请信箱资源
    PUT();
    //V(src); // 这里还不能释放信箱，还没人拿
    V(s1); // 告诉C信放进去了

    // C
    P(s1); // 等待信A的信放入
    GET();
    V(src); // 这时候才能释放信箱资源

    // B
    P(src);
    PUT();
    V(s2);

    // D
    P(s2); // 等待信B的信放入
    GET();
    V(src);
    ```
    ```cpp
    // 独木桥问题
    // 两边通向的在桥上就可以直接过->两个读者
    // 如果限制桥上有K个人，增加Count信号量，初始值为k
    // east_people
    while (true) {
      P(eastCountMutex);
      eastCount++;
      if (eastCount == 1)
        P(bridge);
      V(eastCountMutex);
      
      P(count);
      过桥
      V(count);

      P(eastCountMutext);
      eastCount--;
      if (eastCount == 0)
        V(brige);
      V(eastCountMutext);
    }
    // west_peoplt
    while (true) {
      P(westCountMutex);
      westCount++;
      if (westCount == 1)
        P(bridge);
      V(westCountMutex);

      P(count);
      过桥
      V(count);

      P(westCountMutext);
      westCount--;
      if (westCount == 0)
        V(brige);
      V(westCountMutext);
    }
    ```