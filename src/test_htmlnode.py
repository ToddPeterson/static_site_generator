import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("a", "Testing", [], {"href": "www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Testing")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"href": "www.google.com"})

    def test_no_props(self):
        node = HTMLNode()
        prop_str = node.props_to_html()
        self.assertEqual(prop_str, "")

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_no_value(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is just text")
        self.assertEqual(node.to_html(), "This is just text")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multi_child(self):
        child_node_1 = LeafNode("span", "child1")
        child_node_2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node_1, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")


    def test_to_html_no_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
