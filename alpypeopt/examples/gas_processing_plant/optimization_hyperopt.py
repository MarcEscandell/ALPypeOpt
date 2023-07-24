from alpypeopt import AnyLogicModel
from hyperopt import fmin, tpe, hp
import random

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
# define the space over which to search
space = [
    hp.uniform('dec1 flow allocation', 0.01, 0.99),
    hp.uniform('dec1 temperature', 20.0, 100.0),
    hp.uniform('dec2 temperature', 20.0, 100.0)
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
    return -model_output.getTotalRevenue()

best = fmin(fn=simulation,  # the function to minimize
            space=space,  # the bounds on each dimension of x
            algo=tpe.suggest,  # the algorithm to use
            max_evals=500)  # the number of evaluations of simulation

# Get best X values
best_x = list(best.values())
print(f"Solution is {best} for a value of {-simulation(best_x)}")

# Run simulation with optimal result to use UI to explore results in AnyLogic
simulation(best_x, reset=False)

# Close model
gpp_model.close()
