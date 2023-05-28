<template>
  <div class="common-layout">
    <el-container>
      <el-aside>
        <!-- 相关信息的检索 -->
        <h1>作业指令总数</h1>
        <p>{{ totalAssignmentNum }}</p>
        <h1>每页存放指令数</h1>
        <p>{{ instructionPerPage }}</p>
        <h1>作业占用内存页数</h1>
        <p>{{ usePageNum }}</p>
        <h1>页面置换算法</h1>
        <p>FIFO</p>
        <h1>当前执行页数</h1>
        <p>{{ curStep }}</p>
        <h1>缺页数</h1>
        <p>{{ missingPage }}</p>
        <h1>缺页率</h1>
        <p>{{ missingRate }}</p>
        <h1>执行速度(ms)</h1>
        <p>
          <!-- 可以修改指令连续运行的速度 -->
          <el-input
            v-model="timePerExecution"
            style="width: 100px"
            placeholder="默认300"
          />
        </p>
      </el-aside>
      <el-container>
        <el-header>
          <p>
            Author：2052329 方必诚 请求调页存储管理方式模拟
            <el-link
              href="https://github.com/Baokker/page_management_project"
              target="前往github项目首页"
              >项目GitHub源码</el-link
            >
          </p></el-header
        >

        <el-main>
          <el-container>
            <el-aside>
              <!-- 显示实时Memory中情况 -->
              <table>
                <th v-for="m in this.usePageNum" :key="m">
                  <p>第{{ m }}块</p>
                  <p>
                    内存中第{{
                      usePages[m - 1] == undefined ? "XX" : usePages[m - 1]
                    }}块
                  </p>
                </th>

                <tr v-for="i in this.instructionPerPage" :key="i">
                  <td v-for="j in this.usePageNum" :key="j">
                    <el-check-tag
                      size="large"
                      :checked="
                        this.usePages[j - 1] * this.instructionPerPage + i ==
                        this.selectedID
                      "
                      >{{ i }}</el-check-tag
                    >
                  </td>
                </tr>
              </table>

              <p></p>
              <!-- 三个按钮对应执行函数 -->
              <div style="text-align: center">
                <el-button type="primary" @click="moveOneStep"
                  >单步运行</el-button
                >
                <el-button type="warning" @click="moveForward"
                  >{{ continuousExecutionReminder }}连续执行</el-button
                >
                <el-button type="info" @click="reset">重设</el-button>
              </div>
              <p></p>
            </el-aside>
            <el-main>
              <!-- 显示已经执行的命令表格 -->
              <h1>已经执行的命令</h1>
              <el-table :data="outputData" max-height="400px">
                <el-table-column prop="id" label="执行地址" />
                <el-table-column prop="isPageMissing" label="是否缺页" />
                <el-table-column prop="pageOut" label="换出页" />
                <el-table-column prop="pageIn" label="换入页" />
              </el-table>
            </el-main>
          </el-container>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";

