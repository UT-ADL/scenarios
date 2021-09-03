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

print("Running Test Scenario 7: ", end=' ')

sim = lgsvl.Simulator(LGSVL__SIMULATOR_HOST, LGSVL__SIMULATOR_PORT)

print("Sim version = ", sim.version)


# *** Load the map ***

# Tartu v3 map UUID: e340b6cd-fc15-4293-871b-4cf9cb4410a5
scene_name = env.str("LGSVL__MAP", "e340b6cd-fc15-4293-871b-4cf9cb4410a5")
if sim.current_scene == scene_name:
    sim.reset()
else:
    sim.load(scene_name, seed = 650388) # initial: 650387
    
    

# *** Spawn EGO ***

spawns = sim.get_spawn()
egoState = lgsvl.AgentState()

# Moving directions
forward = lgsvl.utils.transform_to_forward(spawns[0])
right = lgsvl.utils.transform_to_right(spawns[0])

# Spawn location:
egoState.transform = sim.map_point_on_lane(lgsvl.Vector(223.959732055664, 35.8595199584961, 141.793914794922)) # After the bus stop after Turu building 
print("EGO location set")

# Create EGO vehicle
ego = sim.add_agent(name = "289c5010-fd86-4134-8d65-8439a5d3fd40", agent_type = lgsvl.AgentType.EGO, state = egoState)



# *** Spawn NPC-s ***

npcState = lgsvl.AgentState()

# Location NPC 
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(167.006286621094, 35.7150001525879, 86.8554382324219)) # 2nd lane, before Raekoja
# Create player
npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Location NPC
npcState.transform = sim.map_point_on_lane(lgsvl.Vector(137.883590698242, 35.5834655761719, 61.8928718566895)) # 2nd lane, before Raekoja
# Create player
npc_hatchback = sim.add_agent("Hatchback", lgsvl.AgentType.NPC, npcState)
print("NPC car added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(70.8441314697266, 35.7108154296875, 20.5888748168945) # Raekoja, around the crossing
# Create player
npc_bike1 = sim.add_agent("Bicyclist", lgsvl.AgentType.NPC, npcState)
print("NPC bicyclist added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(66.0694122314453, 35.7059631347656, 31.0675354003906) # Raekoja, around the crossing
# Create player
npc_bike2 = sim.add_agent("Bicyclist", lgsvl.AgentType.NPC, npcState)
print("NPC bicyclist added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(70.3364791870117, 35.7130584716797, 19.6686458587646) # Raekoja, around the crossing
# Create player
npc_segway = sim.add_agent("SegwayKickScooterMaxG30LP", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_segway.walk_randomly(True)
print("NPC segway added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(57.7405548095703, 35.699893951416, 27.1777667999268) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(66.9059295654297, 35.7073020935059, 18.7154960632324) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("EntrepreneurFemale", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(62.7869491577148, 35.7033233642578, 29.7536697387695) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Howard", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(74.8051147460938, 35.7080001831055, 22.8980484008789) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Johny", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(72.0412292480469, 35.7300148010254, 35.6478691101074) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Johny", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(74.7052307128906, 35.7213821411133, 16.9852600097656) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Pamela", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(56.4283676147461, 35.6898880004883, 30.6000308990479) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Presley", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(59.8627090454102, 35.7001266479492, 28.835620880127) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Robin", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(66.2516403198242, 35.5999984741211, 20.4688777923584) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Stephen", lgsvl.AgentType.PEDESTRIAN, npcState)
npc_pedestrian.walk_randomly(True)
print("NPC pedestrian added")

# Location NPC 
npcState.transform.position = lgsvl.Vector(52.328067779541, 35.671272277832, 28.9139347076416) # Raekoja, around the crossing
# Create player
npc_pedestrian = sim.add_agent("Zoe", lgsvl.AgentType.PEDESTRIAN, npcState)
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
destination = sim.map_point_on_lane(lgsvl.Vector(-65.8986282348633, 35.154167175293, -13.0648355484009)) # On a straight after Raekoja and the bus stop

print("Point on lane found")

dv.setup_apollo(destination.position.x, destination.position.z, modules)
print("Destination set")


# Run the sim
print("Running the sim..")
sim.run()
print("Done. Test scenario run finished.")
