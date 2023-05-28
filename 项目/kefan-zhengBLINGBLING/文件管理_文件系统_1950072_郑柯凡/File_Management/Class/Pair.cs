using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace File_Management
{

    [Serializable]
    public class Pair
    {     
        SymFCB symfcb;
        BasicFCB basicfcb;

        public Pair()
        {
            symfcb = null;
            basicfcb = null;
        }

        public Pair(SymFCB item, BasicFCB file)
        {
            symfcb = item;
            basicfcb = file;
        }

        public SymFCB getSymFCB()
        {
            return symfcb;
        }

        public BasicFCB getBasicFCB()
        {
            return basicfcb;
        }
        
    }
}
