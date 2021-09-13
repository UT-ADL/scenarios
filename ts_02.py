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

print("Running Test Scenario #02: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-232.292602539063, 34.0190620422363, 151.503433227539)) # Before the 1st traffic light
print("EGO location set")

# Create ego vehicle
# Default SVL Lexus, UT conf:   289c5010-fd86-4134-8d65-8439a5d3fd40
# New UT Bolt Lexus:            9c98739c-05cf-4325-99a5-644b800161ba
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Location NPC 
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-234.575881958008, 34.013126373291, 153.956207275391)) # 2nd lane, before the 1st traffic light

# Create agent
npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Move agent

# Vehicle will follow the lane with max speed and isLaneChange=True/False
npc_sedan.follow_closest_lane(True, 2.8, False)


# Add 2nd NPC vehicle

npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-116.178810119629, 34.693717956543, 201.754211425781)) # 2nd lane, before the 2nd traffic light

npc_sedan_2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)

# Add 3rd NPC car

npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-208.839691162109, 34.1423034667969, 160.910614013672)) # 1st lane, after the traffic light

npc_sedan_3 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)

# Car will follow the lane with max speed and isLaneChange=True/False
npc_sedan_3.follow_closest_lane(True, 3.0, False) 



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
destination = sim.map_point_on_lane(lgsvl.Vector(-79.4582595825195, 34.7000007629395, 213.437240600586)) # After Kivi konsum traffic light
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
