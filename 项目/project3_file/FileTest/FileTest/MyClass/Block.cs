using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FileTest.MyClass
{
    [Serializable]
    // 物理块
    // 可以存放数据，也可以存放索引
    public class Block
    {
        private char[] info;
        public static int capacity = 16;
        private int Length;
        private Index index;
        public Block()
        {
            info = new char[capacity];
            Length = 0;
            index = new Index();
        }
        // 写数据
        public void WriteData(string data)
        {
            // 确定信息长度
            if (data.Length > capacity)
            {
                Length = capacity;
            }
            else
            {
                Length = data.Length;
            }
            // 写入块中
            for (int i = 0; i < Length; ++i)
            {
                info[i] = data[i];
            }
        }
        // 读数据
        public string ReadData()
        {
            string res = new string(info);
            return res;
        }
        // 设置索引
        public bool AddIdx(int idx)
        {
            if (index.Full())
                return false;
            index.AddIdx(idx);
            return true;
        }
        // 索引是否满了
        public bool IdxFull()
        {
            return index.Full();
        }
        // 返回索引列表
        public List<int> GetIndex()
        {
            return index.idxList;
        }
    }
}
