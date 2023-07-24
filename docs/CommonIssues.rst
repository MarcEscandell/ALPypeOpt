################################################
Most common issues and how to troubleshoot them
################################################

These are some of the most common issues captured by users when seting up or running *ALPypeOpt*:

* You missed implementing ``ALPypeOptClientController`` required methods.

If you face an issue that doesn't appear in this list and are unable to solve it, feel free to raise it `here <https://github.com/users/MarcEscandell/projects/1/views/2>`_ as others might benefit from it. 

****************************************************************
You missed the implementation of ``ALPypeOptClientController``
****************************************************************

You can fail to implement ``ALPypeOptClientController`` in two ways:

* You didn't add ``ALPypeOptClientController`` to the list of interfaces of your ``root`` (``Main``) model. When that happens, the python side or ``alpypeopt`` won't be able to control your simulation model in the way that is required. You will be getting the following *class casting exception*:

.. code-block:: console

	java.lang.ClassCastException: class gasprocessingplant.Main cannot be cast to class com.alpypeopt.ALPypeOptClientController (gasprocessingplant.Main and com.alpypeopt.ALPypeOptClientController are in unnamed module of loader 'app')
	at com.alpypeopt.ALPypeOptConnector.getClientController(ALPypeOptConnector.java:226)
	at com.alpypeopt.RLJavaControllerImpl.setupAndRun(RLJavaControllerImpl.java:118)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.base/java.lang.reflect.Method.invoke(Method.java:566)
	at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
	at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
	at py4j.Gateway.invoke(Gateway.java:282)
	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at py4j.commands.CallCommand.execute(CallCommand.java:79)
	at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
	at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
	at java.base/java.lang.Thread.run(Thread.java:834)

From the *python* side you will be able to read:

.. code-block:: console

	It seems you haven't implemented 'ALPypeOptClientController'. Go to your 'root' agent (where you should have dropped 'ALPypeOptConnector') and search for 'Advanced Java / Implements (comma-separated list of interfaces)'. Then add 'ALPypeOptClientController' to your list and implement the required functions

* You forgot to implement ``ALPypeOptClientController`` functions. This is a more visual error, as it will be highlighted during your AnyLogic model compilation. In a way that is good, because it indicates clearly that you are missing something. You'll see something like:

For both case, you might want to review how it is done :ref:`here <The AnyLogic Connector>`.