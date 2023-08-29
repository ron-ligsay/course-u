from django.shortcuts import render
from .utils import load_ml_model, make_prediction

# Create your views here.
def predictor(request):
    if request.method == 'POST':
        sepal_length = request.POST['sepal_length']
        sepal_width = request.POST['sepal_width']
        petal_length = request.POST['petal_length']
        petal_width = request.POST['petal_width']
        # model = load_ml_model('\\models\\iris_model.joblib',"joblib")
        # y_pred = make_prediction(model,[[sepal_length, sepal_width, petal_length, petal_width]])
        # if y_pred[0] == 0:
        #     y_pred = 'Setosa'
        # elif y_pred[0] == 1:
        #     y_pred = 'Versicolor'
        # else:
        #     y_pred = 'Virginica' 
        y_pred = 'Virginica'
        return render(request, 'recommender.html', {'result': y_pred})
    return render(request, 'recommender.html')