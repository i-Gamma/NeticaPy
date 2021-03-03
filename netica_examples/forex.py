from NeticaPy import Netica
import os

BASE_DIR = os.getcwd()

N = Netica()

mesg = bytearray()
env = N.NewNeticaEnviron_ns(b"", None, b"")
res = N.InitNetica2_bn (env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
print("-" * 65 + "\n")

# initializing the network with environment
bayesian_network = N.NewNet_bn (b"ForExConsideration", env)

# create each node in the network
UKInterestRates = N.NewNode_bn(b"UKInterestRates", 5, bayesian_network)
EcuRate = N.NewNode_bn(b"EcuRate", 4, bayesian_network)
FixedCosts = N.NewNode_bn(b"FixedCosts", 3, bayesian_network)
UnitCosts = N.NewNode_bn(b"UnitCosts", 6, bayesian_network)


UnitPrice = N.NewNode_bn(b"UnitPrice", 6, bayesian_network)
UnitSalesSterling = N.NewNode_bn(b"UnitSalesSterling", 9, bayesian_network)
UnitSalesEcu = N.NewNode_bn(b"UnitSalesEcu", 7, bayesian_network)
TotalSales = N.NewNode_bn(b"TotalSales", 3, bayesian_network)



# setting node levels for the contiuous variables that have been made discrete
N.SetNodeStateNames_bn(UKInterestRates, b"static,uplow,downlow,downhigh,uphigh")

N.SetNodeLevels_bn(EcuRate, 4, [160, 165, 170, 175, 176])


N.SetNodeStateNames_bn(EcuRate, b"er_160_165,er_165_170,er_170_175,er_175_176")
N.SetNodeStateNames_bn(FixedCosts, b"s50000,s55000,s60000")
N.SetNodeStateNames_bn(UnitCosts, b"c10,c11,c12,c13,c14,c15")
N.SetNodeStateNames_bn(UnitPrice, b"p1600,p1650,p1700,p1750,p1800,p1850")
N.SetNodeStateNames_bn(UnitSalesEcu, b"e6000,e7000,e8000,e9000,e10000,e11000,e12000")
N.SetNodeStateNames_bn(UnitSalesSterling, b"ss10000,ss11000,ss12000,ss13000,ss14000,ss15000,ss16000,ss17000,ss18000")

N.SetNodeStateNames_bn(TotalSales, b"complete,lose5,lose10")


# adding links between nodes
N.AddLink_bn(UKInterestRates, EcuRate)
N.AddLink_bn(UKInterestRates, FixedCosts)
N.AddLink_bn(EcuRate, UnitCosts)
N.AddLink_bn(FixedCosts, UnitCosts)

N.AddLink_bn(UnitCosts, UnitPrice)
N.AddLink_bn(UnitPrice, UnitSalesSterling)
N.AddLink_bn(UnitPrice, UnitSalesEcu)
N.AddLink_bn(EcuRate, UnitSalesEcu)
N.AddLink_bn(UnitSalesEcu, TotalSales)
N.AddLink_bn(UnitSalesSterling, TotalSales)

# setting the probabilities for each top level node
N.SetNodeProbs (UKInterestRates, 0.10, 0.30, 0.25, 0.25, 0.10)

N.SetNodeProbs (EcuRate, b"static",   0.17, 0.37, 0.28, 0.18)
N.SetNodeProbs (EcuRate, b"uplow",    0.05, 0.15, 0.50, 0.30)
N.SetNodeProbs (EcuRate, b"downlow",  0.25, 0.50, 0.15, 0.10)
N.SetNodeProbs (EcuRate, b"downhigh", 0.75, 0.25, 0.00, 0.00)
N.SetNodeProbs (EcuRate, b"uphigh",   0.00, 0.00, 0.25, 0.75)



N.SetNodeProbs (FixedCosts, b'static',   0.25, 0.55, 0.20)
N.SetNodeProbs (FixedCosts, b'uplow',    0.25, 0.50, 0.25)
N.SetNodeProbs (FixedCosts, b'downlow',  0.40, 0.45, 0.15)
N.SetNodeProbs (FixedCosts, b'downhigh', 0.60, 0.40, 0.00)
N.SetNodeProbs (FixedCosts, b'uphigh',   0.00, 0.40, 0.60)



N.SetNodeProbs(UnitCosts, b'er_160_165', b's50000',0.30, 0.30, 0.20, 0.10, 0.08, 0.02)
N.SetNodeProbs(UnitCosts, b'er_160_165', b's55000',0.20, 0.35, 0.25, 0.10, 0.08, 0.02)
N.SetNodeProbs(UnitCosts, b'er_160_165', b's60000',0.15, 0.40, 0.25, 0.10, 0.08, 0.02)
N.SetNodeProbs(UnitCosts, b'er_165_170', b's50000',0.10, 0.50, 0.20, 0.10, 0.07, 0.03)
N.SetNodeProbs(UnitCosts, b'er_165_170', b's55000',0.05, 0.50, 0.25, 0.10, 0.07, 0.03)
N.SetNodeProbs(UnitCosts, b'er_165_170', b's60000',0.00, 0.40, 0.35, 0.15, 0.07, 0.03)
N.SetNodeProbs(UnitCosts, b'er_170_175', b's50000',0.10, 0.25, 0.30, 0.20, 0.10, 0.05)
N.SetNodeProbs(UnitCosts, b'er_170_175', b's55000',0.05, 0.20, 0.40, 0.25, 0.05, 0.05)
N.SetNodeProbs(UnitCosts, b'er_170_175', b's60000',0.00, 0.15, 0.35, 0.30, 0.15, 0.05)
N.SetNodeProbs(UnitCosts, b'er_175_176', b's50000',0.00, 0.10, 0.15, 0.40, 0.25, 0.10)
N.SetNodeProbs(UnitCosts, b'er_175_176', b's55000',0.00, 0.05, 0.10, 0.30, 0.35, 0.20)
N.SetNodeProbs(UnitCosts, b'er_175_176', b's60000',0.00, 0.00, 0.05, 0.15, 0.50, 0.30)



N.SetNodeFuncState (UnitPrice, 0, b"c10")
N.SetNodeFuncState (UnitPrice, 1, b"c11")
N.SetNodeFuncState (UnitPrice, 2, b"c12")
N.SetNodeFuncState (UnitPrice, 3, b"c13")
N.SetNodeFuncState (UnitPrice, 4, b"c14")
N.SetNodeFuncState (UnitPrice, 5, b"c15")



err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)
print(1)


