def test_main_demo():
    import MLDashboard.Examples.InteractiveDashboardDemo as IDD
    if IDD == IDD:
        pass

def test_custom_callbacks():
    import MLDashboard.Examples.CustomCallbacksDemo as CCD
    if CCD == CCD:
        pass

def every_module_test():
    with open("MLDashboard/Examples/allmodules.json") as f:
        with open("MLDashboard/Examples/dashboarddemo.json", 'w+') as g:
            g.write(f.read())
    import MLDashboard.Examples.InteractiveDashboardDemo as IDD
    import MLDashboard.Examples.CustomCallbacksDemo as CCD
    if IDD == CCD:
        pass