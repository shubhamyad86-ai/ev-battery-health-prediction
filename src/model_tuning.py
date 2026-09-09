from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    cross_val_score
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from xgboost import XGBRegressor

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED = BASE_DIR/"data"/"processed"

MODELS = BASE_DIR/"models"

REPORTS = BASE_DIR/"reports"

MODELS.mkdir(exist_ok=True)

REPORTS.mkdir(exist_ok=True)

df = pd.read_csv(
    PROCESSED/"battery_features.csv"
)

drop_columns = [

    "vehicle_id",

    "timestamp",

    "charger_type",

    "battery_failure_risk"

]

existing = [

    c for c in drop_columns

    if c in df.columns

]

df = df.drop(columns=existing)

X = df.drop(columns=["soh"])

y = df["soh"]

X_train,X_test,y_train,y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

rf_params = {

    "n_estimators":[100,200],

    "max_depth":[10,None],

    "min_samples_split":[2,5],

    "min_samples_leaf":[1,2]

}

rf = RandomForestRegressor(
    random_state=42
)

grid = GridSearchCV(

    estimator=rf,

    param_grid=rf_params,

    cv=5,

    scoring="neg_root_mean_squared_error",

    n_jobs=-1

)

print("Training Random Forest...")

grid.fit(X_train,y_train)

print()

print("Best Parameters")

print(grid.best_params_)

print()

print("Best Score")

print(grid.best_score_)

predictions = grid.predict(X_test)

mae = mean_absolute_error(

    y_test,

    predictions

)

rmse = mean_squared_error(

    y_test,

    predictions

)**0.5

r2 = r2_score(

    y_test,

    predictions

)

print()

print("MAE :",mae)

print("RMSE :",rmse)

print("R2 :",r2)

scores = cross_val_score(

    grid.best_estimator_,

    X,

    y,

    cv=5,

    scoring="r2"

)

print()

print("Cross Validation")

print(scores)

print()

print("Average")

print(scores.mean())

joblib.dump(

    grid.best_estimator_,

    MODELS/"random_forest_tuned.pkl"

)

results = pd.DataFrame({

    "Metric":[

        "MAE",

        "RMSE",

        "R2",

        "CV Mean"

    ],

    "Value":[

        mae,

        rmse,

        r2,

        scores.mean()

    ]

})

results.to_csv(

    REPORTS/"tuning_results.csv",

    index=False

)


with open(

    REPORTS/"best_parameters.txt",

    "w"

) as f:

    f.write(

        str(grid.best_params_)

    )

