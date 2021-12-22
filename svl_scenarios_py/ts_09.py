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

print("Running Test Scenario #09: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-330.781524658203, 34.9901733398438, -74.3826904296875)) # Before the first traffic light at the Botanical garden, behind a vehicle
print("EGO location set")

# Create ego vehicle
# UT Bolt Lexus : 80a96c6b-18b6-494f-a469-e67659ca0ea0
# UT Bolt Lexus (Modular): 9c98739c-05cf-4325-99a5-644b800161ba
# UT Bolt Lexus (Modular TFL): f6fbbc88-87c0-4a83-b858-e2a49e98b4a9
# SVL default Lincoln: 2e9095fa-c9b9-4f3f-8d7d-65fa2bb03921
ego = sim.add_agent(name = "9c98739c-05cf-4325-99a5-644b800161ba", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Location NPC 
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-336.56396484375, 35.0898208618164, -74.7427291870117)) # Before the first traffic light at the Botanical garden

# Create agent
npc_jeep = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Move agent

# Vehicle will follow the lane with max speed and isLaneChange=True/False
npc_jeep.follow_closest_lane(True, 5, False)


# Add 2nd NPC vehicle

npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-395.176513671875, 36.178295135498, -72.37890625)) # On the crossing at Botanical garden 2nd traffic light

npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# No movement for the NPC.


# Add 3rd NPC vehicle

npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-570.116455078125, 35.1528854370117, 93.4908218383789)) # On the roundabout

npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Vehicle will follow the lane with max speed and isLaneChange=True/False
#npc_sedan.follow_closest_lane(True, 2.0, False)

# Vehicle will follow the waypoints with: 
# coordinates, speed, acceleration, rotation, opt wait time, active on idling, opt trigger distance.
waypoints_sedan = [
    lgsvl.DriveWaypoint(lgsvl.Vector(-566.656,35.139,98.900), 6, 0, lgsvl.Vector(0.122, 32.601, 0), 0, False, 15),
    lgsvl.DriveWaypoint(lgsvl.Vector(-564.899,35.152,101.007), 5, 0, lgsvl.Vector(359.719, 39.823, -1.334), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-563.175,35.166,102.788), 5, 0, lgsvl.Vector(359.668, 44.070, 0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-560.938,35.190,104.745), 5, 0, lgsvl.Vector(359.544, 48.810, 0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-558.889,35.181,106.322), 5, 0, lgsvl.Vector(0.204, 52.423, -6.670), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-553.712,35.139,108.911), 5, 0, lgsvl.Vector(0.410, 63.435, -1.334), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-547.096,35.054,110.779), 5, 0, lgsvl.Vector(0.713, 74.227, -2.668), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-541.026,34.970,111.171), 5, 0, lgsvl.Vector(0.784, 86.309, 0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-526.143,34.808,109.943), 5, 0, lgsvl.Vector(0.621, 94.716, 0), 0, False, 0)
]
npc_sedan.follow(waypoints_sedan, loop=False)


## Add 4th NPC - pedestrian

#npcState.transform.position = lgsvl.Vector(-569.733276367188, 35.6070251464844, 39.4083480834961) # Before the roundabout
#npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
#print("NPC pedestrian added")


# Add 5th NPC - pedestrian

npcState.transform.position = lgsvl.Vector(-562.620178222656, 35.5997886657715, 44.8293342590332) # Before the roundabout
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 6th NPC - pedestrian

npcState.transform.position = lgsvl.Vector(-574.94091796875, 35.5904235839844, 67.8564224243164) # Before the roundabout
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")



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
destination = sim.map_point_on_lane(lgsvl.Vector(-563.70751953125, 35.7000007629395, 102.238693237305)) # On the exit of the roundabout
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
