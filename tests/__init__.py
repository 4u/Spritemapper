from attest import Tests

submods = ("test_css",)
all_tests = Tests([getattr(mod, "suite") for mod in
                   (__import__(submod, fromlist=["suite"], level=1)
                    for submod in submods)])
