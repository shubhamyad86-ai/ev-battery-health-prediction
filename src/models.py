from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from xgboost import XGBRegressor


def get_models():

    return {

        "Linear Regression":
            LinearRegression(),

        "Ridge":
            Ridge(random_state=42),

        "Lasso":
            Lasso(random_state=42),

        "Decision Tree":
            DecisionTreeRegressor(
                random_state=42
            ),

        "Random Forest":
            RandomForestRegressor(
                n_estimators=200,
                random_state=42
            ),

        "Gradient Boosting":
            GradientBoostingRegressor(
                random_state=42
            ),

        "XGBoost":
            XGBRegressor(
                random_state=42,
                n_estimators=200,
                learning_rate=0.05,
                max_depth=6
            )
    }
    