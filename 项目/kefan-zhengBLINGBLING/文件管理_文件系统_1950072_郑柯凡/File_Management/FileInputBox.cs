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
    public partial class FileInputBox : Form
    {
        private BasicFCB textBasicFCB;
        private BitMap bitMap = MainWindows.bitMap;
        public DelegateMethod.delegateFunction CallBack;

        public FileInputBox()
        {
            InitializeComponent();
        }

        public FileInputBox(BasicFCB file)
        {
            InitializeComponent();
            textBasicFCB = file;
            showContent();
        }

        private void showContent()
        {
            List<int> indexs = textBasicFCB.indextable.ReadTable();
            string content = "";
            foreach(int i in indexs)
            {
                content += bitMap.getBlock(i);
            }
            richTextBox1.Text = content;
        }

        private void FileEditor_Closing(object sender,EventArgs e)
        {
            if (MessageBox.Show("是否保存更改?", "提示",MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                textBasicFCB.modifiedTime = DateTime.Now;
                writeDisk();
                callBack();
            }
        }

        private void writeDisk()
        {
            string content = richTextBox1.Text;
            textBasicFCB.size = (content.Length * 4).ToString()+"B";
            releaseBlock();
            textBasicFCB.indextable = bitMap.write(content);
        }

        private void callBack()
        {
            if (CallBack != null)
                this.CallBack();
        }

        private void releaseBlock()
        {
            List<int> indexs = textBasicFCB.indextable.ReadTable();
            bitMap.withdraw(indexs);
        }

    }

    public class DelegateMethod
    {
        public delegate void delegateFunction();
    }
}
