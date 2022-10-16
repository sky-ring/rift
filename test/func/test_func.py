from rift.fift.func import FunC, FunCResult


def test_func():
    res = FunC.compile_source(
        """
    (int) main(){
        int v = 0;
        int y = 1;
        var z = v + y;
        return z;
    }
    """,
        optimization_level=0,
    )
    assert isinstance(res, FunCResult)
    print(res.fift_code)
