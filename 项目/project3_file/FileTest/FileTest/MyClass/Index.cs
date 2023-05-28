using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FileTest.MyClass
{
    // 可以序列化才能应用于ViewList
    [Serializable]
    public class Index
    {
        // 设计索引可以最多指向max_index个块
        public List<int> idxList;
        public static int capacity = 256;

        public Index ()
        {
            idxList = new List<int>();
        }
        // 添加索引指向块
        public bool AddIdx(int newIdx)
        {
            // 先判断是否还有位置
            if (Full())
            {
                return false;
            }
            idxList.Add(newIdx);
            return true;
        }
        // 是否满了
        public bool Full()
        {
            return idxList.Count() >= capacity;
        }
    }
}
