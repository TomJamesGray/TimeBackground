from src.main import main
def testZeroArgs():
    assert main(['0','0','testImg.png']) == 1 
def testIntArgs():
    assert main(['1','1','testImg.png']) == 0
