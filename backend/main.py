# ================================
# IMPORT LIBRARIES
# ================================
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

# ================================
# LOAD DATASET
# ================================
df = pd.read_csv("Loan_default.csv")
print("First 5 rows:\n", df.head())
print("Dataset shape:", df.shape)

# ================================
# CLEAN COLUMN NAMES
# ================================
df.columns = df.columns.str.strip().str.lower()

# ================================
# DATA CLEANING
# ================================
df = df.drop(columns=[col for col in ['loanid'] if col in df.columns])

# ================================
# SELECT IMPORTANT FEATURES
# ================================
selected_features = [
    'age',
    'income',
    'loanamount',
    'creditscore'
]

target_col = 'default'

df = df[selected_features + [target_col]]

# ================================
# ENCODING
# ================================
categorical_cols = df.select_dtypes(include=['object', 'string']).columns

le_dict = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# ================================
# SPLIT FEATURES AND TARGET
# ================================
X = df.drop(columns=target_col)
Y = df[target_col]

# ================================
# SCALING
# ================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ================================
# TRAIN TEST SPLIT
# ================================
x_train, x_test, y_train, y_test = train_test_split(
    X_scaled, Y, test_size=0.2, stratify=Y, random_state=2
)

# ================================
# SMOTE
# ================================
smote = SMOTE(random_state=2)
x_train_res, y_train_res = smote.fit_resample(x_train, y_train)

print("Before SMOTE:", np.bincount(y_train))
print("After SMOTE:", np.bincount(y_train_res))

# ================================
# MODEL
# ================================
xgb_model = XGBClassifier(
    n_estimators=800,
    max_depth=8,
    learning_rate=0.05,
    subsample=1.0,
    colsample_bytree=1.0,
    reg_alpha=0,
    reg_lambda=0,
    random_state=2,
    eval_metric='logloss'
)

xgb_model.fit(x_train_res, y_train_res)

# ================================
# PREDICTIONS
# ================================
y_train_pred = xgb_model.predict(x_train_res)
y_test_pred = xgb_model.predict(x_test)

# ================================
# EVALUATION
# ================================
print("\n=== XGBOOST MODEL ===")
print("Train Accuracy:", accuracy_score(y_train_res, y_train_pred))
print("Test Accuracy:", accuracy_score(y_test, y_test_pred))

print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_test_pred))
print("\nClassification Report:\n", classification_report(y_test, y_test_pred))

# ================================
# SAVE MODEL (PICKLE)
# ================================
with open("model.pkl", "wb") as f:
    pickle.dump(xgb_model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("label_encoders.pkl", "wb") as f:
    pickle.dump(le_dict, f)

with open("features.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("\n✅ Model, scaler, encoders saved successfully!")