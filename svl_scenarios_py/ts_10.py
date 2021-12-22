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

print("Running Test Scenario #10: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-578.168518066406, 35.7000007629395, 73.3115463256836)) # Before the roundabout
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
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-548.789367675781, 35.0765838623047, 110.301696777344)) # Roundabout

# Create agent
npc_hatchback = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npcState)
print("NPC hatchpack added")

# Move agent

## Vehicle will follow the lane with max speed and isLaneChange=True/False
#npc_hatchback.follow_closest_lane(True, 5.6, False)

waypoints_hatchback = [
    lgsvl.DriveWaypoint(lgsvl.Vector(-544.156,35.016,111.195), 6, 0, lgsvl.Vector(0.734, 79.080, 0), 0, False, 15),
    lgsvl.DriveWaypoint(lgsvl.Vector(-538.615,34.941,111.152), 5, 0, lgsvl.Vector(0.775, 90.441, -5.336), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-517.421,34.703,108.729), 5, 0, lgsvl.Vector(0.637, 96.522, 0), 0, False, 0),
    lgsvl.DriveWaypoint(lgsvl.Vector(-428.956,34.299,96.753), 5, 0, lgsvl.Vector(0.259, 97.709, 2.668), 0, False, 0)
]
npc_hatchback.follow(waypoints_hatchback, loop=False)



# Add 3rd NPC - pedestrian

### Pedestrians are buggy in v2021.3. Waiting for SVL fix.

npcState.transform.position = lgsvl.Vector(-555.035461425781, 35.6290016174316, 104.12264251709) # After the roundabout
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 4th NPC - pedestrian

npcState.transform.position = lgsvl.Vector(-558.037292480469, 35.7999992370605, 110.737693786621) # After the roundabout
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
destination = sim.map_point_on_lane(lgsvl.Vector(-462.392547607422, 35.0585632324219, 97.4237060546875)) # Delta pocket
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
