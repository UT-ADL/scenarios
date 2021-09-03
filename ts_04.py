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

print("Running Test Scenario 4: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-45.6839637756348, 34.6999969482422, 228.409133911133)) # Before Raatuse traffic light
print("EGO location set")

# Create EGO vehicle
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)



# *** Spawn NPC-s ***
npcState = lgsvl.AgentState()

# Location NPC vehicle
#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-0.450218200683594, 34.7490425109863, 253.205596923828)) # In a bus stop after Raatuse traffic light >> goes to 1st lane in the running sim, not in the bus stop...

## Test if this is better for placing the bus in the actual bus stop 
npcState.transform.position = lgsvl.Vector(-0.450218200683594, 34.7490425109863, 253.205596923828)
npcState.transform.rotation.y = 50

# Create NPC vehicle
npc_sedan = sim.add_agent("SchoolBus", lgsvl.AgentType.NPC, npcState)
print("NPC schoolbus added")


# Location NPC pedestrian
#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(67.3545532226563, 36, 302.627014160156)) # On a crosswalk after Raatuse traffic light
npcState.transform.position = lgsvl.Vector(67.3545532226563, 36, 302.627014160156)

# Create NPC pedestrian
bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
print("NPC Bob added")


# Move NPC
# .. TODO ..
#
#


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
destination = sim.map_point_on_lane(lgsvl.Vector(89.4868850708008, 36, 315.898773193359)) # Slightly after the crosswalk
print("Point on lane found")

dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# Run the sim
print("Running the sim..")
sim.run()
print("Done. Test scenario run finished.")
