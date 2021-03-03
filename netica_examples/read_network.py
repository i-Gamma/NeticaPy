from NeticaPy import Netica
import os

BASE_DIR = os.getcwd()

N = Netica()

mesg = bytearray()
env = N.NewNeticaEnviron_ns(b"", None, b"")
# env = N.NewNeticaEnviron_ns ("",None,"");
res = N.InitNetica2_bn(env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8").replace("\n\n", "\n").strip("\n"))
print("-" * 65 + "\n")

nombre = N. NewFileStream_ns(b"./ChestClinic/ChestClinic.dne", env)
net = N. ReadNet_bn (nombre, 0)

N.CompileNet_bn (net)

belief = N.GetNodeBelief (b"Tuberculosis", b"present", net)
print("The probability of tuberculosis is {:#.4f}".format(belief))

N.EnterFinding (b"XRay", b"abnormal", net);
belief = N.GetNodeBelief (b"Tuberculosis", b"present", net);

print("Given an abnormal X-ray, the probability of tuberculosis is {:#.4f}".format(belief))

N.EnterFinding (b"VisitAsia", b"visit", net)
belief = N.GetNodeBelief (b"Tuberculosis", b"present", net)

print("Given an abnormal X-ray and a visit to Asia, the probability of tuberculosis is {:#.4f}".format(belief))

N.EnterFinding (b"Cancer", b"present", net)
belief = N.GetNodeBelief (b"Tuberculosis", b"present", net)


print("Given abnormal X-ray, Asia visit, and lung cancer, the probability of tuberculosis is {:#.4f}".format(belief))

res = N.CloseNetica_bn (env, mesg)

print("\n" + "-" * 65)
print(mesg.decode("utf-8"))
print("-" * 65 + "\n")
