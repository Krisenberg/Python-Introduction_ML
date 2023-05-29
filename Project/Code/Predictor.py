from sklearn.svm import SVR

class Predictor:
    def __init__(self):
        self.pred_data = None
    
    def set_pred_data(self, data):
        self.pred_data = data

    def predict(self, model: SVR):
        return model.predict(self.pred_data)