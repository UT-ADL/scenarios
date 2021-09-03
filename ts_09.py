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

print("Running Test Scenario 9: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-330.781524658203, 34.9901733398438, -74.3826904296875)) # Before the first traffic light at the Botanical garden, behind a vehicle
print("EGO location set")

# Create EGO vehicle
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)



# *** Spawn NPC-s ***

npcState = lgsvl.AgentState()

## Location NPC 
#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-336.56396484375, 35.0898208618164, -74.7427291870117)) # Before the first traffic light at the Botanical garden
## Create player
#npc_jeep = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npcState)
#print("NPC car added")

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-395.176513671875, 36.178295135498, -72.37890625)) # 
# Create player
npc_jeep = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-585.701110839844, 35.7000045776367, 81.6404571533203)) # 
# Create player
npc_hatchback = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-564.5048828125, 35.7000007629395, 101.415023803711)) # 
# Create player
npc_jeep = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Location NPC
npcState.transform.position = lgsvl.Vector(-569.733276367188, 35.6070251464844, 39.4083480834961) # Before the roundabout
# Create player
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC
npcState.transform.position = lgsvl.Vector(-562.620178222656, 35.5997886657715, 44.8293342590332) # Before the roundabout
# Create player
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC
npcState.transform.position = lgsvl.Vector(-585.439392089844, 35.6998977661133, 65.0804672241211) # Before the roundabout
# Create player
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(-584.79736328125, 35.6999816894531, 64.1584396362305) # Before the roundabout
# Create player
npc_segway = sim.add_agent("SegwayKickScooterMaxG30LP", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_segway.walk_randomly(True)
print("NPC segway added")

# Location NPC
npcState.transform.position = lgsvl.Vector(-574.94091796875, 35.5904235839844, 67.8564224243164) # Before the roundabout
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
destination = sim.map_point_on_lane(lgsvl.Vector(-563.70751953125, 35.7000007629395, 102.238693237305)) # On the exit of the roundabout

print("Point on lane found")

dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# Run the sim
print("Running the sim..")
sim.run()
print("Done. Test scenario run finished.")
