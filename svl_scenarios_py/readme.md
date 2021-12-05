# Running Python test scenarios in Linux

## Prepare

- Install and run [Apollo] (https://github.com/ApolloAuto/apollo).
- Download and run [SVL Simulator] (https://github.com/lgsvl/simulator).
- Place the correct map and vehicle files in the according Apollo directories like guided in Apollo documentation.
    - Map source in SVL sim store [Tartu Beta Release 3](https://wise.svlsimulator.com/maps/profile/bd77ac3b-fbc3-41c3-a806-25915c777022):
    - Vehicle source in SVL sim store [UT Lexus](https://wise.svlsimulator.com/vehicles/profile/55e7bb62-185e-400f-b092-cfd2ef18936d): 

## Simulation

- In SVL web UI create an [API-only simulation](https://www.svlsimulator.com/docs/running-simulations/running-simulator/#apionlysimulation).
- Run the API-only simulation.
- The SVL simulator program window must show "API Ready!".

## Scenario

- Run the Python scenario script.
- Observe the run in SVL sim program window.

## Results

- After the scenario is finished, stop the API-only simulation in SVL web UI.
- To view the results check the Test Results in the web UI.

To run a next scenario, start the API-only sim and run the next Python script.


# Example run of the 1st scenario:

Terminal 1

```
./repos/apollo/docker/scripts/dev_start.sh
./repos/apollo/docker/scripts/dev_into.sh
./scripts/bootstrap_lgsvl.sh
./scripts/bridge.sh
```


Terminal 2

```
./svlsimulator-linux64-2021.2/simulator
```


Browser SVL simulator window + login

- Simulations -> Run the API-only simulation


Terminal 3

```
./svl_test_scen/ts_01.py
```


SVL simulator program window

- Observe the scenario running


Browser SVL simulator window

- Stop the API-only simulation
- View the Test Results in the web UI

# More on SVL Python API with guide and examples by LGSVL

[LGSVL - A Python API repo](https://github.com/lgsvl/PythonAPI)
