from src.main import runIt
def testZeroArgs():
    assert runIt(0,0,'testImg.png') == 1 
def testIntArgs():
    assert runIt(1,1,'testImg.png') == 0
