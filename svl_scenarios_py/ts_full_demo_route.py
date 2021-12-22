#!/usr/bin/env python3

import time
import logging
from environs import Env
import lgsvl


env = Env()

LGSVL__SIMULATOR_HOST = env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1")
LGSVL__SIMULATOR_PORT = env.int("LGSVL__SIMULATOR_PORT", 8181)
LGSVL__AUTOPILOT_0_HOST = env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1")
LGSVL__AUTOPILOT_0_PORT = env.int("LGSVL__AUTOPILOT_0_PORT", 9090)

print("Running test scenario #Full lap ", end=' ')

# To connect to the sim create an instance of the Simulator class
sim = lgsvl.Simulator(LGSVL__SIMULATOR_HOST, LGSVL__SIMULATOR_PORT)

print("Sim version = ", sim.version)



# ---- Load the map ----

# Tartu v4 aka beta:    bd77ac3b-fbc3-41c3-a806-25915c777022
# Tartu beta sim v3:    d2026dd2-31f6-4037-b4e2-722468d46588
# Tartu beta release 3: bd77ac3b-fbc3-41c3-a806-25915c777022
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
# Default SVL Lexus, UT conf:   289c5010-fd86-4134-8d65-8439a5d3fd40
# New white UT Bolt Lexus:      9c98739c-05cf-4325-99a5-644b800161ba
ego = sim.add_agent(name = "9c98739c-05cf-4325-99a5-644b800161ba", agent_type = lgsvl.AgentType.EGO, state = egoState)
print("EGO vehicle added")

#control = lgsvl.VehicleControl()
#control.handbrake = True



# ---- Spawn NPC-s ----

npcState = lgsvl.AgentState()

# Add NPC 1 - pedestrian1

### NPC bugs in 2021.3 are waiting for SVL fix in the next release.

## Location NPC  
#npcState.transform.position = lgsvl.Vector(-412.9, 35.5190963745117, 76.4997787475586)

## Create agent
#bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#print("NPC Bob added")

## Move agent 

## Bob will walk to a random point on sidewalk
#bob.walk_randomly(True)

## Move Bob using waypoints (position, idle, trigger_distance=0, speed=1, trigger=None)

## _______________ waypoints still need editing, play with idle time and speed: _______________

#waypoints = [
  #lgsvl.WalkWaypoint(lgsvl.Vector(-412.900, 35.519, 76.499), 9, 0, 1, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(-412.677, 35.037, 87.926), 1, 0, 1, None)
#]
#bob.follow(waypoints, loop=True)

## -----

## Add NPC 2 - vehicle

## Location NPC 
#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-234.575881958008, 34.013126373291, 153.956207275391)) # 2nd lane, before the 1st traffic light

## Create agent
#npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
#print("NPC car added")

## Move agent
## Vehicle will follow the lane with max speed and isLaneChange=True/False
#npc_sedan.follow_closest_lane(True, 2.8, False)


## Add NPC 3 - vehicle

## Location NPC
#npcState.transform.position = lgsvl.Vector(-0.450218200683594, 34.7490425109863, 253.205596923828) # In Raatuse bus stop
#npcState.transform.rotation.y = 50

## Create agent
#npc_bus = sim.add_agent("SchoolBus", lgsvl.AgentType.NPC, npcState)
#print("NPC schoolbus added")

## Move agent
## Vehicle will follow the lane with max speed and isLaneChange=True/False
#npc_bus.follow_closest_lane(True, 4.0, False)


## Add NPC 4 - pedestrian

#npcState.transform.position = lgsvl.Vector(67.3545532226563, 36, 302.627014160156) # On SPARK crosswalk

#bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#print("NPC Bob added")

## Move pedestrian using waypoints (position, idle, trigger_distance=0, speed=1, trigger=None)
#waypoints = [
  #lgsvl.WalkWaypoint(lgsvl.Vector(68.662, 36.097, 298.176), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(68.695, 36.000, 301.075), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(66.649, 35.997, 301.745), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(68.188, 36.000, 302.914), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(66.366, 35.998, 303.374), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(63.864, 35.996, 307.898), 0, 0, 2, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(69.826, 36.099, 298.005), 0, 0, 2, None)
#]
#bob.follow(waypoints, loop=True)


### Add NPC 5 - pedestrian

