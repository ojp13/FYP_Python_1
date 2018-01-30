from scipy.integrate import cumtrapz

class Movement():
    """A class representing a movement, including original IMU data and other features"""

    def __init__(self, accX, accY, accZ, move_num):
        """Initialize movement with acceleration data"""
        self.move_num = move_num                 
        self.accX = accX
        self.accY = accY
        self.accZ = accZ

        self.classlabel = 0

        self.veloX = cumtrapz(self.accX, initial = 0)
        self.veloY = cumtrapz(self.accY, initial = 0)
        self.veloZ = cumtrapz(self.accZ, initial = 0)

        self.distX = cumtrapz(self.veloX, initial = 0)
        self.distY = cumtrapz(self.veloY, initial = 0)
        self.distZ = cumtrapz(self.veloZ, initial = 0)

        self.total_distX = self.distX[len(self.distX)-1]
        self.total_distY = self.distY[len(self.distY)-1]
        self.total_distZ = self.distX[len(self.distZ)-1]

        print('Movement ' + str(move_num) + ': Calculations are complete.')

    def label_Movement(self):
        """Give a class label to the movement"""
        self.classlabel = int(input('What is the class label of movement ' + str(self.move_num)) + ' ? ')

    def describe_Movement(self):
        print('The distance moved during movement ' + str(self.move_num) + ' in the X direction is ' + str(self.distX[len(self.distX)-1]))
        print('The distance moved during movement ' + str(self.move_num) + ' in the Y direction is ' + str(self.distY[len(self.distY)-1]))
        print('The distance moved during movement ' + str(self.move_num) + ' in the Z direction is ' + str(self.distZ[len(self.distZ)-1]))
        print('The classlabel of movement ' + str(self.move_num) + ' is ' + str(self.classlabel))

