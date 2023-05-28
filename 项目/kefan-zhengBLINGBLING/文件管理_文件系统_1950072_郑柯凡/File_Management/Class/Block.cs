using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{
    //存储块
    [Serializable]
    //块
    public class Block
    {
        private char[] info;
        private int length;

        //构造函数
        public Block()
        {
            info = new char[16];
            length = 0;
         }

        //设置块的信息
        public void setInfo(string new_info)
        {
            length = (new_info.Length > 16) ? 16 : new_info.Length;
            for(int i = 0; i < length; i++)
            {
                info[i] = new_info[i];
            }
        }

        //获取块信息
        public string getInfo()
        {
            string temp = new string(info);
            return temp;
        }
    }
}
