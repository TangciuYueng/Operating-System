using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace FileTest.MyClass
{
    [Serializable]
    // 存储树形结构
    public class SymFCB
    {
        public static int fileCounter = 0;
        public string fileName;
        public string fileType;
        public int fileId;
        public SymFCB father;
        public List<SymFCB> children;

        public SymFCB()
        {
            fileType = "folder";
            fileId = fileCounter++;
            father = null;
            children = new List<SymFCB>();
        }
        public SymFCB(string fileName, string fileType)
        {
            this.fileName = fileName;
            this.fileType = fileType;
            fileId = fileCounter++;
            father = null;
            children = new List<SymFCB>();
        }
        [JsonConstructor]
        public SymFCB(string fileName, string fileType, int fileId, SymFCB father, List<SymFCB> children)
        {
            this.fileName = fileName;
            this.fileType = fileType;
            this.fileId = fileId;
            this.father = father;
            this.children = children;
        }
        public void AddChild(SymFCB child)
        {
            children.Add(child);
            child.father = this;
        }

        public void removeChild(SymFCB sf)
        {
            children.Remove(sf);
        }
    }
}