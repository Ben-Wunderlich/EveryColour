from random import randint

class randict:
    def __init__(self):
        self.data = dict()
        self.length = 0

    def __len__(self):
        return self.length

    def GetRandomElement(self):
        index = randint(0, self.length-1)
        return (self.data[index], index)

    def GetElementAt(self, index):
        if index >= self.length:
            return self.data[self.length-1]
        return self.data[index]

    def AddElement(self, element):
        self.data[self.length] = element
        self.length += 1
    
    def RemoveElement(self, index):

        if self.length >= 2:#2 or more elements
            self.length-=1
            self.data[index] = self.data[self.length]
            del self.data[self.length]#tried using lengthInd instead of del but were both 49secs for 1920x1080
        elif self.length == 1:#exactly one element
            del self.data[0]
            self.length-=1
        else:#no elements
            raise ValueError("You tried to remove an element from an empty randict")

# a = randict()
# print(a.length)
# a.AddElement((1,2))
# a.AddElement((1,2))
# print("it is",len(a))
# print(a.length)
# a.RemoveElement(6)
# a.RemoveElement(6)
# a.RemoveElement(6)
# a.AddElement((3,4))
# a.AddElement((3,5))
# print(a.length)

# print(a.GetRandomElement())
# a.RemoveElement(6)
# a.RemoveElement(6)
# a.RemoveElement(6)
# a.RemoveElement(6)