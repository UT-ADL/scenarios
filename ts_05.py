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

print("Running Test Scenario #05: ", end=' ')

# To connect to the sim create an instance of the Simulator class
sim = lgsvl.Simulator(LGSVL__SIMULATOR_HOST, LGSVL__SIMULATOR_PORT)

print("Sim version = ", sim.version)


# ---- Load the map ----

# Tartu v3 map UUID:    e340b6cd-fc15-4293-871b-4cf9cb4410a5
# Tartu v4:             bd77ac3b-fbc3-41c3-a806-25915c777022
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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(71.8815994262695, 36, 304.734069824219)) # Slightly after Spark crosswalk 
print("EGO location set")

# Create EGO vehicle
# Default SVL Lexus, UT conf:   289c5010-fd86-4134-8d65-8439a5d3fd40
# New UT Bolt Lexus:            9c98739c-05cf-4325-99a5-644b800161ba
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(70.1595001220703, 36.0000038146973, 307.440490722656)) # 2nd lane, next to the ego

# Create agent

npc_jeep = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Move agent

# Vehicle will follow the lane with max speed and isLaneChange=True/False
npc_jeep.follow_closest_lane(True, 5, False)


# Add 2nd NPC vehicle

npcState.transform = sim.map_point_on_lane(lgsvl.Vector(338.482818603516, 35.1646957397461, 265.132659912109)) # Before Kaubamaja crossing, headed towards Riia

npc_bus = sim.add_agent("SchoolBus", lgsvl.AgentType.NPC, npcState)
print("NPC schoolbus added")

# No movement for 2nd NPC.


# Add 3rd NPC vehicle

npcState.transform = sim.map_point_on_lane(lgsvl.Vector(329.894226074219, 35.4422149658203, 274.821685791016)) # Before Kaubamaja crossing, headed towards Riia

npc_bus2 = sim.add_agent("SchoolBus", lgsvl.AgentType.NPC, npcState)
print("NPC schoolbus added")

# No movement for 3rd NPC.



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
dv.set_hd_map(env.str("LGSVL__AUTOPILOT_HD_MAP", 'tartu_4.0'))
dv.set_vehicle(env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'UT Lexus LGSVL'))



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
destination = sim.map_point_on_lane(lgsvl.Vector(333.390045166016, 35.2918090820313, 240.538223266602)) # Slightly after the Kaubamaja traffic light
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
