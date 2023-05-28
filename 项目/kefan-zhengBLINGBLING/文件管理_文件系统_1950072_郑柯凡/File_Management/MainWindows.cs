using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Collections.ObjectModel;
using System.Runtime.Serialization.Formatters.Binary;

namespace File_Management
{
    public partial class MainWindows : Form
    {
        //当前符号目录项
        public SymFCB cur_symfcb;
        //文件控制块栈
        Stack<SymFCB> folderStack = new Stack<SymFCB>();
        //目录结构
        Catalog catalog = new Catalog();
        //符号——基本目录对
        public Dictionary<int, Pair> pairtable = new Dictionary<int, Pair>(); 
        //位图（管理空闲区域）
        public static BitMap bitMap = new BitMap();
        //当前路径
        public string curPath = System.IO.Path.GetDirectoryName(System.IO.Path.GetDirectoryName(Directory.GetCurrentDirectory()));
        //文件显示窗口
        private Dictionary<int, ListViewItem> list_table = new Dictionary<int, ListViewItem>();
        //文件树根结点
        TreeNode root_node;

        public MainWindows()
        {
            //初始化组件
            InitializeComponent();
            // 得到根symfcb
            cur_symfcb = catalog.getRootFCB();
            // 加入栈
            folderStack.Push(cur_symfcb);
            //初始化界面
            InitializeWindows();
        }
        
        public void InitializeWindows()
        {
            //初始化列表
            InitializeListView();
            //初始化目录树
            InitializeTreeView();
            // 得到根symFCB
            cur_symfcb = catalog.getRootFCB();
            textBox1.Text = "root\\";
        }

        // 构建文件号 -> SymFCB 和 BasicFCB的映射
        public void map(SymFCB item, BasicFCB file)
        {
            Pair temp = new Pair(item, file);
            pairtable[item.file_id] = temp;
        }

       

        //更新视图
        public void UpdateView()
        {
            //更新目录树界面
            UpdateTreeView();
            //更新文件列表界面
            UpdateListView(cur_symfcb);
        }

        //初始化列表
        public void InitializeListView()
        {
            //列表清空
            listView1.Items.Clear();
        }

        //初始化目录树
        public void InitializeTreeView()
        {
            //目录树清空
            treeView1.Nodes.Clear();
            //添加根节点
            root_node = new TreeNode("root");
            treeView1.Nodes.Add(root_node);
            treeView1.ExpandAll();
        }

        //更新目录树
        public void UpdateTreeView()
        {
            treeView1.Nodes.Clear();
            root_node = new TreeNode("root");
            DFStree(root_node,catalog.getRootFCB());
            treeView1.Nodes.Add(root_node);
            treeView1.ExpandAll();
        }

        //更新列表
        public void UpdateListView(SymFCB item)
        {
            list_table = new Dictionary<int, ListViewItem>();
            listView1.Items.Clear();
            if(item.son != null)
            {
                SymFCB son = item.son;
                do
                {
                    BasicFCB temp = pairtable[son.file_id].getBasicFCB();
                    ListViewItem file = new ListViewItem(new string[]
                    {
                        temp.name,
                        temp.size,
                        temp.type,
                        temp.modifiedTime.ToString()
                    });
                    if (temp.type == "folder")
                        file.ImageIndex = 0;
                    else
                        file.ImageIndex = 1;

                    listMap(temp, file);
                    listView1.Items.Add(file);
                    son = son.next;
                } while (son != null);
            }
        }

        //DFS构造一棵完整的树
        private void DFStree(TreeNode node,SymFCB curFCB)
        {
            if(curFCB.son != null)
            {
                SymFCB son = curFCB.son;
                do
                {
                    if (son.fileType == SymFCB.FileType.folder)
                    {
                        TreeNode new_node = new TreeNode(son.fileName);
                        DFStree(new_node, son);
                        node.Nodes.Add(new_node);
                    }
                    else if(son.fileType == SymFCB.FileType.txt)
                    {
                        TreeNode new_node = new TreeNode(son.fileName);
                        new_node.ImageIndex = 1;
                        node.Nodes.Add(new_node);
                    }
                    son = son.next;
                } while(son != null);
            }
        }

