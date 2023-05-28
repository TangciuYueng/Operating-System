using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{
    //使用位图管理块
    [Serializable]
    public class BitMap
    {
        public static int Capcity = 1000000;
        private Block[] blocks = new Block[Capcity];
        private bool[] bitMap = new bool[Capcity];
        private int bit_id = 0;

        //位图构造函数
        public BitMap()
        {
            //所有块都空闲
            for (int i = 0; i < Capcity; i++)
            {
                bitMap[i] = true;
            }
        }

        //获取某一块的信息
        public string getBlock(int i)
        {
            return blocks[i].getInfo();
        }

        //找到第一个空的块
        public int allocateBlock(string data)
        {
            bit_id %= Capcity;
            int tempPointer = bit_id;
            while (true)
            {
                if (bitMap[tempPointer])
                {
                    blocks[tempPointer] = new Block();
                    blocks[tempPointer].setInfo(data);
                    bit_id = tempPointer + 1;
                    return tempPointer;
                }
                else
                {
                    tempPointer = (tempPointer + 1) % Capcity;
                }
                //遍历一整边还未找到，说明没有空的    
                if (tempPointer == bit_id)
                {
                    break;
                }
            }
            return -1;
        }

        //取出一块
        public void withdraw(int index)
        {
            bitMap[index] = true;
        }

        //取出多块
        public void withdraw(List<int> indexs)
        {
            foreach(int i in indexs)
            {
                bitMap[i] = true;
            }
        }

        //建立一个索引表来保存一个文件块的数字
        public IndexTable write(string data)
        {
            IndexTable table = new IndexTable();
            while (data.Count() > 16)
            {
                // alloc 返回放入数据16字符的块号
                // 将块号加入 文件 对应的 索引表
                table.addIndex(allocateBlock(data.Substring(0, 15)));
                data = data.Remove(0, 15);
            }
            table.addIndex(allocateBlock(data));

            return table;
        }
    }
}
