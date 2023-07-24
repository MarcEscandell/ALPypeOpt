import logging
from alpypeopt.anylogic.model.connector import AnyLogicModelConnector


class AnyLogicModel:
    """
    The python class that contains the AnyLogic model connection and is in 
    charge of setting and retrieving the information required to be returned to the
    optimization model
    """

    def __init__(
        self,
        env_config: dict = {
            'run_exported_model': True,
            'exported_model_loc': './exported_model',
            'show_terminals': False,
            'server_mode_on': False,
            'verbose': False
        }
    ):
        """
        Internal AnyLogic environment wrapper constructor

        :param env_config: Environment configuration which includes:

            * ``'run_exported_model'``: In case you want to run an exported 
              version of the model. Otherwise it will wait for the AnyLogic 
              model to connect. 
            * ``'exported_model_loc'``: The location of the exported model folder. 
            * ``'show_terminals'``: This only applies if running an exported 
              model and the user wants a terminal to be launched for every 
              model instance (could be useful for debugging purposes). 
            * ``'verbose'``: To be activated in case DEBUG logger wants to be 
              activated. 

        :type env_config: dict
        
        """
        # Initialise `env_config` to avoid problems when handling `None`
        self.env_config = env_config if env_config is not None else []

        # Initialise logger
        verbose = (
            'verbose' in self.env_config
            and self.env_config['verbose']
        )
        # Only log message from `alpyperl`
        ch = logging.StreamHandler()
        ch.addFilter(logging.Filter('alpypeopt'))
        # Create logger configuration
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.INFO,
            format=f"%(asctime)s [%(name)s][%(levelname)8s] %(message)s",
            handlers=[ch],
        )
        self.logger = logging.getLogger(__name__)

        # Launch or connect to AnyLogic model using the connector and launcher.
        self.anylogic_connector = AnyLogicModelConnector(
            run_exported_model=(
                self.env_config['run_exported_model'] 
                if 'run_exported_model' in self.env_config 
                else True
            ),
            exported_model_loc=(
                self.env_config['exported_model_loc'] 
                if 'exported_model_loc' in self.env_config 
                else './exported_model'
            ),
            show_terminals=(
                self.env_config['show_terminals'] 
                if 'show_terminals' in self.env_config 
                else False
            )
        )
        # The gateway is the direct interface to the AnyLogic model.
        self.anylogic_model = self.anylogic_connector.gateway

        # Initialise and prepare the model by calling `reset` method.
        self.anylogic_model.reset()
        
        self.logger.info("AnyLogic model has been initialized correctly!")

    def setup_and_run(self, model_configuration):
        """`[INTERNAL]` Basic function for controlling the AnyLogic simulation.
        It requires a `model configuration` as an input. After that
        the simulation will be run until the end.
        """

        # Run fast simulation until next action is required (which will be
        # controlled and requested from the AnyLogic model)
        return self.anylogic_model.setupAndRun(model_configuration)


    def reset(self, *, seed=None, options=None):
        """`[INTERNAL]` Reset function will restart the AnyLogic model to its 
        initial status.
        """
        # Reset simulation to restart from initial conditions
        # Return tuble: STATE, INFO
        return self.anylogic_model.reset()

    def get_model_output(self):
        """`[INTERNAL]` Retrieve model output object from AnyLogic simulation
        """
        return self.anylogic_model.getModelOutput()


    def close(self):
        """`[INTERNAL]` Close executables if any was created"""
        self.anylogic_connector.close_connection()

    def get_jvm(self):
        return self.anylogic_model.jvm
