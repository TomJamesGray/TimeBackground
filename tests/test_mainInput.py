from main import main
def testZeroArgs():
    assert main(['0','0']) == 1 
def testIntArgs():
    assert main(['1','1']) == 0
