# <h1><b>Disease Prediction with GUI<b></h1>
# A disease prediction model working on support vector machine (SVM). It takes the symptoms of the user as input along with its location and predicts the most probable disease which the user might be facing. The same data can be sent to cloud and being later analysed using analytical tool tableau.
# The data has been taken from https://www.kaggle.com/itachi9604/disease-symptom-description-dataset.
# <h2>Importing the libraries</h2>
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import seaborn as sns
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFormLayout, QPushButton, QVBoxLayout, QComboBox, QTextEdit,QMessageBox,QHBoxLayout
import joblib
class DiseasePredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.list=[]
        self.info=[1,2,3,4,5,6]
        self.df = pd.read_csv(r'dataset\dataset.csv') 
        self.df1 = pd.read_csv('dataset/Symptom-severity.csv')
        self.df2=pd.read_csv(r"dataset\symptom_Description.csv",index_col="Disease")
        self.CHATmodel=self.load_model()
        self.init_ui()
    def call(self):
        if self.isHidden()==True:
            self.show()
        else:
            if __name__ == '__main__':
                exit()
            else:
                self.hide()
    def hide_page(self):
        self.call()
        self.result_text.clear()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(200, 100, 800, 600)
        self.setWindowTitle('News App')
        self.setStyleSheet("background-color: yellow;")

        layout = QVBoxLayout()

        title_label = QLabel("Disease Prediction From Symptoms")
        title_label.setStyleSheet("font-size: 42pt; font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        form_layout = QFormLayout()
        

        symptoms_options = ["Na","fatigue", "yellowish_skin", "loss_of_appetite", "yellowing_of_eyes", 'family_history',
                            "stomach_pain","acidity","excessive_hunger","stiff_neck", 'dizziness',"depression",'headache', "ulcers_on_tongue", "vomiting", "cough", "chest_pain"]
        locations_options = ["New Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru"]

        self.setup_combo_box(form_layout, "Symptom 1", symptoms_options)
        self.setup_combo_box(form_layout, "Symptom 2", symptoms_options)
        self.setup_combo_box(form_layout, "Symptom 3", symptoms_options)
        self.setup_combo_box(form_layout, "Symptom 4", symptoms_options)
        self.setup_combo_box(form_layout, "Symptom 5", symptoms_options)
        self.setup_combo_box(form_layout, "Location", locations_options)

        predict_button = QPushButton("Predict")
        predict_button.clicked.connect(self.message)
        predict_button.setFont(QFont('Arial', 28))
        hide_button = QPushButton('Close page')
        hide_button.setFont(QFont('Arial', 28))
        hide_button.setStyleSheet("background-color: green;")
        hide_button.clicked.connect(self.hide_page)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5,15,5,15)
        button_layout.addWidget(predict_button)
        button_layout.addWidget(hide_button)
        layout.addLayout(button_layout)
        result=QHBoxLayout()
        result_label = QLabel("Prediction Result:")
        result_label.setStyleSheet("font-size: 28pt; font-weight: bold; margin-top: -2px;")
        result.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setStyleSheet("font-size: 24pt;")
        result.addWidget(self.result_text)
        layout.addLayout(result)
        self.setLayout(layout)
        """_summary_
        added ui for prediction and stuff
        need of button for basic info on disease and Prevntion protocols
        """
    def setup_combo_box(self, layout, label_text, options):
        label = QLabel(label_text)
        label.setFont(QFont('Arial', 18))
        combo_box = QComboBox()
        combo_box.setStyleSheet("QComboBox { background-color: cyan; border: 2px solid transparent; border-radius: 35px; }"
                                "QComboBox::drop-down { border-radius: 35px; }"
                                """QComboBox QAbstractItemView {
                                background-color: red;
                                selection-background-color: green;
                                }"""
                                "QComboBox:hover { background-color: lightblue; border-radius: 35px; }")
        combo_box.setFont(QFont('Arial', 22))
        combo_box.addItems(options)
        layout.addRow(label, combo_box)
        self.list.append(combo_box)
        
    def message(self):
        
        self.result_text.clear()
        for i in range(6):
            if self.list[i].currentText()!="Na":
                self.info[i]=self.list[i].currentText()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("enter the symptoms properly ")
                msg.setWindowTitle("Error Window")
                msg.setStyleSheet("background: aqua;")
                msg.setFont(QFont('Times', 24))

                yes_button = msg.addButton(QMessageBox.Ok)
                yes_button.setFont(QFont('Times', 24))
                no_button = msg.addButton(QMessageBox.Cancel)
                no_button.setFont(QFont('Times', 24))
                no_button.clicked.connect(self.on_no_clicked)
                msg.exec_()
                break
        else:
            self.SVM()
    def on_no_clicked(self):
        exit()
    def SVM(self):
        psymptoms = self.info[0:5]
        loc = self.info[-1]
        a = np.array(self.df1["Symptom"])
        b = np.array(self.df1["weight"])
        for j in range(len(psymptoms)):
            for k in range(len(a)):
                if psymptoms[j]==a[k]:
                    psymptoms[j]=b[k]

        nulls = [0,0,0,0,0,0,0,0,0,0,0,0]
        psy = [psymptoms + nulls]

        pred2 = self.CHATmodel.predict(psy)
        self.disease=pred2[0]
        self.result_text.setText(f"The most probable disease as per the given symptoms is {pred2[0]}")
    def model_compilation(self):
        
    # <h2>Importing the dataset</h2>

    # <h2>Cleaning of Data</h2>
        self.df.isna().sum()
        self.df.isnull().sum()

        cols = self.df.columns
        data = self.df[cols].values.flatten()

        s = pd.Series(data)
        s = s.str.strip()
        s = s.values.reshape(self.df.shape)

        df = pd.DataFrame(s, columns=self.df.columns)

        df = df.fillna(0)

    # <h2>Encoding the the symptoms with their severity weight</h2>

        vals = df.values
        symptoms = self.df1['Symptom'].unique()

        for i in range(len(symptoms)):
            vals[vals == symptoms[i]] = self.df1[self.df1['Symptom'] == symptoms[i]]['weight'].values[0]
    
            d = pd.DataFrame(vals, columns=cols)

        d = d.replace('dischromic _patches', 0)
        d = d.replace('spotting_ urination',0)
        df = d.replace('foul_smell_of urine',0)
    # <h2> Storing the diseases and encoded symptoms in seperate dataframes</h2>
        (df[cols] == 0).all()

        df['Disease'].value_counts()

        df['Disease'].unique()

        data = df.iloc[:,1:].values
        labels = df['Disease'].values

# <h2>Splitting the data and training the model</h2>

        x_train, x_test, y_train, y_test = train_test_split(data, labels, shuffle=True, train_size = 0.85)

        model = SVC()
        model.fit(x_train, y_train)

        preds = model.predict(x_test)

        conf_mat = confusion_matrix(y_test, preds)
        df_cm = pd.DataFrame(conf_mat, index=df['Disease'].unique(), columns=df['Disease'].unique())
        sns.heatmap(df_cm)
        joblib.dump(model, "disease_prediction_model.joblib")
        return model
    def load_model(self):
        try:
            model = joblib.load("disease_prediction_model.joblib")
        except FileNotFoundError:
            model = self.model_compilation()
        return model
if __name__=="__main__":    
    app = QApplication([])
    window = DiseasePredictionApp()
    window.call()
    app.exec_()
