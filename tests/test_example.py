import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.sample = "hello"

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


# class DefaultWidgetSizeTestCase(unittest.TestCase):
#     def test_default_widget_size(self):
#         widget = Widget("The widget")
#         self.assertEqual(widget.size(), (50, 50))


# class WidgetTestCase(unittest.TestCase):
#     def setUp(self):
#         self.widget = Widget("The widget")

#     def test_default_widget_size(self):
#         self.assertEqual(self.widget.size(), (50, 50), "incorrect default size")

#     def test_widget_resize(self):
#         self.widget.resize(100, 150)
#         self.assertEqual(self.widget.size(), (100, 150), "wrong size after resize")


# class WidgetTestCase(unittest.TestCase):
#     def setUp(self):
#         self.widget = Widget("The widget")

#     def tearDown(self):
#         self.widget.dispose()


if __name__ == "__main__":
    unittest.main()
