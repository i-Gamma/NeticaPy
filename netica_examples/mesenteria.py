from NeticaPy import Netica
import os

BASE_DIR = os.getcwd()

N = Netica()

INFINITY_ns = N.GetInfinityDbl_ns()
mesg = bytearray()
env = N.NewNeticaEnviron_ns(b"", None, b"")
res = N.InitNetica2_bn (env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
print("-" * 65 + "\n")

# initializing the network with environment
bayesian_network = N.NewNet_bn (b"Mesentria", env)

# create each node in the network
Snags = N.NewNode_bn(b"Snags", 3, bayesian_network)
Stumps = N.NewNode_bn(b"Stumps", 3, bayesian_network)
TreeCanopyCover = N.NewNode_bn(b"TreeCanopyCover", 3, bayesian_network)
MesicIndicatorPlants = N.NewNode_bn(b"MesicIndicatorPlants", 3, bayesian_network)
DecayClass = N.NewNode_bn(b"DecayClass", 4, bayesian_network)
SubstrateType = N.NewNode_bn(b"SubstrateType", 2, bayesian_network)
LocalSlope = N.NewNode_bn(b"LocalSlope", 2, bayesian_network)
LocalVegetation = N.NewNode_bn(b"LocalVegetation", 2, bayesian_network)
Pinaceae = N.NewNode_bn(b"Pinaceae", 2, bayesian_network)
BMesPresence = N.NewNode_bn(b"BMesPresence", 2, bayesian_network)



# setting node levels for the contiuous variables that have been made discrete
N.SetNodeLevels_bn(Snags,3,[0,0,100,INFINITY_ns])
N.SetNodeLevels_bn(Stumps,3,[0,0,100,INFINITY_ns])
N.SetNodeLevels_bn(TreeCanopyCover,3,[0,50,80,100])
N.SetNodeLevels_bn(LocalSlope,2,[0,30,INFINITY_ns])


N.SetNodeStateNames_bn(Snags, b"r0,r0_100,greater100")
N.SetNodeStateNames_bn(Stumps, b"r0,r0_100,greater100")
N.SetNodeStateNames_bn(TreeCanopyCover, b"r0_50,r50_80,r80_100")
N.SetNodeStateNames_bn(LocalSlope, b"r0_30,greater30")
N.SetNodeStateNames_bn(MesicIndicatorPlants, b"abundant,sparse,absent")
N.SetNodeStateNames_bn(DecayClass, b"sound,intermediate,decayed,none")
N.SetNodeStateNames_bn(SubstrateType, b"adequate,inadequate")
N.SetNodeStateNames_bn(LocalVegetation, b"adequate,inadequate")
N.SetNodeStateNames_bn(Pinaceae, b"adequate,inadequate")
N.SetNodeStateNames_bn(BMesPresence, b"present,absent")



# adding links between nodes
N.AddLink_bn(Stumps, SubstrateType)
N.AddLink_bn(Snags, SubstrateType)
N.AddLink_bn(MesicIndicatorPlants, LocalVegetation)
N.AddLink_bn(TreeCanopyCover, LocalVegetation)
N.AddLink_bn(SubstrateType, Pinaceae)
N.AddLink_bn(DecayClass, Pinaceae)
N.AddLink_bn(Pinaceae, BMesPresence)
N.AddLink_bn(LocalVegetation, BMesPresence)
N.AddLink_bn(LocalSlope, BMesPresence)


N.SetNodeProbs (SubstrateType, b'r0', b'r0',0.0,1.0)
N.SetNodeProbs (SubstrateType, b'r0', b'r0_100',0.5,0.5)
N.SetNodeProbs (SubstrateType, b'r0', b'greater100',1,0)
N.SetNodeProbs (SubstrateType, b'r0_100', b'r0',0.5,0.5)
N.SetNodeProbs (SubstrateType, b'r0_100', b'r0_100',0.5,0.5)
N.SetNodeProbs (SubstrateType, b'r0_100', b'greater100',1,0)
N.SetNodeProbs (SubstrateType, b'greater100', b'r0',1,0)
N.SetNodeProbs (SubstrateType, b'greater100', b'r0_100',1,0)
N.SetNodeProbs (SubstrateType, b'greater100', b'greater100',1,0)

N.SetNodeProbs (LocalVegetation, b'abundant', b'r0_50',0.1,0.9)
N.SetNodeProbs (LocalVegetation, b'abundant', b'r50_80',0.8,0.2)
N.SetNodeProbs (LocalVegetation, b'abundant', b'r80_100',1,0)
N.SetNodeProbs (LocalVegetation, b'sparse', b'r0_50',0.1,0.9)
N.SetNodeProbs (LocalVegetation, b'sparse', b'r50_80',0.5,0.5)
N.SetNodeProbs (LocalVegetation, b'sparse', b'r80_100',0.7,0.3)
N.SetNodeProbs (LocalVegetation, b'absent', b'r0_50',0,1)
N.SetNodeProbs (LocalVegetation, b'absent', b'r50_80',0.2,0.8)
N.SetNodeProbs (LocalVegetation, b'absent', b'r80_100',0.5,0.5)

N.SetNodeProbs (Pinaceae, b'adequate', b'sound',0.2,0.8)
N.SetNodeProbs (Pinaceae, b'adequate', b'intermediate',1,0)
N.SetNodeProbs (Pinaceae, b'adequate', b'decayed',1,0)
N.SetNodeProbs (Pinaceae, b'adequate', b'none',0,1)
N.SetNodeProbs (Pinaceae, b'inadequate', b'sound',0.1,0.9)
N.SetNodeProbs (Pinaceae, b'inadequate', b'intermediate',0.5,0.5)
N.SetNodeProbs (Pinaceae, b'inadequate', b'decayed',0.5,0.5)
N.SetNodeProbs (Pinaceae, b'inadequate', b'none',0,1)


N.SetNodeProbs (BMesPresence, b'adequate', b'adequate', b'r0_30',1,0)
N.SetNodeProbs (BMesPresence, b'adequate', b'adequate', b'greater30',0.8,0.2)
N.SetNodeProbs (BMesPresence, b'adequate', b'inadequate', b'r0_30',0.8,0.2)
N.SetNodeProbs (BMesPresence, b'adequate', b'inadequate', b'greater30',0.5,0.5)
N.SetNodeProbs (BMesPresence, b'inadequate', b'adequate', b'r0_30',0.1,0.9)
N.SetNodeProbs (BMesPresence, b'inadequate', b'adequate', b'greater30',0.05,0.95)
N.SetNodeProbs (BMesPresence, b'inadequate', b'inadequate', b'r0_30',0.05,0.95)
N.SetNodeProbs (BMesPresence, b'inadequate', b'inadequate', b'greater30',0,1)


# print the error message in case of any errors within Netica
err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)

# compile the final network
N.CompileNet_bn (bayesian_network)            

belief = N.GetNodeBelief (b"BMesPresence", b"absent", bayesian_network)
print("The probability is {:#.5g}".format(belief))

assert belief == 0.6162800788879395
