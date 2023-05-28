using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace FileTest.MyClass
{
    [Serializable]
    // 存储实际文件相关信息
    public class BasicFCB
    {
        public int fileId;
        public string name, type, size, path;
        public DateTime modifiedTime;
        public IndexTable indexTable;

        public BasicFCB(string name, string size)
        {
            this.name = name;
            this.size = size;
            modifiedTime = DateTime.Now;
            indexTable = new IndexTable();
        }
        public BasicFCB(SymFCB sf, string fatherPath="")
        {
            name = sf.fileName;
            size = "0";
            type = sf.fileType;
            path = fatherPath + "\\" + name;
            fileId = sf.fileId;
            indexTable = new IndexTable();
            modifiedTime = DateTime.Now;
        }
        [JsonConstructor]
        public BasicFCB(int fileId, string name, string type, 
            string size, string path, DateTime modifiedTime, 
            IndexTable indexTable)
        {
            this.fileId = fileId;
            this.name = name;
            this.type = type;
            this.size = size;
            this.path = path;
            this.modifiedTime = modifiedTime;
            this.indexTable = indexTable;
        }
    }
}
