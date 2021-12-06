# ADL test scenarios repository

## This repository contains test scenarios for running with SVL simulation and Apollo 

### SVL scenarios json

- contains SVL scenarios to run with VSE and a howto

### SVL scenarios py

- contains SVL scenarios to run with Python API and a howto

### Test Cases

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
