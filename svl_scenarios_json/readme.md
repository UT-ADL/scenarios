# Running VSE test scenarios in Linux

## Prepare

- Install and run [Apollo] (https://github.com/ApolloAuto/apollo).
- Download and run [SVL Simulator] (https://github.com/lgsvl/simulator).
- Place the correct map and vehicle files in the according Apollo directories like guided in Apollo documentation or in our quick Apollo summary guide [here](https://gitlab.cs.ut.ee/autonomous-driving-lab/apollo-ut-misc/-/tree/master/tutorials#apollo-setup).
    - Map source in SVL sim store [Tartu Beta Release 3](https://wise.svlsimulator.com/maps/profile/bd77ac3b-fbc3-41c3-a806-25915c777022).
    - Vehicle source in SVL sim store [UT Lexus](https://wise.svlsimulator.com/vehicles/profile/55e7bb62-185e-400f-b092-cfd2ef18936d).

## Simulation

- In SVL web UI create a [VSE based simulation](https://www.svlsimulator.com/docs/running-simulations/running-simulator/#vsesimulation).
- During the step of selecting the Test Case, select the desired json file of the scenario.
- Run the VSE based simulation.
- The SVL simulator program window must show that any maps/vehicles are downloading (when running first time) and after that the simulation starts playing.

## Scenario

- The scenario configuration is in the json file. 
- The scenario description is provided with the scenario (and below under the example run).
- Observe the run in SVL sim program window.

## Results

- After the scenario is finished, stop the VSE based simulation in SVL web UI.
- To view the results check the Test Results in the web UI.

To run another scenario, change the json file in the VSE based sim and run the sim again in the web UI.

## Example run of the full lap scenario (no NPC-s)

File name: `vse_sim3_fullLap_fromGarage_toPocket_utLexus_noNpc.json`

Description of the scenario & test cases

- There are no NPC-s in this scenario. The map is Tartu Beta Release 3 and the ego vehicle is UT Lexus with Apollo modular testing configuration.
    1. The start of the scenario is Delta driveway in front of the Delta garage.
    1. The destination of the scenario is in the Delta pocket.
    1. The ego vehicle starts driving from the Delta driveway.
    1. The vehicle is positioned correctly in the lane and keeps the first lane.
    1. The vehicle handles the speed regulations correctly.
    1. The vehicle handles the traffic lights correctly.
    1. The vehicle performs all turns along the route correctly.
    1. The vehicle drives one full lap following the first lane.
    1. The vehicle finishes the lap by pulling over to the Delta pocket and stops there.

Terminal 1

```
./repos/apollo/docker/scripts/dev_start.sh
./repos/apollo/docker/scripts/dev_into.sh
./scripts/bootstrap_lgsvl.sh
./scripts/bridge.sh
```

Terminal 2

```
./svlsimulator-linux64-2021.3/simulator
```

Browser SVL simulator window + login

- Simulations -> Run the VSE based simulation

SVL simulator program window

- Observe the scenario running

Browser SVL simulator window

- Stop the VSE based simulation
- View the Test Results in the web UI


# More on SVL VSE with guide and examples by LGSVL

You can also create your own scenarios easily in the SVL VSE editor and then run your own json files.

[SVL documentation about VSE](https://www.svlsimulator.com/docs/visual-scenario-editor/about-vse/)
