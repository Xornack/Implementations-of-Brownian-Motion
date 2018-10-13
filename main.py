"""
3D Brownian tree with multiple centers. This program takes input points and draws
a Brownian tree that "grows." Each node can only reproduce two other nodes before
it "burns out." The best appearance happens with only two children nodes.
The program keeps track of every node, which is just a rendered ball (sphere)
so that they never overlap each other.

There is an option for a cerebellum simulation. This is inspired by Dr. Roger Bird
at SNI Imaging at the Barrow Neurological Insitute and a paper in Neural Development.
(Sudarov, Anamaria & L Joyner, Alexandra. (2007). Cerebellum morphogenesis: The foliation
pattern is orchestrated by multi-cellular anchoring centers. Neural development.
2. 26. 10.1186/1749-8104-2-26. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2246128/)
The orientation comes roughly from the paper. The color scheme comes directly
from the paper.

This program allows you to manipulate the simulation as it is growing using the
standard Panda3D mouse inputs. Left click, right click, both mouse buttons
together. Left click moves the balls in the x and z planes, right click in the
y plane. Both together rotates around (0, 0, 0).

Note that the (x, y, z) coordinates in Panda3D are as follows:
x - right and left
y - in and out
z - up and down
"""
# Dependancies for math
from math import pi, sin, cos, sqrt
from random import randint
# Dependancies for Panda 3D
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.showbase import DirectObject
from panda3d.core import AmbientLight, DirectionalLight, Material
from panda3d.core import LVector3, Mat4, TextNode
from pandac.PandaModules import VBase4
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *

# Useful function to make the color of the sphere random.
# No input, just outputs a random VBase4 color.
def random_color():
    random_color = VBase4(float(randint(0, 100))/100,
                          float(randint(0, 100))/100,
                          float(randint(0, 100))/100,
                          1)
    return random_color

# Useful function for finding the Euclidean distance in 3D.
def euclidean(vector1, vector2):
    def square(x): return float(x)*float(x)
    return sqrt(square(vector1[0] - vector2[0])
                + square(vector1[1] - vector2[1])
                + square(vector1[2] - vector2[2]))

