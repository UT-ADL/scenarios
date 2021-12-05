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

print("Running Test Scenario #08: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-64.3112945556641, 35.1543846130371, -12.6320610046387)) # On a straight after Raekoja 
print("EGO location set")

# Create ego vehicle
# Default SVL Lexus, UT conf:   289c5010-fd86-4134-8d65-8439a5d3fd40
# New UT Bolt Lexus:            9c98739c-05cf-4325-99a5-644b800161ba
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Location NPC 
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-80.2668304443359, 35.5404357910156, -26.9127502441406)) # Gildi street

# Create agent
npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Move agent

# Vehicle will follow the lane with max speed and isLaneChange=True/False
npc_sedan.follow_closest_lane(True, 7, False)


# Add 2nd NPC vehicle

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-90.3041229248047, 35.1508331298828, -19.6207733154297)) # On a straight after Gildi street

# Create agent
npc_jeep = sim.add_agent("Jeep", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Move agent

# Vehicle will follow the lane with max speed and isLaneChange=True/False
npc_jeep.follow_closest_lane(True, 3.5, False)


# Add 3rd NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(-344.361389160156, 35.1095428466797, -80.8969879150391) # Botanical garden traffic light 1, around the crossing
# Create agent
bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
print("NPC pedestrian added")

# Move pedestrian using waypoints (position, idle, trigger_distance=0, speed=1, trigger=None)
waypoints = [
  lgsvl.WalkWaypoint(lgsvl.Vector(-346.33, 34.61, -63.73), 0, 0, 1, None),
  lgsvl.WalkWaypoint(lgsvl.Vector(-348.94, 35.05, -64.99), 0, 0, 1, None),
  lgsvl.WalkWaypoint(lgsvl.Vector(-343.98, 35.10, -80.85), 0, 0, 2, None)
]
bob.follow(waypoints, loop=True)



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
destination = sim.map_point_on_lane(lgsvl.Vector(-379.425476074219, 35.7591323852539, -71.6994018554688)) # After the first traffic light at Botanical garden
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
