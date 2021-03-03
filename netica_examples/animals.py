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
bayesian_network = N.NewNet_bn (b"Animals", env)

# create each node in the network
Animal = N.NewNode_bn(b"Animal", 5, bayesian_network)
HasShell = N.NewNode_bn(b"HasShell", 2, bayesian_network)
Environment = N.NewNode_bn(b"Environment", 3, bayesian_network)
Class = N.NewNode_bn(b"Class", 3, bayesian_network)
BearsYoung = N.NewNode_bn(b"BearsYoung", 2, bayesian_network)
WarmBlooded = N.NewNode_bn(b"WarmBlooded", 2, bayesian_network)
BodyCovering = N.NewNode_bn(b"BodyCovering", 3, bayesian_network)

# adding states to each node
N.SetNodeStateNames_bn(Animal, b"monkey,penguin,platypus,robin,turtle")
N.SetNodeStateNames_bn(HasShell, b"true,false")
N.SetNodeStateNames_bn(Environment, b"air,land,water")
N.SetNodeStateNames_bn(Class, b"bird,mammal,reptile")
N.SetNodeStateNames_bn(WarmBlooded, b"true,false")
N.SetNodeStateNames_bn(BodyCovering, b"fur,feathers,scales")


# adding links between nodes
N.AddLink_bn(Animal, HasShell)
N.AddLink_bn(Animal, BearsYoung)
N.AddLink_bn(Animal, Class)
N.AddLink_bn(Animal, Environment)
N.AddLink_bn(Class, WarmBlooded)
N.AddLink_bn(Class, BodyCovering)


# setting the probabilities for each top level node
#N.SetNodeProbs (Animal, 0.2, 0.2, 0.2, 0.2, 0.2)

N.SetNodeFuncState (HasShell, 1, b'monkey')
N.SetNodeFuncState (HasShell, 1, b'penguin')
N.SetNodeFuncState (HasShell, 1, b'platypus')
N.SetNodeFuncState (HasShell, 1, b'robin')
N.SetNodeFuncState (HasShell, 0, b'turtle')


N.SetNodeProbs (Environment, b'monkey',0,1,0)
N.SetNodeProbs (Environment, b'penguin',0, 0.5,0.5)
N.SetNodeProbs (Environment, b'platypus',0,0,1)
N.SetNodeProbs (Environment, b'robin',0.5,0.5,0)
N.SetNodeProbs (Environment, b'turtle',0,0.5,0.5)


N.SetNodeFuncState (BearsYoung,0, b'monkey')
N.SetNodeFuncState (BearsYoung,1, b'penguin')
N.SetNodeFuncState (BearsYoung,1, b'platypus')
N.SetNodeFuncState (BearsYoung,1, b'robin')
N.SetNodeFuncState (BearsYoung,1, b'turtle')


N.SetNodeFuncState (Class,1, b'monkey')
N.SetNodeFuncState (Class,0, b'penguin')
N.SetNodeFuncState (Class,1, b'platypus')
N.SetNodeFuncState (Class,0, b'robin')
N.SetNodeFuncState (Class,2, b'turtle')


N.SetNodeFuncState (WarmBlooded,0, b'bird')
N.SetNodeFuncState (WarmBlooded,0, b'mammal')
N.SetNodeFuncState (WarmBlooded,1, b'reptile')


N.SetNodeFuncState (BodyCovering,1, b'bird')
N.SetNodeFuncState (BodyCovering,0, b'mammal')
N.SetNodeFuncState (BodyCovering,2, b'reptile')


# print the error message in case of any errors within Netica
err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)

# compile the final network
N.CompileNet_bn (bayesian_network)            

# get the belief for each state for PopulationOutcome
belief = N.GetNodeBelief (b"Animal", b"turtle", bayesian_network)
print("The probability of being turtle is {:#.4f}".format(belief))


N.EnterFinding (b"WarmBlooded", b'true', bayesian_network)
belief = N.GetNodeBelief (b"Animal", b"turtle", bayesian_network)
print("The probability of being turtle when its WarmBlooded {:#.4f}".format(belief))


# delete the network and print the returned message
N.DeleteNet_bn (bayesian_network)
res = N.CloseNetica_bn (env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8"))
print("-" * 65 + "\n")