        //判断同一目录下名字是否重复，并生成新的文件名
        private string Checkname(string s,string ext = "")
        {
            SymFCB current_curPath = cur_symfcb.son;
            int counter = 0;
            while(current_curPath != null)
            {
                string[] sArray = current_curPath.fileName.Split('(');
                if (sArray[0] != current_curPath.fileName && sArray[0] == s) 
                {
                    counter++;
                }
                else if (current_curPath.fileName == s + ext)
                {
                    counter++;
                }
                current_curPath = current_curPath.next;
            }
            if(counter > 0)
                s += "(" + counter.ToString() + ")";
            return s + ext;
        }

        private void 打开ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0 )
            {
               current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();

            openClick(current_fcb, current_file);
        }

        //判断打开的是文件还是文件夹
        private void openClick(SymFCB fcb,BasicFCB file)
        {
            switch (fcb.fileType){
                case SymFCB.FileType.folder:
                    cur_symfcb = fcb;
                    folderStack.Push(fcb);
                    textBox1.Text = pairtable[cur_symfcb.file_id].getBasicFCB().path;
                    UpdateListView(fcb);
                    break;
                case SymFCB.FileType.txt:
                    FileInputBox fileEditor = new FileInputBox(file);
                    fileEditor.Show();
                    fileEditor.CallBack = UpdateView;
                    break;
                default:
                    break;
            }
        }

        //新建文件
        private void 文件ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string file_name = Checkname("New text", ".txt");
            string fatherPath;
            //添加一个新的SymFCB
            SymFCB new_fcb = new SymFCB(file_name, SymFCB.FileType.txt);
            cur_symfcb.addSonItem(new_fcb);

            //添加新的BasicFCB
            //创建新的文件路径
            BasicFCB father = null;
            if (pairtable.ContainsKey(cur_symfcb.file_id))
            {
                father = pairtable[cur_symfcb.file_id].getBasicFCB();
            }
            fatherPath = (father == null) ? "root" : father.path;
            BasicFCB new_file = new BasicFCB(new_fcb, fatherPath);
            map(new_fcb, new_file);

