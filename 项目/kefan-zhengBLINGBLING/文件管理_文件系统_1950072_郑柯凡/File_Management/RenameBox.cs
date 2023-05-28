using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace File_Management
{
    public partial class RenameBox : Form
    {
        private BasicFCB renaming_file;
        private SymFCB renaming_fcb;
        public DelegateMethod.delegateFunction CallBack;

        public RenameBox(BasicFCB file,SymFCB fcb)
        {
            InitializeComponent();
            renaming_file = file;
            renaming_fcb = fcb;
        }

        private void InputBox_Closing(object sender, EventArgs e)
        {
            if (MessageBox.Show("是否保存更改?", "提示", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                renaming_file.name = textBox1.Text;
                renaming_fcb.fileName = textBox1.Text;
                renaming_file.modifiedTime= DateTime.Now;
                callBack();
            }
        }

        private void callBack()
        {
            if(CallBack != null)
            {
                this.CallBack();
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void InputBox_Load(object sender, EventArgs e)
        {

        }
    }
}
