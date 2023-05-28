using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{
    [Serializable]
    //物理结构_单级索引类
    class Index
    {
        public int[] index;
        public int index_id;
        public Index()
        {
            index = new int[100];
            index_id = 0;
        }
        public void addIndex(int data)
        {
            index[index_id] = data;
            index_id++;
        }
        public bool isfull()
        {
            return (index_id >= 100);
        }
    }
}
