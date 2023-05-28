using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace File_Management
{
    //文件物理结构_索引组织_综合模式
    [Serializable]
    public class IndexTable
    {
        //一级索引
        private Index primaryindex;
        //二级索引
        private Index secondaryindex;
        //三级索引
        private Index thirdindex;

        //构造函数
        public IndexTable()
        {
            primaryindex = new Index();
        }

        public bool addIndex(int data)
        {
            if (!primaryindex.isfull())
            {
                primaryindex.addIndex(data);              
                if(primaryindex.isfull() == true)
                {
                    secondaryindex = new Index();
                }
            }
            else if (!secondaryindex.isfull())
            {
                secondaryindex.addIndex(data);
                if (secondaryindex.isfull())
                {
                    thirdindex = new Index();
                }
            }
            else if(!thirdindex.isfull())
            {
               thirdindex.addIndex(data);
            }
            else
            {
                return false;
            }
            return true;
        }

        public List<int> ReadTable()
        {
            List<int> content = new List<int>();
            for(int i = 0; i < primaryindex.index_id; i++)
            {
                content.Add(primaryindex.index[i]);
            }
            if(primaryindex != null && primaryindex.isfull())
            {
                for(int j = 0;j < secondaryindex.index_id; j++)
                {
                    content.Add(secondaryindex.index[j]);
                }
            }
            if (secondaryindex != null && secondaryindex.isfull())
            {
                for(int k = 0; k <thirdindex.index_id; k++)
                {
                    content.Add(thirdindex.index[k]);
                }
            }

            return content;
        }
    }
}
