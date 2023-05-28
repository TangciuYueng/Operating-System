using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{
    //符号目录项
    [Serializable]
    public class SymFCB
    {
        public enum FileType { folder, txt };
        //文件名
        public string fileName;
        //文件号
        public int file_id;
        //文件类型
        public FileType fileType;
        //符号目录项的树结构
        public SymFCB father = null, son = null, next = null, pre = null;
        //计数
        public static int file_counter = 0;

        //构造函数
        public SymFCB()
        {
            this.fileType = FileType.folder;
            this.file_id = file_counter++;
        }

        //赋值构造函数
        public SymFCB(string fileName,FileType fileType)
        {
            this.fileName = fileName;
            this.fileType = fileType;
            this.file_id = file_counter++;
        }

        //添加符号目录项
        public void addSonItem(SymFCB newItem)
        {
            //空文件
            if(this.son == null)
            {
                this.son = newItem;
                newItem.father = this;
            }
            //文件非空
            else
            {
                SymFCB temp = this.son;
                while(temp.next != null)
                {
                    temp = temp.next;
                }
                temp.next = newItem;
                newItem.pre = temp;
            }
        }

        //删除符号目录项
        public void remove()
        {
            if(pre==null)
            {
                father.son = next;
            }
            else if (pre != null)
            {
                pre.next = next;
            }
        }
    }
}
