import unittest
import Calculator as calc


class TestCalculator(unittest.TestCase):

    @classmethod
    def tearDown(self):
        calc.clear_all()

    def test_clear(self):
        calc.calc_input.insert('end-1c', "15687")
        calc.calc_output.config(text= "15687")
        calc.clear_all()
        self.assertEqual(calc.calc_input.get('1.0','end-1c'), '')
        self.assertEqual(calc.calc_output.cget('text'), '')

    def test_input(self):
        calc.number_btns[0].invoke()
        calc.add_btn.invoke()
        calc.bracket_left_btn.invoke()
        calc.number_btns[1].invoke()
        calc.sub_btn.invoke()
        calc.number_btns[2].invoke()
        calc.mult_btn.invoke()
        calc.number_btns[3].invoke()
        calc.float_btn.invoke()
        calc.number_btns[5].invoke()
        calc.bracket_right_btn.invoke()
        calc.pow_btn.invoke()
        calc.number_btns[9].invoke()
        calc.div_btn.invoke()
        calc.number_btns[4].invoke()
        calc.equal_btn.invoke()
        self.assertEqual(calc.calc_output.cget('text'), '0+(1-2*3.5)^9/4')
    
    def test_eval(self):
        calc.calc_input.insert('end-1c','-8*8.5/(7+3)**3')
        calc.equal_btn.invoke()
        result = -8*8.5/(7+3)**3
        self.assertEqual(calc.calc_input.get('1.0','end-1c'),str(result))

    def test_valid_input(self):
        calc.calc_input.insert('1.0', '0s+(1d-2*f3.sdf5)^sdf9e/4wer_?&%')
        calc.equal_btn.invoke()
        self.assertEqual(calc.calc_output.cget('text'), '0+(1-2*3.5)^9/4')
        result = int(0+(1-2*3.5)**9/4)
        self.assertEqual(calc.calc_input.get('1.0','end-1c'), str(result+1))
        
        

if __name__ == "__main__":
    unittest.main()