            UpdateView();
        }

        //新建文件夹
        private void 文件夹ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string file_name = Checkname("New folder");
            string fatherPath;
            //添加新的 SymFCB
            SymFCB new_fcb = new SymFCB(file_name, SymFCB.FileType.folder);
            cur_symfcb.addSonItem(new_fcb);

            //添加新的 BasicFCB
            //创建文件路径
            BasicFCB father = null;
            if (pairtable.ContainsKey(cur_symfcb.file_id))
            {
                father = pairtable[cur_symfcb.file_id].getBasicFCB();
            }
            fatherPath = (father == null) ? "root" : father.path;
            BasicFCB new_file = new BasicFCB(new_fcb, fatherPath);
            map(new_fcb, new_file);

            UpdateView();
        }

        //删除功能
        private void 删除ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ListViewItem current_item;
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();
            //获取文件块并从位图中删除
            List<int> indexs = current_file.indextable.ReadTable();
            bitMap.withdraw(indexs);
            //删除符号目录项树中的符号目录项
            current_fcb.remove();
            //删除目录中的FCB
           pairtable.Remove(current_fcb.file_id);

            UpdateView();
        }

        
        public void listMap(BasicFCB file, ListViewItem item)
        {
            list_table[file.file_id] = item;
        }
                
        public int getPointer(ListViewItem item)
        {
            if (list_table.ContainsValue(item))
            {
                foreach (KeyValuePair<int, ListViewItem> kvp in list_table)
                {
                    if (kvp.Value.Equals(item))
                        return kvp.Key;
                }
                return -1;
            }
            else
            {
                MessageBox.Show("无法获取地址");
                return -1;
            }
        }


        //文件列表双击
        private void listView_DoubleClick(object sender, EventArgs e)
        {
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();

            openClick(current_fcb, current_file);
        }

        //重命名
        private void 重命名ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();

            RenameBox renameBox = new RenameBox(current_file,current_fcb);
            renameBox.Show();
            renameBox.CallBack = UpdateView;

        }

        //保存文件
        public void saveData()
        {
            FileStream fileStream1, fileStream2, fileStream3;
            BinaryFormatter a = new BinaryFormatter();

            fileStream1 = new FileStream(System.IO.Path.Combine(curPath, "pairTable.dat"), FileMode.Create);
            a.Serialize(fileStream1, pairtable);
            fileStream1.Close();

            fileStream2 = new FileStream(System.IO.Path.Combine(curPath, "catalogTable.dat"), FileMode.Create);
            a.Serialize(fileStream2, catalog);
            fileStream2.Close();

            fileStream3 = new FileStream(System.IO.Path.Combine(curPath, "bitMap.dat"), FileMode.Create);
            a.Serialize(fileStream3, bitMap);
            fileStream3.Close();

            MessageBox.Show("历史数据已保存" , "提示");
        }

        //加载文件
        public void loadData()
        {
            FileStream fileStream1, fileStream2, fileStream3;
            BinaryFormatter b = new BinaryFormatter();

            fileStream1 = new FileStream(System.IO.Path.Combine(curPath, "pairTable.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            pairtable = b.Deserialize(fileStream1) as Dictionary<int, Pair>;
            fileStream1.Close();

            fileStream2 = new FileStream(System.IO.Path.Combine(curPath, "catalogTable.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            catalog = b.Deserialize(fileStream2) as Catalog;
            fileStream2.Close();

            fileStream3 = new FileStream(System.IO.Path.Combine(curPath, "bitMap.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            bitMap = b.Deserialize(fileStream3) as BitMap;
            fileStream3.Close();
            
            InitializeWindows();
            UpdateView();
            MessageBox.Show("文件已加载", "提示");
        }

        //关闭窗口
        public void MainWindows_Closing(object sender, EventArgs e)
        {
            if (MessageBox.Show("是否保存数据?", "提示", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                saveData();
            }
        }

        
        //返回功能
        private void button1_Click(object sender, EventArgs e)
        {
            if (cur_symfcb == catalog.getRootFCB())
                return;
            cur_symfcb = cur_symfcb.father;
            if (cur_symfcb == catalog.getRootFCB())
                textBox1.Text = "root\\";
            else
                textBox1.Text = pairtable[cur_symfcb.file_id].getBasicFCB().path;
            UpdateListView(cur_symfcb);
        }


        //格式化功能
        private void 格式化ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            pairtable = new Dictionary<int, Pair>();
            catalog = new Catalog();
            folderStack = new Stack<SymFCB>();
            bitMap = new BitMap();
            cur_symfcb = catalog.getRootFCB();
            UpdateView();
            InitializeWindows();
        }

        //项目信息
        private void 关于ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            MessageBox.Show("同济大学软件学院\n2019级操作系统文件管理课程项目" +
                "\n1950072 郑柯凡", "关于项目", MessageBoxButtons.OK);
        }

        //加载之前数据
        private void 载入历史文件ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            loadData();
            UpdateView();
        }

        private void 保存ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveData();
        }

        //右击属性
        private void contextMenuStrip1_Opening(object sender, CancelEventArgs e)
        {

        }

        //重命名1
        private void 重命名ToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();

            RenameBox renameBox = new RenameBox(current_file, current_fcb);
            renameBox.Show();
            renameBox.CallBack = UpdateView;

        }


        //删除功能1
        private void 删除ToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            ListViewItem current_item;
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();
            //获取文件块并从位图中删除
            List<int> indexs = current_file.indextable.ReadTable();
            bitMap.withdraw(indexs);
            //删除符号目录项树中的符号目录项
            current_fcb.remove();
            //删除目录中的FCB
            pairtable.Remove(current_fcb.file_id);

            UpdateView();
        }

        //打开
        private void 打开ToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            ListViewItem current_item = new ListViewItem();
            if (listView1.SelectedItems.Count != 0)
            {
                current_item = listView1.SelectedItems[0];
            }
            else
            {
                MessageBox.Show("请选择一个对象");
                return;
            }

            BasicFCB current_file = pairtable[getPointer(current_item)].getBasicFCB();
            SymFCB current_fcb = pairtable[current_file.file_id].getSymFCB();

            openClick(current_fcb, current_file);
        }

    }
}
