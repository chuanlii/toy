import unittest
import ccjson 
class ccjsonTest(unittest.TestCase):
    def test_json_to_str(self):
        d = {"name":"tom","age":12,"like":["red","blue",{"family":['a','b','c']}]}
        print(ccjson.json_to_str(d))
    def test_str_to_json(self):
        d =' {"name":"tom","age":12,"like":["red","blue",{"family":["a","b","c"]}],"family":{"a":"b"}}'
        print(ccjson.str_to_json(d))

if __name__ == '__main__':
    unittest.main()
