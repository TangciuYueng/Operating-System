using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{
    // 文件目录结构
    [Serializable]
    public class Catalog
    {
        SymFCB root_fcb ;
        
        public Catalog()
        {
            root_fcb = new SymFCB();
        }

        public SymFCB getRootFCB()
        {
            return root_fcb;
        }
    }
}
