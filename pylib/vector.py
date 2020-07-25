#-*-coding:utf-8-*-
__version__=1.0

import math,types

# Judging if a number or a series of numbers satisfied with the conditions given.
def isDigitals(numbers,numType='digital',numState='digital'):
    t=['int','float','digital']
    s=['positive','negative','digital']
    if type(numbers)==types.ListType:
        for n in numbers:
            if not isDigitals(n,numType,numState):
                return False
        return True
    else:
        if not (numType in t and numState in s):
            raise ValueError('Verify args failed. Variables numType and numState are not found.')
        number=str(numbers)
        if numType=='int':
            if numState=='positive':
                if number.isdigit():
                    return True
                else:
                    return False
            elif numState=='negative':
                if number[0]=='-':
                    if number[1:].isdigit():
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                if number[0]=='-':
                    number=number[1:]
                return isDigitals(number,'int','positive')

        elif numType=='float':
            if not '.' in number:
                return False
            else:
                position=number.find('.')
                number=number[:position]+number[position+1:]
            return isDigitals(number,'int',numState)

        else:
            if '.' in number:
                return isDigitals(number,'float',numState)
            else:
                return isDigitals(number,'int',numState)

# A Vector with two dimensions.
class Vector(object):
    def __init__(self,x=0,y=0):
        if type(x)==Vector and y==0:
            self.x=x.x
            self.y=x.y
        elif (type(x)==types.TupleType or type(x)==types.ListType) and len(x)==2 and y==0:
            self.x=x[0]
            self.y=x[1]
        elif type(x)==types.DictionaryType and x.keys()==['y','x'] and y==0:
            self.x=x['x']
            self.y=x['y']
        else:
            self.x=x
            self.y=y
        if isDigitals(self.x):
            self.x=float(self.x)
        else:
            raise VectorError('Vector element x is not a number. Element x:'+str(self.x))
        if isDigitals(self.y):
            self.y=float(self.y)
        else:
            raise VectorError('Vector element y is not a number. Element y:'+str(self.y))

        self.vector=(self.x,self.y)

    def __str__(self):
        return("Vector(%s,%s)"%(str(self.x),str(self.y)))

    def value(self):
        return (self.x,self.y)

    # +
    def __add__(self, other):
        if type(other)==Vector:
            x=other.x
            y=other.y
            return Vector(self.x+x,self.y+y)
        else:
            raise TypeError('Unsupported operand type(s) for +. '+str(other)+' is not in type of Vector.')

    # -
    def __sub__(self, other):
        if type(other)==Vector:
            x=other.x
            y=other.y
            return Vector(self.x-x,self.y-y)
        else:
            raise TypeError('Unsupported operand type(s) for -. '+str(other)+' is not in type of Vector.')

    # * (dot product)
    def __mul__(self, other):
        if type(other)==Vector:
            x=other.x
            y=other.y
            return self.x*x+self.y*y
        elif isDigitals(other):
            return Vector(self.x*float(other),self.y*float(other))
        else:
            raise TypeError('Unsupported operand type(s) for *. '+str(other)+' is not in type of Vector or number.')

    # /
    def __div__(self, other):
        if isDigitals(other):
            return Vector(self.x/float(other),self.y/float(other))
        else:
            raise TypeError('Unsupported operand type(s) for /. '+str(other)+' is not a number.')

    # ^ (Vector product)
    def __xor__(self, other):
        if type(other)==Vector:
            x=other.x
            y=other.y
            return Vector3(0,0,self.x*y-x*self.y)
        else:
            raise TypeError('Unsupported operand type(s) for ^. '+str(other)+' is not in type of Vector.')

    # ==
    def __eq__(self, other):
        if type(other)==Vector:
            x=other.x
            y=other.y
            if self.x==x and self.y==y:
                return True
            else:
                return False
        else:
            return False

    # Get length of the self.vector.
    def length(self):
        return math.sqrt(self.x**2+self.y**2)

    # Get unit vector of the self.vector.
    def unit(self):
        if self.x!=0 or self.y!=0:
            return Vector(self.vector)/Vector(self.vector).length()
        else:
            raise VectorError('Unit vector of Vector(0,0)is not exist.')

    # Get theta angle with sign between the self.vector and other vector.
    # Theta is positive while angle is anticlockwise revolved and negative while clockwise revolved.
    def theta(self,other):
        if type(other)==Vector:
            theta=(Vector(self.vector)*other)/(Vector(self.vector).length()*other.length())
            theta=math.acos(theta)*180/math.pi
            if (Vector(self.vector)^other).z<0:
                return -1*theta
            else:
                return theta
        else:
            raise VectorError(str(other)+' is not in type of Vector.')

class VectorError(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)
