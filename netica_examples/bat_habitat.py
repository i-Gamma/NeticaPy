from NeticaPy import Netica
import os

BASE_DIR = os.getcwd()

N = Netica()

INFINITY_ns = N.GetInfinityDbl_ns()
mesg = bytearray()
env = N.NewNeticaEnviron_ns(b"", None, b"")
res = N.InitNetica2_bn(env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
print("-" * 65 + "\n")

# initializing the network with environment
bayesian_network = N.NewNet_bn(b"BatHabitatBasinscale", env)

# create each node in the network
RangeExpansionContraction = N.NewNode_bn(b"RangeExpansionContraction", 5, bayesian_network)
Connectivity = N.NewNode_bn(b"Connectivity", 5, bayesian_network)
EnvIndexRelHistorical = N.NewNode_bn(b"EnvIndexRelHistorical", 5, bayesian_network)
OtherOrganisms = N.NewNode_bn(b"OtherOrganisms", 2, bayesian_network)
PopulationSizeEffect = N.NewNode_bn(b"PopulationSizeEffect", 2, bayesian_network)
EnvironmentalOutcome = N.NewNode_bn(b"EnvironmentalOutcome", 5, bayesian_network)
NonHabitatInfluences = N.NewNode_bn(b"NonHabitatInfluences", 3, bayesian_network)
PopulationOutcome = N.NewNode_bn(b"PopulationOutcome", 5, bayesian_network)

# setting node levels for the contiuous variables that have been made discrete
N.SetNodeLevels_bn(RangeExpansionContraction, 5, [0, 20, 40, 60, 80, INFINITY_ns])
N.SetNodeLevels_bn(Connectivity, 5, [0, 20, 40, 60, 80, INFINITY_ns])
N.SetNodeLevels_bn(EnvIndexRelHistorical, 5, [0, 20, 40, 60, 80, INFINITY_ns])

# adding states to each node
N.SetNodeStateNames_bn(OtherOrganisms, b"absent,present")
N.SetNodeStateNames_bn(PopulationSizeEffect, b"absent,present")
N.SetNodeStateNames_bn(EnvironmentalOutcome, b"A,B,C,D,E")
N.SetNodeStateNames_bn(NonHabitatInfluences, b"strong,medium,weak")
N.SetNodeStateNames_bn(PopulationOutcome, b"A,B,C,D,E")
N.SetNodeStateNames_bn(RangeExpansionContraction, b"r0_20,r20_40,r40_60,r60_80,greater80")
N.SetNodeStateNames_bn(Connectivity, b"r0_20,r20_40,r40_60,r60_80,greater80")
N.SetNodeStateNames_bn(EnvIndexRelHistorical, b"r0_20,r20_40,r40_60,r60_80,greater80")

# adding links between nodes
N.AddLink_bn(RangeExpansionContraction, EnvironmentalOutcome)
N.AddLink_bn(Connectivity, EnvironmentalOutcome)
N.AddLink_bn(EnvIndexRelHistorical, EnvironmentalOutcome)
N.AddLink_bn(OtherOrganisms, NonHabitatInfluences)
N.AddLink_bn(PopulationSizeEffect, NonHabitatInfluences)
N.AddLink_bn(EnvironmentalOutcome, PopulationOutcome)
N.AddLink_bn(NonHabitatInfluences, PopulationOutcome)

# setting the probabilities for each top level node
N.SetNodeProbs(RangeExpansionContraction, 0.2, 0.2, 0.2, 0.2, 0.2)
N.SetNodeProbs(Connectivity, 0.2, 0.2, 0.2, 0.2, 0.2)
N.SetNodeProbs(EnvIndexRelHistorical, 0.2, 0.2, 0.2, 0.2, 0.2)
N.SetNodeProbs(OtherOrganisms, 0.5, 0.5)
N.SetNodeProbs(PopulationSizeEffect, 0.5, 0.5)

# assigning probabilities for the lower level nodes
N.SetNodeProbs(NonHabitatInfluences, b"absent", b"absent", 0.0, 0.0, 1.0)
N.SetNodeProbs(NonHabitatInfluences, b"absent", b"present", 0.5, 0.4, 0.1)
N.SetNodeProbs(NonHabitatInfluences, b"present", b"absent", 0.1, 0.3, 0.6)
N.SetNodeProbs(NonHabitatInfluences, b"present", b"present", 0.9, 0.1, 0.0)

# Set the node probabilities for EnvironmentalOutcome from a TSV file
# since there are too many values
ranges = [b"r0_20", b"r20_40", b"r40_60", b"r60_80", b"greater80"]

with open(BASE_DIR + '/Environmental Outcome.txt') as f:
    env_data = [list(map(float, i.split())) for i in f.readlines()]

count = 0
for i in ranges:
    for j in ranges:
        for k in ranges:
            N.SetNodeProbs(EnvironmentalOutcome, i, j, k, env_data[count][0], env_data[count][1],
                           env_data[count][2], env_data[count][3], env_data[count][4])
            # print "N.SetNodeProbs (EnvironmentalOutcome, "+i+", "+j+", "+k+", "+str(env_data[count][0])+", "+str(env_data[count][1])+", "+str(env_data[count][2])+", "+str(env_data[count][3])+", "+str(env_data[count][4])
            count += 1

# set the node function for the Population Outcome
N.SetNodeFuncState(PopulationOutcome, 2, b"A", b'strong')
N.SetNodeFuncState(PopulationOutcome, 1, b"A", b'medium')
N.SetNodeFuncState(PopulationOutcome, 0, b"A", b'weak')
N.SetNodeFuncState(PopulationOutcome, 3, b"B", b'strong')
N.SetNodeFuncState(PopulationOutcome, 2, b"B", b'medium')
N.SetNodeFuncState(PopulationOutcome, 1, b"B", b'weak')
N.SetNodeFuncState(PopulationOutcome, 4, b"C", b'strong')
N.SetNodeFuncState(PopulationOutcome, 3, b"C", b'medium')
N.SetNodeFuncState(PopulationOutcome, 2, b"C", b'weak')
N.SetNodeFuncState(PopulationOutcome, 4, b"D", b'strong')
N.SetNodeFuncState(PopulationOutcome, 4, b"D", b'medium')
N.SetNodeFuncState(PopulationOutcome, 3, b"D", b'weak')
N.SetNodeFuncState(PopulationOutcome, 4, b"E", b'strong')
N.SetNodeFuncState(PopulationOutcome, 4, b"E", b'medium')
N.SetNodeFuncState(PopulationOutcome, 4, b"E", b'weak')

# print the error message in case of any errors within Netica
err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)
# compile the final network
N.CompileNet_bn(bayesian_network)

# get the belief for each state for PopulationOutcome
belief = N.GetNodeBelief(b"PopulationOutcome", b"A", bayesian_network)
print("The probability is {}".format(belief))

belief = N.GetNodeBelief(b"PopulationOutcome", b"B", bayesian_network)
print("The probability is {}".format(belief))

belief = N.GetNodeBelief(b"PopulationOutcome", b"C", bayesian_network)
print("The probability is {}".format(belief))

belief = N.GetNodeBelief(b"PopulationOutcome", b"D", bayesian_network)
print("The probability is {}".format(belief))

belief = N.GetNodeBelief(b"PopulationOutcome", b"E", bayesian_network)
print("The probability is {}".format(belief))

# delete the network and print the returned message
N.DeleteNet_bn(bayesian_network)

res = N.CloseNetica_bn(env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8"))
print("-" * 65 + "\n")

