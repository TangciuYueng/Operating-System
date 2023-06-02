using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using FileTest.MyClass;

namespace FileTest
{
    public partial class RenameBox : Form
    {
        private SymFCB sf, curSf;
        private BasicFCB bf;
        bool changed;
        public DelegateMethod.delegateFunction CallBack;
        public RenameBox()
        {
            InitializeComponent();
        }
        public RenameBox(SymFCB sf, BasicFCB bf, SymFCB curSf)
        {
            InitializeComponent();
            this.sf = sf;
            this.bf = bf;
            this.curSf = curSf;
            changed = false;
        }
        private void MyCallBack()
        {
            if (CallBack != null)
            {
                CallBack();
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            changed = true;
        }

        private void RenameBox_FormClosing(object sender, FormClosingEventArgs e)
        {
            // 弹出消息窗口确认是否保存
            if (changed && MessageBox.Show("Do you want to save changes", "Tip", MessageBoxButtons.YesNo)
                == DialogResult.Yes)
            {
                bf.modifiedTime = DateTime.Now;
                bf.name = textBox.Text;
                MyCallBack();
            }
        }

        private void btn_Yes_Click(object sender, EventArgs e)
        {
            // 点击确定直接修改并关闭窗口
            bf.modifiedTime = DateTime.Now;
            string fileName = textBox.Text;
            // 列表记录同名的共多少个
            List<int> sameNameFile = new List<int>();
            // 在当前目录下找是否有重名
            foreach (SymFCB child in curSf.children)
            {
                // 文件类型不同
                if (!(child.fileType == bf.type))
                {
                    continue;
                }

                // 去掉最后一个圆括号及其之后的内容，[^\(]* 表示任意不是左括号的字符可以出现 0 次或多次
                string childFileName = Regex.Replace(child.fileName, @"\(\d+\)[^(\(\d+\))]*$", "");
                // 去掉后缀
                childFileName = Regex.Replace(childFileName, String.Format(@"\.{0}", child.fileType), "");

                if (childFileName == fileName)
                {
                    // 获得当前最后一个圆括号，匹配.之前的数字和圆括号
                    Match match1;
                    if (child.fileType == "folder")
                        match1 = Regex.Match(child.fileName, @"\(\d+\)$", RegexOptions.RightToLeft);
                    else
                        match1 = Regex.Match(child.fileName, @"\(\d+\)\.", RegexOptions.RightToLeft);
                    // 没有匹配的第0个
                    if (!match1.Success)
                    {
                        sameNameFile.Add(0);
                        continue;
                    }
                    // 获取括号中的数字
                    Match match2 = Regex.Match(match1.Value, @"\d+");
                    // 数字转换为下标
                    int idx = int.Parse(match2.Value);
                    // 标记为true
                    sameNameFile.Add(idx);
                }
            }
            // 出现重名
            for (int i = 0; i < curSf.children.Count + 1; ++i)
            {
                if (sameNameFile.Contains(i))
                    continue;
                // 找第一个缺的数字，i == 0就不用增加
                if (i != 0)
                    fileName += "(" + i.ToString() + ")";
                break;
            }
            // 不是文件夹才加后缀
            if (bf.type != "folder")
            {
                fileName += "." + bf.type;
            }
            bf.name = fileName;
            sf.fileName = fileName;
            MyCallBack();
            // 将修改为设置为false标识修改完成已经不需要再消息窗口弹出
            changed = false;
            // 关闭窗口
            Close();
        }

        private void btn_No_Click(object sender, EventArgs e)
        {
            // 点击取消直接关闭窗口
            Close();
        }
        // 判断回车与确定按钮绑定
        private void RenameBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                btn_Yes_Click(sender, e);
            }
        }
    }
}
