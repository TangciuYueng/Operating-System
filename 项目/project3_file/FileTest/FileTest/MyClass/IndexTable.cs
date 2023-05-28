using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace FileTest.MyClass
{
    [Serializable]
    // 一个文件对应一个索引表
    // 存储指向数据的以及下一级索引表的索引
    public class IndexTable
    {
        // 指向数据块的索引列表
        public List<int> dataIdxList;
        public static int dataIdxCapacity = 10;
        // 指向索引块的索引列表
        public List<int> idxIdxList;
        public static int idxIdxCapacity = 3;

        public IndexTable()
        {
            // 先只创建指向数据块的索引
            dataIdxList = new List<int>(dataIdxCapacity);
            idxIdxList = new List<int>();
        }
        [JsonConstructor]
        public IndexTable(List<int> dataIdxList, List<int> idxIdxList)
        {
            this.dataIdxList = dataIdxList;
            this.idxIdxList = idxIdxList;
        }
        public void AddDataIndex(int idx)
        {
            dataIdxList.Add(idx);
        }
        public bool DataFull()
        {
            return dataIdxList.Count() >= dataIdxCapacity;
        }
        public void AddIdxIndex(int idx)
        {
            idxIdxList.Add(idx);
        }
        public bool IdxFull()
        {
            return idxIdxList.Count() >= dataIdxCapacity;
        }
        // 返回所有数据块、索引块索引
        public List<int> GetAllIndex()
        {
            if (idxIdxList.Count() != 0)
            {
                return dataIdxList.Concat(idxIdxList).ToList<int>();
            }
            else
            {
                return dataIdxList;
            }
        }
    }
}
