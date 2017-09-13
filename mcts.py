"""
MIT License

Copyright (c) 2017 Alasdair Macindoe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Run this program several times to see how the values change!
"""
import random

class Node:
    def __init__(self, children=None, success=0, total=0, valid=False):
        """
        Defines a node object. Forms a B+ Tree with an arbitary number of
        children.
        Success is the number of routes that lead to a successful result.
        Total is the number of attempted routes.
        """
        self.children = children
        self.success = success
        self.total = total
        self.valid = valid

    def add_successful(self):
        """ Modifies internal state to add a successful route to leaf node """
        self.success += 1
        self.total += 1

    def add_failure(self):
        """ Modifies internal state for an unsuccessful route """
        self.total += 1

    def success_rate(self):
        """ Returns the MCTS value """
        if self.total == 0:
            return float('nan')
        return self.success / self.total

# We are going to create a tree
root = Node()
# Child 0 is a failure, and Child 1 and 2 are not a leaf nodes
root.children = [Node(), Node(), Node()]
# Child 1 (from above) has one successful node and one failure node
root.children[1].children = [Node(valid=True), Node()]
# Child 2 (from above) has two children nodes which are not leaf nodes
root.children[2].children = [Node(), Node()]
root.children[2].children[0].children = [Node(valid=True), Node(valid=True)]
root.children[2].children[1].children = [Node()]


# Now let's make a MCTS.
def mcts(node):
    nodes = [node] #we are going to use this as a stack
    #Check that is it not a leaf node
    while node.children != None and len(node.children) >= 1:
        r = random.randint(0, len(node.children) - 1)
        node = node.children[r]
        nodes.append(node)
    #Then backpropogate regardless
    node = nodes[len(nodes) - 1] #start with our last node
    while len(nodes) > 0:
        n = nodes.pop() #move back up the tree
        n.add_successful() if node.valid else n.add_failure()


def success_rates(node):
    """ Dpeth first print out the success rates """
    if node != None:
        print("Rate: {}".format(node.success_rate()))
        if node.children != None:
            for child in node.children:
                success_rates(child)
# Because this example is so small we will SELECT the root node
# That means we will expand the two children
# We will use a random heuristic for the route to take
mcts(root)

#We can then see that it has finished by checking the values
success_rates(root)
#We can the do another MCTS and see that the results change
print("")
print("New res")
mcts(root)
success_rates(root)

def create_rnd_tree(depth, parent, rate=98, max_children=3):
    """ Creates a random tree """
    if depth and not parent.valid:
        r = random.randint(0, max_children) #create this number of children
        parent.children = []
        #ensure leaf nodes remain leaf nodes
        for i in range(r):
            valid = random.randint(0, 100)
            condition = (valid >= rate)
            parent.children.append(Node(valid=condition))
            create_rnd_tree(depth - 1, parent.children[i])


root = Node()
#Try adjusting this value and see what happens
#Try adjusting the optional parameters too!
create_rnd_tree(4, root)
#We can then apply MCTS to it!
print("")
print("With our random tree!")
mcts(root)
success_rates(root)
print("")
print("And once more after 5 MCTS")
mcts(root)
mcts(root)
mcts(root)
mcts(root)
mcts(root)
success_rates(root)
