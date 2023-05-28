using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{
    [Serializable]
    //基本目录项
    public class BasicFCB
    {
        //文件名、大小、类型、路径
        public string name, size, type, path;
        //上次修改时间
        public DateTime modifiedTime;
        //文件号
        public int file_id;
        //每一个文件都有的物理索引表
        public IndexTable indextable;

        //构造函数
        public BasicFCB(string name,string size)
        {
            this.name = name;
            this.size = size;
            this.modifiedTime = DateTime.Now;
            indextable = new IndexTable(); 
        }

        public BasicFCB(SymFCB item,string fatherPath = "")
        {
            name = item.fileName;
            size = "0";
            type = item.fileType.ToString();
            path = fatherPath + '\\' + name;
            file_id = item.file_id;
            indextable = new IndexTable();
            modifiedTime = DateTime.Now;
        }
    }
}
