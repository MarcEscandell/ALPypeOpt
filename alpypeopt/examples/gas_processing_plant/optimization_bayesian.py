from alpypeopt import AnyLogicModel
from bayes_opt import BayesianOptimization

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
# Create input variable ratios as (min, max) to
# define the bounds of the search space
pbounds = {
    'dec1_flow_allocation': (0.01, 0.99),
    'dec1_temperature': (20.0, 100.0),
    'dec2_temperature': (20.0, 100.0)
}

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

# Setup and execute sequential optimmization model
def simulation_with_named_args(dec1_flow_allocation, dec1_temperature, dec2_temperature):
    x = [dec1_flow_allocation, dec1_temperature, dec2_temperature]
    return simulation(x)

# run the optimizer
optimizer = BayesianOptimization(
    f=simulation_with_named_args,
    pbounds=pbounds,
    random_state=1234
)

optimizer.maximize(
    init_points=5,  # the number of random initialization points
    n_iter=100  # the number of evaluations of simulation
)

print(f"Solution is {optimizer.max['params']} for a value of {optimizer.max['target']}")

# Run simulation with optimal result to use UI to explore results in AnyLogic
best_x = list(optimizer.max['params'].values())
simulation(best_x, reset=False)

# Close model
gpp_model.close()