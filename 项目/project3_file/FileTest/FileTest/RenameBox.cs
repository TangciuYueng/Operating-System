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
    }
}
