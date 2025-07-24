class Observer:
    def __init__(self, phi, qualia):
        self.phi = phi
        self.qualia = qualia
        self.attended_nodes = []

    def attend(self, node):
        self.attended_nodes.append(node)

    def can_create_bridge(self):
        return self.phi >= 2.5

observer = Observer(phi=3.1, qualia=["red", "warm"])
if observer.can_create_bridge():
    print("Synesthetic bridge formed!")