from alpypeopt import AnyLogicModel
import optuna

gpp_model = AnyLogicModel(
    env_config={
        'run_exported_model': False,
        'exported_model_loc': './resources/exported_models/gas_processing_plant',
        'show_terminals': True,
        'verbose': False
    }
)

# Initialize model setup
gpp_setup = gpp_model.get_jvm().gasprocessingplant.GPPSetup()
# Start setting up gas product prices
gpp_setup.setProductPrices(30.0, 10.0)
# Create input variable ratios as (min, max)
# GPU 1&2 plant load ratios
plant_load_ratio = (0.01, 0.99)
# GPU 1&2 distillation column operating temperature
gpp_opp_temp_ratio = (20.0, 100.0)
bounds = [
    plant_load_ratio,       # dec1 flow allocation
    gpp_opp_temp_ratio,     # dec1 temperature
    gpp_opp_temp_ratio      # dec2 temperature
]

# Encapsulate simulation model as a python function
def simulation(x, reset=True):
    # Setup selected plant loads and temperatures
    gpp_setup.setFlowAllocRateToDec1(x[0])
    gpp_setup.setDecTemperatures(x[1], x[2])
    # Pass input setup and run model until end
    gpp_model.setup_and_run(gpp_setup)
    # Extract model output or simulation result
    model_output = gpp_model.get_model_output()
    if reset:
        # Reset simulation model to be ready for next iteration
        gpp_model.reset()
    # Return simulation value. 'skopt' package only allows minimization problems
    # Because of that, value must be negated
    return model_output.getTotalRevenue()

# Setup and execute black box optimmization model
def objective(trial):
    x = [
        trial.suggest_float('dec1 flow allocation', 0.01, 0.99),
        trial.suggest_float('dec1 temperature', 20.0, 100.0),
        trial.suggest_float('dec2 temperature', 20.0, 100.0)
    ]
    return simulation(x)

# run the optimizer
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=500)

best = study.best_params
print(f"Solution is {best} for a value of {study.best_value}")

# Run simulation with optimal result to use UI to explore results in AnyLogic
best_x = list(best.values())
simulation(best_x, reset=False)

# Close model
gpp_model.close()




