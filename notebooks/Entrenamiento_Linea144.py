# Se clasificara el nivel de riesgo entre los valores "Alto" o "Medio", 
# utilizando Random Forest Classifier como XGBoost.
# Random Forest será para clasificar el riesgo de la llamada,
# mientras que XGBoost será utilizado para predecir el volumen de llamadas de los próximos días.

# Importación de Librerias
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBRegressor
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, mean_squared_error, mean_absolute_error, r2_score


# Formula para determinar el riesgo de la llamada
def definir_riesgo(row):
    
    # Criterio de Riesgo Alto (2)
    if (row['tipo_de_violencia_fisica_si'] == 1 or row['tipo_de_violencia_sexual_si'] == 1) and row['vinculo_alto_riesgo'] == 1:
        return 2
    
    # Criterio de Riesgo Medio (1)
    elif row['score_tipos_violencia'] > 4 or row['score_modalidades_criticas'] > 2:
        return 1
    
    # Criterio de Riesgo Bajo (0)
    return 0

# Carga, entrenamiento y evaluación del dataset procesado.
def main():
    
    # Recuperación del dataset procesado
    print("Cargando dataset procesado...")

    app_dir = os.path.dirname(__file__)
    df = pd.read_parquet(f'{app_dir}/dataset_procesado.parquet')

    # Llama a la función 'definir_riesgo()' para determinar el riesgo de la llamada
    print("Calculando variable sintética de riesgo...")
    df['nivel_riesgo'] = df.apply(definir_riesgo, axis=1)

    # Nos quedamos únicamente con los riesgos Medio (1) y Alto (2)
    df = df[df['nivel_riesgo'].isin([1, 2])].copy()

    # Selección de Features y exclusión de Data Leakage
    # Quitamos del mapa las variables que se uso para construir la formula matemática.
    columnas_a_excluir = [
        'nivel_riesgo',
        'Fecha',
        'poblacion_provincia',
        'tipo_de_violencia_fisica_si',
        'tipo_de_violencia_sexual_si',
        'vinculo_alto_riesgo',
        'score_tipos_violencia',
        'score_modalidades_criticas',
        'interaccion_gravedad_domestica',
        'pandemia'
    ]

    # Variable objetivo que el modelo debe aprender a predecir
    Y_riesgo = df['nivel_riesgo']

    # Se disminuye la cantidad de variables a las realmente importantes
    features_importantes = [
        'edad_persona_en_situacion_de_violencia',
        'log_pobl_prov',
        'is_weekend',
        'tipo_de_violencia_psicologica_si',
        'tipo_de_violencia_simbolica_si',
        'tipo_de_violencia_economica_y_patrimonial_si',
        'tipo_de_violencia_domestica_si',
        'modalidad_de_violencia_institucional_si',
        'modalidad_de_violencia_laboral_si',
        'modalidad_de_violencia_otras_si',
        'vinculo_con_la_persona_agresora_pareja',
        'vinculo_con_la_persona_agresora_ex pareja',
        'vinculo_con_la_persona_agresora_otro',
        'vinculo_con_la_persona_agresora_otro familiar',
        'genero_persona_en_situacion_de_violencia_mujer',
        'genero_persona_en_situacion_de_violencia_varon',
        'genero_de_la_persona_agresora_varon',
        'genero_de_la_persona_agresora_mujer'
    ]

    # Guarda en 'X_riesgo' las variables a utilizar.
    X_excluidas = df.drop(columns=columnas_a_excluir, errors='ignore')
    X_riesgo = X_excluidas[features_importantes].copy()
    
    # Partición de datos - Split (80% entrenamiento y 20% testeo).
    X_train, X_test, Y_train, Y_test = train_test_split(
        X_riesgo, Y_riesgo, test_size=0.2, random_state=42, stratify=Y_riesgo
    )
    
    # Configura e inicia la búsqueda de hiperparámetros con GridSearchCV.
    print("Iniciando GridSearchCV para Random Forest...")
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [5, 10, 15, None],
        'min_samples_split':[2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'class_weight': ['balanced']
    }
    
    rf_base = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        estimator=rf_base,
        param_grid=param_grid,
        cv=3,
        scoring='f1_macro',     # Busca maximizar la métrica 'f1_macro'
        n_jobs=-1
    )
    grid_search.fit(X_train, Y_train)
    
    best_rf = grid_search.best_estimator_
    print(f"\nMejores parámetros encontrados: {grid_search.best_params_}")


    # Predicción y Evaluación del modelo
    Y_pred = best_rf.predict(X_test)
    
    print("\n================ REPORTE DE CLASIFICACIÓN ================")
    print(classification_report(Y_test, Y_pred, labels=[1, 2], target_names=['Medio', 'Alto']))
    print("==========================================================")

      
    # Gráfica de importancia de variables
    importances = best_rf.feature_importances_
    indices = np.argsort(importances)[-10:] # Top 10 variables más 

    # Ejemplo inspirado en la Sección 6 de la notebook para detectar overfitting
    resultados_clf = pd.DataFrame({
        "Métrica": ["F1-Macro", "Accuracy"],
        "Entrenamiento": [
            classification_report(Y_train, best_rf.predict(X_train), output_dict=True)['macro avg']['f1-score'],
            best_rf.score(X_train, Y_train)
        ],
        "Prueba": [
            classification_report(Y_test, Y_pred, output_dict=True)['macro avg']['f1-score'],
            best_rf.score(X_test, Y_test)
        ]
    })

    display(resultados_clf)
    
    plt.figure(figsize=(10, 6))
    plt.title("Top 10 Características Críticas en la Determinación de Riesgo (Modelo Real)")
    plt.barh(range(len(indices)), importances[indices], color='teal', align='center')
    plt.yticks(range(len(indices)), [X_riesgo.columns[i] for i in indices])
    plt.xlabel('Importancia Relativa')
    plt.tight_layout()
    
    plt.savefig('importancia_features_riesgo.png', dpi=300)
    print("\nGráfica de importancia guardada como 'importancia_features_riesgo.png'")
    plt.show()

    # Matriz de confusión
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_estimator(
        best_rf, X_test, Y_test, 
        display_labels=['Medio', 'Alto'], 
        cmap='Blues', colorbar=False, ax=ax
    )
    ax.set(title="Matriz de Confusión - Random Forest", xlabel="Predicción", ylabel="Real")
    plt.tight_layout()
    plt.savefig('matriz_confusion_rf.png', dpi=300)
    plt.show()

    modelo = predecir_volumen_llamadas(app_dir)

    import joblib

    joblib.dump(modelo.best_estimator_, "volumen.joblib", compress=3)

    joblib.dump(best_rf.best_estimator_, "riesgo.joblib", compress=3)

