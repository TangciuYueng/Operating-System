from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication
import sys

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

def create_tree_widget(node):
    qtree_item = QTreeWidgetItem([str(node.val)])
    for child in node.children:
        child_qtree_item = create_tree_widget(child)
        qtree_item.addChild(child_qtree_item)
    return qtree_item

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree_widget = QTreeWidget()
    root = TreeNode(1)
    child1 = TreeNode(2)
    child2 = TreeNode(3)
    child3 = TreeNode(4)
    grandchild1 = TreeNode(5)
    grandchild2 = TreeNode(6)

    root.add_child(child1)
    root.add_child(child2)
    root.add_child(child3)
    child1.add_child(grandchild1)
    child1.add_child(grandchild2)

    tree_widget.addTopLevelItem(create_tree_widget(root))
    tree_widget.show()
    sys.exit(app.exec_())
