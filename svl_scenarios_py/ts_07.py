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

print("Running Test Scenario #07: ", end=' ')

# To connect to the sim create an instance of the Simulator class
sim = lgsvl.Simulator(LGSVL__SIMULATOR_HOST, LGSVL__SIMULATOR_PORT)

print("Sim version = ", sim.version)



# ---- Load the map ----

# Tartu Beta Release 3:             bd77ac3b-fbc3-41c3-a806-25915c777022
scene_name = env.str("LGSVL__MAP", "bd77ac3b-fbc3-41c3-a806-25915c777022")
if sim.current_scene == scene_name:
    sim.reset()
else:
    sim.load(scene_name, seed = 650388) # initial: 650387
    
    

# ---- Spawn EGO ----

spawns = sim.get_spawn()
egoState = lgsvl.AgentState()

# Moving directions
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# Spawn location:
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(223.959732055664, 35.8595199584961, 141.793914794922)) # After the bus stop on Vabaduse 
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
npcState.transform.position = lgsvl.Vector(170.644607543945, 35.7785263061523, 98.5207672119141) # Parking spot before Raekoja
npcState.transform.rotation.y = 229

# Create agent
npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# No movement for the NPC.


# Add 2nd NPC - vehicle

npcState.transform.position = lgsvl.Vector(153.18913269043, 35.6518669128418, 82.6977005004883) # Parking spot before Raekoja
npcState.transform.rotation.y = 230
# Create agent
npc_hatchback = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# No movement for the NPC.


# Add 3rd NPC - pedestrian

# Pedestrians are buggy in 2021.3. Waiting for SVL fix.

# Location NPC 
npcState.transform.position = lgsvl.Vector(57.7405548095703, 35.699893951416, 27.1777667999268) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 4th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(66.9059295654297, 35.7073020935059, 18.7154960632324) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("EntrepreneurFemale", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 5th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(62.7869491577148, 35.7033233642578, 29.7536697387695) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Howard", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 6th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(74.8051147460938, 35.7080001831055, 22.8980484008789) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Johny", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 7th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(72.0412292480469, 35.7300148010254, 35.6478691101074) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Johny", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 8th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(74.7052307128906, 35.7213821411133, 16.9852600097656) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Pamela", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 9th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(56.4283676147461, 35.6898880004883, 30.6000308990479) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Presley", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 10th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(59.8627090454102, 35.7001266479492, 28.835620880127) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Robin", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")


# Add 11th NPC - pedestrian

# Location NPC 
npcState.transform.position = lgsvl.Vector(66.2516403198242, 35.5999984741211, 20.4688777923584) # Raekoja, around the crossing
# Create agent
npc_pedestrian = sim.add_agent("Stephen", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
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
destination = sim.map_point_on_lane(lgsvl.Vector(-65.8986282348633, 35.154167175293, -13.0648355484009)) # On a straight after Raekoja
print("Point on lane found")
dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# ---- Run sim ----

print("Running the sim..")
sim.run()
print("Done.")
