import sys

def adaptName(name):
    name = name.lstrip("(").rstrip(")")
    if name.startswith("GLFW_"):
        return name[5:] # strip off the GLFW_ part
    return name

with open(sys.argv[2], "w") as out:
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            line = line.lstrip()
            if line.startswith("#define GLFW_"):
                terms = line.split()
                name = adaptName(terms[1])
                i = 2
                while i < len(terms):
                    if terms[i] == '/*':
                        break
                    i += 1
                if i == 2:
                    continue
                init = " ".join([adaptName(term) for term in terms[2:i]])
                out.write(f"    const {name}: {init}\n")
