import qiskit._accelerate.circuit as my_package

import inspect

# TODO: command line argument for package/module, output file
# TODO: file writer state machine with indentation
# TODO: extract __init__ signature from doc header maybe?

EXEMPT_MEMBERS: list[str] = [
    "__doc__",
    "__module__",
    "__class__",
    "__new__",
]

with open('typings/qiskit/_accelerate/circuit.pyi', 'w') as f:
    f.write("from _typeshed import Incomplete\n")

    for name, obj in inspect.getmembers(my_package):
        if inspect.isclass(obj):
            f.write("\n\n")
            bases = obj.__bases__

            if len(bases) == 1 and bases[0] == object:
                f.write(f"class {name}:\n")
            else:
                f.write(f"class {name}(")
                for cls in bases:
                    f.write(cls.__name__)
                f.write("):\n")

            f.write(f"    \"\"\"{obj.__doc__}\"\"\"\n")

            for member_name, member in inspect.getmembers(obj):
                if member_name not in EXEMPT_MEMBERS:
                    # Skip built-ins
                    if inspect.isbuiltin(member):
                        continue

                    f.write("\n")

                    # Methods
                    if inspect.ismethoddescriptor(member):
                        f.write(f"    def {member_name}{inspect.signature(member)}:\n")
                        if member.__doc__ != "":
                            f.write(f"        \"\"\"{member.__doc__}\"\"\"\n")
                        f.write("        ...\n")

                    # Data descriptor
                    elif inspect.isdatadescriptor(member):
                        f.write(f"    {member_name}: Incomplete  # DATA DESCRIPTOR\n")
                        if member.__doc__ != "":
                            f.write(f"    \"\"\"{member.__doc__}\"\"\"\n")

                    # Plain-old attribute
                    else:
                        if member is not None:
                            f.write(f"    {member_name}: {type(member).__name__}\n")

                    # f.write(f"# ismethoddescriptor = {inspect.ismethoddescriptor(member)}\n")
                    # f.write(f"# ismethod = {inspect.ismethod(member)}\n")
                    # f.write(f"# isfunction = {inspect.isfunction(member)}\n")
                    # f.write(f"# isbuiltin = {inspect.isbuiltin(member)}\n")
                    # f.write(f"# isdatadescriptor = {inspect.isdatadescriptor(member)}\n")
                    # f.write(f"# isgetsetdescriptor = {inspect.isgetsetdescriptor(member)}\n")
                    # f.write(f"# ismemberdescriptor = {inspect.ismemberdescriptor(member)}\n")
                    # f.write(f"# isclass = {inspect.isclass(member)}\n")

            names: list[str] = [tup[0] for tup in inspect.getmembers(obj)]
            if "__getitem__" in names and "__iter__" not in names:
                print(f"Old-style Iterable: {name}")
                f.write("\n")
                f.write("    def __iter__(self):\n")
                f.write("        \"\"\"MOCKED TO MAKE THIS AN OLD-STYLE ITERABLE!\"\"\"\n")
                f.write("        ...\n")