### Location NPC 
##npcState.transform.position = lgsvl.Vector(57.7405548095703, 35.699893951416, 27.1777667999268) # Raekoja, around the crossing
### Create agent
##npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
##npc_pedestrian.walk_randomly(True)
##print("NPC pedestrian added")


### Add NPC 6 - pedestrian

### Location NPC 
##npcState.transform.position = lgsvl.Vector(66.2516403198242, 35.5999984741211, 20.4688777923584) # Raekoja, around the crossing
### Create agent
##npc_pedestrian = sim.add_agent("Stephen", lgsvl.AgentType.PEDESTRIAN, npcState)
##npc_pedestrian.walk_randomly(True)
##print("NPC pedestrian added")


## Add NPC 7 - vehicle

## Location NPC 
#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-80.2668304443359, 35.5404357910156, -26.9127502441406)) # Gildi street
## Create agent
#npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
#print("NPC car added")
## Move agent
## Vehicle will follow the lane with max speed and isLaneChange=True/False
#npc_sedan.follow_closest_lane(True, 7, False)


## Add NPC 8 - pedestrian

## Location NPC 
#npcState.transform.position = lgsvl.Vector(-344.361389160156, 35.1095428466797, -80.8969879150391) # Botanical garden traffic light 1, around the crossing
## Create agent
#bob = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#print("NPC pedestrian added")

## Move pedestrian using waypoints (position, idle, trigger_distance=0, speed=1, trigger=None)
#waypoints = [
  #lgsvl.WalkWaypoint(lgsvl.Vector(-346.33, 34.61, -63.73), 0, 0, 1, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(-348.94, 35.05, -64.99), 0, 0, 1, None),
  #lgsvl.WalkWaypoint(lgsvl.Vector(-343.98, 35.10, -80.85), 0, 0, 2, None)
#]
#bob.follow(waypoints, loop=True)


## Add NPC 9 - vehicle

#npcState.transform = sim.map_point_on_lane(lgsvl.Vector(-395.176513671875, 36.178295135498, -72.37890625)) # On the crossing at Botanical garden 2nd traffic light

#npc_sedan = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npcState)
#print("NPC car added")

## No movement for the NPC.


## Add NPC 10 - pedestrian

#npcState.transform.position = lgsvl.Vector(-562.620178222656, 35.5997886657715, 44.8293342590332) # Before the roundabout
#npc_pedestrian = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, npcState)
#npc_pedestrian.walk_randomly(True)
#print("NPC pedestrian added")






# Callback on collision:

def on_collision(agent1, agent2, contact):
  name1 = "STATIC OBSTACLE" if agent1 is None else agent1.name
  name2 = "STATIC OBSTACLE" if agent2 is None else agent2.name
  print("{} collided with {} at {}".format(name1, name2, contact))
  sim.stop()

ego.on_collision(on_collision)




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
destination = sim.map_point_on_lane(lgsvl.Vector(-472.491394042969, 34.6208724975586, 98.7638397216797)) # Delta pocket
print("Point on lane found")
#dv.setup_apollo(destination.position.x, destination.position.z, modules)
#print("Destination set")
# Instead of dv.setup_apollo(), try this alternative for not starting the sim until Apollo is ready:

print("enable Localization")
dv.enable_module('Localization')
print("enable Transform")
dv.enable_module('Transform')
print("enable Routing")
dv.enable_module('Routing')
print("enable Prediction")
dv.enable_module('Prediction')
print("enable control")
dv.enable_module('Control')

modules_status = dv.get_module_status()
if (modules_status['Planning']):
    print("disable Planning")
    dv.disable_module('Planning')

while(not modules_status['Routing']):
    print('waiting for Routing module')
    time.sleep(1)
    modules_status = dv.get_module_status()
    
print("Setting the destination..")

# Set EGO destination
destination = sim.map_point_on_lane(lgsvl.Vector(-472.491394042969, 34.6208724975586, 98.7638397216797)) # Delta pocket
print("Point on lane found")
dv.set_destination(destination.position.x, destination.position.z)
print("Destination set")
print("Enabling planning..")
dv.enable_module('Planning')

while(not modules_status['Planning']):
    print('Waiting for Planning module')
    time.sleep(1)
    modules_status = dv.get_module_status()
    
print("wait")
time.sleep(5)
print("waiting over")


# ---- Run sim ----

print("Running the sim..")
sim.run(360) # Increasing the time may be needed if NPC-s enabled, depending on NPC related behavior.
print("Done.")
