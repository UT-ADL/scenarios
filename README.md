## ADL test scenarios repository

### This repository contains test scenarios for running with SVL simulation and Apollo 

#### SVL scenarios json

- contains SVL scenarios to run with VSE and a howto

#### SVL scenarios py

- contains SVL scenarios to run with Python API and a howto

#### Test Cases

Overview what is covered in the **full lap** test scenarios:

| Test case | Covered in scenario | Not covered |
|-----------|---------------------|:-----------:|
| The start of the scenario is in the Delta driveway | VSE (json): garage-to-pocket UT Lexus no NPC | |
| The start of the scenario is in the Delta pocket | VSE (json): pocket-to-pocket UT Lexus NPC vehicles | |
| The destination of the scenario is in the Delta pocket | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The ego vehicle starts driving from the Delta pocket | VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle is positioned correctly in the lane and keeps the first lane | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle handles the speed regulations correctly | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle handles the traffic lights correctly | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle keeps safe distance with a vehicle ahead | VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle performs all turns along the route correctly | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle drives one full lap following the first lane | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| The vehicle finishes the lap by pulling over to the Delta pocket and stops there | VSE (json): garage-to-pocket UT Lexus no NPC <br> VSE (json): pocket-to-pocket UT Lexus NPC vehicles ||
| Pedestrian related test cases || :white_check_mark: |


#### Known Issues

SVL sim v2021.3 + Apollo 6 (Modular)

1. Sometimes NPC-s are not in exactly the same places when running the sim multiple times in a row. Depending on how much time it takes for the Apollo to start, NPC-s may have moved less or more. It is better with waypoint behavior but not perfect.
1. Sometimes the ego vehicle drives into the NPC vehicle and the other way around (the two meshes visually overlap in the sim). Happens even when the NPC is detected and the ego vehicle reduces speed because of it. The collision event is still expected to be registered and visible under the SVL web UI Test Results.
1. Sometimes NPC vehicles perform maneuvers chunkily. Can be smoothed out by placing the NPC waypoints very close together to create a smoother turning curve or use already smoother turning curve. But it is still not perfect.
1. Pedestrians with waypoints don't work as expected currently. Waiting for the fix by SVL. Not using pedestrians waypoint movement until then.
1. The blinker is not visible in the sim.
