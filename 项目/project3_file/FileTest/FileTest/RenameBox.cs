using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using FileTest.MyClass;

namespace FileTest
{
    public partial class RenameBox : Form
    {
        private SymFCB sf;
        private BasicFCB bf;
        bool changed;
        public DelegateMethod.delegateFunction CallBack;
        public RenameBox()
        {
            InitializeComponent();
        }
        public RenameBox(SymFCB sf, BasicFCB bf)
        {
            InitializeComponent();
            this.sf = sf;
            this.bf = bf;
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
            bf.name = textBox.Text;
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
