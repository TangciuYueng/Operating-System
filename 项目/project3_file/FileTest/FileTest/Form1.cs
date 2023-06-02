using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Forms;
using FileTest.MyClass;
using Newtonsoft.Json;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using System.Collections;

namespace FileTest
{
    public partial class MainWindow : Form
    {
        // 修改标识
        bool changed;
        // 当前symfcb
        public SymFCB curSymFCB;
        // 根symfcb
        public SymFCB rootSymFCB;
        // 字典fileId -> fcb的映射
        public Dictionary<int, Pair> fileDict;
        // 管理
        public Manager manager;
        // 当前路径
        public string curPath = Path.GetDirectoryName(Path.GetDirectoryName(Directory.GetCurrentDirectory()));
        // 文件显示窗口
        private Dictionary<int, ListViewItem> listTable;
        // 文件树根结点
        TreeNode rootNode;
        // 保存前进方向
        Stack<SymFCB> fileStack;

        public MainWindow()
        {
            InitializeComponent();
            rootSymFCB = new SymFCB("ROOT", "folder");
            curSymFCB = rootSymFCB;
            manager = new Manager();
            fileDict = new Dictionary<int, Pair>();
            fileStack = new Stack<SymFCB>();
            changed = false;

            //BasicFCB rootBasicFCB = new BasicFCB(rootSymFCB, "ROOT");
            //CreateMap(rootSymFCB, rootBasicFCB);

            InitializeView();
        }

        // 初始化界面
        public void InitializeView()
        {
            //初始化列表
            InitializeListView();
            //初始化目录树
            InitializeTreeView();
            // 得到根
            curSymFCB = rootSymFCB;
            cur_path_text.Text = "> ROOT\\";
        }
        // 初始化树形界面
        public void InitializeListView()
        {
            listView.Items.Clear();
        }
        // 初始化列表
        public void InitializeTreeView()
        {
            treeView.Nodes.Clear();
            rootNode = new TreeNode("ROOT");
            treeView.Nodes.Add(rootNode);
            treeView.ExpandAll();
        }
        // 更新界面
        public void UpdateView()
        {
            UpdateTreeView();
            UpdateListView();
        }
        // 更新树形界面
        public void UpdateTreeView()
        {
            treeView.Nodes.Clear();
            rootNode = new TreeNode("ROOT");
            CreateTreeView(rootNode, rootSymFCB);
            treeView.Nodes.Add(rootNode);
            treeView.ExpandAll();
        }
        // 递归函数生成树形界面
        public void CreateTreeView(TreeNode rootNode, SymFCB curFCB)
        {
            foreach (SymFCB child in curFCB.children)
            {
                TreeNode childNode = new TreeNode(child.fileName);
                // 如果是txt设置第二个图标 默认是第一个
                if (child.fileType == "txt")
                {
                    childNode.ImageIndex = 1;
                    childNode.SelectedImageIndex = 1;
                }
                CreateTreeView(childNode, child);
                rootNode.Nodes.Add(childNode);
            }
        }
        // 更新列表界面
        public void UpdateListView()
        {
            listTable = new Dictionary<int, ListViewItem>();
            listView.Items.Clear();
            foreach (SymFCB child in curSymFCB.children)
            {
                BasicFCB file = fileDict[child.fileId].basicFCB;
                ListViewItem item = new ListViewItem(new string[]
                {
                    file.name,
                    file.modifiedTime.ToString(),
                    file.type,
                    file.size
                }, file.type == "folder" ? 0: 1);

                listTable[file.fileId] = item;
                // 加入列表视图
                listView.Items.Add(item);

            }
        }
        // 构建文件号到Pair的映射
        public void CreateMap(SymFCB item, BasicFCB file)
        {
            fileDict[item.fileId] = new Pair(item, file);
        }
        // 检查是否重名
        private string CheckSameName(string fileName, string ext="")
        {
            // 位向量记录结尾数字是否存在
            // BitArray sameNameFile = new BitArray(curSymFCB.children.Count + 1, false);
            List<int> sameNameFile = new List<int>();
            // 在当前目录下找是否有重名
            foreach (SymFCB child in curSymFCB.children)
            {
                // 文件类型不同
                if (!((child.fileType == "folder" && ext == "") || (child.fileType == ext)))
                {
                    continue;
                }
                
                // 去掉最后一个圆括号及其之后的内容，[^\(]* 表示任意不是左括号的字符可以出现 0 次或多次
                string childFileName = Regex.Replace(child.fileName, @"\(\d+\)[^(\(\d+\))]*$", "");
                // 去掉后缀
                childFileName = Regex.Replace(childFileName, String.Format(@"\.{0}", ext), "");

                if (childFileName == fileName)
                {
                    // 获得当前最后一个圆括号，匹配.之前的数字和圆括号
                    Match match1;
                    if (child.fileType == "folder")
                        match1 = Regex.Match(child.fileName, @"\(\d+\)$", RegexOptions.RightToLeft);
                    else
                        match1 = Regex.Match(child.fileName, @"\(\d+\)\.", RegexOptions.RightToLeft);
                    // 没有匹配的第0个
                    if (!match1.Success)
                    {
                        sameNameFile.Add(0);
                        continue;
                    }
                    // 获取括号中的数字
                    Match match2 = Regex.Match(match1.Value, @"\d+");
                    // 数字转换为下标
                    int idx = int.Parse(match2.Value);
                    // 标记为true
                    sameNameFile.Add(idx);
                }
            }
            // 出现重名
            for (int i = 0; i < curSymFCB.children.Count + 1; ++i)
            {
                if (sameNameFile.Contains(i))
                    continue;
                // 找第一个缺的数字，i == 0就不用增加
                if (i != 0)
                    fileName += "(" + i.ToString() + ")";
                break;
            }
            
            return fileName + ((ext == "") ? "" : ("." + ext));
        }