N.SetNodeProbs (UnitSalesSterling, b"p1600", 0.0, 0.0, 0.0, 0.0, 0.05, 0.10, 0.20, 0.45, 0.20)
err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)


N.SetNodeProbs (UnitSalesSterling, b"p1650", 0.0, 0.0, 0.0, 0,0.10, 0.15, 0.35, 0.30, 0.10)
N.SetNodeProbs (UnitSalesSterling, b"p1700", 0.0, 0.0, 0.10, 0.15, 0.25, 0.30, 0.10, 0.10, 0.0)
N.SetNodeProbs (UnitSalesSterling, b"p1750", 0.0, 0.05, 0.15, 0.40, 0.20, 0.10, 0.5, 0.05, 0.0)
N.SetNodeProbs (UnitSalesSterling, b"p1800", 0.0, 0.20, 0.40, 0.25, 0.10, 0.05, 0.0, 0.0, 0.0)
N.SetNodeProbs (UnitSalesSterling, b"p1850", 0.15, 0.35, 0.20, 0.20, 0.05, 0.05, 0.0, 0.0, 0.0)
#N.SetNodeProbs (UnitSalesSterling, "p1900", 0.35, 0.40, 0.20, 0.05, 0.0, 0.0, 0.0, 0.0, 0.0)


err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)
print(1)



N.SetNodeProbs(UnitSalesEcu, b'p1600', b'er_160_165',0.00, 0.00, 0.00, 0.00, 0.20, 0.30, 0.50)

err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)
print(2)


