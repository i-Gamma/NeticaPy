from NeticaPy import Netica
import os

BASE_DIR = os.getcwd()
print(BASE_DIR)

# Initialize Netica
N = Netica()

# Get data to find the net and feed my Netica licence
with open("mis_datos.txt", "r", encoding= "utf-8") as my_file:
    my_data = my_file.readlines()

# Start Netica
my_bn = bytearray(my_data[1].strip("\n"), "utf8")
lic = bytearray(my_data[0].strip("\n"), "utf8")
mesg = bytearray()
env = N.NewNeticaEnviron_ns(lic, None, b"")
# env = N.NewNeticaEnviron_ns ("",None,"");
res = N.InitNetica2_bn(env, mesg)

print("\n" + "-" * 85)
print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
print("Ecosystem Integrity and Geographic-Ecological Descriptors")
print("-" * 85 + "\n")

# Load my network
nombre = N. NewFileStream_ns(my_bn, env)
net = N. ReadNet_bn (nombre, 0)

# Prepare Network for processing by compiling it
N.CompileNet_bn (net)
auto_update = N.SetNetAutoUpdate_bn(net, 0)  # 256 = on, 0 = off

# Get Nodes list and display their names, avoid "documentation nodes"
nodes_lst = N.GetNetNodes_bn(net)
n_nodes = N.LengthNodeList_bn (nodes_lst)
nodes_dic ={}
for n in range(n_nodes):
    node_pt =  N.NthNode_bn(nodes_lst, n)
    name = N.GetNodeName_bn(node_pt).decode("utf8")
    if not ("NOTE" in name or  "TITLE" in name):
        # Find the levels within each node
        n_levels = N.GetNodeNumberStates_bn(node_pt)
        node_levels = N.GetNodeLevels_bn(node_pt)
        nodes_dic[name] = {"node": node_pt,
                           "n": n_levels,
                           "levels": node_levels}
        print("----", name, n_levels, node_levels)

# Report on "tipo_uso" querying level "natural
bel_tipo_uso_natural = N.GetNodeBelief(b"tipo_uso", b"natural", net)
print("Tipo de uso natural: ", bel_tipo_uso_natural)

# Report on the "base" status of node "tipo_uso", recover all levels "priors"
bels_tipo_uso_natural = N.GetNodeBeliefs_bn(nodes_dic["tipo_uso"]["node"])
bels_tipo_uso_natural = [bels_tipo_uso_natural[l] for l in range(nodes_dic["tipo_uso"]["n"])]
print(bels_tipo_uso_natural)

# Report on the "base" status of node "tipo_uso": finding set to level "0", note retracting and updating operation
N.RetractNodeFindings_bn(nodes_dic["tipo_uso"]["node"])
N.EnterFinding_bn(nodes_dic["tipo_uso"]["node"], 0) # Equivalent to set evidence as to the given level
auto_update = N.SetNetAutoUpdate_bn (net, auto_update)

# Get results from adding some findings to the net
bels_tipo_uso_natural = N.GetNodeBeliefs_bn(nodes_dic["tipo_uso"]["node"])
bels_tipo_uso_natural = [bels_tipo_uso_natural[l] for l in range(nodes_dic["tipo_uso"]["n"])]
bels_ecor = N.GetNodeBeliefs_bn(nodes_dic["ecoregionsmx_lvl2"]["node"])
bels_ecor = [bels_ecor[l] for l in range(nodes_dic["ecoregionsmx_lvl2"]["n"])]
print(bels_tipo_uso_natural)
print(bels_ecor)

res = N.CloseNetica_bn (env, mesg)

print("\n" + "-" * 85)
print(mesg.decode("utf-8"))
print("-" * 85 + "\n")

