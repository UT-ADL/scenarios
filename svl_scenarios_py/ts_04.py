#!/usr/bin/env python3

import time
import logging
from environs import Env
import lgsvl


FORMAT = "[%(levelname)6s] [%(name)s] %(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
log = logging.getLogger(__name__)

env = Env()

LGSVL__SIMULATOR_HOST = env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1")
LGSVL__SIMULATOR_PORT = env.int("LGSVL__SIMULATOR_PORT", 8181)
LGSVL__AUTOPILOT_0_HOST = env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1")
LGSVL__AUTOPILOT_0_PORT = env.int("LGSVL__AUTOPILOT_0_PORT", 9090)

print("Running Test Scenario #04: ", end=' ')

# To connect to the sim create an instance of the Simulator class
sim = lgsvl.Simulator(LGSVL__SIMULATOR_HOST, LGSVL__SIMULATOR_PORT)

print("Sim version = ", sim.version)



# ---- Load the map ----

# Tartu Beta Release 3:             bd77ac3b-fbc3-41c3-a806-25915c777022
scene_name = env.str("LGSVL__MAP", "bd77ac3b-fbc3-41c3-a806-25915c777022")
if sim.current_scene == scene_name:
    sim.reset()
else:
    sim.load(scene_name, seed = 650387)
    
    

# ---- Spawn EGO ----

spawns = sim.get_spawn()
egoState = lgsvl.AgentState()

# Moving directions
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# Spawn location:
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-45.6839637756348, 34.6999969482422, 228.409133911133)) # Before Raatuse traffic light
#egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-39.8863754272461, 34.5125274658203, 231.681564331055)) # After Raatuse tfl stop line
print("EGO location set")

# Create EGO vehicle
# White UT Bolt Lexus : 80a96c6b-18b6-494f-a469-e67659ca0ea0
# White UT Bolt Lexus (Modular): 9c98739c-05cf-4325-99a5-644b800161ba
# White UT Bolt Lexus (Modular TFL): f6fbbc88-87c0-4a83-b858-e2a49e98b4a9
ego = sim.add_agent(name = "9c98739c-05cf-4325-99a5-644b800161ba", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Location NPC
npcState.transform.position = lgsvl.Vector(-3.50375366210938, 34.5999984741211, 251.514205932617)
npcState.transform.rotation = lgsvl.Vector(359.895416259766, 55.5014457702637, 3.33505845162563)


# Create agent
npc_bus = sim.add_agent("SchoolBus", lgsvl.AgentType.NPC, npcState)
print("NPC schoolbus added")

# Move agent

# Vehicle will follow the lane with max speed and isLaneChange=True/False
#npc_bus.follow_closest_lane(True, 4.0, False)

# Vehicle will follow the waypoints with: 
# coordinates, speed, acceleration, rotation, opt wait time, active on idling, opt trigger distance.
waypoints_bus = [
    lgsvl.DriveWaypoint(lgsvl.Vector(5.491,34.619,257.696), 6, 0, lgsvl.Vector(359.895, 55.501, 0.0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(9.271,34.645,261.596), 5, 0, lgsvl.Vector(359.728, 44.098, -6.670), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(13.432,34.688,266.259), 5, 0, lgsvl.Vector(359.610, 41.750, -2.668), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(49.419,34.778,294.043), 5, 0, lgsvl.Vector(359.885, 52.329, 6.670), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(62.929,34.545,303.019), 5, 0, lgsvl.Vector(0.824, 56.399, -2.668), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(95.488,34.648,324.829), 5, 0, lgsvl.Vector(359.849, 56.183, 0.0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(98.133,34.667,329.132), 5, 0, lgsvl.Vector(359.781, 31.576, -1.334), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(99.556,34.826,333.803), 5, 0, lgsvl.Vector(358.134, 16.951, -2.669), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(100.884,34.865,340.404), 5, 0, lgsvl.Vector(359.668, 11.373, -6.670), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(100.278,34.926,349.244), 5, 0, lgsvl.Vector(359.607, 356.074, -8.337), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(99.370,34.875,354.753), 5, 0, lgsvl.Vector(0.523, 350.648, 3.335), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(97.980,34.642,361.229), 5, 0, lgsvl.Vector(2.007, 347.884, 0.0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(97.183,34.546,364.139), 5, 0, lgsvl.Vector(1.831, 344.681, -5.338), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(94.529,34.442,379.626), 5, 0, lgsvl.Vector(0.379, 350.275, 3.335), 0, False, 0)
]
npc_bus.follow(waypoints_bus, loop=False)


# Add pedestrian 

# Pedestrians movement buggy in SVL sim v2021.3. Waiting for the fix.

#npcState.transform.position = lgsvl.Vector(67.3545532226563, 36, 302.627014160156) # On the crosswalk

#bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#print("NPC Bob added")

## Move pedestrian using waypoints (position, idle, trigger_distance=0, speed=1, trigger=None)
#waypoints = [
  #lgsvl.WalkWaypoint(lgsvl.Vector(68.662, 36.097, 298.176), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(68.695, 36.000, 301.075), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(66.649, 35.997, 301.745), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(68.188, 36.000, 302.914), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(66.366, 35.998, 303.374), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(63.864, 35.996, 307.898), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(69.826, 36.099, 298.005), 0, 0, 2, None)
#]
#bob.follow(waypoints, loop=True)



# ---- Connect bridge ----

# Connect the EGO to a bridge at the specified IP and port
ego.connect_bridge(LGSVL__AUTOPILOT_0_HOST, LGSVL__AUTOPILOT_0_PORT) 
print("Waiting for connection...")
while not ego.bridge_connected:
    time.sleep(1)
print("Bridge connected:", ego.bridge_connected)



# ---- Apollo Dreamview setup ----

print("Starting DV setup.. ")
dv = lgsvl.dreamview.Connection(sim, ego, LGSVL__AUTOPILOT_0_HOST)
dv.set_hd_map(env.str("LGSVL__AUTOPILOT_HD_MAP", 'Tartu Beta Release 3'))
dv.set_vehicle(env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'UT Lexus'))
#dv.set_vehicle(env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'Lincoln2017MKZ_LGSVL'))


# Ensure all modules initially OFF
dv.disable_apollo()

# Enable needed modules
modules = [
        'Localization',
        'Transform',
        'Routing',
        'Prediction',
        'Planning',
        'Control'
        ]


print("Setting destination..")

# Set EGO destination
destination = sim.map_point_on_lane(lgsvl.Vector(89.4868850708008, 36, 315.898773193359)) # Slightly after the crosswalk
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