N.SetNodeProbs(UnitSalesEcu, b'p1600', b'er_165_170', 0.00, 0.00, 0.00, 0.10, 0.15, 0.35, 0.40)
N.SetNodeProbs(UnitSalesEcu, b'p1600', b'er_170_175', 0.0, 0.0, 0.05, 0.15, 0.15, 0.30, 0.35)
N.SetNodeProbs(UnitSalesEcu, b'p1600', b'er_175_176', 0.0, 0.0, 0.05, 0.20, 0.25, 0.30, 0.20)
N.SetNodeProbs(UnitSalesEcu, b'p1650', b'er_160_165', 0.0, 0.0, 0.10, 0.25, 0.30, 0.20, 0.15)
N.SetNodeProbs(UnitSalesEcu, b'p1650', b'er_165_170', 0.0, 0.05, 0.15, 0.20, 0.30, 0.20, 0.10)
N.SetNodeProbs(UnitSalesEcu, b'p1650', b'er_170_175', 0.05, 0.10, 0.20, 0.30, 0.15, 0.10, 0.10)
N.SetNodeProbs(UnitSalesEcu, b'p1650', b'er_175_176', 0.10, 0.15, 0.25, 0.20, 0.15, 0.10, 0.05)
N.SetNodeProbs(UnitSalesEcu, b'p1700', b'er_160_165', 0.15, 0.20, 0.25, 0.20, 0.10, 0.07, 0.03)
N.SetNodeProbs(UnitSalesEcu, b'p1700', b'er_165_170', 0.20, 0.20, 0.25, 0.15, 0.10, 0.05, 0.05)
N.SetNodeProbs(UnitSalesEcu, b'p1700', b'er_170_175', 0.25, 0.20, 0.20, 0.15, 0.10, 0.05, 0.05)
N.SetNodeProbs(UnitSalesEcu, b'p1700', b'er_175_176', 0.30, 0.25, 0.20, 0.15, 0.05, 0.05, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1750', b'er_160_165', 0.30, 0.30, 0.20, 0.10, 0.05, 0.05, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1750', b'er_165_170', 0.35, 0.30, 0.20, 0.10, 0.05, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1750', b'er_170_175', 0.40, 0.35, 0.15, 0.05, 0.05, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1750', b'er_175_176', 0.45, 0.40, 0.10, 0.05, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1800', b'er_160_165', 0.45, 0.40, 0.10, 0.05, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1800', b'er_165_170', 0.50, 0.40, 0.05, 0.05, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1800', b'er_170_175', 0.55, 0.40, 0.05, 0.0, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1800', b'er_175_176', 0.60, 0.40, 0.0, 0.0, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1850', b'er_160_165', 0.60, 0.40, 0.0, 0.0, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1850', b'er_165_170', 0.65, 0.35, 0.0, 0.0, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1850', b'er_170_175', 0.70, 0.30, 0.0, 0.0, 0.0, 0.0, 0.0)
N.SetNodeProbs(UnitSalesEcu, b'p1850', b'er_175_176', 0.75, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0)
#N.SetNodeProbs(UnitSalesEcu,'p1900','er_160_165',0.75, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0)
#N.SetNodeProbs(UnitSalesEcu,'p1900','er_165_170',0.80, 0.20, 0.0, 0.0, 0.0, 0.0, 0.0)
#N.SetNodeProbs(UnitSalesEcu,'p1900','er_170_175',0.85, 0.15, 0.0, 0.0, 0.0, 0.0, 0.0)
#N.SetNodeProbs(UnitSalesEcu,'p1900','er_175_176',0.90, 0.10, 0.0, 0.0, 0.0, 0.0, 0.0)

N.SetNodeFuncState(TotalSales, 0, b'ss10000', b'e6000')
N.SetNodeFuncState(TotalSales, 0, b'ss10000', b'e7000')
N.SetNodeFuncState(TotalSales, 0, b'ss10000', b'e8000')
N.SetNodeFuncState(TotalSales, 0, b'ss10000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss10000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss10000', b'e11000')
N.SetNodeFuncState(TotalSales, 1, b'ss10000', b'e12000')
N.SetNodeFuncState(TotalSales, 0, b'ss11000', b'e6000')
N.SetNodeFuncState(TotalSales, 0, b'ss11000', b'e7000')
N.SetNodeFuncState(TotalSales, 0, b'ss11000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss11000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss11000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss11000', b'e11000')
N.SetNodeFuncState(TotalSales, 1, b'ss11000', b'e12000')
N.SetNodeFuncState(TotalSales, 0, b'ss12000', b'e6000')
N.SetNodeFuncState(TotalSales, 0, b'ss12000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss12000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss12000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss12000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss12000', b'e11000')
N.SetNodeFuncState(TotalSales, 1, b'ss12000', b'e12000')
N.SetNodeFuncState(TotalSales, 0, b'ss13000', b'e6000')
N.SetNodeFuncState(TotalSales, 1, b'ss13000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss13000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss13000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss13000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss13000', b'e11000')
N.SetNodeFuncState(TotalSales, 1, b'ss13000', b'e12000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e6000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e11000')
N.SetNodeFuncState(TotalSales, 1, b'ss14000', b'e12000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e6000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e11000')
N.SetNodeFuncState(TotalSales, 1, b'ss15000', b'e12000')
N.SetNodeFuncState(TotalSales, 1, b'ss16000', b'e6000')
N.SetNodeFuncState(TotalSales, 1, b'ss16000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss16000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss16000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss16000', b'e10000')
N.SetNodeFuncState(TotalSales, 1, b'ss16000', b'e11000')
N.SetNodeFuncState(TotalSales, 2, b'ss16000', b'e12000')
N.SetNodeFuncState(TotalSales, 1, b'ss17000', b'e6000')
N.SetNodeFuncState(TotalSales, 1, b'ss17000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss17000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss17000', b'e9000')
N.SetNodeFuncState(TotalSales, 1, b'ss17000', b'e10000')
N.SetNodeFuncState(TotalSales, 2, b'ss17000', b'e11000')
N.SetNodeFuncState(TotalSales, 2, b'ss17000', b'e12000')
N.SetNodeFuncState(TotalSales, 1, b'ss18000', b'e6000')
N.SetNodeFuncState(TotalSales, 1, b'ss18000', b'e7000')
N.SetNodeFuncState(TotalSales, 1, b'ss18000', b'e8000')
N.SetNodeFuncState(TotalSales, 1, b'ss18000', b'e9000')
N.SetNodeFuncState(TotalSales, 2, b'ss18000', b'e10000')
N.SetNodeFuncState(TotalSales, 2, b'ss18000', b'e11000')
N.SetNodeFuncState(TotalSales, 2, b'ss18000', b'e12000')



## set the node function for the Population Outcome
#N.SetNodeFuncState(PopulationOutcome, 2,"A",'strong')
#N.SetNodeFuncState(PopulationOutcome, 1,"A",'medium')
#N.SetNodeFuncState(PopulationOutcome, 0,"A",'weak')
#N.SetNodeFuncState(PopulationOutcome, 3,"B",'strong')
#N.SetNodeFuncState(PopulationOutcome, 2,"B",'medium')
#N.SetNodeFuncState(PopulationOutcome, 1,"B",'weak')
#N.SetNodeFuncState(PopulationOutcome, 4,"C",'strong')
#N.SetNodeFuncState(PopulationOutcome, 3,"C",'medium')
#N.SetNodeFuncState(PopulationOutcome, 2,"C",'weak')
#N.SetNodeFuncState(PopulationOutcome, 4,"D",'strong')
#N.SetNodeFuncState(PopulationOutcome, 4,"D",'medium')
#N.SetNodeFuncState(PopulationOutcome, 3,"D",'weak')
#N.SetNodeFuncState(PopulationOutcome, 4,"E",'strong')
#N.SetNodeFuncState(PopulationOutcome, 4,"E",'medium')
#N.SetNodeFuncState(PopulationOutcome, 4,"E",'weak')



# print the error message in case of any errors within Netica
err_mesg = str(N.ErrorMessage_ns(N.GetError_ns(N, 5, 0)), "utf-8")
if err_mesg:
    print("Error within Netica: ", err_mesg)


# compile the final network
N.CompileNet_bn (bayesian_network)

# get the belief for each state for PopulationOutcome
belief = N.GetNodeBelief (b"TotalSales", b"complete", bayesian_network)
print("The probability is {}".format(belief))

#belief = N.GetNodeBelief ("PopulationOutcome", "B", bayesian_network)
#print """The probability is %g"""% belief
#
#belief = N.GetNodeBelief ("PopulationOutcome", "C", bayesian_network)
#print """The probability is %g"""% belief
#
#belief = N.GetNodeBelief ("PopulationOutcome", "D", bayesian_network)
#print """The probability is %g"""% belief
#
#belief = N.GetNodeBelief ("PopulationOutcome", "E", bayesian_network)
#print """The probability is %g"""% belief

# delete the network and print the returned message
N.DeleteNet_bn (bayesian_network)
res = N.CloseNetica_bn (env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8"))
print("-" * 65 + "\n")

