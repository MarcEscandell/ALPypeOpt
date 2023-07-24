###########################################
Running ``alpypeopt`` in a docker container
###########################################

If you are planning to develop your project in a **docker container**, you must be aware of the following:

* Connection between **python** and **AnyLogic** will potentially **fail**. This is due to *alpypeopt* trying to connect to a port that is not mapped between the **docker container** and **docker host**.
* Howerver, this is possible when running with an **exported model** as execution of the model will take place in the container. In the terminal, AnyLogic will share the port in case you want to access the model UI.

    .. code-block:: console
        :emphasize-lines: 3

        root@1ebabc066103:/workspaces/ALPypeOpt# python alpypeopt/examples/gas_processing_plant/optimization_skopt.py 
        chmod: cannot access 'chromium/chromium-linux64/chrome': No such file or directory
        Couldn't find browser: chromium/chromium-linux64/chrome. Attempting to open system-default browser for url: http://localhost:25057
        2023-07-21 05:57:15,062 [alpypeopt.wrapper.envs.anylogic_env][    INFO] AnyLogic model has been initialized correctly!