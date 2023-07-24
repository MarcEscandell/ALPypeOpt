##########################################
Running your model directly from AnyLogic
##########################################

If you are **debugging** or **unable to export** your model (e.g. you don't have a valid license) you can run your simulation experiment directly from *AnyLogic* and connect to your *python script*.

To do so, you should take into account the following considerations:

* In your *python script*, regardless of the framework that you use, you should ensure that:

    * You add the ``run_exported_model`` into the ``env_config`` dictionary and set to ``False``.
    * Your framework **only launches 1 instance** of the environment. 

* You execute first your *python script* and then launch your *AnyLogic* model. When you run your python script, you will receive a message like this:

    .. code-block:: console

        2023-07-21 13:51:43,569 [alpypeopt.anylogic.model.connector][    INFO] You can now launch your AnyLogic model! 'ALPypeOptConnector' will handle the connection for you.

  After that, you are good to proceed to *AnyLogic*.