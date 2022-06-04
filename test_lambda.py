import lambda_function as lf

def lf():

    status = lf.lambda_handler()

    assert status == 200