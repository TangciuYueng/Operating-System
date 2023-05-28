using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using FileTest.MyClass;

namespace FileTest
{
    public partial class TxtInputWindow : Form
    {
        // 修改标识
        bool changed;
        // 该文件的FCB
        private BasicFCB bf;
        // 
        private SymFCB sf;
        // 
        private Dictionary<int, Pair> fileDict;
        // 为了管理blocks
        private Manager manager;
        // 编辑前的大小
        private string sizeBefore;
        // ?
        public DelegateMethod.delegateFunction CallBack;

        public TxtInputWindow()
        {
            InitializeComponent();
        }
        public TxtInputWindow(SymFCB sf, BasicFCB bf, Dictionary<int, Pair> fileDict, Manager manager, string sizeBefore)
        {
            InitializeComponent();
            this.bf = bf;
            this.sf = sf;
            this.fileDict = fileDict;
            this.manager = manager;
            // 展示磁盘对应内容
            ShowText();
            // 窗口标题显示文件名
            Text = bf.name;
            // 没修改
            changed = false;
            // 编辑前的大小
            this.sizeBefore = sizeBefore;
        }
        private void ShowText()
        {
            // 得到该文件的所有索引
            List<int> indexList = bf.indexTable.GetAllIndex();
            string text = "";
            foreach (int idx in indexList)
            {
                // 数据块
                if (manager.GetBlock(idx).GetIndex().Count == 0)
                {
                    text += manager.GetBlockData(idx);
                }
                else
                {
                    // 读索引块中索引对应数据块
                    foreach (int index in manager.GetBlock(idx).GetIndex())
                    {
                        text += manager.GetBlockData(index);
                    }
                }
            }
            // 设置到文本
            textBox.Text = text;
        }
        private void WriteData()
        { 
            string text = textBox.Text;
            // 计算文件大小
            string ext = "B";
            long size = text.Length * 4;
            // 单位升级
            /*
            if (size > 1024)
            {
                size /= 1024;
                ext = "KB";
            }
            if (size > 1024)
            {
                size /= 1024;
                ext = "MB";
            }
            */
            bf.size = size.ToString() + ext;
            // 释放之前的磁盘块
            FreeBlock();
            // 重新写数据 返回新的索引表
            bf.indexTable = manager.WriteData(text);
        }
        private void UpdateFile(string sizeBefore, string sizeAfter)
        {
            // 大小差值
            int delta = int.Parse(Regex.Match(sizeAfter, @"\d+").Value)
                - int.Parse(Regex.Match(sizeBefore, @"\d+").Value);
            // 不用改变
            //if (delta == 0)
            //{
            //    return;
            //}
            SymFCB curSf = sf.father;
            // 找到根节点停止
            while (fileDict.ContainsKey(curSf.fileId))
            {
                BasicFCB curBf = fileDict[curSf.fileId].basicFCB;
                curBf.modifiedTime = DateTime.Now;
                int newSize = int.Parse(Regex.Match(curBf.size, @"\d+").Value) + delta;
                curBf.size = newSize.ToString() + 
                   (Regex.Match(curBf.size, @"\D+").Value == "" ? "B" : Regex.Match(curBf.size, @"\D+").Value);

                curSf = curSf.father;
            }
        }

        private void MyCallBack()
        {
            if (CallBack != null)
            {
                CallBack();
            }
        }
        private void FreeBlock()
        {
            // 得到索引表中所有索引
            List<int> indexList = bf.indexTable.GetAllIndex();
            // 删除索引表以及索引数据
            manager.remove(indexList);
        }

        private void TxtInputWindow_FormClosing(object sender, FormClosingEventArgs e)
        {
            // 弹出消息窗口确认是否保存
            if (changed && MessageBox.Show("Do you want to save changes", "Tip", MessageBoxButtons.YesNo)
                == DialogResult.Yes)
            {
                bf.modifiedTime = DateTime.Now;
                WriteData();
                UpdateFile(sizeBefore, bf.size);
                MyCallBack();
            }
        }
        // 改变后加个星星 才要保存
        private void textBox_TextChanged(object sender, EventArgs e)
        {
            // 没有修改过才加星星
            if (!changed)
            {
                Text += "*";
                changed = true;
            }
            
        }
    }
    public class DelegateMethod
    {
        public delegate void delegateFunction();
    }
}
