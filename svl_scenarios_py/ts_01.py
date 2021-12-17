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

print("Running test scenario #01: ", end=' ')

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
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(-412.969665527344, 35.5481224060059, 72.5444946289063)) # Delta garage
print("EGO location set")

# Create ego vehicle
# White UT Bolt Lexus (Modular): 9c98739c-05cf-4325-99a5-644b800161ba
ego = sim.add_agent(name = "9c98739c-05cf-4325-99a5-644b800161ba", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Location NPC  
npcState.transform.position = lgsvl.Vector(-412.9, 35.5190963745117, 76.4997787475586)
#npcState.transform.position = egoState.transform.position + (2 * -right) # x meters ahead of the EGO and in the direction related to spawn[0] point

# Create agent
bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
print("NPC Bob added")

# Move agent 

# Bob will walk to a random point on sidewalk
bob.walk_randomly(True)

# Move pedestrian using waypoints (position, idle, trigger_distance=0, speed=1, trigger=None)
#waypoints = [
  #lgsvl.WalkWaypoint(lgsvl.Vector(-412.7, 35.4, 76.499), 20, 0)
  ##lgsvl.WalkWaypoint(egoState.transform.position + (2 * -right), 30, 0)
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
destination = sim.map_point_on_lane(lgsvl.Vector(-191.551727294922, 34.2335243225098, 167.90690612793)) # After 1st traffic light
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
