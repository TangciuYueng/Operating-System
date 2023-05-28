using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace FileTest.MyClass
{
    [Serializable]
    public class Manager
    {
        // 最多多少个块
        public static int capacity = 1000000;
        // 磁盘块列表
        private Block[] blocks;
        // 位图管理空余空间
        private bool[] bitMap;
        // 管理位图的指针
        private int bitIdx;

        [JsonConstructor]
        //public Manager()
        public Manager()
        {
            blocks = new Block[capacity];
            bitMap = new bool[capacity];
            bitIdx = 0;
            // 空闲位为true
            for (int i = 0; i < capacity; ++i)
            {
                bitMap[i] = true;
            }
        }
        // 获取某一块的数据
        public string GetBlockData(int idx)
        {
            return blocks[idx].ReadData();
        }
        // 获取某一快
        public Block GetBlock(int idx)
        {
            return blocks[idx];
        }
        // 找到一个空闲块，返回空闲块索引
        public int AllocBlock()
        {
            bitIdx %= capacity;
            int tempIdx = bitIdx;
            while (true)
            {
                // 有空闲块
                if (bitMap[tempIdx])
                {
                    // 找到空位申请新空间
                    blocks[tempIdx] = new Block();
                    // blocks[tempIdx].WriteData(data);
                    bitIdx = tempIdx + 1;
                    return tempIdx;
                }
                // 没有空闲块下一个
                else
                {
                    // 防止越界
                    tempIdx = (tempIdx + 1) % capacity;
                }
                // 找了一圈没找到
                if (tempIdx == bitIdx)
                {
                    break;
                }
            }
            return -1;
        }
        // 删除块数据
        public void remove(int idx)
        {
            System.Diagnostics.Debug.Assert(idx >= 0 && idx < capacity);
            // 数据块直接清除，但索引块还要清除block中的index列表中的所有索引
            bitMap[idx] = true;
            foreach (int index in blocks[idx].GetIndex())
            {
                bitMap[index] = true;
            }
        }
        public void remove(List<int> idx_list)
        {
            foreach (int idx in idx_list)
            {
                // System.Diagnostics.Debug.Assert(idx >= 0 && idx < capacity);
                // bitMap[idx] = true;
                remove(idx);
            }
        }
        // 添加数据，构建索引表
        public IndexTable WriteData(string data)
        {
            IndexTable table = new IndexTable();
            while (data.Length > Block.capacity)
            {
                // 找到空闲块索引
                int emptyIdx = AllocBlock();
                // 保证索引在范围内
                System.Diagnostics.Debug.Assert(emptyIdx >= 0 && emptyIdx < capacity);
                // 写入数据
                blocks[emptyIdx].WriteData(data.Substring(0, Block.capacity));
                // 可以直接添加入数据索引
                if (!table.DataFull())
                {
                    table.AddDataIndex(emptyIdx);
                }
                // 加入索引的索引
                else
                {
                    // 检查是否添加索引成功
                    bool flag = false;
                    // 检查table中的idxIdxList指向的索引块
                    for (int i = 0; i < table.idxIdxList.Count(); ++i)
                    {
                        int idx = table.idxIdxList[i];
                        // 索引块满了下一个
                        if (blocks[idx].IdxFull())
                        {
                            continue;
                        }
                        // 没满继续添加
                        else
                        {
                            blocks[idx].AddIdx(emptyIdx);
                            flag = true;
                            break;
                        }
                    }
                    // 没添加成功，申请新的索引块，并加入table的索引列表
                    if (!flag)
                    {
                        int IdxEmptyIdx = AllocBlock();
                        // 索引块中存储指向数据块的索引
                        blocks[IdxEmptyIdx].AddIdx(emptyIdx);
                        // 将索引块的索引添加入table的索引块的索引列表中
                        System.Diagnostics.Debug.Assert(!table.IdxFull());
                        table.AddIdxIndex(IdxEmptyIdx);
                    }
                }
                data = data.Remove(0, Block.capacity);
            }
            // 剩下的肯定可以装进一个块
            // 找到空闲块索引
            int _emptyIdx = AllocBlock();
            // 保证索引在范围内
            System.Diagnostics.Debug.Assert(_emptyIdx >= 0 && _emptyIdx < capacity);
            // 写入数据
            blocks[_emptyIdx].WriteData(data);
            // 可以直接添加入数据索引
            if (!table.DataFull())
            {
                table.AddDataIndex(_emptyIdx);
            }
            // 加入索引的索引
            else
            {
                // 检查是否添加索引成功
                bool flag = false;
                // 检查table中的idxIdxList指向的索引块
                for (int i = 0; i < table.idxIdxList.Count(); ++i)
                {
                    int idx = table.idxIdxList[i];
                    // 索引块满了下一个
                    if (blocks[idx].IdxFull())
                    {
                        continue;
                    }
                    // 没满继续添加指向数据块的索引
                    else
                    {
                        blocks[idx].AddIdx(_emptyIdx);
                        flag = true;
                        break;
                    }
                }
                // 没添加成功，申请新的索引块，并加入table的索引列表
                if (!flag)
                {
                    int IdxEmptyIdx = AllocBlock();
                    // 索引块中存储指向数据块的索引
                    blocks[IdxEmptyIdx].AddIdx(_emptyIdx);
                    // 将索引块的索引添加入table的索引块的索引列表中
                    System.Diagnostics.Debug.Assert(!table.IdxFull());
                    table.AddIdxIndex(IdxEmptyIdx);
                }
            }


            return table;
        }
    }
}