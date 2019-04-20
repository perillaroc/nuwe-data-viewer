# coding: utf-8


def find_node_by_path(root, id_path):
    parent_item = root
    flag = True
    for node_id in id_path:
        current_found = False
        child_count = parent_item.rowCount()
        for i in range(0, child_count):
            child_node = parent_item.child(i)
            if node_id == child_node.node_id:
                parent_item = child_node
                current_found = True
                break

        if not current_found:
            flag = False
            break

    if not flag:
        return None

    return parent_item