# Main class. 
class main(ShowBase):
 
    def __init__(self):
        ShowBase.__init__(self)

        self.SPHERE_SIZE = 5
        self.radius = self.SPHERE_SIZE/1.5
        # This is the extra distance between the spheres not immediately adjacent.
        # extra_distance specifies how much crowding is allowed.
        self.extra_distance = int(round(1.8*self.radius))
        self.DIST_BTW = 35
        self.v1 = [1]
        self.v3 = [True]
        self.v4 = [1]
        self.params = [self.SPHERE_SIZE, 1, self.DIST_BTW, True, 1]
        """
        Output:
        params[0] - sphere size
        params[1] - One point = 1, Two points = 2, Cerebellum simulation = 3
        params[2] - how far apart two points will be if you choose two (2 for params[1])
        params[3] - How many points for the cerebellar simulation, 4 = True, 5 = False
        params[4] - What color scheme. Gray = 1, random = 2, RGBY(W) = 3
        """
        # possible_vectors is calculated in self.calculate()
        possible_vectors = []
        self.possible_vectors = possible_vectors
        # List of all the spheres.
        sphere_list = []
        self.sphere_list = sphere_list
        # Lists of spheres that can actually grow.
        self.outside_sphere_list0 = []
        self.outside_sphere_list1 = []
        self.outside_sphere_list2 = []
        self.outside_sphere_list3 = []
        self.outside_sphere_list4 = []
        # Counters for the lists that can grow.
        self.counter_list0 = []
        self.counter_list1 = []
        self.counter_list2 = []
        self.counter_list3 = []
        self.counter_list4 = []

        # Set background color to white.
        base.setBackgroundColor(1,1,1)
        # Set ambient and directional light on the sphere.
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((0.3 , 0.4, 0.5, 1))
        self.directionalLight = DirectionalLight("directionalLight")
        # Angles the light just a little.
        self.directionalLight.setDirection(LVector3(0, 5, -5))
        self.directionalLight.setColor((0.9, 0.9, 0.9, 1))

        # Have to disable mouse to enable camera position.
        self.disableMouse()
        self.camera.setPos(0, -300, 0) # Sets the camera back.
        # Stock code from the Panda3D manual that reactivates the mouse standard.
        # Left click moves in the x and z planes, right click in the y plane.
        # Both together rotates around (0, 0, 0).
        mat=Mat4(camera.getMat())
        mat.invertInPlace()
        base.mouseInterfaceNode.setMat(mat)
        base.enableMouse()

        # Call input_variables, DirectGui start screen.
        # It allows a user to adjust a few features of the Brownian tree(s)
        # and color. At present, the sphere size can be changed, but it
        # quickly runs into limited size due to limiting factors in the
        # self.add_sphere() function. It can't be too crowded around a sphere
        # or else you can't see anything between the rendered spheres.
        self.input_variables()

    def input_variables(self):
        # Calls to the text and button widgets.      
        # Q0 sphere size.
        button0_text = OnscreenText(text = "Sphere Size",
                                    scale = 0.1, pos = (0, 0.9),
                                    align = TextNode.ACenter)
        button0 = DirectEntry(text = "",
                              command = self.item0, initialText = "5",
                              scale = 0.1, width = 10,
                              numLines = 1, pos = (-0.4, 0, 0.75))
        # Q1 User chooses one point, two points, or cerebellum simulation
        button1_text = OnscreenText(text = "What type of simulation?",
                                    scale = 0.1, pos = (0, 0.6),
                                    align = TextNode.ACenter)
        # For DirectButton variables, the value has to be in the form of a list.
        # This value can be anything, but you have to call it later as,
        # in this case, v1[0] to return a value and not a list.
        button11 = DirectRadioButton(text = "One Point",
                                     command = self.item1, variable = self.v1,
                                     value = [1], scale = 0.1,
                                     pos = (-0.56, 0, 0.45),
                                     pressEffect = 1, indicatorValue = 0)
        button12 = DirectRadioButton(text = "Two Point",
                                     command = self.item1, variable = self.v1,
                                     value = [2], scale = 0.1,
                                     pos = (0, 0, 0.45),
                                     pressEffect = 1, indicatorValue = 0)
        button13 = DirectRadioButton(text = "Cerebellum",
                                     command = self.item1, variable = self.v1,
                                     value = [3], scale = 0.1,
                                     pos = (0.6, 0, 0.45),
                                     pressEffect = 1, indicatorValue = 0)

        # You have to setOthers() to have the DirectRadioButton allow only one
        # value for each button clicked. The current 'checked' box won't
        # 'uncheck' when you select a different button without this.
        buttons1 = [button11, button12, button13]
        for button in buttons1:
            button.setOthers(buttons1)
        
        # Q2 How far apart will the two points be if you use two.
        button2_text = OnscreenText(text = "How far apart (if two points)",
                                    scale = 0.1, pos = (0, 0.3),
                                    align = TextNode.ACenter)

        button2 = DirectEntry(text = "",
                              command = self.item2, initialText = "30",
                              scale = 0.1, width = 10,
                              numLines = 1, pos = (-0.4, 0, 0.15))

        # Q3 How many points in the cerebellar simulation?
        button3_text = OnscreenText(text = "What type of simulation?",
                                    scale = 0.1, pos = (0, 0),
                                    align = TextNode.ACenter)
        button31 = DirectRadioButton(text = "Four",
                                     command = self.item3, variable = self.v3,
                                     value = [True], scale = 0.1,
                                     pos = (-0.2, 0, -0.15),
                                     pressEffect = 1, indicatorValue = 0)
        button32 = DirectRadioButton(text = "Five",
                                     command = self.item3, variable = self.v3,
                                     value = [False], scale = 0.1,
                                     pos = (0.2, 0, -0.15),
                                     pressEffect = 1, indicatorValue = 0)

        buttons3 = [button31, button32]
        for button in buttons3:
            button.setOthers(buttons3)

        # Q4 What color scheme? Gray, random, RGBY(W)? The colors come from
        # the paper mentioned at the start.
        button4_text = OnscreenText(text = "What color scheme?",
                                    scale = 0.1, pos = (0, -0.3),
                                    align = TextNode.ACenter)
        
        button41 = DirectRadioButton(text = "Gray",
                                     command = self.item4, variable = self.v4,
                                     value = [1], scale = 0.1,
                                     pos = (-0.5, 0, -0.45),
                                     pressEffect = 1, indicatorValue = 0)
        button42 = DirectRadioButton(text = "Random",
                                     command = self.item4, variable = self.v4,
                                     value = [2], scale = 0.1,
                                     pos = (-0.05, 0, -0.45),
                                     pressEffect = 1, indicatorValue = 0)

        button43 = DirectRadioButton(text = "RGBY(W)",
                                     command = self.item4, variable = self.v4,
                                     value = [3], scale = 0.1,
                                     pos = (0.5, 0, -0.45),
                                     pressEffect = 1, indicatorValue = 0)

        buttons4 = [button41, button42, button43]
        for button in buttons4:
            button.setOthers(buttons4)

        # Exit.
        exit_button = DirectButton(text = "Make it so!",
                                   command = self.exit_button,
                                   scale = 0.1,
                                   pos = (0, 0, -0.75),
                                   pressEffect = 1)

        self.button0_text = button0_text
        self.button0 = button0
        self.button1_text = button1_text
        self.button11 = button11
        self.button12 = button12
        self.button13 = button13
        self.button2_text = button2_text
        self.button2 = button2
        self.button3_text = button3_text
        self.button31 = button31
        self.button32 = button32
        self.button4_text = button4_text
        self.button41 = button41
        self.button42 = button42
        self.button43 = button43
        self.exit_button = exit_button
        
    # sphere size
    def item0(self, param0):
        try:
            param0 = int(param0)
        except ValueError:
            param0 = 5
        self.params[0] = param0

    # One point, two points, cerebellum simulation
    def item1(self):
        # For variables entries, 
        self.params[1] = self.v1[0]
            
    # How far apart will the two points be if you use two.
    def item2(self, param2):
        try:
            param2 = int(param2)
        except ValueError:
            param2 = 30
        self.params[2] = param2

    # How many points in the cerebellar simulation, 4 or 5
    def item3(self):
        self.params[3] = self.v3[0]

    # What color scheme. Gray, random, RGBY(W)?
    def item4(self):
        self.params[4] = self.v4[0]

    def exit_button(self):
        self.button0_text.cleanup()
        self.button0.destroy()
        self.button1_text.cleanup()
        self.button11.destroy()
        self.button12.destroy()
        self.button13.destroy()
        self.button2_text.cleanup()
        self.button2.destroy()
        self.button3_text.cleanup()
        self.button31.destroy()
        self.button32.destroy()
        self.button4_text.cleanup()
        self.button41.destroy()
        self.button42.destroy()
        self.button43.destroy()
        self.exit_button.destroy()
        # Call the meat of the program upon exit of start menu.
        self.calculate()
        self.choose_and_run()

    def calculate(self):
        # one or two points or the cerebellum simulation
        self.SPHERE_SIZE = self.params[0]
        self.DIST_BTW = self.params[2]
        self.radius = self.SPHERE_SIZE/1.5
        self.extra_distance = int(round(1.8*self.radius))

        # Allowable vectors from a point.
        # Calculates number of possible vectors of a certain distance.
        # That distance is proportional to radius.
        # Turns degrees into radians 1 degree through 360 degrees.
        thetas = [(float(i)*pi)/180 for i in range(360)]
        phis = thetas

        for theta in thetas:
            for phi in phis:   
                x = self.radius * sin(theta) * cos(phi)
                y = self.radius * sin(theta) * sin(phi)
                z = self.radius * cos(theta)
                x = int(round(x))
                y = int(round(y))
                z = int(round(z))

                self.possible_vectors.append((x, y, z))

        self.possible_vectors = list(set(self.possible_vectors))

    def choose_and_run(self):
        # one sphere at (0, 0, 0)
        if self.params[1] == 1:
            self.sphere_list = [(0, 0, 0)]

            self.outside_sphere_list0 = []
            self.outside_sphere_list0.append(self.sphere_list[0])
            self.counter_list0 = [0]
            
            if self.params[4] == 1:
                COLOR = VBase4(0.4, 0.4, 0.4, 1)
            # Choose random color
            if self.params[4] == 2:
                COLOR = random_color()
            if self.params[4] == 3:
                g = randint(0, 4)
                COLOR = (
                    [VBase4(1, 0, 0, 1),
                     VBase4(0, 0.5, 0, 1),
                     VBase4(0, 0, 1, 1),
                     VBase4(1, 1, 0, 1),
                     VBase4(1, 1, 1, 1)][g]
                    )
                
        # Two spheres DIST_BTW apart if user selects "Two Spheres"
        # Sets cerebellum to True if user selects "Cerebellum?"
        elif self.params[1] == 2:
            self.sphere_list = [(-self.DIST_BTW/2, 0, 0),
                                (self.DIST_BTW/2, 0, 0)]

            if self.params[4] == 1:
                COLOR = [VBase4(0.4, 0.4, 0.4, 1), VBase4(0.6, 0.6, 0.6, 1)]
            elif self.params[4] == 2:
                COLOR = []
                COLOR.append(random_color())
                COLOR.append(random_color())
            elif self.params[4] == 3:
                COLOR = []
                for i in range(2):
                    g = randint(0, 4)
                    COLOR.append(
                        [VBase4(1, 0, 0, 1),
                         VBase4(0, 0.5, 0, 1),
                         VBase4(0, 0, 1, 1),
                         VBase4(1, 1, 0, 1),
                         VBase4(1, 1, 1, 1)][g]
                        )
                    
            # Will need these local variable lists. They define which
            # nodes are chosen each iteration to 'grow.'
            # Will need one list for each time we want a new node
            # (coudn't find a way around it).
            self.outside_sphere_list0.append(self.sphere_list[0])
            self.counter_list0 = [0]
            self.outside_sphere_list1.append(self.sphere_list[1])
            self.counter_list1 = [0]
            
        elif self.params[1] == 3:
            self.sphere_list = [(-25, 0, 0), (25, 0, 0), (0, 0, 13), (0, 0, -17), (-25, 0, -17)]

            # choose colors based on user input.
            if self.params[4] == 1:
                COLOR = [VBase4(float(i)/10, float(i)/10, float(i)/10, 1) for i in range(3, 8)]
            elif self.params[4] == 2:
                COLOR = [random_color() for i in range(5)]
            elif self.params[4] == 3:
                COLOR = [VBase4(1, 0, 0, 1),
                         VBase4(0, 0.5, 0, 1),
                         VBase4(0, 0, 1, 1),
                         VBase4(1, 1, 0, 1),
                         VBase4(1, 1, 1, 1)]

            # Similar to if the user chooses two points, but more points obviously
            self.outside_sphere_list0.append(self.sphere_list[0])
            self.counter_list0 = [0]
            self.outside_sphere_list1.append(self.sphere_list[1])
            self.counter_list1 = [0]
            self.outside_sphere_list2.append(self.sphere_list[2])
            self.counter_list2 = [0]
            self.outside_sphere_list3.append(self.sphere_list[3])
            self.counter_list3 = [0]

            if self.params[3] == False:
                self.outside_sphere_list4 = []
                self.outside_sphere_list4.append(self.sphere_list[4])
                self.counter_list4 = [0]
            
        # task manager for drawing the spheres with add_sphere below
        if self.params[1] == 1:
            self.load_sphere(self.sphere_list[0], self.directionalLight,
                             self.ambientLight, COLOR)
            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR,
                                          self.sphere_list[0],
                                          self.outside_sphere_list0,
                                          self.counter_list0],
                             appendTask = True)

        if self.params[1] == 2:
            self.load_sphere(self.sphere_list[0], self.directionalLight,
                             self.ambientLight, COLOR[0])
            self.load_sphere(self.sphere_list[1], self.directionalLight,
                             self.ambientLight, COLOR[1])            
            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR[0],
                                          self.sphere_list[0],
                                          self.outside_sphere_list0,
                                          self.counter_list0],
                             appendTask = True)
            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR[1],
                                          self.sphere_list[1],
                                          self.outside_sphere_list1,
                                          self.counter_list1],
                             appendTask = True)

        # This is for all the spheres in the cerebellum simulation.
        if self.params[1] == 3:
            if self.params[3] == True:
                four_or_five = 4
            elif self.params[3] == False:
                four_or_five = 5

            for i in range(four_or_five):
                self.load_sphere(self.sphere_list[i],
                                 self.directionalLight,
                                 self.ambientLight,
                                 COLOR[i])

            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR[0],
                                          self.sphere_list[0],
                                          self.outside_sphere_list0,
                                          self.counter_list0],
                             appendTask = True)
            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR[1],
                                          self.sphere_list[1],
                                          self.outside_sphere_list1,
                                          self.counter_list1],
                             appendTask = True)
            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR[2],
                                          self.sphere_list[2],
                                          self.outside_sphere_list2,
                                          self.counter_list2],
                             appendTask = True)
            self.taskMgr.add(self.add_sphere, "add_sphere",
                             extraArgs = [COLOR[3],
                                          self.sphere_list[3],
                                          self.outside_sphere_list3,
                                          self.counter_list3],
                             appendTask = True)
            if self.params[3] == False:
                self.taskMgr.add(self.add_sphere, "add_sphere",
                                 extraArgs = [COLOR[4],
                                              self.sphere_list[4],
                                              self.outside_sphere_list4,
                                              self.counter_list4],
                                 appendTask = True)
            
    # Loads a sphere. The inputs are self explanatory.
    # I set the directional and ambient light to class globals,
    # so it wouldn't creat a new light per sphere, which is possible
    # but apparently expensive.
    def load_sphere(self,
                    position,
                    directionalLight,
                    ambientLight,
                    color):

        # Load a sphere.
        pos = position
        self.sphere = self.loader.loadModel("ball")
        self.sphere.setScale(self.SPHERE_SIZE,
                             self.SPHERE_SIZE,
                             self.SPHERE_SIZE)
        self.sphere.setPos(pos)
       
        # Sets the sphere color.
        self.sphere.setColor(color)
        self.sphere.reparentTo(render)

        # Make the sphere a material (to behave with the light).
        material = Material()
        material.setShininess(10.0)
        self.sphere.setMaterial(material)
                
        # Set lighting on the sphere.
        self.sphere.setLight(self.sphere.attachNewNode(directionalLight))
        self.sphere.setLight(self.sphere.attachNewNode(ambientLight))

    # Adds spheres to the scene.
    def add_sphere(self, color, starting_node,
                   outside_sphere_list, counter_list, task):
        # select randomly from the list of spheres
        n = randint(0, len(outside_sphere_list) - 1)
        chosen_sphere = outside_sphere_list[n]
        # select randomly from the list of possible vectors
        n = randint(0, len(self.possible_vectors) - 1)
        chosen_vector = self.possible_vectors[n]

        # add the vectors together to get a new location
        # for a sphere
        x = chosen_sphere[0] + chosen_vector[0]
        y = chosen_sphere[1] + chosen_vector[1]
        z = chosen_sphere[2] + chosen_vector[2]

        # calculates the distance from where the new sphere will randomly be
        # drawn to the other spheres, removes reduntant numbers
        d = []
        f = []
        distances = []
        pop = list(self.sphere_list)
        if len(pop) > 1:
            pop.remove(chosen_sphere)
        d = [(x, y, z) for i in range(len(pop))]
        distances = [int(euclidean(d[i], pop[i]))  \
                     for i in range(len(pop))]
        distances = list(set(distances))

        # Recalculate distances from the other spheres for the chosen_sphere.
        # This method of culling spheres is a little inefficient. Perhaps in
        # the future I could make it more efficient by just choosing spheres
        # that are nearby. I'm not sure yet how to accomplish this.
        d = []
        chosen_distances = []
        d = [chosen_sphere for i in range(len(pop))]
        chosen_distances = [int(euclidean(d[i], pop[i])) for i in range(len(pop))]
        chosen_distances = list(set(chosen_distances))
        # Sorts the chosen_distances lowest to highest.
        chosen_distances.sort()
        
        # temp will be used to index the counter of chosen_sphere.
        temp = outside_sphere_list.index(chosen_sphere)

        # Make the new sphere list and render the sphere.
        # First if statement only allows the render if the sphere
        # is going to be a certain distance away from all the other spheres,
        # in this case a 'radius' distance away.
        if min(distances) >= int(self.radius):
            if counter_list[temp] <= 1:
                if len(chosen_distances) <= 5:

                    outside_sphere_list.append((x, y, z))
                    self.sphere_list.append((x, y, z))
                    counter_list.append(0)
                    # The chosen_sphere counter goes up by one.
                    counter_list[temp] += 1

                    # Render sphere.
                    self.load_sphere((x, y, z),
                                     self.directionalLight,
                                     self.ambientLight,
                                     color)

                if len(chosen_distances) > 5 \
                   and chosen_distances[5] >= int(self.radius) \
                   + self.extra_distance:
                    
                    outside_sphere_list.append((x, y, z))
                    self.sphere_list.append((x, y, z))
                    counter_list.append(0)
                    # The chosen_sphere counter goes up by one.
                    counter_list[temp] += 1

                    # draw sphere
                    self.load_sphere((x, y, z),
                                     self.directionalLight,
                                     self.ambientLight,
                                     color)

            # The only available spheres for selection are the outside
            # ones in sphere_list. They 'burn out' after the number chosen
            # in the if statement.
            if counter_list[temp] > 1:
                outside_sphere_list.remove(chosen_sphere)
                del counter_list[temp]
                
        return Task.cont

Cerebellum = main()
Cerebellum.run()