export default {
  name: "app",
  data() {
    return {
      // 是否连续执行
      isBeginLoop: false,
      selectedID: undefined,
      // 总共多少条指令
      totalAssignmentNum: 320,
      // 一页中可以装多少条指令
      instructionPerPage: 10,
      // 内存中可用多少页
      usePageNum: 4,
      // 缺失页的数量
      missingPage: 0,
      // 内存中的页的列表
      usePages: [],
      // 上一个执行的指令地址
      lastAddress: undefined,
      // 当前执行步数，也是当前执行的指令数
      curStep: 0, // start from 0
      // 记录页面进入内存顺序
      order: [],
      outputData: [],
      // 连续执行时执行一个指令多少ms
      timePerExecution: 300,
    };
  },
  computed: {
    // 计算属性，实时计算当前缺页率
    missingRate() {
      return this.curStep == 0 ? "XX" : this.missingPage / this.curStep;
    },
    // 计算属性更新第二个按钮上的文字
    continuousExecutionReminder() {
      return this.isBeginLoop ? "暂停" : "开始";
    },
  },
  watch: {
    // 监视输入数据保证为数字，是数字才赋值
    executeSpeed(timePerExecution) {
      if (isNaN(timePerExecution)) {
        this.timePerExecution = timePerExecution;
      }
    },
  },
  methods: {
    // 重开过程
    reset() {
      this.missingPage = 0;
      this.order = [];
      this.usePages = [];
      this.outputData = [];
      this.curStep = 0;
    },
    // 产生下一个地址
    // range: [0,319]
    generateTask() {
      var result;
      if (this.lastAddress != undefined) {
        let proability = Math.random();
        console.log("proability: " + proability);
        if (proability < 0.5) {
          if (this.lastAddress + 1 < this.totalAssignmentNum) {
            result = this.lastAddress + 1;
          } else {
            result = Math.floor(Math.random() * this.totalAssignmentNum);
          }
        } else if (proability >= 0.5 && proability < 0.75) {
          result = Math.floor(
            Math.random() * (this.totalAssignmentNum - this.lastAddress) +
              this.lastAddress
          );
        } else {
          result = Math.floor(Math.random() * this.lastAddress);
        }
      } else {
        result = Math.floor(Math.random() * this.totalAssignmentNum);
      }
      this.lastAddress = result;
      this.selectedID = result;
      return result;
    },
    // 先入先出选择替换的page
    FIFO(pageID) {
      // 删去先进来的，order的第一个
      var index = this.usePages.indexOf(this.order.shift());
      var pre = this.usePages[index];
      // 调换
      this.move(pageID, index);
      return "第" + index.toString() + "块，地址为：" + pre.toString();
    },
    // 方法：将第pageID页转移到memoryID的页面中
    move(pageID, memoryID) {
      console.log("pageID: ", pageID, "memoryID: ", memoryID);
      if (memoryID < 0 || memoryID >= this.usePageNum) {
        alert("out of range !!");
      }
      // 后进来的加入order的最后
      this.order.push(pageID);
      // 加入内存中
      this.usePages[memoryID] = pageID;
      console.log("MOVEEEEE this.usePages[%d]= %d", memoryID, pageID);
    },
    // 跳转到下一个地址
    // 如果没有直接找到，就根据情况
    // 如果usePage未满（最开始），则调入新的页面
    // 否则采用FIFO
    // 同时将数据输出到outputData中
    jumptoNext(nextAddress) {
      let isFound = false;
      // 得到下一个地址 是哪一个页面
      let pageID = Math.floor(nextAddress / this.instructionPerPage);
      // 检查页面是否在内存的页面列表中
      for (var i = 0; i < this.usePages.length; i++)
        if (this.usePages[i] == pageID) isFound = true;

      // 页面在内存中
      if (isFound == true) {
        this.outputData.push({
          id: nextAddress,
          isPageMissing: false,
          pageOut: "-",
          pageIn: "-",
        });
      } else {
        // 在内存中的4个页中找不到当前要执行的指令
        this.missingPage++;
        // false
        // 内存中还可以调页面进来
        if (this.usePages.length < this.usePageNum) {
          this.move(pageID, this.usePages.length);
          this.outputData.push({
            id: nextAddress,
            isPageMissing: true,
            pageOut: "-",
            pageIn: pageID,
          });
        } else {
          // 不能调页面进来
          this.outputData.push({
            id: nextAddress,
            isPageMissing: false,
            pageOut: this.FIFO(pageID),
            pageIn: pageID,
          });
        }
      }
      console.log(
        "nextaddress: " +
          nextAddress +
          " pageID: " +
          pageID +
          " usePages: " +
          this.usePages
      );
    },
    // 移动一步
    moveOneStep() {
      if (this.curStep >= this.totalAssignmentNum) {
        ElMessage.success({
          type: "success",
          message: "执行完毕！",
        });
        return;
      }
      console.log("curstep: " + this.curStep);
      this.jumptoNext(this.generateTask());
      this.curStep++;
    },
    // 连续移动
    // setInterval定时调用
    moveForward() {
      if (this.curStep > this.totalAssignmentNum) {
        ElMessage.success({
          type: "success",
          message: "执行完毕！",
        });
      }
      // 第二个按钮，开始/结束连续执行，利用isBeginLoop true or false控制
      // 结束连续执行
      if (this.isBeginLoop == true) {
        clearInterval(this.timer);
        this.isBeginLoop = false;
      } else {
        // 开始连续执行
        // 每隔this.timePerExecution执行一次this.moveOneStep()
        this.timer = setInterval(() => {
          if (this.curStep < this.totalAssignmentNum) this.moveOneStep();
        }, this.timePerExecution);
        this.isBeginLoop = true;
      }
    },
  },
};
</script>

<style>
h1 {
  text-align: center;
}
p {
  text-align: center;
}
table {
  text-align: center;
  border: 0;
}
.el-header {
  position: relative;
  margin: 10px;
  border: 2px solid #ecf5ff;

  border-radius: 10px;
  -webkit-box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
  -moz-box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
  box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
}
.el-aside {
  color: var(--el-text-color-primary);
  /* background: var(--el-color-primary-light-8); */
  border-radius: 10px;
  margin: 10px;
  border: 2px solid #ecf5ff;

  -webkit-box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
  -moz-box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
  box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
}
.el-main {
  border-radius: 10px;
  margin: 10px;
  border: 2px solid #ecf5ff;

  -webkit-box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
  -moz-box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
  box-shadow: 0px 9px 5px 0px rgba(50, 50, 50, 0.28);
}
body {
  margin: 10px;
}
</style>
