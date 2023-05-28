using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace FileTest.MyClass
{
    [Serializable]
    public class Pair
    {
        public SymFCB symFCB;
        public BasicFCB basicFCB;
        [JsonConstructor]
        public Pair(SymFCB item, BasicFCB file)
        {
            symFCB = item;
            basicFCB = file;
        }
    }
}
