#################################################################
Running your simulation model as an AnyLogic ``CustomExperiment``
#################################################################

The ``CustomExperiment`` is a specific AnyLogic experiment type, enabling developers to generate and control experiments **solely through code**, without utilizing a graphical interface or predefined settings. For instance, in a *Monte-Carlo experiment*, users can define custom expressions for the simulation model parameters for each iteration and the output value to display in the results histogram.

This experiment type is commonly employed by developers to run the model without any visual elements (no simulation window will be launched), enabling interaction with the model exclusively through the *Console*. This approach is particularly advantageous when the primary focus is on **performance** or on running as many iterations as possible in a minimal time frame. This is facilitated by the absence of visual element rendering.

.. warning::
    However, **ALPypeOpt** requires you to notify the ``ALPypeOptConnector`` that it is running under a ``CustomExperiment`` and pass the required information (which include the *experiment command line arguments*).

    **At the moment, ALPypeOpt is unable to collect this information by itself.**

Here's a guide on how to proceed in case of the :ref:`Gas Processing Plant example<How to optimize your simulation model. The GPP example.>`:

.. code-block:: java
    :emphasize-lines: 17

    // Create Engine, initialize random number generator:
    Engine engine = createEngine();
    engine.setTimeUnit( SECOND );
    // Fixed seed (reproducible simulation runs)
    engine.getDefaultRandomGenerator().setSeed( System.currentTimeMillis() );
    engine.setStartTime( 0.0 );
    engine.setStartDate( toDate( 2023, FEBRUARY, 28, 16, 0, 0 ) );
    // Set stop time:
    engine.setStopTime( 3600.0 );
    // Create new root object:
    Main root = new Main( engine, null, null );
    // Setup parameters of root object here
    root.setParametersToDefaultValues();
    // Flag connection to python optimization script
    root.connectToOpt = true;
    // Notify ALPypeOptConnector is running under a custom experiment
    root.alPypeOptConnector.isCustomExperiment(getCommandLineArguments());
    // Prepare Engine for simulation:
    engine.start( root );

.. note::
    Do remember to set the *connectToOpt* as ``true`` as shown in the example.

    This is required in the package **examples** as the connection flag is set via an additional parameter. If you define this parameter directly at ``ALPypeOptConnector`` then you do not need to specify its value in the code.

If you want to test a ``CustomExperiment`` or use it as a base model for your project, you can find it at:

* The experiment has been created and stored inside the ``.alp`` file for the **GasProcessingPlant** example at ``./alpypeopt/examples/gas_processing_plant/GasProcessingPlant``.
* There is also an exported version located at ``./resources/exported_models/gas_processing_plant_custom_experiment``. Remember to point to this folder in your ``optimization.py`` script ``env_config`` and ``exported_model_loc`` when defining your environment.



