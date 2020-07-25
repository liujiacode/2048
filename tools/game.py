#-*-coding:utf-8-*-
# 游戏工具程序

from pylib.vector import Vector
import random
import time
import sys

mainPath=sys.path[0]

class Game(object):
    def __init__(self,row,test=False):
        self.step=0
        self.row=row
        self.box=[[0 for i in range(self.row)] for j in range(self.row)]
        self.up_dir=Vector(0,-1)
        self.down_dir=Vector(0,1)
        self.left_dir=Vector(-1,0)
        self.right_dir=Vector(1,0)
        self.test=test
        if self.test==True:
            self.current_time=time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime())

    def start_test(self):
        if self.test:
            self.file=open(mainPath+'/log/game'+self.current_time+'.log','w')

    def end_test(self):
        if self.test:
            self.file.close()

    ##### 获取函数 #####
    def get_box(self):
        return self.box

    def get_num(self,vector):
        i=int(vector.x)
        j=int(vector.y)
        return self.box[j][i]

    def change_num(self,vector,n):
        i=int(vector.x)
        j=int(vector.y)
        self.box[j][i]=n
        return True

    def get_max(self):
        n=0
        for line in self.box:
            for num in line:
                if num>n:
                    n=num
        return n

    ##### 判断函数 #####
    def is_equal(self,vector1,vector2):
        if vector1==vector2:
            print('CAUTION:<is_equal@Game>:Two vectors are equal!\n')
            return False

        if self.get_num(vector1)==self.get_num(vector2):
            return True
        else:
            return False

    def is_near(self,vector1,vector2):
        if vector1==vector2:
            print('CAUTION:<is_near@Game>:Two vectors are equal!\n')
            return False

        if (vector2-vector1).get_length()==1:
            return True
        else:
            return False

    def is_full(self):
        for line in self.box:
            for vect in line:
                if vect==0:
                    return False

        return True

    def is_in_range(self,vector):
        i=vector.x
        j=vector.y
        if i>=0 and i<self.row and j>=0 and j<self.row:
            return True
        else:
            return False

    ##### 移动函数 #####
    def move_dir(self,vector,direction):
        if direction[0]=='u':
            direction=self.up_dir
        elif direction[0]=='d':
            direction=self.down_dir
        elif direction[0]=='l':
            direction=self.left_dir
        elif direction[0]=='r':
            direction=self.right_dir
        else:
            exit('ERROR:<move_dir@Game>:Direction is not defined!\n')

        num=self.get_num(vector)
        if num==0:
            return False

        else:
            next_vector=vector+direction
            if not self.is_in_range(next_vector):
                if self.test:
                    self.file.write('BACKTRACK:<move_dir@Game>:Can not move a number on border '+str(vector)+'.\n')
                return False

            while self.is_in_range(next_vector) and self.get_num(next_vector)==0:
                next_vector+=direction

            if self.is_in_range(next_vector):
                if num==self.get_num(next_vector):
                    if self.test:
                        self.file.write('BACKTRACK:<move_dir@Game>:Move and add '+str(vector)+' Number'+str(num)+' to '+str(next_vector)+'.\n')
                    self.change_num(next_vector,2*num)
                    self.change_num(vector,0)

                else:
                    next_vector=next_vector-direction
                    if next_vector==vector:
                        if self.test:
                            self.file.write('BACKTRACK:<move_dir@Game>:Stay in situ '+str(vector)+'.\n')
                        return False
                    else:
                        self.change_num(next_vector,num)
                        self.change_num(vector,0)
                        if self.test:
                            self.file.write('BACKTRACK:<move_dir@Game>:Move but not add '+str(vector)+str(num)+' to '+str(next_vector)+'.\n')

            else:
                if self.test:
                    self.file.write('BACKTRACK:<move_dir@Game>:Do not move '+str(vector)+str(num)+' to '+str(next_vector)+'.\n')
                self.change_num(next_vector-direction,num)
                self.change_num(vector,0)

    def move(self,direction):
        if self.test:
            self.step=self.step+1
            self.file.write('STEP:<move@Game>:'+str(self.step)+'.\n')
        if direction=='u':
            if self.test:
                self.file.write('BACKTRACK:<move@Game>:Moving up.\n')
            for j in range(self.row):
                for i in range(self.row):
                    self.move_dir(Vector(i,j),'u')
        elif direction=='d':
            if self.test:
                self.file.write('BACKTRACK:<move@Game>:Moving down.\n')
            for j in range(self.row):
                for i in range(self.row):
                    self.move_dir(Vector(i,self.row-1-j),'d')
        elif direction=='l':
            if self.test:
                self.file.write('BACKTRACK:<move@Game>:Moving left.\n')
            for i in range(self.row):
                for j in range(self.row):
                    self.move_dir(Vector(i,j),'l')
        elif direction=='r':
            if self.test:
                self.file.write('BACKTRACK:<move@Game>:Moving right.\n')
            for i in range(self.row):
                for j in range(self.row):
                    self.move_dir(Vector(self.row-1-i,j),'r')
        else:
            exit('ERROR:<move@Game>:Direction is not defined!\n')

        if self.test:
            self.file.write('BACKTRACK:<move@Game>:Box:\n')
            self.file.write('\n----------Box----------\nVectory\t')
            for x in range(self.row):
                self.file.write('x'+str(x)+'\t')
            self.file.write('\n')
            y=0
            for line in self.box:
                self.file.write('y'+str(y)+'\t')
                for num in line:
                    self.file.write(str(num)+'\t')
                self.file.write('\n')
                y=y+1
            self.file.write('----------End----------\n\n')

    ##### 随机函数 #####
    def get_rand_num(self):
        num=random.choice([2,4])
        if self.test:
            self.file.write('BACKTRACK:<get_rand_num@Game>:Get random number '+str(num)+'.\n')
        return num

    def get_rand_vector(self):
        if self.is_full():
            return False
        i=random.randint(0,self.row-1)
        j=random.randint(0,self.row-1)
        while self.get_num(Vector(i,j)):
            i=random.randint(0,self.row-1)
            j=random.randint(0,self.row-1)
        if self.test:
            vect=Vector(i,j)
            self.file.write('BACKTRACK:<get_rand_vector@Game>:Get random vector '+str(vect)+'.\n')
        return Vector(i,j)