# Se utilizara XGBoost para estimar la demanda diaria de llamadas,
# esto para poder organizar y administrar la cantidad de operadores
# o contestadores necesarios dentro de una fecha en particular.

# Se mapean las clases a [0, 1].
# XGBoost exige etiquetas consecutivas que comiencen en 0.
# Mapeados: Clase 1 (Medio) -> 0  |  Clase 2 (Alto) -> 1

def predecir_volumen_llamadas(app_dir):

    print("\n--- Iniciando modelo XGBoost para Predicción de Volumen de Llamadas ---")
    
    # Carga el dataset procesado original.
    df = pd.read_parquet(f'{app_dir}/dataset_procesado.parquet')
    
    # Agrupa por fecha para obtener la cantidad de llamadas diarias.
    df_volumen = df.groupby('Fecha').size().reset_index(name='volumen_llamadas')
    df_volumen = df_volumen.sort_values('Fecha').reset_index(drop=True)
    
    # Ingeniería de atributos temporales.
    df_volumen['dia_semana'] = df_volumen['Fecha'].dt.dayofweek
    df_volumen['mes'] = df_volumen['Fecha'].dt.month
    df_volumen['dia'] = df_volumen['Fecha'].dt.day
    
    # Crear rezagados (lags): el volumen de días anteriores ayuda a predecir el futuro.
    df_volumen['lag_1'] = df_volumen['volumen_llamadas'].shift(1)  # Día anterior
    df_volumen['lag_7'] = df_volumen['volumen_llamadas'].shift(7)  # Misma semana previa
    
    # Elimina valores nulos generados por los lags.
    df_volumen = df_volumen.dropna().reset_index(drop=True)
    
    # Definir Features (X) y Target (Y).
    features_volumen = ['dia_semana', 'mes', 'dia', 'lag_1', 'lag_7']
    X_vol = df_volumen[features_volumen]
    Y_vol = df_volumen['volumen_llamadas']
    
    # Partición cronológica (80% pasado para entrenar, 20% futuro para testear)
    train_size = int(len(X_vol) * 0.8)
    X_train_vol, X_test_vol = X_vol.iloc[:train_size], X_vol.iloc[train_size:]
    Y_train_vol, Y_test_vol = Y_vol.iloc[:train_size], Y_vol.iloc[train_size:]
    
    # 6. Configurar GridSearchCV para entrenar XGBoost Regressor
    print("Iniciando GridSearchCV para XGBoost Regressor...")
    param_grid_xgb = {
        'n_estimators': [50, 100, 150],
        'max_depth': [3, 4, 6],
        'learning_rate': [0.01, 0.1]
    }
    
    xgb_base = XGBRegressor(random_state=42, n_jobs=-1)
    
    # TimeSeriesSplit respeta el orden temporal para la validación cruzada
    tscv = TimeSeriesSplit(n_splits=3)
    
    grid_search_xgb = GridSearchCV(
        estimator=xgb_base,
        param_grid=param_grid_xgb,
        cv=tscv,
        scoring='neg_mean_absolute_error', # Mide el error absoluto medio negativo
        n_jobs=-1
    )
    grid_search_xgb.fit(X_train_vol, Y_train_vol)
    
    best_xgb_reg = grid_search_xgb.best_estimator_
    print(f"\nMejores parámetros encontrados para XGBoost: {grid_search_xgb.best_params_}")

    
    # Predicción y Evaluación
    Y_pred_vol = best_xgb_reg.predict(X_test_vol)
    
    mae = mean_absolute_error(Y_test_vol, Y_pred_vol)
    rmse = np.sqrt(mean_squared_error(Y_test_vol, Y_pred_vol))
    r2 = r2_score(Y_test_vol, Y_pred_vol)
    
    print("\n================ EVALUACIÓN DE PREDICCIÓN DE VOLUMEN ==================")
    print(f"MAE (Error Absoluto Medio): {mae:.2f} llamadas por día")
    print(f"RMSE (Raíz del Error Cuadrático Medio): {rmse:.2f}")
    print(f"R² (Coeficiente de Determinación): {r2:.4f}")
    print("========================================================================")

    # Comparación de las métricas
    y_train_pred_vol = best_xgb_reg.predict(X_train_vol)
    
    # Tabla comparativa de entrenamiento vs prueba (Inspirado en la Sección 6 de la notebook)
    resultados_volumen = pd.DataFrame({
        "Métrica": ["MAE", "RMSE", "R²"],
        "Entrenamiento": [
            mean_absolute_error(Y_train_vol, y_train_pred_vol),
            np.sqrt(mean_squared_error(Y_train_vol, y_train_pred_vol)),
            r2_score(Y_train_vol, y_train_pred_vol)
        ],
        "Prueba": [
            mae,
            rmse,
            r2
        ]
    })
    
    print("\nResumen Comparativo (Entrenamiento vs. Prueba):")
    display(resultados_volumen.round(3))

    plt.figure(figsize=(12, 5))
    plt.plot(df_volumen['Fecha'].iloc[train_size:], Y_test_vol, label='Volumen Real', color='blue')
    plt.plot(df_volumen['Fecha'].iloc[train_size:], Y_pred_vol, label='Volumen Predicho (XGBoost)', color='orange', linestyle='--')
    plt.title('Demanda Diaria de Llamadas: Real vs Predicha')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad de Llamadas')
    plt.legend()
    plt.tight_layout()
    plt.savefig('prediccion_volumen_llamadas.png', dpi=300)
    plt.show()

    return best_xgb_reg

if __name__ == '__main__':
    main()