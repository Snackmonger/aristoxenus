from console_ui import menu

x = menu.Tree()

y = menu.Node(x)

z = menu.Node(y)

a = menu.Node(y)

b = menu.Node(y)

c = menu.Node(b)


d = menu.Node(c)

e = menu.Node(d)

f = menu.Node(e)


print(f.nodes_to_root())



x.detach(b, sever=False)

print(enumerate(f.nodes_to_root()))
