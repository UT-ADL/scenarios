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


# Description of the test scenarios 01-10

TS_01

Start driving from Delta driveway after a pedestrian has left from the ego vehicle’s path (adult human standing in front of the car at ~2 m distance). Make a right turn to the road and with max speed 40 km/h continue in the first lane, then stop at red traffic light. The blinker must be turned on and off as expected for the maneuver.


TS_02

Start driving at green light next to another car in the left lane. With max speed 40 km/h, continue straight. Stop behind a car at red traffic light, next to more stopped cars in the left lane.


TS_03

Start driving at green light and start following a vehicle ahead. With max speed 40 km/h, continue straight. Stop behind the leading car at red light, then continue when the lead car starts moving with green. Stop following the leading car when it leaves (to the left changing the lane) and continue straight until the traffic light. Stop at red light.


TS_04

Start driving at green light and start following a public transport vehicle who came from the bus stop on the right. With max speed 40 km/h, follow the bus until it leaves the lane, then stop following it. Give way (stop fully if necessary to keep safe distance) to a pedestrian straight ahead on the unregulated pedestrian crossing. Then continue driving and stop after the crosswalk.


TS_05

Drive by following the lane in a slight curve of the road and move to the new lane on the right as it appears after the bridge. The blinker must be used correctly for the maneuver. Stop at red light before turning right on the crossing.


TS_06

Start driving from Kaubamaja traffic light when green, complete the right turn and handle also the next traffic light. Then continue straight, follow a slow car and handle one more traffic light. Be ready to respond to a bus pulling out from the stop.


TS_07

With max speed 40 km/h drive pass the cars who have parked on the right side of the road and be ready to react to them pulling out or being too much on the road. Stop if necessary for safety. After passing the parking spots, stop at red light in Raekoja. Be ready to stop for pedestrians who may cross the road also when it is green for the ego car. After that start driving with green.


TS_08

With max speed 40 km/h drive straight and start following a vehicle ahead until it leaves to the left. Stop behind the red traffic light or a pedestrian crossing the road with wrong light.


TS_09

Start driving behind a leading car and handle the traffic lights correctly even if the leading car starts driving with red light. Continue across the Delta bridge and be ready to stop for pedestrians on the crosswalks before the roundabout. Drive out to the roundabout and be ready to follow a vehicle on the roundabout.


TS_10

Enter the roundabout, be ready to follow a vehicle and be ready to stop for pedestrians on the crosswalk right after the roundabout. Continue driving and if needed, follow a vehicle. To finish the drive, go to the pocket after the bus stop and stop there in a way that does not disturb other vehicles who drive on the road.

