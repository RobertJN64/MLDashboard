def test_main_demo():
    import MLDashboard.Examples.InteractiveDashboardDemo as IDD
    IDD.run(testmode=True)

def test_custom_callbacks():
    import MLDashboard.Examples.CustomCallbacksDemo as CCD
    CCD.run(testmode=True)

def test_every_module():
    with open("MLDashboard/Examples/allmodules.json") as f:
        with open("MLDashboard/Examples/dashboarddemo.json", 'w+') as g:
            g.write(f.read())
    import MLDashboard.Examples.InteractiveDashboardDemo as IDD
    import MLDashboard.Examples.CustomCallbacksDemo as CCD
    IDD.run(testmode=True)
    CCD.run(testmode=True)