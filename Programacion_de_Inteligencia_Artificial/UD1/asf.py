from sklearn.linear_model import Perceptron
red = Perceptron(max_iter = 2000, random_state = 40, n_jobs= -1)
red.fit(x_train, y_train)
red.predict([x_test[0]])
y_test[0]
y_pred = red.predict(x_test)
# Mostramos el f1_score resultante de la clasificación
from sklearn.metrics import f1_score

f1_score(y_test, y_pred, average='weighted')
