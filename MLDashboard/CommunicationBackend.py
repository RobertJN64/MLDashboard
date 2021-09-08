class Message:
    def __init__(self, mode: int, body: dict):
        self.mode = mode
        self.body = body

    def __repr__(self):
        return "Message with mode: " + str(self.mode) + " and data payload: " + str(self.body) + " At location: " + object.__repr__(self)

class MessageMode:
    #control characters
    Start = 0
    End = 1
    ForceUpdate = 2
    CustomData = 3 #handles status module comm
    Command = 4 #handles data return

    #custom messages
    Evaluation = 5

    #callback messages
    Train_Batch_End = 10
    Epoch_End = 11

    #data request messages
    Train_Set_Sample = 20
    Test_Set_Sample = 21
    Pred_Sample = 22 #from test set
    Pred_Sample_Train = 23
    Wrong_Pred_Sample = 24 #from test set
    Wrong_Pred_Sample_Train = 25