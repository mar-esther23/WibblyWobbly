import unittest
import warnings
import pandas as pd
from random import seed

import wibblywobbly as ww


class TestCore(unittest.TestCase):

    def setUp(self):
        self.ctlg = ["Mouse", "Cat", "Dog", "Human"]
        self.data = ["mice",  "CAT ", "doggo", "PERSON", 999]
        df = [['CAT ', 'Cat', 100], 
              ['doggo', 'Dog', 90], 
              ['mice', 'mice', 0], 
              ['PERSON', 'PERSON', 0], 
              [999, 999, 0],
              ]
        df = pd.DataFrame(df, columns=["Data", "Option1", "Score1"])
        self.df_res=df

    def test_simplify_string(self):
        """Remove spaces, special characters, etc"""
        tex = ' (S . cerevisiáe  )'
        res = 's cerevisiae'
        self.assertEqual( res, ww.simplify_string(res) )

    def test_warn_review(self):
        """Check the warning text is correctly created depending on options"""
        res = "WOBBLY: Human\n\tOptions: Human (100), Homo sapiens (95), Person (90)\n"
        ctg, top = "WOBBLY", "Human"
        options  = [("Human", 100), ("Homo sapiens", 95), ("Person", 90)]
        # catch warnings to check them
        with warnings.catch_warnings(record=True) as warn:
            warnings.simplefilter("always")
            # check the text is created
            resul = ww.warn_review(ctg, top, options)
            for w in warn:
                self.assertEqual( res, str(w.message) )

    def test_map_dataframe(self):
        sol = ww.map_list_to_catalog(self.data, self.ctlg, max_options=1)
        self.assertTrue( sol.equals(self.df_res) )

    def test_map_dictionary(self):
        res = {'mice': 'mice', 'CAT ': 'Cat', 'doggo': 'Dog', 
               'PERSON': 'PERSON', 999: 999 }
        sol = ww.map_list_to_catalog(self.data, self.ctlg, output_format="dictionary")
        self.assertEqual( res, sol )

    def test_map_thr_accept(self):
        res = {'mice': 'mice', 'CAT ': 'Cat', 'doggo': 'Dog', 
               'PERSON': 'PERSON', 999: 999 }
        sol = ww.map_list_to_catalog(self.data, self.ctlg, output_format="dictionary", thr_accept=91)
        self.assertEqual( res, sol )

    def test_map_thr_reject(self):
        res = {'mice': 'Mouse', 'CAT ': 'Cat', 'doggo': 'Dog', 
               'PERSON': 'PERSON', 999: 999 }
        sol = ww.map_list_to_catalog(self.data, self.ctlg, output_format="dictionary", thr_reject=43)
        self.assertEqual( res, sol )

    def test_map_reject_value(self):
        res = {'mice': 'Other', 'CAT ': 'Cat', 'doggo': 'Dog', 
               'PERSON': 'Other', 999: 999 }
        sol = ww.map_list_to_catalog(self.data, self.ctlg, output_format="dictionary", reject_value='Other')
        self.assertEqual( res, sol )

    def test_map_max_options(self):
        res = ["Data", "Option1", "Score1", "Option2", "Score2", "Option3", "Score3"]
        sol = ww.map_list_to_catalog(self.data, self.ctlg, max_options=3)
        self.assertEqual( res[0:3], sol.columns.to_list() )
        sol = ww.map_list_to_catalog(self.data, self.ctlg, max_options=3, thr_reject=20)
        self.assertEqual( res, sol.columns.to_list() )

    def test_map_warnings(self):
        res = ["WOBBLY: PERSON\n\tOptions: Dog (30)\n",
               "WOBBLY: mice\n\tOptions: Mouse (44)\n" ]
        # catch warnings to check them
        with warnings.catch_warnings(record=True) as warn:
            warnings.simplefilter("always")
            # check the text is created
            sol = ww.map_list_to_catalog(self.data, self.ctlg, thr_reject=20, max_options=1, warnings=True)
            for w in warn:
                self.assertIn( str(w.message), res )

    def test_cluster_strings(self):
        data = ['mice', 'CAT ', 'doggo', 'PERSON', 'guinea pig', 'pig', 'Gorilla', 'Chimpanzee', 'orangután', 'chinpanze', 'gorila', nan, 'dogs', 'rats', 'mouse', 'kitty', 'Cat', 'macaco']
        res = [['gorila', 'Gorilla'],   ['chinpanze'],   ['  mouse'],   ['macaco'],   ['pig', 'guinea pig'],   ['doggo'],   ['mice'],   ['PERSON'],   ['dogs'],   ['orangután'],   ['CAT ', 'Cat'],   ['Chimpanzee'],   ['kitty']]
        seed(10)
        sol = ww.cluster_strings(df_data['Animal'])
        self.assertEqual( res, sol )

    def test_cluster_strings_noptions(self):
        data = ['mice', 'CAT ', 'doggo', 'PERSON', 'guinea pig', 'pig', 'Gorilla', 'Chimpanzee', 'orangután', 'chinpanze', 'gorila', nan, 'dogs', 'rats', 'mouse', 'kitty', 'Cat', 'macaco']
        res = ['gorila', 'chinpanze', 'mouse', 'macaco', 'pig', 'doggo', 'mice', 'PERSON', 'dogs', 'orangután', 'CAT ', 'kitty']
        seed(10)
        sol = ww.cluster_strings(df_data['Animal'], thr_accept=75, max_options=1)
        self.assertEqual( res, sol )


if __name__ == '__main__':
    unittest.main()






