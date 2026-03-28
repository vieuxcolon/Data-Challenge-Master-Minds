# ================================
# 0. Mount Google Drive
# ================================
from google.colab import drive
drive.mount('/content/drive')

# ================================
# 1. Imports
# ================================
import pandas as pd
import numpy as np
import lightgbm as lgb
import optuna
import joblib
import random

from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ================================
# 2. Load dataset
# ================================
FINAL_PATH = "/content/drive/MyDrive/final_model_dataset_cleaned.csv"
TARGET = "NbPaxTotal"

df = pd.read_csv(FINAL_PATH, parse_dates=['LTScheduledDatetime'])
df = df.sort_values('LTScheduledDatetime').reset_index(drop=True)
print("Dataset shape:", df.shape)

# ================================
# 3. Feature selection (numeric only)
# ================================
FEATURES = [c for c in df.columns if c not in ['LTScheduledDatetime', TARGET] and not c.startswith('Id')]
X = df[FEATURES].select_dtypes(include=[np.number])
y = df[TARGET]

print("Final feature count:", X.shape[1])

# ================================
# 4. Temporal split (80/10/10)
# ================================
n = len(df)
train_end = int(n * 0.8)
val_end = int(n * 0.9)

X_train, y_train = X.iloc[:train_end], y.iloc[:train_end]
X_val, y_val = X.iloc[train_end:val_end], y.iloc[train_end:val_end]
X_test, y_test = X.iloc[val_end:], y.iloc[val_end:]

print("Train:", X_train.shape, "Val:", X_val.shape, "Test:", X_test.shape)

# ================================
# 5. TimeSeries CV
# ================================
tscv = TimeSeriesSplit(n_splits=5)

# ================================
# 6. Optuna objective
# ================================
def objective_lgb(trial):
    params = {
        'objective': 'regression_l1',  # MAE
        'metric': 'mae',
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 31, 128),
        'max_depth': trial.suggest_int('max_depth', 4, 12),
        'min_data_in_leaf': trial.suggest_int('min_data_in_leaf', 20, 100),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.6, 1.0),
        'bagging_fraction': trial.suggest_float('bagging_fraction', 0.6, 1.0),
        'bagging_freq': 1,
        'verbosity': -1,
        'random_state': 42,
        'deterministic': True,
        'n_jobs': -1
    }

    scores = []
    for train_idx, val_idx in tscv.split(X_train):
        X_tr, X_va = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_va = y_train.iloc[train_idx], y_train.iloc[val_idx]

        model = lgb.LGBMRegressor(**params, n_estimators=1000)
        model.fit(
            X_tr, y_tr,
            eval_set=[(X_va, y_va)],
            eval_metric='mae',
            callbacks=[lgb.early_stopping(50, verbose=False)]
        )
        preds = model.predict(X_va)
        scores.append(mean_absolute_error(y_va, preds))

    return np.mean(scores)

# ================================
# 7. Run Optuna
# ================================
study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=42))
study.optimize(objective_lgb, n_trials=25)

print("\nBest parameters:", study.best_params)
print("Best CV MAE:", study.best_value)

# ================================
# 8. Train final model
# ================================
final_model = lgb.LGBMRegressor(
    **study.best_params,
    objective='regression_l1',
    n_estimators=1000,
    random_state=42,
    deterministic=True,
    n_jobs=-1
)

final_model.fit(
    pd.concat([X_train, X_val]),
    pd.concat([y_train, y_val]),
    eval_set=[(X_val, y_val)],
    eval_metric='mae',
    callbacks=[lgb.early_stopping(50)]
)

best_iter = final_model.best_iteration_

# ================================
# 9. Evaluate
# ================================
def evaluate(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    print(f"\n{name}")
    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")
    return {"mae": mae, "rmse": rmse, "r2": r2}

y_pred = final_model.predict(X_test, num_iteration=best_iter)
metrics_lgb = evaluate(y_test, y_pred, "LightGBM")

# ================================
# 10. Save final model
# ================================
MODEL_PATH = "/content/drive/MyDrive/lightgbm_model.pkl"
joblib.dump({
    "model": final_model,
    "best_iteration": best_iter,
    "features": list(X.columns)
}, MODEL_PATH)
print(f"\n✅ Model saved at {MODEL_PATH}")