        // 由ListViewItem得到fileId
        public int GetFileId(ListViewItem item)
        {
            foreach (var kv in listTable)
            {
                if (kv.Value.Equals(item))
                {
                    return kv.Key;
                }
            }
            // 找不到
            MessageBox.Show("FILE NOT FOUND");
            return -1;
        }
        // 新建文件
        private void txtToolStripMenuItem_Click(object sender, EventArgs e)
        {
            changed = true;
            string fileName = CheckSameName("NEW TEXT", "txt");
            string fatherPath;
            // 添加到当前目录下的孩子中
            SymFCB newSymFCB = new SymFCB(fileName, "txt");
            curSymFCB.AddChild(newSymFCB);

            BasicFCB father = null;
            if (fileDict.ContainsKey(curSymFCB.fileId))
            {
                father = fileDict[curSymFCB.fileId].basicFCB;
            }
            fatherPath = father == null ? "ROOT" : father.path;
            BasicFCB newFile = new BasicFCB(newSymFCB, fatherPath);
            CreateMap(newSymFCB, newFile);
            UpdateView();
        }
        // 新建文件夹
        private void folderToolStripMenuItem_Click(object sender, EventArgs e)
        {
            changed = true;
            string fileName = CheckSameName("NEW FOLDER");
            string fatherPath;
            // 添加到当前目录下的孩子中
            SymFCB newSymFCB = new SymFCB(fileName, "folder");
            curSymFCB.AddChild(newSymFCB);

            BasicFCB father = null;
            if (fileDict.ContainsKey(curSymFCB.fileId))
            {
                father = fileDict[curSymFCB.fileId].basicFCB;
            }
            fatherPath = father == null ? "ROOT" : father.path;
            BasicFCB newFile = new BasicFCB(newSymFCB, fatherPath);
            CreateMap(newSymFCB, newFile);
            UpdateView();
        }
        // 格式化
        private void formatToolStripMenuItem_Click(object sender, EventArgs e)
        {
            fileDict = new Dictionary<int, Pair>();
            rootSymFCB = new SymFCB("ROOT", "folder");
            curSymFCB = rootSymFCB;
            manager = new Manager();
            fileStack = new Stack<SymFCB>();
            changed = false;
            //BasicFCB rootBasicFCB = new BasicFCB(rootSymFCB, "ROOT");
            //CreateMap(rootSymFCB, rootBasicFCB);

            InitializeView();
        }
        // 删除文件点击响应
        private void deleteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (listView.SelectedItems.Count == 0)
            {
                MessageBox.Show("PLEASE SELECT A FILE OR  FOLDER");
                return;
            }
            // 找到每个item对应的fileId，从而找到对应数据块、索引块的索引
            foreach (ListViewItem item in listView.SelectedItems)
            {
                int fileId = GetFileId(item);
                BasicFCB bf = fileDict[fileId].basicFCB;
                List<int> idxList = bf.indexTable.GetAllIndex();
                // 取消占用标记
                manager.remove(idxList);
                // 删除树形结构中的记录
                curSymFCB.removeChild(fileDict[fileId].symFCB);
                // 映射表中移除
                fileDict.Remove(fileId);
                // 更新视图
                UpdateView();
            }
        }
        // 打开文件点击响应
        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (listView.SelectedItems.Count != 1)
            {
                MessageBox.Show("请选择一个对象");
                return;
            }
            ListViewItem curItem = listView.SelectedItems[0];
            int fileId = GetFileId(curItem);
            OpenFile(fileId);
        }
        // 打开文件的操作
        private void OpenFile(int fileId)
        {
            SymFCB sf = fileDict[fileId].symFCB;
            BasicFCB bf = fileDict[fileId].basicFCB;
            string sizeBefore = bf.size;
            // 根据文件类型判断操作
            if (sf.fileType == "folder")
            {
                // 变换当前视图sym结构根节点
                curSymFCB = sf;
                cur_path_text.Text = "> " + bf.path;
                // 打开文件夹后可以返回
                btn_return.Enabled = true;
                // 打开文件夹后不能前进
                btn_forward.Enabled = false;
                // 打开新的文件把旧的栈中清除
                fileStack.Clear();
                // 变换列表视图
                UpdateListView();
            }
            else if (sf.fileType == "txt")
            {
                TxtInputWindow txtInputWindow = new TxtInputWindow(sf, bf, fileDict, manager, sizeBefore);
                txtInputWindow.Show();
                txtInputWindow.CallBack = UpdateView;
            }
        }
        // 双击列表视图
        private void listView_DoubleClick(object sender, EventArgs e)
        {
            // 选中的不是一个就不响应
            if (listView.SelectedItems.Count != 1)
            {
                return;
            }
            ListViewItem item = listView.SelectedItems[0];
            // 获得文件Id
            int fileId = GetFileId(item);
            // 打开文件操作
            OpenFile(fileId);
        }
        
        // 重命名
        private void renameToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            // 选中不止一个无效
            if (listView.SelectedItems.Count != 1)
            {
                return;
            }
            ListViewItem curItem = listView.SelectedItems[0];
            int fileId = GetFileId(curItem);
            SymFCB sf = fileDict[fileId].symFCB;
            BasicFCB bf = fileDict[fileId].basicFCB;
            RenameBox renameBox = new RenameBox(sf, bf);
            renameBox.Show();
            renameBox.CallBack = UpdateView;
        }
        // 返回上一级按钮
        private void btn_return_Click(object sender, EventArgs e)
        {
            // 是根目录就不返回了
            if (curSymFCB.fileId == rootSymFCB.fileId)
            {
                return;
            }
            // 能返回就一定能前进
            btn_forward.Enabled = true;
            // 加入前进栈
            fileStack.Push(curSymFCB);
            // 返回上一级
            curSymFCB = curSymFCB.father;
            if (curSymFCB.fileId == rootSymFCB.fileId)
            {
                cur_path_text.Text = "> ROOT\\";
                // 根目录下不能返回
                btn_return.Enabled = false;
            }
            else
            {
                cur_path_text.Text = "> " + fileDict[curSymFCB.fileId].basicFCB.path;
            }
            // 更新列表视图
            UpdateListView();
        }
        // 前进按钮
        private void btn_forward_Click(object sender, EventArgs e)
        {
            if (fileStack.Count == 0)
            {
                return;
            }
            curSymFCB = fileStack.Pop();
            if (fileStack.Count == 0)
            {
                btn_forward.Enabled = false;
            }
            cur_path_text.Text = "> " + fileDict[curSymFCB.fileId].basicFCB.path;
            // 能前进必然也能后退
            btn_return.Enabled = true;
            UpdateListView();
        }
        // 加载已有文件
        private void loadToolStripMenuItem_Click(object sender, EventArgs e)
        {
            // 先查看当前目录下有无需要的文件 转换为文件名
            var jsonFileList = new List<string>(Directory.GetFiles(curPath, "*.*").Where(s => s.EndsWith(".dat") || s.EndsWith(".txt")).Select(Path.GetFileName));
            //var jsonFileList = Directory.GetFiles(curPath, "*.json").ToList();
            string[] targetFile = new string[] { "fileDict.dat", "rootSymFCB.dat", "manager.dat", "fileCount.txt" };
            foreach (string file in targetFile)
            {
                // 不包含任何一个目标函数
                if (!jsonFileList.Contains(file))
                {
                    // 弹出窗口提示并退出
                    MessageBox.Show("TARGET FILE NOT FOUND!", "WARNING");
                    return;
                }
            }
            // 加载文件
            LoadData();
            // 检查循环引用
            CheckFather();
            // 更新界面
            UpdateView();
        }
        // 保存当前文件
        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            SaveData();
        }
        // 保存数据
        private void SaveData()
        {
            // 缩进保存
            //var options = new JsonSerializerOptions { WriteIndented = true };
            // 处理循环引用
            /*
            var settings = new JsonSerializerSettings
            {
                PreserveReferencesHandling = PreserveReferencesHandling.Objects,
                Formatting = Formatting.Indented
            };
            
            // 转换为json格式
            //string jsonFileDict = JsonSerializer.Serialize(fileDict, options);
            string jsonFileDict = JsonConvert.SerializeObject(fileDict, settings);
            // 创建一个新文件，若已存在会覆盖
            File.WriteAllText(Path.Combine(curPath, "fileDict.json"), jsonFileDict);
            // 转换为json格式
            //string jsonRootSymFCB = JsonConvert.SerializeObject(rootSymFCB, settings);
            // 创建一个新文件，若已存在会覆盖
            //File.WriteAllText(Path.Combine(curPath, "rootSymFCB.json"), jsonRootSymFCB);
            // 转换为json格式
            string jsonManager = JsonConvert.SerializeObject(manager, settings);
            // 创建一个新文件，若已存在会覆盖
            File.WriteAllText(Path.Combine(curPath, "manager.json"), jsonManager);
            */
            BinaryFormatter bf = new BinaryFormatter();

            var fileDictStream = new FileStream(Path.Combine(curPath, "fileDict.dat"), FileMode.Create);
            bf.Serialize(fileDictStream, fileDict);
            fileDictStream.Close();

            var rootSymFCBStream = new FileStream(Path.Combine(curPath, "rootSymFCB.dat"), FileMode.Create);
            bf.Serialize(rootSymFCBStream, rootSymFCB);
            rootSymFCBStream.Close();

            var managerStream = new FileStream(Path.Combine(curPath, "manager.dat"), FileMode.Create);
            bf.Serialize(managerStream, manager);
            managerStream.Close();

            // int类型直接存入txt文件
            var fileCountStream = new FileStream(Path.Combine(curPath, "fileCount.txt"), FileMode.Create, FileAccess.Write);
            var sw = new StreamWriter(fileCountStream);
            sw.WriteLine(SymFCB.fileCounter.ToString());
            sw.Close();
            fileCountStream.Close();

            // 提示消息
            MessageBox.Show("Save Successfully\n" + curPath, "Tip");
        }   

        private void LoadData()
        {
            /*
            // 处理循环引用
            var settings = new JsonSerializerSettings
            {
                PreserveReferencesHandling = PreserveReferencesHandling.Objects
            };
            // 从文件中读取 反序列化
            string jsonFileDict = File.ReadAllText(Path.Combine(curPath, "fileDict.json"));
            // fileDict = JsonSerializer.Deserialize<Dictionary<int, Pair>>(jsonFileDict);
            JsonConvert.PopulateObject(jsonFileDict, fileDict, settings);
            // fileDict = JsonConvert.DeserializeObject<Dictionary<int, Pair>>(jsonFileDict);
            // 从文件中读取 反序列化
            // string jsonRootSymFCB = File.ReadAllText(Path.Combine(curPath, "rootSymFCB.json"));
            // JsonConvert.PopulateObject(jsonRootSymFCB, rootSymFCB, settings);
            // rootSymFCB = JsonConvert.DeserializeObject<SymFCB>(jsonRootSymFCB);
            // 从文件中读取 反序列化
            string jsonManager = File.ReadAllText(Path.Combine(curPath, "manager.json"));
            JsonConvert.PopulateObject(jsonManager, manager, settings);
            // manager = JsonConvert.DeserializeObject<Manager>(jsonManager);
            */

            BinaryFormatter bf = new BinaryFormatter();

            var fileDictStream = new FileStream(Path.Combine(curPath, "fileDict.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            fileDict = bf.Deserialize(fileDictStream) as Dictionary<int, Pair>;
            fileDictStream.Close();

            var rootSymFCBStream = new FileStream(Path.Combine(curPath, "rootSymFCB.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            rootSymFCB = bf.Deserialize(rootSymFCBStream) as SymFCB;
            rootSymFCBStream.Close();

            var managerStream = new FileStream(Path.Combine(curPath, "manager.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            manager = bf.Deserialize(managerStream) as Manager;
            managerStream.Close();

            // var fileCountStream = new FileStream(Path.Combine(curPath, "fileCount.dat"), FileMode.Open, FileAccess.Read, FileShare.Read);
            // SymFCB.fileCounter = int.Parse(bf.Deserialize(fileCountStream) as string);
            // fileCountStream.Close();
            string res = "";
            using (StreamReader sr = new StreamReader(Path.Combine(curPath, "fileCount.txt")))
            {
                string line;
                while ((line = sr.ReadLine()) != null)
                {
                    res += line;
                }
            }
            SymFCB.fileCounter = int.Parse(res);

            // 初始化
            InitializeView();
            MessageBox.Show("Load successfully", "Tip");
        }
        private void CheckFather()
        {
            foreach (SymFCB child in rootSymFCB.children)
            {
                child.father = rootSymFCB;
            }
        }

        private void MainWindow_FormClosing(object sender, FormClosingEventArgs e)
        {
            // 关闭窗口时弹出消息窗口是否保存
            if (changed && MessageBox.Show("Do you want save the data?", "Tip", MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                SaveData();
            }
        }
        // 关于信息
        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AboutBox aboutBox = new AboutBox();
            aboutBox.Show();
        }
    }
}
