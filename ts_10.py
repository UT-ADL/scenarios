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



# *** Load the map ***

# Tartu v3 map UUID: e340b6cd-fc15-4293-871b-4cf9cb4410a5
scene_name = env.str("LGSVL__MAP", "e340b6cd-fc15-4293-871b-4cf9cb4410a5")
if sim.current_scene == scene_name:
    sim.reset()
else:
    sim.load(scene_name, seed = 650387) 
    
    

# *** Spawn EGO ***

spawns = sim.get_spawn()
egoState = lgsvl.AgentState()

# Moving directions
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# Spawn location:
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-578.168518066406, 35.7000007629395, 73.3115463256836)) # Before the roundabout
print("EGO location set")

# Create vehicle
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# *** Spawn NPC-s ***

npcState = lgsvl.AgentState()

# Location NPC 
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-569.962829589844, 35.7000045776367, 93.7434005737305)) # Roundabout
# Create agent
npc_hatchback = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npcState)
print("NPC hatchpack added")
# Move agent
npc_hatchback.follow_closest_lane(True, 5.6, False)
print("NPC hatchback moving")

## Location NPC
#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-535.827392578125, 35.2202301025391, 107.277183532715)) # After the roundabout
## Create player
#npc_truck = sim.add_agent("BoxTruck", lgsvl.AgentType.NPC, npcState)
#print("NPC car added")

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-438.066497802734, 34.4155693054199, 97.8415832519531)) # After Delta pocket
# Create player
npc_truck = sim.add_agent("BoxTruck", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Location NPC
npcState.transform.position = lgsvl.Vector(-555.035461425781, 35.6290016174316, 104.12264251709) # After the roundabout
# Create player
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC
npcState.transform.position = lgsvl.Vector(-558.037292480469, 35.7999992370605, 110.737693786621) # After the roundabout
# Create player
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")



# Connect the EGO to a bridge at the specified IP and port
ego.connect_bridge(LGSVL__AUTOPILOT_0_HOST, LGSVL__AUTOPILOT_0_PORT) 
print("Waiting for connection...")
while not ego.bridge_connected:
    time.sleep(1)
print("Bridge connected:", ego.bridge_connected)



# *** Apollo Dreamview setup ***

print("Starting DV setup.. ")
dv = lgsvl.dreamview.Connection(sim, ego, LGSVL__AUTOPILOT_0_HOST)
dv.set_hd_map(env.str("LGSVL__AUTOPILOT_HD_MAP", 'tartu_3.0'))
dv.set_vehicle(env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'UT Lexus LGSVL'))


# Make sure all modules are initially off
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


# Set EGO destination
print("Setting destination..")
destination = sim.map_point_on_lane(lgsvl.Vector(-462.392547607422, 35.0585632324219, 97.4237060546875)) # Delta pocket

print("Point on lane found")

dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# *** Run the sim ***

print("Running the sim..")
sim.run()
print("Done. Test scenario run finished.")
